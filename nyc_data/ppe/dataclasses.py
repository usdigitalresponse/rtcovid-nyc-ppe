from enum import Enum


class MayoralCategory(str, Enum):
    eye_protection = "Eye Protection"
    ventilators_full_service = "Ventilators - Full Service"
    ventilators_non_full_service = "Ventilators - Non Full Service"
    gloves = "Gloves"
    iso_gowns = "ISO Gowns"
    n95_masks = "N95 Masks"
    non_surgical_masks = "Non - Surgical Masks"
    other_ppe = "Other PPE"
    surgical_masks = "Surgical Masks"
    other_medical_supplies = "Other Medical Supplies"

    def display(self):
        return self.value


class Unit(str, Enum):
    each = "each"
    yard = "yard"
    lb = "lb"


class OrderType(str, Enum):
    Purchase = "purchase"
    Make = "make"


# tightly control this column to keep the DB clean
class Item(str, Enum):
    faceshield = "faceshield"
    gown = "gown"
    gown_material = "gown_material"
    coveralls = "coveralls"

    n95_mask_non_surgical = "n95_mask"
    n95_mask_surgical = "n95_mask_surgical"
    kn95_mask = "kn95_mask"
    surgical_mask = "surgical_mask"
    mask_other = "mask_other"

    goggles = "goggles"

    gloves = "gloves"

    ventilators_full_service = "ventilators_full"
    ventilators_non_full_service = "ventilators_non_full"

    ppe_other = "ppe_other"
    unknown = "unknown"

    def to_mayoral_category(self):
        return ITEM_TO_MAYORAL[self]

    def display(self):
        return ITEM_TO_DISPLAYNAME[self]


ITEM_TO_DISPLAYNAME = {
    Item.faceshield: 'Face Shields',
    Item.gown: 'Gowns',
    Item.gown_material: 'Gown Material',
    Item.coveralls: 'Coveralls',

    Item.n95_mask_non_surgical: 'Non-surgical n95 Masks',
    Item.n95_mask_surgical: 'Surgical n95 Masks',
    Item.kn95_mask: 'KN95 Masks',
    Item.surgical_mask: 'Surgical Masks',
    Item.mask_other: 'Other Face Masks',

    Item.goggles: 'Goggles',
    Item.gloves: 'Gloves',

    Item.ventilators_full_service: 'Full Service Ventilators',
    Item.ventilators_non_full_service: 'Non Full Service Ventilators',

    Item.ppe_other: 'Other PPE',
    Item.unknown: 'Unknown'

}

ITEM_TO_MAYORAL = {
    Item.faceshield: MayoralCategory.eye_protection,
    Item.gown: MayoralCategory.iso_gowns,
    Item.gown_material: None,
    Item.coveralls: MayoralCategory.other_ppe,

    Item.n95_mask_non_surgical: MayoralCategory.non_surgical_masks,
    Item.n95_mask_surgical: MayoralCategory.n95_masks,
    Item.kn95_mask: MayoralCategory.n95_masks,
    Item.surgical_mask: MayoralCategory.surgical_masks,
    Item.mask_other: MayoralCategory.non_surgical_masks,

    Item.goggles: MayoralCategory.eye_protection,
    Item.gloves: MayoralCategory.gloves,

    Item.ventilators_full_service: MayoralCategory.ventilators_full_service,
    Item.ventilators_non_full_service: MayoralCategory.ventilators_non_full_service,

    Item.ppe_other: MayoralCategory.other_ppe,
    Item.unknown: None
}
