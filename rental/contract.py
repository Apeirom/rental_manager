# rental/contract.py
import uuid


##"id", "guarantee", "rental_deposit", "guarantee_id" ,"rent_amount", "room_name" , "property_id", "tenant_id", "real_estate_id", "acting", "file_path" 
class Contract:
    def __init__(self, guarantee, rental_deposit, rent_amount,  room_name, property_id, tenant_id, real_estate_id, guarantee_id=None, file_path=None, acting=True):
        self.id = str(uuid.uuid4())
        self.guarantee = guarantee  # Tipo de garantia (ex: caução, fiador, seguro fiança)
        self.rental_deposit = rental_deposit  # Valor da caução do Aluguel
        self.guarantee_id = guarantee_id # 
        self.rent_amount = rent_amount # Valor Atual do Aluguel
        self.room_name = room_name  # Nome da sala alugada
        self.property_id = property_id
        self.tenant_id = tenant_id
        self.real_estate_id = real_estate_id
        self.file_path = file_path  # Caminho até o arquivo do contrato
        self.acting = acting # Indica se o contrato está ativo ou não

    def setActive(self, active):
        self.acting = active