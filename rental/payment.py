# rental/payment.py
import uuid
from utils.dateProcessing import get_current_iso_datetime

class Payment:
    def __init__(self, contract_id, receipt_path, month_ref, year_ref):
        self.id = str(uuid.uuid4())
        self.payment_date = get_current_iso_datetime()  # formato ISO 8601
        self.month_ref = month_ref  # int: 1-12
        self.year_ref = year_ref    # int: ex: 2025
        self. contract_id = contract_id
        self.receipt_path = receipt_path
