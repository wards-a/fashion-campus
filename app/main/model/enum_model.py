import enum

class ShippingMethod(enum.Enum):
    REGULAR = "regular"
    NEXT_DAY = "next day"

class ProductCondition(enum.Enum):
    NEW = "new"
    USED = "used"

class Deleted(enum.Enum):
    NO = "0"
    YES = "1"

class Role(enum.Enum):
    SELLER = "seller"
    BUYER = "buyer"
