import uuid
from enum import Enum
from typing import NamedTuple, Dict

from django.contrib.postgres.fields import JSONField
from django.db import models

import ppe.dataclasses as dc
from ppe.data_mappings import DataSource


def enum2choices(enum):
    return [(v[0], v[0]) for v in enum.__members__.items()]


def ChoiceField(enum, default=None):
    return models.TextField(
        choices=[(v[0], v[0]) for v in enum.__members__.items()], default=default
    )


class ImportStatus(str, Enum):
    active = "active"
    replaced = "replaced"
    candidate = "candidate"
    cancelled = "cancelled"


class DataImport(models.Model):
    import_date = models.DateTimeField(auto_now_add=True, db_index=True)
    status = ChoiceField(ImportStatus)
    data_source = ChoiceField(DataSource)

    uploaded_by = models.TextField(blank=True)
    file_checksum = models.TextField()
    file_name = models.TextField()
    file = models.FileField

    @classmethod
    def sanity(cls):
        # for each data_source, at most 1 active
        for _, src in DataSource.__members__.items():
            ct = DataImport.objects.filter(data_source=src, status=ImportStatus.active).count()
            if ct > 1:
                print(f'Something is weird, more than one active object for {src}')
                return False
        return True

    def cancel(self):
        self.status = ImportStatus.cancelled

    def display(self):
        return f'File uploaded {self.import_date.strftime("%d/%m/%y")} by {self.uploaded_by or "unknown"}. Filename: {self.file_name}'

    def compute_delta(self):
        if not self.sanity():
            raise Exception("Can't compute a delta. Something is horribly wrong in the DB")
        if self.status != ImportStatus.candidate:
            raise Exception('Can only compute a delta on a candidate import')

        active_import = DataImport.objects.filter(status=ImportStatus.active, data_source=self.data_source).first()

        if active_import:
            active_objects = active_import.imported_objects()
        else:
            active_objects = {}

        new_objects = {
            k: set(objs).difference(active_objects.get(k)) if k in active_objects.keys() else set(objs) \
                for k, objs in self.imported_objects().items() 
        }

        return UploadDelta(
            previous=active_import,
            active_stats={tpe.__name__: len(objs) for (tpe, objs) in active_objects.items()},
            candidate_stats={tpe.__name__: len(objs) for (tpe, objs) in active_objects.items()},
            new_objects=new_objects

        )

    def imported_objects(self):
        return {tpe: tpe.objects.prefetch_related('source').filter(source=self) for tpe in
                [Delivery, Inventory, Purchase]}

class UploadDelta(NamedTuple):
    previous: DataImport
    active_stats: Dict[str, int]
    candidate_stats: Dict[str, int]

    new_objects: Dict[str, any]

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(DataImport, on_delete=models.CASCADE)

    @classmethod
    def active(cls):
        return cls.objects.prefetch_related('source').filter(source__status=ImportStatus.active)

    class Meta:
        abstract = True


class Purchase(BaseModel):
    order_type = ChoiceField(dc.OrderType)

    item = ChoiceField(dc.Item)
    description = models.TextField(blank=True)
    quantity = models.IntegerField()
    unit = ChoiceField(dc.Unit, default=dc.Unit.each)

    vendor = models.TextField()
    cost = models.IntegerField(null=True)

    raw_data = JSONField()


class Inventory(BaseModel):
    item = ChoiceField(dc.Item)
    quantity = models.IntegerField()

    raw_data = JSONField()


class Delivery(BaseModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    delivery_date = models.DateField(null=True)
    quantity = models.IntegerField()

    def to_dataclass(self):
        return dc.Delivery(
            item=dc.Item(self.purchase.item).display(),
            description=self.purchase.description,
            delivery_date=self.delivery_date,
            quantity=self.quantity,
            vendor=self.purchase.vendor,
            source=self.source.display()
        )


class Hospital(BaseModel):
    # TODO: need to figure out what resolution is needed. Could bring in the full geocoding hospital
    # model from covidhospitalstatus
    name = models.TextField()


class Need(BaseModel):
    item = models.TextField(choices=enum2choices(dc.Item))
    date = models.DateField()

    quantity = models.IntegerField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    satisfied = models.BooleanField()
