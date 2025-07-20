Para rodar esse projeto é necessário instalar o python e seu interpretador.

Agora instale também as dependencias doprojeto usando diretio o terminal:  pip install -r requirements.txt

Se você está começando a usar o projeto agora, inicialize as tabelas que serão usadas para o pertencimento de dados: py initialize_data.py




Estrutura do repositório:

rental_manager/
│
├── main.py                       # Arquivo principal (terminal/menu de interação)
├── requirements.txt              # Lista de dependências (como openpyxl, pandas etc)
├── README.md                     # Descrição do projeto e instruções de uso
├── initialize_data               # Inicializador de Tabelas
│
├── data/
|   ├── tenant.xlsx               # Arquivo Excel que armazena os dados de cada Inquilino
│   ├── property.xlsx             # Arquivo Excel que armazena os dados de cada Imóvel
|   ├── contract.xlsx             # Arquivo Excel que armazena os dados de cada Contrato
│   ├── real_estate.xlsx          # Arquivo Excel que armazena os dados de cada Imobiliária
│   ├── payments.xlsx             # Arquivo Excel que armazena os dados de cada Pagamentos
|   ├── gaurantor.xlsx            # Arquivo Excel que armazena os dados de cada Fiador
|   ├── extract.xlsx              # Arquivo Excel que armazena os dados de cada extrato
|   └── bail_insurance.xlsx       # Arquivo Excel que armazena os dados de cada Seguradora
│
├── documents/
│   ├── contratos/                # Contratos de locação
│   ├── comprovantes_pagamento/   # Comprovantes de pagamentos de aluguel
│   ├── analises/                 # Arquivos de analises feitas
│   ├── estratos/                 # Estratos enviados para a imobiliária
│   └── outros/                   # Qualquer outro tipo de documento relevante
│
├── rental/
│   ├── __init__.py
│   ├── tenant.py                 # Classe Tenant (Inquilino)
│   ├── property.py               # Classe Property (Imóvel)
│   ├── contract.py               # Classe Contract (Contrato)
|   ├── real_estate.py            # Classe real_estate (Imobiliária)
|   ├── payments.py               # Classe Payments (Pagamentos)
|   ├── gaurantor.py              # Classe Gaurantor (Fiadores)
|   ├── extract.py                # Classe Extract (Extratos)
|   ├── bail_insurance.py         # Classe Bail_insurance (Seguradoras)
|   ├── data_manager.py           # Classe para ler/escrever no Excel
│   └── sistema.py                # Classe ou funções de controle geral do sistema
│
└── utils/                        # Funções auxiliares (ex: validações, datas, etc.)
    ├── __init__.py
    ├── dateProcessing.py
    ├── analysis.py
    └── numberProcessing               