import uuid

class Extract:
    def __init__(self, contract_id, month_ref, year_ref, rent_amount, receipt_path=None, iptu=None, water=None, agreement=None):
        self.id = str(uuid.uuid4())
        self.contract_id = contract_id
        self.month_ref = month_ref  # 1-12
        self.year_ref = year_ref    # ex: 2023
        self.rent_amount = float(rent_amount)
        self.receipt_path = receipt_path  # Caminho do comprovante
        self.iptu = float(iptu)          # Valor do IPTU
        self.water = float(water)        # Valor da água
        self.agreement = float(agreement)  # Valor pagamento acordado

    def update_values(self, rent_amount=None, iptu=None, water=None):
        """Atualiza valores financeiros do extrato"""
        if rent_amount is not None:
            self.rent_amount = rent_amount
        if iptu is not None:
            self.iptu = iptu
        if water is not None:
            self.water = water