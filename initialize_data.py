# initialize_data.py
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Define os nomes dos arquivos e as colunas de cada tabela

tables = {
    "tenant.xlsx": [
        "id", "name", "cpf", "cnpj"
    ],
    "property.xlsx": [
        "id", "property_name", "owner_name", "address", "room_count"
    ],
    "contract.xlsx": [
        "id", "guarantee", "rental_deposit", "guarantee_id" ,"rent_amount", "room_name" , "property_id", "tenant_id", "real_estate_id", "acting", "file_path"
    ],
    "real_estate.xlsx": [
        "id", "name", "cnpj", "address", "commission", "phone", "property_ids"
    ],
    "payments.xlsx": [
        "id", "payment_date", "month_ref", "year_ref", "contract_id", "receipt_path" #
    ],
    "extract.xlsx": [
        "id", "contract_id", "month_ref", "year_ref", "rent_amount", "receipt_path", "iptu", "water", "agreement" #
    ],
    "guarantor.xlsx": [
        "id", "name", "cpf", "cnpj"
    ],
    "bail_insurance.xlsx": [
        "id", "value", "vality", "insurance_company"
    ],
}

def create_excel_tables():
    os.makedirs(DATA_DIR, exist_ok=True)
    for filename, columns in tables.items():
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            df = pd.DataFrame(columns=columns)
            df.to_excel(path, index=False)
            print(f"✅ Criado: {filename}")
        else:
            print(f"⚠️  Já existe: {filename} — nada foi sobrescrito.")

if __name__ == "__main__":
    create_excel_tables()
