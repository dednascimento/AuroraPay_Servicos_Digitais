from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List
from typing import Optional

class BillingAction(Enum):
    SEND_EMAIL = "SEND_EMAIL"
    SKIP = "SKIP"
    ERROR = "ERROR"

@dataclass
class InvoiceItem:
    description: str
    amount: float

@dataclass
class Invoice:
    invoice_id: str
    customer_name: str
    amount: float
    due_date: date
    email: str
    accepts_communication: bool
    items: List[InvoiceItem] = None # New field

    def __post_init__(self):
        if self.items is None:
            self.items = [] = True
