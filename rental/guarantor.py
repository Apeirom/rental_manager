import uuid

class Guarantor:
    def __init__(self, name, cpf=None, cnpj=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.cpf = cpf      # CPF para pessoa física
        self.cnpj = cnpj    # CNPJ para pessoa jurídica
        
        if not cpf and not cnpj:
            raise ValueError("Fiador deve ter CPF ou CNPJ")

    def is_company(self):
        """Verifica se o fiador é uma pessoa jurídica"""
        return self.cnpj is not None