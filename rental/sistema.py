from rental.data_manager import DataManager
from rental.tenant import Tenant
from rental.property import Property
from rental.contract import Contract
from rental.payment import Payment
from rental.real_estate import real_estate
from rental.extract import Extract
from rental.guarantor import Guarantor
from rental.bail_insurance import BailInsurance
from tabulate import tabulate

from utils.numbersProcessing import format_phone
from utils.dateProcessing import iso_para_formatado

class RentalSystem:
    def __init__(self, data_folder):
        self.data_manager = DataManager(data_folder)
        self.tenants = {}
        self.properties = {}
        self.contracts = {}
        self.payments = {}
        self.agencies = {}
        self.extracts = {}
        self.guarantors = {}
        self.bail_insurances = {}
        self.load_all()

    def load_all(self):
        self.tenants = self.data_manager.load_tenants()
        self.properties = self.data_manager.load_properties()
        self.contracts = self.data_manager.load_contracts()
        self.payments = self.data_manager.load_payments()
        self.agencies = self.data_manager.load_real_states()
        self.extracts = self.data_manager.load_extracts()
        self.guarantors = self.data_manager.load_guarantors()
        self.bail_insurances = self.data_manager.load_bail_insurances()

    def save_all(self):
        self.data_manager.save_all(
            self.agencies, self.tenants, self.properties, 
            self.contracts, self.payments, self.extracts,
            self.guarantors, self.bail_insurances
        )

    # ===============================
    # Métodos de gerenciamento
    # ===============================

    def add_tenant(self, name, cpf=None, cnpj=None):
        t = Tenant(name, cpf, cnpj)
        self.tenants[t.id] = t
        return t.id

    def remove_tenant(self, tenant_id):
        if tenant_id in self.tenants:
            del self.tenants[tenant_id]

    def add_property(self, property_name, owner_name, address, room_count=0):
        p = Property(property_name, owner_name, address, room_count)
        self.properties[p.id] = p
        return p.id

    def remove_property(self, property_id):
        if property_id in self.properties:
            del self.properties[property_id]

    def add_contract(self, guarantee, rental_deposit, rent_amount, room_name, property_id, tenant_id, real_estate_id, guarantee_id, file_path):
        c = Contract(guarantee, rental_deposit, rent_amount, room_name,
                     property_id, tenant_id, real_estate_id, guarantee_id, file_path)
        self.contracts[c.id] = c

        # Atualiza lista de imóveis da agência correspondente
        if real_estate_id in self.agencies:
            self.agencies[real_estate_id].add_property(property_id)

        return c.id

    def remove_contract(self, contract_id):
        if contract_id in self.contracts:
            del self.contracts[contract_id]
            

    def add_payment(self, contract_id, receipt_path, month_ref, year_ref):
        p = Payment(contract_id, receipt_path, month_ref, year_ref)
        self.payments[p.id] = p
        return p.id

    def remove_payment(self, payment_id):
        if payment_id in self.payments:
            del self.payments[payment_id]

    def add_real_estate(self, name, cnpj, commission, phone=None, address=None):
        a = real_estate(name, cnpj, address, commission, phone)
        self.agencies[a.id] = a
        return a.id

    def remove_real_estate(self, real_estate_id):
        if real_estate_id in self.agencies:
            del self.agencies[real_estate_id]

    def add_extract(self, contract_id, month_ref, year_ref, rent_amount, receipt_path, iptu=None, water=None, agreement=None):
        e = Extract(
            contract_id, month_ref, year_ref, 
            rent_amount, receipt_path, iptu, water, agreement
        )
        self.extracts[e.id] = e
        return e.id
    
    def remove_extract(self, extract_id):
        if extract_id in self.extracts:
            del self.extracts[extract_id]

    def add_guarantor(self, name, cpf, cnpj=None):
        g = Guarantor(name, cpf, cnpj)
        self.guarantors[g.id] = g
        return g.id
    
    def remove_guarantor(self, guarantor_id):
        if guarantor_id in self.guarantors:
            del self.guarantors[guarantor_id]

    def add_bail_insurance(self, value, insurance_company, vality):
        b = BailInsurance(value, insurance_company, vality)
        self.bail_insurances[b.id] = b
        return b.id
    
    def remove_bail_insurance(self, bail_insurance_id):
        if bail_insurance_id in self.bail_insurances:
            del self.bail_insurances[bail_insurance_id]

    # ===============================
    ## Find By ID Methods
    # ===============================

    def find_tenant_by_id(self, tenant_id):
        return self.tenants.get(tenant_id)

    def find_property_by_id(self, property_id):
        return self.properties.get(property_id)

    def find_real_estate_by_id(self, real_estate_id):
        return self.agencies.get(real_estate_id)

    def find_contract_by_id(self, contract_id):
        return self.contracts.get(contract_id)

    def find_payment_by_id(self, payment_id):
        return self.payments.get(payment_id)

    def find_extract_by_id(self, extract_id):
        return self.extracts.get(extract_id)

    def find_guarantor_by_id(self, guarantor_id):
        return self.guarantors.get(guarantor_id)

    def find_bail_insurance_by_id(self, bail_insurance_id):
        return self.bail_insurances.get(bail_insurance_id)
    
    # ===============================
    # Métodos de visualização (refatorados)
    # ===============================

    def show_tenants(self, only_acting=False):
        print("\n-- INQUILINOS --")
        tenants = list(self.tenants.values())
        if only_acting:
            active_ids = {c.tenant_id for c in self.contracts.values()}
            tenants = [t for t in tenants if t.id in active_ids]
        
        # Adiciona numeração começando em 1
        numbered_data = [
            [i+1, t.name, t.cpf, t.cnpj] 
            for i, t in enumerate(tenants)
        ]
        
        print(tabulate(
            numbered_data,
            headers=["#", "Nome", "CPF", "CNPJ"],
            showindex=False
        ))

    def show_properties(self, only_acting=False):
        print("\n-- IMÓVEIS --")
        properties = list(self.properties.values())
        if only_acting:
            active_ids = {c.property_id for c in self.contracts.values()}
            properties = [p for p in properties if p.id in active_ids]
            
        numbered_data = [
            [i+1, p.property_name, p.owner_name, p.address, p.room_count] 
            for i, p in enumerate(properties)
        ]
        
        print(tabulate(
            numbered_data,
            headers=["#", "Nome", "Proprietário", "Endereço", "Quantidade de Salas"],
            showindex=False
        ))

    def show_contracts(self, only_acting=False):
        print("\n-- CONTRATOS --")
        contracts = list(self.contracts.values())
        if only_acting:
            contracts = [c for c in contracts if c.acting]
            
        numbered_data = [
            [i+1, self.find_tenant_by_id(c.tenant_id).name, self.find_real_estate_by_id(c.real_estate_id).name, self.find_property_by_id(c.property_id).property_name, c.rent_amount, c.rental_deposit, c.room_name, c.file_path]
            for i, c in enumerate(contracts)
        ]
        
        print(tabulate(
            numbered_data,
            headers=["#", "Inquilino", "Imobiliária", "Imóvel", "Aluguel", "Caução", "Sala", "Arquivo"],
            showindex=False
        ))

    def show_payments(self, only_acting=False):
        print("\n-- PAGAMENTOS --")
        payments = list(self.payments.values())
        if only_acting:
            active_tenants = {c.tenant_id for c in self.contracts.values() if c.acting}
            payments = [p for p in payments if p.tenant_id in active_tenants]
        
        numbered_data = []
        for i, p in enumerate(payments):
            contract = self.find_contract_by_id(p.contract_id)
            numbered_data.append([
                i + 1,
                self.find_tenant_by_id(contract.tenant_id).name,
                self.find_real_estate_by_id(contract.real_estate_id).name,
                self.find_property_by_id(contract.property_id).property_name,
                p.month_ref,
                p.year_ref,
                iso_para_formatado(p.payment_date),
                p.receipt_path
            ])
        
        print(tabulate(
            numbered_data,
            headers=["#", "Inquilino", "Imobiliária", "Imóvel", "Mês", "Ano", "Data do cadastro", "Comprovante"],
            showindex=False
        ))

    def show_real_states(self, only_acting=False):
        print("\n-- IMOBILIÁRIAS --")
        agencies = list(self.agencies.values())
        if only_acting:
            active_ids = {c.real_estate_id for c in self.contracts.values() if c.acting}
            agencies = [a for a in agencies if a.id in active_ids]
            
        numbered_data = [
            [i+1, a.name, a.cnpj, a.address, a.commission, format_phone(a.phone)]
            for i, a in enumerate(agencies)
        ]
        
        print(tabulate(
            numbered_data,
            headers=["#", "Nome", "CNPJ", "Endereço", "Comissão", "Telefone"],
            showindex=False
        ))

    def show_extracts(self):
        print("\n-- EXTRATOS --")
        extracts = list(self.extracts.values())
        
        numbered_data = []
        for i, e in enumerate(extracts):
            contract = self.find_contract_by_id(e.contract_id)
            numbered_data.append([
                i + 1,
                self.find_tenant_by_id(contract.tenant_id).name,
                self.find_real_estate_by_id(contract.real_estate_id).name,
                self.find_property_by_id(contract.property_id).property_name,
                e.month_ref,
                e.year_ref,
                e.rent_amount,
                e.iptu,
                e.water,
                e.agreement,
                e.receipt_path
            ])
        
        print(tabulate(
            numbered_data,
            headers=["#", "Inquilino", " Imobiliária", "Imóvel", "Mês", "Ano", "Aluguel", "IPTU", "Água", "Acordo", "Comprovante"],
            showindex=False
        ))

    def show_guarantors(self):
        print("\n-- FIADORES --")
        guarantors = list(self.guarantors.values())
        
        numbered_data = [
            [i+1, g.name, g.cpf, g.cnpj] 
            for i, g in enumerate(guarantors)
        ]
        
        print(tabulate(
            numbered_data,
            headers=["#", "Nome", "CPF", "CNPJ"],
            showindex=False
        ))

    def show_bail_insurances(self):
        print("\n-- SEGUROS DE CAUÇÃO --")
        bail_insurances = list(self.bail_insurances.values())
        
        numbered_data = [
            [i+1, b.insurance_company, b.value, b.vality] 
            for i, b in enumerate(bail_insurances)
        ]
        
        print(tabulate(
            numbered_data,
            headers=["#", "Seguradora", "Valor", "Validade"],
            showindex=False
        ))