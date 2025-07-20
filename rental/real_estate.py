# rental/real_estate.py

import uuid

class real_estate:
    def __init__(self, name, cnpj, address, commission, phone=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.cnpj = cnpj
        self.address = address
        self.commission = commission
        self.phone = phone
        self.property_ids = []   # Lista de IDs de imóveis gerenciados

    def add_property(self, property_id):
        if property_id not in self.property_ids:
            self.property_ids.append(property_id)

    def remove_property(self, property_id):
        if property_id in self.property_ids:
            self.property_ids.remove(property_id)

