# config.py
import os

# Pega o diretório onde este arquivo (config.py) está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # Chave de segurança para sessões e proteção contra CSRF (essencial no Flask)
    SECRET_KEY = 'sua_chave_secreta_aqui_troque_isso_em_producao'
    
    # Define onde fica a pasta 'data'
    DATA_FOLDER = os.path.join(BASE_DIR, 'data')
    
    # Define onde fica a pasta 'static' (antiga dist/public)
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')