from datetime import date
from tabulate import tabulate
import pandas as pd
import os

def menu_analises(rental_system):
    print("\n=== ANÁLISES ===")
    print("1. Analisar extratos para imposto de renda")
    print("2. Voltar ao menu principal")
    choice = input("Escolha uma opção: ")

    match choice:
        case "1":
            analise_imposto_de_renda_extratos(rental_system)
        case "2":
            return
        case _:
            print("Opção inválida. Tente novamente.")

def analise_imposto_de_renda_extratos(rental_system):
    ano_inicio = int(input("Ano de início: "))
    mes_inicio = int(input("Mês de início (1-12): "))
    ano_fim = int(input("Ano de fim: "))
    mes_fim = int(input("Mês de fim (1-12): "))
    df = construir_dataframe_imposto_de_renda(rental_system, ano_inicio, mes_inicio, ano_fim, mes_fim)
    
    print("Como deseja exibir a análise?")
    print("1. Exibir no terminal")
    print("2. Salvar em arquivo Excel")
    exibir_opcao = input("Escolha uma opção: ")
    match exibir_opcao:
        case "1":
            exibir_analise_terminal(df)
        case "2":
            salvar_analise_excel(df)
        case _:
            print("Opção inválida. Tente novamente.")

def construir_dataframe_imposto_de_renda(rental_system, ano_inicio, mes_inicio, ano_fim, mes_fim):
    """
    Filtra extratos por intervalo de tempo e constrói um DataFrame para análise do imposto de renda.
    A renda é calculada como (aluguel + acordo) * (1 - comissão da imobiliária).
    """
    registros = []
    data_inicio = date(ano_inicio, mes_inicio, 1)
    data_fim = date(ano_fim, mes_fim, 1)

    for extract in rental_system.extracts.values():
        data_extrato = date(extract.year_ref, extract.month_ref, 1)

        if not (data_inicio <= data_extrato <= data_fim):
            continue

        contract = rental_system.find_contract_by_id(extract.contract_id)
        tenant = rental_system.find_tenant_by_id(contract.tenant_id)
        real_estate = rental_system.find_real_estate_by_id(contract.real_estate_id)
        property_obj = rental_system.find_property_by_id(contract.property_id)

        aluguel = extract.rent_amount or 0
        acordo = extract.agreement or 0
        iptu = extract.iptu or 0
        agua = extract.water or 0
        comissao = real_estate.commission or 0

        base = aluguel + acordo
        renda = base * (1 - comissao)

        registros.append({
            "Data Ref": f"{extract.month_ref:02}/{extract.year_ref}",
            "Inquilino": tenant.name,
            "CPF/CNPJ": tenant.cpf or tenant.cnpj or "",
            "Tipo Documento": "CPF" if tenant.cpf else "CNPJ" if tenant.cnpj else "N/D",
            "Sala/Imóvel": f"{property_obj.property_name} - {contract.room_name}",
            "Aluguel (R$)": aluguel,
            "IPTU (R$)": iptu,
            "Água (R$)": agua,
            "Acordo (R$)": acordo,
            "Comissão (R$)": comissao * base,
            "Renda Líquida (R$)": renda
        })

    df = pd.DataFrame(registros)
    df["Ano"] = df["Data Ref"].str[-4:].astype(int)
    df["Mês"] = df["Data Ref"].str[:2].astype(int)
    df = df.sort_values(by=["Ano", "Mês"]).drop(columns=["Ano", "Mês"]).reset_index(drop=True)
    return df

def exibir_analise_terminal(df):
    """
    Agrupa e exibe a análise de imposto de renda por mês/ano no terminal usando tabulate.
    """
    if df.empty:
        print("Nenhum dado encontrado para o intervalo selecionado.")
        return

    grupos = df.groupby("Data Ref")

    for data_ref, grupo in grupos:
        print(f"\n=== {data_ref} ===")
        print(tabulate(
            grupo[[
                "Inquilino", "CPF/CNPJ", "Sala/Imóvel",
                "Aluguel (R$)", "IPTU (R$)", "Água (R$)", "Acordo (R$)", "Comissão (R$)", "Renda Líquida (R$)"
            ]],
            headers="keys",
            tablefmt="grid",
            showindex=False
        ))

def salvar_analise_excel(df):
    """
    Salva a análise de imposto de renda em um arquivo .xlsx dentro de documents/analises/.
    """
    if df.empty:
        print("Nenhum dado para salvar.")
        return

    pasta_destino = os.path.join("documents", "analises")
    os.makedirs(pasta_destino, exist_ok=True)

    data_inicio = df["Data Ref"].iloc[0].replace("/", "-")
    data_fim = df["Data Ref"].iloc[-1].replace("/", "-")
    nome_arquivo = f"analise_imposto_renda_{data_inicio}_a_{data_fim}.xlsx"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)

    df.to_excel(caminho_completo, index=False)
    print(f"Análise salva em: {caminho_completo}")