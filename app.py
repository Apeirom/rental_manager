from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from rental.sistema import RentalSystem

app = Flask(__name__)
app.config.from_object(Config)

# --- INSTANCIA O SISTEMA ---
system = RentalSystem(app.config['DATA_FOLDER'])

# --- HELPER: Renderização Inteligente (SPA) ---
def render_spa(partial_name, title="Sistema Aluguel", **kwargs):
    if request.headers.get('HX-Request'):
        return render_template(partial_name, **kwargs)
    return render_template('base_spa_wrapper.html', 
                           partial_name=partial_name, 
                           title=title, 
                           **kwargs)

# --- DASHBOARD ---
@app.route('/')
def dashboard():
    counts = {
        'tenants': len(system.tenants),
        'properties': len(system.properties),
        'contracts': len(system.get_active_contracts()),
        'payments': len(system.payments),
        'agencies': len(system.agencies),
        'extracts': len(system.extracts),
        'guarantors': len(system.guarantors),
        'bail_insurances': len(system.bail_insurances)
    }
    if request.headers.get('HX-Request'):
         return render_template('partials/dashboard.html', counts=counts)
    return render_template('index.html', counts=counts)

@app.route('/dashboard/partial')
def dashboard_partial():
    return dashboard()

@app.route('/salvar')
def save_data():
    system.save_all()
    flash('Dados salvos com sucesso!', 'success')
    return redirect(url_for('dashboard'))

# ==========================================
# CRUDs SIMPLES
# ==========================================

# --- 1. INQUILINOS ---
@app.route('/tenants', methods=['GET', 'POST'])
def tenants_list():
    if request.method == 'POST':
        system.add_tenant(request.form.get('name'), request.form.get('cpf'), request.form.get('cnpj'))
        system.save_all()
        flash('Inquilino adicionado!', 'success')
        return render_template('partials/tenants/list.html', tenants=system.tenants)
    return render_spa('partials/tenants/list.html', title="Inquilinos", tenants=system.tenants)

@app.route('/tenants/new')
def tenants_form():
    return render_template('partials/tenants/form.html')

@app.route('/tenants/edit/<id>', methods=['GET', 'POST'])
def tenants_edit(id):
    tenant = system.tenants.get(id)
    if request.method == 'POST':
        tenant.name = request.form.get('name')
        tenant.cpf = request.form.get('cpf')
        tenant.cnpj = request.form.get('cnpj')
        system.save_all()
        flash('Inquilino atualizado!', 'success')
        return render_template('partials/tenants/list.html', tenants=system.tenants)
    return render_template('partials/tenants/form.html', tenant=tenant)

@app.route('/tenants/<id>', methods=['DELETE'])
def tenants_delete(id):
    system.remove_tenant(id)
    system.save_all()
    return render_template('partials/tenants/list.html', tenants=system.tenants)

# --- 2. IMÓVEIS ---
@app.route('/properties', methods=['GET', 'POST'])
def properties_list():
    if request.method == 'POST':
        system.add_property(
            request.form.get('property_name'), request.form.get('owner_name'), 
            request.form.get('address'), int(request.form.get('room_count', 0))
        )
        system.save_all()
        flash('Imóvel salvo!', 'success')
        return render_template('partials/properties/list.html', properties=system.properties)
    return render_spa('partials/properties/list.html', title="Imóveis", properties=system.properties)

@app.route('/properties/new')
def properties_form():
    return render_template('partials/properties/form.html')

@app.route('/properties/edit/<id>', methods=['GET', 'POST'])
def properties_edit(id):
    prop = system.properties.get(id)
    if request.method == 'POST':
        prop.property_name = request.form.get('property_name')
        prop.owner_name = request.form.get('owner_name')
        prop.address = request.form.get('address')
        prop.room_count = int(request.form.get('room_count', 0))
        system.save_all()
        flash('Imóvel atualizado!', 'success')
        return render_template('partials/properties/list.html', properties=system.properties)
    return render_template('partials/properties/form.html', property=prop)

@app.route('/properties/<id>', methods=['DELETE'])
def properties_delete(id):
    system.remove_property(id)
    system.save_all()
    return render_template('partials/properties/list.html', properties=system.properties)

# --- 3. IMOBILIÁRIAS ---
@app.route('/real_estates', methods=['GET', 'POST'])
def real_estates_list():
    if request.method == 'POST':
        system.add_real_estate(
            name=request.form.get('name'), cnpj=request.form.get('cnpj'),
            commission=float(request.form.get('commission', 0)),
            phone=request.form.get('phone'), address=request.form.get('address')
        )
        system.save_all()
        flash('Imobiliária adicionada!', 'success')
        return render_template('partials/real_estates/list.html', agencies=system.agencies)
    return render_spa('partials/real_estates/list.html', title="Imobiliárias", agencies=system.agencies)

@app.route('/real_estates/new')
def real_estates_form():
    return render_template('partials/real_estates/form.html')

@app.route('/real_estates/<id>', methods=['DELETE'])
def real_estates_delete(id):
    system.remove_real_estate(id)
    system.save_all()
    return render_template('partials/real_estates/list.html', agencies=system.agencies)

# --- 4. FIADORES ---
@app.route('/guarantors', methods=['GET', 'POST'])
def guarantors_list():
    if request.method == 'POST':
        system.add_guarantor(request.form.get('name'), request.form.get('cpf'), request.form.get('cnpj'))
        system.save_all()
        flash('Fiador adicionado!', 'success')
        return render_template('partials/guarantors/list.html', guarantors=system.guarantors)
    return render_spa('partials/guarantors/list.html', title="Fiadores", guarantors=system.guarantors)

@app.route('/guarantors/new')
def guarantors_form():
    return render_template('partials/guarantors/form.html')

@app.route('/guarantors/<id>', methods=['DELETE'])
def guarantors_delete(id):
    system.remove_guarantor(id)
    system.save_all()
    return render_template('partials/guarantors/list.html', guarantors=system.guarantors)

# --- 5. SEGUROS ---
@app.route('/bail_insurances', methods=['GET', 'POST'])
def bail_insurances_list():
    if request.method == 'POST':
        system.add_bail_insurance(
            value=float(request.form.get('value', 0)),
            insurance_company=request.form.get('insurance_company'), vality=request.form.get('vality')
        )
        system.save_all()
        flash('Seguro adicionado!', 'success')
        return render_template('partials/bail_insurances/list.html', bail_insurances=system.bail_insurances)
    return render_spa('partials/bail_insurances/list.html', title="Seguros Fiança", bail_insurances=system.bail_insurances)

@app.route('/bail_insurances/new')
def bail_insurances_form():
    return render_template('partials/bail_insurances/form.html')

@app.route('/bail_insurances/<id>', methods=['DELETE'])
def bail_insurances_delete(id):
    system.remove_bail_insurance(id)
    system.save_all()
    return render_template('partials/bail_insurances/list.html', bail_insurances=system.bail_insurances)

# ==========================================
# CRUDs COMPLEXOS (Com Relacionamentos)
# ==========================================

# --- 6. CONTRATOS ---
@app.route('/contracts', methods=['GET', 'POST'])
def contracts_list():
    if request.method == 'POST':
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
                file_path=request.form.get('file_path')
            )
            system.save_all()
            flash('Contrato criado!', 'success')
        except Exception as e:
            flash(f'Erro: {str(e)}', 'error')
        
        return render_template('partials/contracts/list.html', 
                               contracts=system.contracts.values(),
                               tenants=system.tenants,
                               properties=system.properties,
                               agencies=system.agencies)

    return render_spa('partials/contracts/list.html', title="Contratos", 
                      contracts=system.contracts.values(),
                      tenants=system.tenants,
                      properties=system.properties,
                      agencies=system.agencies)

@app.route('/contracts/new')
def contracts_form():
    return render_template('partials/contracts/form.html', 
                           tenants=system.tenants, properties=system.properties, 
                           agencies=system.agencies, guarantors=system.guarantors, 
                           bail_insurances=system.bail_insurances)

@app.route('/contracts/<id>', methods=['DELETE'])
def contracts_delete(id):
    system.remove_contract(id)
    system.save_all()
    return render_template('partials/contracts/list.html', 
                           contracts=system.contracts.values(),
                           tenants=system.tenants, properties=system.properties, agencies=system.agencies)

# --- 7. PAGAMENTOS ---
@app.route('/payments', methods=['GET', 'POST'])
def payments_list():
    if request.method == 'POST':
        system.add_payment(
            contract_id=request.form.get('contract_id'),
            receipt_path=request.form.get('receipt_path'),
            month_ref=int(request.form.get('month_ref')), year_ref=int(request.form.get('year_ref'))
        )
        system.save_all()
        flash('Pagamento registrado!', 'success')
        
        return render_template('partials/payments/list.html', 
                               payments=system.payments,
                               contracts=system.contracts,
                               tenants=system.tenants,
                               properties=system.properties)

    return render_spa('partials/payments/list.html', title="Pagamentos", 
                      payments=system.payments,
                      contracts=system.contracts,
                      tenants=system.tenants,
                      properties=system.properties)

@app.route('/payments/new')
def payments_form():
    # ADICIONADO: tenants e properties para o lookup no select
    return render_template('partials/payments/form.html', 
                           contracts=system.contracts,
                           tenants=system.tenants,
                           properties=system.properties)

@app.route('/payments/<id>', methods=['DELETE'])
def payments_delete(id):
    system.remove_payment(id)
    system.save_all()
    return render_template('partials/payments/list.html', 
                           payments=system.payments, contracts=system.contracts,
                           tenants=system.tenants, properties=system.properties)

# --- 8. EXTRATOS ---
@app.route('/extracts', methods=['GET', 'POST'])
def extracts_list():
    if request.method == 'POST':
        rent_val = request.form.get('rent_amount')
        iptu_val = request.form.get('iptu')
        water_val = request.form.get('water')
        agreement_val = request.form.get('agreement')

        system.add_extract(
            contract_id=request.form.get('contract_id'),
            month_ref=int(request.form.get('month_ref')), 
            year_ref=int(request.form.get('year_ref')),
            rent_amount=float(rent_val) if rent_val else 0.0,
            receipt_path=request.form.get('receipt_path'),
            iptu=float(iptu_val) if iptu_val else 0.0, 
            water=float(water_val) if water_val else 0.0,
            agreement=float(agreement_val) if agreement_val else 0.0
        )
        system.save_all()
        flash('Extrato gerado!', 'success')
        
        return render_template('partials/extracts/list.html', 
                               extracts=system.extracts,
                               contracts=system.contracts,
                               tenants=system.tenants,
                               properties=system.properties)

    return render_spa('partials/extracts/list.html', title="Extratos", 
                      extracts=system.extracts,
                      contracts=system.contracts,
                      tenants=system.tenants,
                      properties=system.properties)

@app.route('/extracts/new')
def extracts_form():
    # ADICIONADO: tenants e properties para o lookup no select
    return render_template('partials/extracts/form.html', 
                           contracts=system.contracts,
                           tenants=system.tenants,
                           properties=system.properties)

@app.route('/extracts/edit/<id>', methods=['GET', 'POST'])
def extracts_edit(id):
    extract = system.extracts.get(id)
    
    if request.method == 'POST':
        rent_val = request.form.get('rent_amount')
        iptu_val = request.form.get('iptu')
        water_val = request.form.get('water')
        agreement_val = request.form.get('agreement')

        extract.contract_id = request.form.get('contract_id')
        extract.month_ref = int(request.form.get('month_ref'))
        extract.year_ref = int(request.form.get('year_ref'))
        extract.rent_amount = float(rent_val) if rent_val else 0.0
        extract.iptu = float(iptu_val) if iptu_val else 0.0
        extract.water = float(water_val) if water_val else 0.0
        extract.agreement = float(agreement_val) if agreement_val else 0.0
        
        system.save_all()
        flash('Extrato atualizado!', 'success')
        
        return render_template('partials/extracts/list.html', 
                               extracts=system.extracts,
                               contracts=system.contracts,
                               tenants=system.tenants,
                               properties=system.properties)

    # GET: ADICIONADO tenants e properties
    return render_template('partials/extracts/form.html', 
                           extract=extract, 
                           contracts=system.contracts,
                           tenants=system.tenants,
                           properties=system.properties)

@app.route('/extracts/<id>', methods=['DELETE'])
def extracts_delete(id):
    system.remove_extract(id)
    system.save_all()
    return render_template('partials/extracts/list.html', 
                           extracts=system.extracts, contracts=system.contracts,
                           tenants=system.tenants, properties=system.properties)

if __name__ == '__main__':
    app.run(debug=True)