import uuid
from datetime import datetime, timedelta

class BailInsurance:
    def __init__(self, value, insurance_company, vality):
        self.id = str(uuid.uuid4())
        self.value = value              # Valor coberto pelo seguro
        self.insurance_company = insurance_company
        self.vality = vality