import enum

class ShippingMethod(enum.Enum):
    SAME_DAY = "same day"
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

class Admin(enum.Enum):
    NO = '0'
    YES = '1'