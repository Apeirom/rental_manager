import os
from tabulate import tabulate
from rental.sistema import RentalSystem
from utils.analysis import menu_analises

# --- CONFIGURAÇÕES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
system = RentalSystem(DATA_DIR)


# --- FUNÇÕES UTILITÁRIAS ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("Pressione Enter para continuar...")


# --- INTERFACE DE MENU ---
def show_menu():
    print("\n===== RENTAL SYSTEM MENU =====")
    print("1. Adicionar inquilino")
    print("2. Adicionar imóvel")
    print("3. Adicionar contrato")
    print("4. Adicionar pagamento")
    print("5. Adicionar imobiliária")
    print("6. Adicionar extrato")
    print("7. Adicionar fiador")
    print("8. Adicionar seguro fiança")
    print("9. Visualizar dados")
    print("10. Remover item")
    print("11. Analises")
    print("12. Salvar")
    print("13. Salvar e sair")


def show_class_options():
    print("\n===== CLASSES DISPONÍVEIS =====")
    classes = [
        "Inquilino", "Imóvel", "Contrato", "Pagamento",
        "Imobiliária", "Extrato", "Fiador", "Seguro fiança"
    ]
    for i, cls in enumerate(classes, start=1):
        print(f"{i}. {cls}")


def escolher_id_por_nome(itens_dict, campos, titulo):
    itens = list(itens_dict.values())
    if not itens:
        print(f"Nenhum {titulo.lower()} cadastrado.")
        return None

    print(f"\n-- {titulo.upper()} DISPONÍVEIS --")
    tabela = [[i + 1] + [getattr(item, campo, '') for campo in campos] for i, item in enumerate(itens)]
    headers = ["#"] + campos
    print(tabulate(tabela, headers=headers, showindex=False))

    try:
        escolha = int(input(f"Escolha o número do(a) {titulo.lower()} (0 para cancelar): "))
        return itens[escolha - 1].id if 1 <= escolha <= len(itens) else None
    except ValueError:
        print("Entrada inválida! Digite um número.")
        return None


# --- AÇÕES DE ADIÇÃO ---
def adicionar_extrato():
    clear_screen()
    print("=== ADICIONAR EXTRATO ===")

    contratos = list(system.contracts.values())
    if not contratos:
        print("Nenhum contrato cadastrado.")
        return

    tabela = []
    for i, c in enumerate(contratos, start=1):
        tenant = system.find_tenant_by_id(c.tenant_id)
        real_estate = system.find_real_estate_by_id(c.real_estate_id)
        prop = system.find_property_by_id(c.property_id)
        tabela.append([
            i,
            tenant.name if tenant else "N/A",
            real_estate.name if real_estate else "N/A",
            prop.property_name if prop else "N/A",
            c.room_name,
            c.rent_amount
        ])

    print(tabulate(
        tabela,
        headers=["#", "Inquilino", "Imobiliária", "Imóvel", "Sala", "Aluguel (R$)"],
        showindex=False
    ))

    try:
        escolha = int(input("Escolha o número do contrato (0 para cancelar): "))
        if escolha == 0:
            print("Operação cancelada.")
            return
        if not 1 <= escolha <= len(contratos):
            raise ValueError
        contrato_escolhido = contratos[escolha - 1]
    except (ValueError, IndexError):
        print("Número inválido.")
        return

    month_ref = int(input("Mês de referência (1-12): "))
    year_ref = int(input("Ano de referência: "))
    rent_amount = float(input("Valor do aluguel: "))
    receipt_path = input("Caminho do comprovante (opcional): ") or None
    iptu = float(input("Valor do IPTU: ") or 0)
    water = float(input("Valor da água: ") or 0)
    agreement = input("Termos do acordo: ")

    system.add_extract(
        contrato_escolhido.id,
        month_ref, year_ref,
        rent_amount, receipt_path,
        iptu, water, agreement
    )
    print("Extrato adicionado com sucesso.")

def adicionar_fiador():
    clear_screen()
    print("=== ADICIONAR FIADOR ===")
    name = input("Nome completo: ")
    cpf = input("CPF (opcional - deixe em branco para PJ): ") or None
    cnpj = input("CNPJ (opcional - deixe em branco para PF): ") or None

    if not cpf and not cnpj:
        print("Erro: Fiador deve ter CPF ou CNPJ")
        return

    system.add_guarantor(name, cpf, cnpj)
    print("Fiador adicionado com sucesso!")


def adicionar_seguro_fianca():
    clear_screen()
    print("=== ADICIONAR SEGURO FIANÇA ===")
    value = float(input("Valor coberto pelo seguro: "))
    vality = input("Data de validade (DD/MM/YYYY): ")
    insurance_company = input("Nome da seguradora: ")

    system.add_bail_insurance(value, insurance_company, vality)
    print("Seguro fiança adicionado com sucesso!")


# --- VISUALIZAÇÃO DE DADOS ---
def show_data():
    clear_screen()
    show_class_options()
    option = input("Escolha a classe para visualizar: ").strip()

    only_acting = option in {'1', '2', '3', '5'} and input(
        "Deseja ver apenas registros com contratos ativos? (s/n): ").strip().lower() == "s"

    clear_screen()

    match option:
        case "1": system.show_tenants(only_acting)
        case "2": system.show_properties(only_acting)
        case "3": system.show_contracts(only_acting)
        case "4": system.show_payments(only_acting)
        case "5": system.show_real_states(only_acting)
        case "6": system.show_extracts()
        case "7": system.show_guarantors()
        case "8": system.show_bail_insurances()
        case _: print("Opção inválida.")


# --- REMOÇÃO DE ITENS ---
def remover_item():
    clear_screen()
    show_class_options()
    tipo = input("Escolha o tipo de item para remover (1-8): ").strip()

    tipo_dict = {
        "1": ("tenant", system.tenants, system.remove_tenant, system.show_tenants),
        "2": ("property", system.properties, system.remove_property, system.show_properties),
        "3": ("contract", system.contracts, system.remove_contract, system.show_contracts),
        "4": ("payment", system.payments, system.remove_payment, system.show_payments),
        "5": ("real_estate", system.agencies, system.remove_real_estate, system.show_real_states),
        "6": ("extract", system.extracts, system.remove_extract, system.show_extracts),
        "7": ("guarantor", system.guarantors, system.remove_guarantor, system.show_guarantors),
        "8": ("bail_insurance", system.bail_insurances, system.remove_bail_insurance, system.show_bail_insurances),
    }

    if tipo not in tipo_dict:
        print("Tipo inválido.")
        return

    _, itens, remover, mostrar = tipo_dict[tipo]
    mostrar()

    try:
        escolha = int(input("Digite o número do item que deseja remover (0 para cancelar): "))
        if escolha == 0:
            return
        item_id = list(itens.values())[escolha - 1].id
        remover(item_id)
        print("Item removido com sucesso!")
    except (ValueError, IndexError):
        print("Entrada inválida.")


# --- LOOP PRINCIPAL ---
while True:
    clear_screen()
    show_menu()
    choice = input("Escolha uma opção: ").strip()

    match choice:
        case "1":
            clear_screen()
            name = input("Nome: ")
            cpf = input("Caso pessoa física insira o CPF: ") or None
            cnpj = input("Caso pessoa jurídica insira o CNPJ: ") or None
            system.add_tenant(name, cpf, cnpj)

        case "2":
            clear_screen()
            nome = input("Nome do imóvel (apelido ou sala): ")
            proprietario = input("Nome do proprietário: ")
            endereco = input("Endereço: ")
            salas = int(input("Número de salas (opcional, padrão 0): ") or 0)
            system.add_property(nome, proprietario, endereco, salas)

        case "3":
            clear_screen()
            file_path = input("Caminho do arquivo do contrato: ") or None

            print("Tipo de garantia:\n1. Caução\n2. Fiador\n3. Seguro fiança")
            tipo = input("Escolha (1-3): ").strip()
            if tipo == "1":
                guarantee = "Caução"
                rental_deposit = float(input("Valor da caução: "))
                guarantee_id = None
            elif tipo == "2":
                guarantee = "Fiador"
                rental_deposit = 0.0
                guarantee_id = escolher_id_por_nome(system.guarantors, ["name", "cpf", "cnpj"], "Fiador")
            elif tipo == "3":
                guarantee = "Seguro Fiança"
                rental_deposit = 0.0
                guarantee_id = escolher_id_por_nome(system.bail_insurances, ["insurance_company", "value"], "Seguro Fiança")
            else:
                print("Opção inválida.")
                pause()
                continue

            rent_amount = float(input("Valor do aluguel: "))
            room_name = input("Nome da sala: ")
            property_id = escolher_id_por_nome(system.properties, ["property_name", "address"], "Imóvel")
            tenant_id = escolher_id_por_nome(system.tenants, ["name", "cpf"], "Inquilino")
            real_estate_id = escolher_id_por_nome(system.agencies, ["name", "cnpj"], "Imobiliária")

            if None in (property_id, tenant_id, real_estate_id):
                print("Operação cancelada. Dados obrigatórios ausentes.")
                pause()
                continue
        
            system.add_contract(
                guarantee, rental_deposit, rent_amount, room_name,
                property_id, tenant_id, real_estate_id, guarantee_id, file_path
            )

        case "4":
            clear_screen()
            print("=== SELECIONAR CONTRATO PARA PAGAMENTO ===")

            contratos = list(system.contracts.values())
            if not contratos:
                print("Nenhum contrato cadastrado.")
                pause()
                continue

            tabela = []
            for i, c in enumerate(contratos, start=1):
                tenant = system.find_tenant_by_id(c.tenant_id)
                real_estate = system.find_real_estate_by_id(c.real_estate_id)
                prop = system.find_property_by_id(c.property_id)
                tabela.append([
                    i,
                    tenant.name if tenant else "N/A",
                    real_estate.name if real_estate else "N/A",
                    prop.property_name if prop else "N/A",
                    c.room_name,
                    c.rent_amount
                ])

            print(tabulate(
                tabela,
                headers=["#", "Inquilino", "Imobiliária", "Imóvel", "Sala", "Aluguel (R$)"],
                showindex=False
            ))

            try:
                escolha = int(input("Escolha o número do contrato (0 para cancelar): "))
                if escolha == 0:
                    print("Operação cancelada.")
                    pause()
                    continue
                if not 1 <= escolha <= len(contratos):
                    raise ValueError
                contrato_escolhido = contratos[escolha - 1]
            except (ValueError, IndexError):
                print("Número inválido.")
                pause()
                continue

            receipt_path = input("Caminho do comprovante: ")
            month_ref = int(input("Mês de referência (1-12): "))
            year_ref = int(input("Ano de referência: "))

            system.add_payment(contrato_escolhido.id, receipt_path, month_ref, year_ref)
            print("Pagamento adicionado com sucesso.")

        case "5":
            clear_screen()
            name = input("Nome da imobiliária: ")
            cnpj = input("CNPJ: ")
            address = input("Endereço (opcional): ") or None
            commission = float(input("Comissão (ex: 0.1): "))
            phone = input("Telefone (opcional): ") or None
            system.add_real_estate(name, cnpj, commission, phone, address)

        case "6": adicionar_extrato()
        case "7": adicionar_fiador()
        case "8": adicionar_seguro_fianca()
        case "9": show_data()
        case "10": remover_item()
        case "11":
            clear_screen()
            menu_analises(system)
        case "12":
            system.save_all()
            print("Dados salvos.")
        case "13":
            system.save_all()
            print("Dados salvos. Encerrando o sistema...")
            break
        case _: print("Opção inválida.")

    pause()
