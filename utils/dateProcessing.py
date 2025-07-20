from datetime import datetime

monthsNames = [
    "Janeiro",  "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

def get_current_iso_datetime():
    """
    Retorna a data e hora atual no formato ISO 8601.
    Exemplo: '2025-07-05T19:22:35'
    """
    return datetime.now().isoformat()

def iso_para_formatado(data_iso):
    """
    Converte uma data ISO (string) para o formato DD/MM/YYYY HH:MM:SS (string).
    
    Args:
        data_iso (str): Data no formato ISO (ex: '2023-12-31T23:59:59' ou '2023-12-31')
    
    Returns:
        str: Data no formato DD/MM/YYYY HH:MM:SS (se tiver horário) ou DD/MM/YYYY (se não tiver)
    """
    try:
        # Tenta parsear com horário
        dt = datetime.fromisoformat(data_iso)
        if 'T' in data_iso:
            return dt.strftime('%d/%m/%Y %H:%M:%S')
        else:
            return dt.strftime('%d/%m/%Y')
    except ValueError:
        raise ValueError("Formato ISO inválido. Use como 'YYYY-MM-DDTHH:MM:SS' ou 'YYYY-MM-DD'")
    
def formatado_para_iso(data_formatada):
    """
    Converte uma data no formato DD/MM/YYYY (string) para o formato ISO (string).
    
    Args:
        data_formatada (str): Data no formato DD/MM/YYYY (ex: '31/12/2023')
    
    Returns:
        str: Data no formato ISO (YYYY-MM-DD)
    """
    try:
        dt = datetime.strptime(data_formatada, '%d/%m/%Y')
        return dt.date().isoformat()
    except ValueError:
        raise ValueError("Formato inválido. Use como 'DD/MM/YYYY'")