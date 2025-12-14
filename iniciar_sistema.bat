@echo off
TITLE Sistema de Aluguel - NAO FECHE ESTA JANELA
echo Iniciando o sistema...

:: 1. Entra na pasta do projeto
cd /d "C:\Users\monil\Documents\Codando\Alugueis\rental_manager"

:: 2. Abre o navegador (Chrome/Edge) no endereço certo
:: O comando 'start' abre o navegador padrão
start http://127.0.0.1:5000

:: 3. Ativa o ambiente virtual e inicia o Flask
call venv\Scripts\activate
python app.py

:: Se o sistema fechar por erro, pausa para ler o que houve
pause