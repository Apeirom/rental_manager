# utils/visualization.py

from tabulate import tabulate
from utils.dateProcessing import iso_para_formatado
from utils.numbersProcessing import format_phone

def show_tenants(tenants):
    print("\n=== TENANTS ===")
    data = [[i + 1, t.name, t.cpf or "", t.cnpj or ""] for i, t in enumerate(tenants)]
    print(tabulate(data, headers=["#", "Name", "CPF", "CNPJ"], tablefmt="grid"))

def show_properties(properties):
    print("\n=== PROPERTIES ===")
    data = [[i + 1, p.property_name, p.owner_name, p.address, p.room_count] for i, p in enumerate(properties)]
    print(tabulate(data, headers=["#", "Name", "Owner", "Address", "Room Count"], tablefmt="grid"))

def show_real_estates(real_estates):
    print("\n=== REAL ESTATES ===")
    data = [[i + 1, r.name, format_phone(r.phone), r.commission] for i, r in enumerate(real_estates)]
    print(tabulate(data, headers=["#", "Name", "Phone", "Commission"], tablefmt="grid"))

def show_contracts(contracts, find_tenant, find_real_estate, find_property):
    print("\n=== CONTRACTS ===")
    data = []
    for i, c in enumerate(contracts):
        tenant = find_tenant(c.tenant_id)
        real_estate = find_real_estate(c.real_estate_id)
        prop = find_property(c.property_id)
        data.append([
            i + 1,
            tenant.name,
            real_estate.name,
            prop.property_name,
            c.rent_amount,
            c.rental_deposit,
            c.room_name,
            c.file_path,
            "Active" if c.acting else "Inactive"
        ])
    print(tabulate(data, headers=["#", "Tenant", "Real Estate", "Property", "Rent", "Deposit", "Room", "File", "Status"], tablefmt="grid"))

def show_extracts(extracts, find_contract, find_tenant, find_property, find_real_estate):
    print("\n=== EXTRACTS ===")
    data = []
    for i, e in enumerate(extracts):
        contract = find_contract(e.contract_id)
        tenant = find_tenant(contract.tenant_id)
        prop = find_property(contract.property_id)
        real_estate = find_real_estate(contract.real_estate_id)

        data.append([
            i + 1,
            f"{e.month_ref:02}/{e.year_ref}",
            tenant.name,
            prop.property_name,
            contract.room_name,
            real_estate.name,
            e.rent_amount or 0,
            e.water or 0,
            e.agreement or 0
        ])
    print(tabulate(data, headers=["#", "Reference", "Tenant", "Property", "Room", "Real Estate", "Rent", "Water", "Agreement"], tablefmt="grid"))

def show_payments(payments, find_tenant, find_property, find_real_estate):
    print("\n=== PAYMENTS ===")
    data = []
    for i, p in enumerate(payments):
        tenant = find_tenant(p.tenant_id)
        prop = find_property(p.property_id)
        real_estate = find_real_estate(p.real_estate_id)

        data.append([
            i + 1,
            f"{p.month_ref:02}/{p.year_ref}",
            tenant.name,
            prop.property_name,
            real_estate.name,
            p.file_path,
            iso_para_formatado(p.created_at)
        ])
    print(tabulate(data, headers=["#", "Reference", "Tenant", "Property", "Real Estate", "Receipt Path", "Created At"], tablefmt="grid"))

def show_guarantors(guarantors):
    print("\n=== GUARANTORS ===")
    data = [[i + 1, g.name, g.cpf or "", g.cnpj or "", format_phone(g.phone)] for i, g in enumerate(guarantors)]
    print(tabulate(data, headers=["#", "Name", "CPF", "CNPJ", "Phone"], tablefmt="grid"))

def show_bail_insurances(bail_insurances):
    print("\n=== BAIL INSURANCES ===")
    data = [[i + 1, b.name, b.cnpj, b.email, format_phone(b.phone)] for i, b in enumerate(bail_insurances)]
    print(tabulate(data, headers=["#", "Name", "CNPJ", "Email", "Phone"], tablefmt="grid"))
