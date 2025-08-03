# main.py

import os
from rental.sistema import RentalSystem
from utils.analysis import menu_analises

# --- CONFIGURATIONS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
system = RentalSystem(DATA_DIR)


# --- UTILITY FUNCTIONS ---
def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Pauses execution until Enter is pressed."""
    input("\nPressione Enter para continuar...")

def prompt_for_input(prompt, required_type=str, default=None):
    """
    Prompts the user for input, handling type casting and validation.
    An empty input will return the default value if provided.
    """
    while True:
        try:
            value = input(prompt).strip()
            if not value and default is not None:
                return default
            # Handle optional inputs where an empty string is acceptable
            if not value and required_type == str:
                return None
            return required_type(value)
        except (ValueError, TypeError):
            print(f"Entrada inválida. Por favor, forneça um valor do tipo '{required_type.__name__}'.")

# --- CORE INTERACTION LOGIC ---

def select_item(item_type: str) -> str | None:
    """
    Displays a list of items using its visualization function and prompts the user to select one.
    
    Args:
        item_type (str): The key for the entity in ENTITY_CONFIG (e.g., 'tenant').

    Returns:
        str | None: The ID of the selected item, or None if cancelled or invalid.
    """
    config = ENTITY_CONFIG[item_type]
    collection = config['collection']
    
    if not collection:
        print(f"Nenhum(a) {config['title'].lower()} cadastrado(a) para selecionar.")
        return None

    print(f"\n--- SELECIONE UM(A) {config['title'].upper()} ---")
    
    # Use the existing show function to display the items
    config['show_func']()
    
    items = list(collection.values())
    try:
        choice = int(input(f"Escolha o número do(a) {config['title'].lower()} (0 para cancelar): "))
        if 1 <= choice <= len(items):
            return items[choice - 1].id
        elif choice == 0:
            print("Seleção cancelada.")
            return None
        else:
            print("Número inválido.")
            return None
    except (ValueError, IndexError):
        print("Entrada inválida. Por favor, digite um número da lista.")
        return None

def _get_guarantee_details():
    """Handles the specific logic for selecting a contract guarantee."""
    print("\nTipo de garantia:\n1. Caução\n2. Fiador\n3. Seguro fiança")
    choice = prompt_for_input("Escolha (1-3): ", int)

    if choice == 1:
        return {
            "guarantee": "Caução",
            "rental_deposit": prompt_for_input("Valor da caução: ", float),
            "guarantee_id": None
        }
    if choice == 2:
        return {
            "guarantee": "Fiador",
            "rental_deposit": 0.0,
            "guarantee_id": select_item('guarantor')
        }
    if choice == 3:
        return {
            "guarantee": "Seguro Fiança",
            "rental_deposit": 0.0,
            "guarantee_id": select_item('bail_insurance')
        }
    
    print("Opção de garantia inválida.")
    return None

def handle_add(item_type: str):
    """Generic handler for adding any type of item."""
    clear_screen()
    config = ENTITY_CONFIG[item_type]
    print(f"=== ADICIONAR {config['title'].upper()} ===")
    
    item_data = {}
    
    # Handle special cases first
    if item_type == 'contract':
        guarantee_details = _get_guarantee_details()
        if guarantee_details is None or guarantee_details.get('guarantee_id') is None and guarantee_details.get('guarantee') != 'Caução':
            print("A seleção da garantia é obrigatória. Operação cancelada.")
            return
        item_data.update(guarantee_details)

    # Prompt for fields defined in config
    for field, (prompt, field_type, default) in config.get('add_fields', {}).items():
        if field.endswith('_id'): # Handle selection of related items
            related_item_type = field.replace('_id', '')
            item_id = select_item(related_item_type)
            if not item_id:
                print(f"A seleção de um(a) {ENTITY_CONFIG[related_item_type]['title']} é obrigatória. Operação cancelada.")
                return
            item_data[field] = item_id
        else:
            item_data[field] = prompt_for_input(prompt, field_type, default)
            
    try:
        config['add_func'](**item_data)
        print(f"\n{config['title']} adicionado(a) com sucesso!")
    except Exception as e:
        print(f"\nOcorreu um erro ao adicionar o item: {e}")

def handle_view_data():
    """Handles viewing data for a selected class."""
    clear_screen()
    print("\n===== VISUALIZAR DADOS =====")
    for key, config in ENTITY_CONFIG.items():
        print(f"{config['menu_option']}. {config['title']}")
    
    choice = input("Escolha a classe para visualizar: ").strip()
    config = next((v for v in ENTITY_CONFIG.values() if v['menu_option'] == choice), None)
    
    if not config:
        print("Opção inválida.")
        return

    clear_screen()
    only_acting = input("Deseja ver apenas registros com contratos ativos? (s/n): ").strip().lower() == 's'
    
    # The show functions in `sistema.py` already handle the `only_acting` flag
    config['show_func'](only_acting=only_acting)

def handle_remove():
    """Generic handler for removing any type of item."""
    clear_screen()
    print("\n===== REMOVER ITEM =====")
    for key, config in ENTITY_CONFIG.items():
        print(f"{config['menu_option']}. {config['title']}")
    
    choice = input("Escolha o tipo de item para remover: ").strip()
    config = next((v for v in ENTITY_CONFIG.values() if v['menu_option'] == choice), None)

    if not config:
        print("Opção inválida.")
        return
        
    clear_screen()
    item_id_to_remove = select_item(config['item_key'])
    
    if item_id_to_remove:
        config['remove_func'](item_id_to_remove)
        print(f"\n{config['title']} removido com sucesso!")

def handle_edit():
    """Generic handler for editing any type of item."""
    clear_screen()
    print("=== EDIÇÃO DE INFORMAÇÕES ===")
    for key, config in ENTITY_CONFIG.items():
        print(f"{config['menu_option']}. {config['title']}")
    
    choice = input("Escolha o tipo de item para editar: ").strip()
    config = next((v for v in ENTITY_CONFIG.values() if v['menu_option'] == choice), None)

    if not config:
        print("Opção inválida.")
        return

    clear_screen()
    obj_id = select_item(config['item_key'])
    if not obj_id:
        return

    obj = config['collection'].get(obj_id)
    if not obj:
        print("Objeto não encontrado.")
        return

    print("\n--- ATRIBUTOS DISPONÍVEIS PARA EDIÇÃO ---")
    # Filter out private attributes, methods, and id fields
    editable_attrs = {k: v for k, v in vars(obj).items() if not k.startswith('_') and not k.endswith('_id') and k != 'id'}
    
    attr_list = list(editable_attrs.keys())
    for i, attr_name in enumerate(attr_list, 1):
        print(f"{i}. {attr_name} = {editable_attrs[attr_name]}")

    try:
        idx = int(input("\nEscolha o número do atributo para editar: ").strip())
        attr_name = attr_list[idx - 1]
    except (ValueError, IndexError):
        print("Seleção de atributo inválida.")
        return

    current_value = getattr(obj, attr_name)
    value_type = type(current_value) if current_value is not None else str
    
    new_value_str = input(f"Novo valor para '{attr_name}' (atual: {current_value}): ").strip()

    try:
        # Convert to the correct type
        if value_type == bool:
            new_value = new_value_str.lower() in ("true", "1", "sim", "s")
        else:
            new_value = value_type(new_value_str)
        
        setattr(obj, attr_name, new_value)
        print(f"\n✅ Atributo '{attr_name}' atualizado para: {new_value}")
    except Exception as e:
        print(f"Erro ao atualizar o valor: {e}")


# --- DATA AND MENU CONFIGURATION ---

ENTITY_CONFIG = {
    # Key: item_key, Title, Menu Option, Collection, Add Func, Remove Func, Show Func, Fields for adding
    'tenant': {
        'item_key': 'tenant', 'title': 'Inquilino', 'menu_option': '1',
        'collection': system.tenants, 'add_func': system.add_tenant,
        'remove_func': system.remove_tenant, 'show_func': system.show_tenants,
        'add_fields': {
            'name': ('Nome: ', str, None),
            'cpf': ('Caso pessoa física insira o CPF: ', str, None),
            'cnpj': ('Caso pessoa jurídica insira o CNPJ: ', str, None),
        }
    },
    'property': {
        'item_key': 'property', 'title': 'Imóvel', 'menu_option': '2',
        'collection': system.properties, 'add_func': system.add_property,
        'remove_func': system.remove_property, 'show_func': system.show_properties,
        'add_fields': {
            'property_name': ('Nome do imóvel (apelido ou sala): ', str, None),
            'owner_name': ('Nome do proprietário: ', str, None),
            'address': ('Endereço: ', str, None),
            'room_count': ('Número de salas: ', int, 0)
        }
    },
    'contract': {
        'item_key': 'contract', 'title': 'Contrato', 'menu_option': '3',
        'collection': system.contracts, 'add_func': system.add_contract,
        'remove_func': system.remove_contract, 'show_func': system.show_contracts,
        'add_fields': {
            'rent_amount': ('Valor do aluguel: ', float, None),
            'room_name': ('Nome da sala: ', str, None),
            'property_id': ('', None, None), # Placeholder for selection
            'tenant_id': ('', None, None),   # Placeholder for selection
            'real_estate_id': ('', None, None), # Placeholder for selection
            'file_path': ('Caminho do arquivo do contrato (opcional): ', str, None),
        }
    },
    'payment': {
        'item_key': 'payment', 'title': 'Pagamento', 'menu_option': '4',
        'collection': system.payments, 'add_func': system.add_payment,
        'remove_func': system.remove_payment, 'show_func': system.show_payments,
        'add_fields': {
            'contract_id': ('', None, None), # Placeholder for selection
            'receipt_path': ('Caminho do comprovante: ', str, None),
            'month_ref': ('Mês de referência (1-12): ', int, None),
            'year_ref': ('Ano de referência: ', int, None),
        }
    },
    'real_estate': {
        'item_key': 'real_estate', 'title': 'Imobiliária', 'menu_option': '5',
        'collection': system.agencies, 'add_func': system.add_real_estate,
        'remove_func': system.remove_real_estate, 'show_func': system.show_real_states,
        'add_fields': {
            'name': ('Nome da imobiliária: ', str, None),
            'cnpj': ('CNPJ: ', str, None),
            'commission': ('Comissão (ex: 0.1): ', float, None),
            'phone': ('Telefone (opcional): ', str, None),
            'address': ('Endereço (opcional): ', str, None),
        }
    },
    'extract': {
        'item_key': 'extract', 'title': 'Extrato', 'menu_option': '6',
        'collection': system.extracts, 'add_func': system.add_extract,
        'remove_func': system.remove_extract, 'show_func': system.show_extracts,
        'add_fields': {
            'contract_id': ('', None, None), # Placeholder for selection
            'month_ref': ('Mês de referência (1-12): ', int, None),
            'year_ref': ('Ano de referência: ', int, None),
            'rent_amount': ('Valor do aluguel: ', float, None),
            'receipt_path': ('Caminho do comprovante (opcional): ', str, None),
            'iptu': ('Valor do IPTU: ', float, 0),
            'water': ('Valor da água: ', float, 0),
            'agreement': ('Termos do acordo: ', str, None)
        }
    },
    'guarantor': {
        'item_key': 'guarantor', 'title': 'Fiador', 'menu_option': '7',
        'collection': system.guarantors, 'add_func': system.add_guarantor,
        'remove_func': system.remove_guarantor, 'show_func': system.show_guarantors,
        'add_fields': {
            'name': ('Nome completo: ', str, None),
            'cpf': ('CPF (opcional - deixe em branco para PJ): ', str, None),
            'cnpj': ('CNPJ (opcional - deixe em branco para PF): ', str, None),
        }
    },
    'bail_insurance': {
        'item_key': 'bail_insurance', 'title': 'Seguro Fiança', 'menu_option': '8',
        'collection': system.bail_insurances, 'add_func': system.add_bail_insurance,
        'remove_func': system.remove_bail_insurance, 'show_func': system.show_bail_insurances,
        'add_fields': {
            'value': ('Valor coberto pelo seguro: ', float, None),
            'insurance_company': ('Nome da seguradora: ', str, None),
            'vality': ('Data de validade (DD/MM/YYYY): ', str, None)
        }
    }
}

MENU_ACTIONS = {
    '1': lambda: handle_add('tenant'),
    '2': lambda: handle_add('property'),
    '3': lambda: handle_add('contract'),
    '4': lambda: handle_add('payment'),
    '5': lambda: handle_add('real_estate'),
    '6': lambda: handle_add('extract'),
    '7': lambda: handle_add('guarantor'),
    '8': lambda: handle_add('bail_insurance'),
    '9': handle_view_data,
    '10': handle_remove,
    '11': lambda: menu_analises(system),
    '12': handle_edit,
    '13': system.save_all,
}

# --- MAIN APPLICATION LOOP ---
def main():
    while True:
        clear_screen()
        print("\n===== MENU DO SISTEMA DE ALUGUEL =====")
        print("1. Adicionar Inquilino         8. Adicionar Seguro Fiança")
        print("2. Adicionar Imóvel            9. Visualizar Dados")
        print("3. Adicionar Contrato          10. Remover Item")
        print("4. Adicionar Pagamento         11. Análises")
        print("5. Adicionar Imobiliária       12. Editar Dados")
        print("6. Adicionar Extrato           13. Salvar")
        print("7. Adicionar Fiador            14. Salvar e Sair")
        
        choice = input("\nEscolha uma opção: ").strip()

        if choice == '14':
            system.save_all()
            print("Dados salvos. Encerrando o sistema...")
            break
        
        action = MENU_ACTIONS.get(choice)
        
        if action:
            clear_screen()
            action()
            if choice == '13':
                print("Dados salvos com sucesso.")
        else:
            print("Opção inválida.")
            
        pause()

if __name__ == "__main__":
    main()