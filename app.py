from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from config import Config
from rental.sistema import RentalSystem

app = Flask(__name__)
app.config.from_object(Config)

# --- INSTANCIA O SISTEMA ---
system = RentalSystem(app.config['DATA_FOLDER'])

# --- HELPER: Renderização Inteligente (SPA) ---
def render_spa(partial_name, title="Sistema Aluguel", **kwargs):
    """
    Se for requisição HTMX: retorna apenas o HTML parcial (sem cabeçalho/menu).
    Se for acesso direto (F5): retorna o base.html com o parcial injetado dentro.
    """
    if request.headers.get('HX-Request'):
        return render_template(partial_name, **kwargs)
    
    # Se for acesso direto pelo navegador, carregamos o layout base
    # e passamos o nome do template parcial para ser incluído
    return render_template('base_spa_wrapper.html', 
                           partial_name=partial_name, 
                           title=title, 
                           **kwargs)

# --- DASHBOARD & GERAL ---

@app.route('/')
def dashboard():
    # Calcula contagens para os cards
    counts = {
        'tenants': len(system.tenants),
        'properties': len(system.properties),
        'contracts': len(system.get_active_contracts()),
        'payments': len(system.payments)
    }
    
    # Se for HTMX (clique no menu), retorna só o miolo
    if request.headers.get('HX-Request'):
         # Precisamos criar um partial específico ou retornar o index.html sem o extends
         # Para simplificar, vamos retornar o index normal, mas o index precisa ser adaptado
         # O ideal é ter um partial para o dashboard também.
         return render_template('partials/dashboard.html', counts=counts)
         
    return render_template('index.html', counts=counts)

@app.route('/dashboard/partial')
def dashboard_partial():
    """Rota específica para o botão 'Dashboard' carregar via HTMX"""
    counts = {
        'tenants': len(system.tenants),
        'properties': len(system.properties),
        'contracts': len(system.get_active_contracts()),
        'payments': len(system.payments)
    }
    # Reutiliza o mesmo bloco de HTML do index, mas idealmente seria um arquivo separado
    return render_template('partials/dashboard.html', counts=counts)

@app.route('/salvar')
def save_data():
    system.save_all()
    flash('Todos os dados foram salvos com sucesso!', 'success')
    return redirect(url_for('dashboard'))

# --- TENANTS (INQUILINOS) ---

@app.route('/tenants', methods=['GET', 'POST'])
def tenants_list():
    if request.method == 'POST':
        # Criar novo inquilino
        name = request.form.get('name')
        cpf = request.form.get('cpf')
        cnpj = request.form.get('cnpj')
        
        system.add_tenant(name, cpf, cnpj)
        system.save_all()
        flash('Inquilino adicionado!', 'success')
        
        # Retorna a lista atualizada para o HTMX substituir
        return render_template('partials/tenants/list.html', tenants=system.tenants)

    # GET: Listar
    return render_spa('partials/tenants/list.html', title="Inquilinos", tenants=system.tenants)

@app.route('/tenants/new')
def tenants_form():
    return render_template('partials/tenants/form.html')

@app.route('/tenants/<id>', methods=['DELETE'])
def tenants_delete(id):
    system.remove_tenant(id)
    system.save_all()
    # Retorna a lista atualizada após deletar
    return render_template('partials/tenants/list.html', tenants=system.tenants)

# --- PROPERTIES (IMÓVEIS) ---

@app.route('/properties', methods=['GET', 'POST'])
def properties_list():
    if request.method == 'POST':
        p_name = request.form.get('property_name')
        o_name = request.form.get('owner_name')
        addr = request.form.get('address')
        rooms = request.form.get('room_count', 0)
        
        system.add_property(p_name, o_name, addr, int(rooms))
        system.save_all()
        flash('Imóvel salvo!', 'success')
        
        return render_template('partials/properties/list.html', properties=system.properties)

    return render_spa('partials/properties/list.html', title="Imóveis", properties=system.properties)

@app.route('/properties/new')
def properties_form():
    return render_template('partials/properties/form.html')

@app.route('/properties/<id>', methods=['DELETE'])
def properties_delete(id):
    system.remove_property(id)
    system.save_all()
    return render_template('partials/properties/list.html', properties=system.properties)

# --- CONTRACTS (CONTRATOS) ---

@app.route('/contracts', methods=['GET', 'POST'])
def contracts_list():
    if request.method == 'POST':
        # Lógica de criação de contrato
        try:
            system.add_contract(
                guarantee=request.form.get('guarantee'),
                rental_deposit=float(request.form.get('rental_deposit', 0)),
                rent_amount=float(request.form.get('rent_amount', 0)),
                room_name=request.form.get('room_name'),
                property_id=request.form.get('property_id'),
                tenant_id=request.form.get('tenant_id'),
                real_estate_id=request.form.get('real_estate_id'),
                guarantee_id=request.form.get('guarantee_id'),
                file_path=None # Upload de arquivo seria tratado aqui
            )
            system.save_all()
            flash('Contrato criado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao criar contrato: {str(e)}', 'error')

        # Precisamos recarregar as listas para renderizar a tabela corretamente se usarmos nomes
        return render_template('partials/contracts/list.html', contracts=system.contracts.values())

    return render_spa('partials/contracts/list.html', title="Contratos", contracts=system.contracts.values())

@app.route('/contracts/new')
def contracts_form():
    # Precisamos enviar os dados para preencher os <select>
    return render_template('partials/contracts/form.html', 
                           tenants=system.tenants,
                           properties=system.properties,
                           agencies=system.agencies)

@app.route('/contracts/<id>', methods=['DELETE'])
def contracts_delete(id):
    system.remove_contract(id)
    system.save_all()
    return render_template('partials/contracts/list.html', contracts=system.contracts.values())

if __name__ == '__main__':
    app.run(debug=True)