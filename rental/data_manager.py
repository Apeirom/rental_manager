import os
import pandas as pd
from pathlib import Path

from rental.bail_insurance import BailInsurance
from rental.extract import Extract
from rental.guarantor import Guarantor
from rental.real_estate import real_estate
from rental.contract import Contract
from rental.payment import Payment
from rental.property import Property
from rental.tenant import Tenant

class DataManager:
    def __init__(self, data_folder):
        self.data_folder = Path(data_folder)
        self._ensure_data_folder()
        
    def _ensure_data_folder(self):
        """Garante que a pasta de dados existe"""
        if not self.data_folder.exists():
            self.data_folder.mkdir(parents=True)
    
    def _load_data(self, filename):
        """Carrega dados de um arquivo Excel e retorna como lista de dicionários"""
        filepath = self.data_folder / filename
        try:
            if filepath.exists():
                df = pd.read_excel(filepath, engine='openpyxl')
                # Converte NaN para None e depois para dicionário
                return df.where(pd.notnull(df), None).to_dict('records')
            return []
        except Exception as e:
            print(f"Erro ao carregar {filename}: {str(e)}")
            return []

    def _save_data(self, filename, data):
        """Salva uma lista de dicionários em um arquivo Excel"""
        filepath = self.data_folder / filename
        try:
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False, engine='openpyxl')
        except Exception as e:
            print(f"Erro ao salvar {filename}: {str(e)}")

    # Métodos específicos para cada classe
    def load_tenants(self):
        """Carrega inquilinos e retorna dicionário {id: Tenant}"""
        tenants = {}
        for item in self._load_data("tenant.xlsx"):
            try:
                t = Tenant(
                    name=item['name'],
                    cpf=item['cpf'],
                    cnpj=item['cnpj']
                )
                t.id = item['id']
                tenants[t.id] = t
            except Exception as e:
                print(f"Erro ao carregar inquilino: {str(e)}")
        return tenants

    def load_properties(self):
        """Carrega propriedades e retorna dicionário {id: Property}"""
        properties = {}
        for item in self._load_data("property.xlsx"):
            try:
                p = Property(
                    property_name=item['property_name'],
                    owner_name=item['owner_name'],
                    address=item['address'],
                    room_count=item.get('room_count', 0)
                )
                p.id = item['id']
                properties[p.id] = p
            except Exception as e:
                print(f"Erro ao carregar propriedade: {str(e)}")
        return properties

    def load_contracts(self):
        """Carrega contratos e retorna dicionário {id: Contract}"""

        ##"id", "guarantee", "rental_deposit", "guarantee_id" ,"rent_amount", "room_name" , "property_id", "tenant_id", "real_estate_id", "acting", "file_path" 

        contracts = {}
        for item in self._load_data("contract.xlsx"):
            try:
                c = Contract(
                    guarantee=item['guarantee'],  # Tipo de garantia (ex: caução, fiador, seguro fiança)
                    rental_deposit=item['rental_deposit'],
                    guarantee_id=item.get('guarantee_id'),  # ID da garantia (se aplicável)
                    rent_amount=item['rent_amount'],
                    room_name=item['room_name'],
                    property_id=item['property_id'],
                    tenant_id=item['tenant_id'],
                    real_estate_id=item['real_estate_id'],
                    acting=item.get('acting', True),
                    file_path=item.get('file_path'),
                )
                c.id = item['id']
                contracts[c.id] = c
            except Exception as e:
                print(f"Erro ao carregar contrato: {str(e)}")
        return contracts

    def load_real_states(self):
        """Carrega agências e retorna dicionário {id: real_estate}"""
        agencies = {}
        for item in self._load_data("real_estate.xlsx"):
            try:
                a = real_estate(
                    name=item['name'],
                    cnpj=item['cnpj'],
                    address=item['address'],
                    commission=item['commission'],
                    phone=item.get('phone'),
                )
                a.id = item['id']
                # Tratamento especial para property_ids
                prop_ids = item.get('property_ids')
                if prop_ids is not None and not isinstance(prop_ids, float):
                    a.property_ids = str(prop_ids).split(',')
                else:
                    a.property_ids = []
                agencies[a.id] = a
            except Exception as e:
                print(f"Erro ao carregar agência: {str(e)}")
        return agencies

    def load_payments(self):
        """Carrega pagamentos e retorna dicionário {id: Payment}"""
        payments = {}
        for item in self._load_data("payments.xlsx"):
            try:
                p = Payment(
                    contract_id=item['contract_id'],
                    receipt_path=item['receipt_path'],
                    month_ref=item['month_ref'],
                    year_ref=item['year_ref']
                )
                p.id = item['id']
                p.payment_date = item.get('payment_date')
                payments[p.id] = p
            except Exception as e:
                print(f"Erro ao carregar pagamento: {str(e)}")
        return payments
    
    ## "id", "tenant_id", "property_id", "real_estate_id", "month_ref", "year_ref", "rent_amount", "receipt_path", "iptu", "water", "agreement"
    def load_extracts(self):
        """Carrega extratos e retorna dicionário {id: Extract}"""
        extracts = {}
        for item in self._load_data("extract.xlsx"):
            try:
                # Pré-processamento dos valores numéricos
                def parse_number(value):
                    if value is None or value == '':
                        return None
                    if isinstance(value, str):
                        value = value.replace('.', '').replace(',', '.')
                    try:
                        return float(value)
                    except:
                        return None

                # Conversão segura dos valores
                month_ref = int(item['month_ref']) if item.get('month_ref') is not None else None
                year_ref = int(parse_number(item['year_ref'])) if item.get('year_ref') is not None else None
                rent_amount = parse_number(item['rent_amount'])
                iptu = parse_number(item.get('iptu'))
                water = parse_number(item.get('water'))

                e = Extract(
                    contract_id=str(item['contract_id']),
                    month_ref=month_ref,
                    year_ref=year_ref,
                    rent_amount=rent_amount if rent_amount is not None else 0.0,
                    receipt_path=item.get('receipt_path'),
                    iptu=iptu,
                    water=water,
                    agreement=item.get('agreement')
                )
                
                # Mantém o ID original
                e.id = str(item['id'])
                extracts[e.id] = e
                
            except Exception as e:
                print(f"Erro ao carregar extrato ID {item.get('id', 'desconhecido')}: {str(e)}")
                print(f"Dados problemáticos: {item}")
                
        return extracts
    
    def load_guarantors(self):
        """Carrega fiadores e retorna dicionário {id: Guarantor}"""
        guarantors = {}
        for item in self._load_data("guarantor.xlsx"):
            try:
                # Verifica se os campos existem e trata valores vazios
                cpf = item.get('cpf')
                cnpj = item.get('cnpj')
                
                # Converte valores vazios para None
                cpf = cpf if (cpf and str(cpf).strip()) else None
                cnpj = cnpj if (cnpj and str(cnpj).strip()) else None
                
                g = Guarantor(
                    name=item['name'],
                    cpf=cpf,
                    cnpj=cnpj
                )
                
                # Mantém o ID original se existir
                if 'id' in item and item['id']:
                    g.id = str(item['id'])
                    
                guarantors[g.id] = g
                
            except Exception as e:
                print(f"Erro ao carregar fiador ID {item.get('id', 'desconhecido')}: {str(e)}")
                print(f"Dados problemáticos: {item}")
                
        return guarantors
    
    def load_bail_insurances(self):
        """Carrega seguros de fiança e retorna dicionário {id: BailInsurance}"""
        bail_insurances = {}
        for item in self._load_data("bail_insurance.xlsx"):
            try:
                # Conversão do valor (formato brasileiro)
                value_str = str(item['value']).replace('.', '').replace(',', '.')
                value = float(value_str)
                
                
                b = BailInsurance(
                    value=value,
                    insurance_company=item['insurance_company'],
                    vality=item['vality']
                )
                
                # Mantém o ID original se existir
                if 'id' in item and item['id']:
                    b.id = str(item['id'])
                    
                bail_insurances[b.id] = b
                
            except Exception as e:
                print(f"Erro ao carregar seguro ID {item.get('id', 'desconhecido')}: {str(e)}")
                print(f"Dados problemáticos: {item}")
                
        return bail_insurances

    def save_all(self, agencies, tenants, properties, contracts, payments, extracts, guarantors, bail_insurances):
        """Salva todos os dados no sistema"""
        try:
            # Converte objetos para dicionários simples
            tenants_data = [vars(t) for t in tenants.values()]
            properties_data = [vars(p) for p in properties.values()]
            contracts_data = [vars(c) for c in contracts.values()]
            
            # Agências precisam de tratamento especial para property_ids
            agencies_data = []
            for a in agencies.values():
                real_estate_dict = vars(a).copy()
                real_estate_dict['property_ids'] = ','.join(a.property_ids) if a.property_ids else ''
                agencies_data.append(real_estate_dict)
            
            payments_data = [vars(p) for p in payments.values()]
            
            extracts_data = [vars(e) for e in extracts.values()]
            guarantors_data = [vars(g) for g in guarantors.values()]
            bail_insurances_data = [vars(b) for b in bail_insurances.values()]
            
            # Salva todos os arquivos
            self._save_data("tenant.xlsx", tenants_data)
            self._save_data("property.xlsx", properties_data)
            self._save_data("contract.xlsx", contracts_data)
            self._save_data("real_estate.xlsx", agencies_data)
            self._save_data("payments.xlsx", payments_data)
            self._save_data("extract.xlsx", extracts_data)
            self._save_data("guarantor.xlsx", guarantors_data)
            self._save_data("bail_insurance.xlsx", bail_insurances_data)
            
        except Exception as e:
            print(f"Erro ao salvar dados: {str(e)}")