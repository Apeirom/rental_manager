# rental/tenant.py
import uuid

class Tenant:
    def __init__(self, name, cpf=None, cnpj=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.cpf = cpf
        self.cnpj = cnpj