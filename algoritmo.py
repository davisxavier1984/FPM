import numpy as np

def estimar_fus(dados_2024):
    """
    Estimar valores do FUS para 2025 com base nos dados de 2024
    
    Args:
        dados_2024: Dados do FUS de 2024
        
    Returns:
        Dicionário com as estimativas do FUS para 2025
    """
    # Fator de correção para 2025 (estimativa de crescimento)
    fator_crescimento = 1.08  # 8% de crescimento estimado

    # Fatores de correção por decêndio para abril (exemplo)
    fatores_decendio_abril = {
        '10': 1.08, # Fator para o decêndio do dia 10 de abril
        '20': 0.98, # Fator para o decêndio do dia 20 de abril
        '30': 0.95  # Fator para o decêndio do dia 30 de abril
    }
    
    # Dicionário para armazenar as previsões
    previsoes = {}
    
    # Meses para previsão
    meses = ['janeiro', 'fevereiro', 'marco', 'abril']
    abreviacoes = {'janeiro': 'jan', 'fevereiro': 'fev', 'marco': 'mar', 'abril': 'abr'}
    
    # Para cada decêndio em 2024
    for item in dados_2024["2024"]:
        decendio = item['data']
        
        # Para cada mês que queremos prever
        for mes in meses:
            # Verificar se há valor para esse mês em 2024
            if mes in item and item[mes] > 0:
                # Calcular a previsão com o fator de crescimento
                valor_base = item[mes]
                if mes == 'abril' and decendio in fatores_decendio_abril:
                    valor_previsto = valor_base * fatores_decendio_abril[decendio]
                else:
                    valor_previsto = valor_base * fator_crescimento
                
                # Armazenar no formato "decêndio/mês_abrev/ano"
                chave = f"{decendio}/{abreviacoes[mes]}/2025"
                previsoes[chave] = valor_previsto
    
    return previsoes

def calcular_totais_mensais(df):
    """
    Calcular totais mensais do FUS
    
    Args:
        df: DataFrame com dados do FUS
        
    Returns:
        DataFrame com totais mensais
    """
    # Agrupar por mês e ano, somando os valores
    totais = df.groupby(['Ano', 'Mês', 'Tipo']).agg({'Valor': 'sum'}).reset_index()
    return totais

def estimar_fpm(valor_base, mes_destino):
    """
    Estima o valor do FPM com base em um valor de referência
    
    Args:
        valor_base: Valor base para cálculo
        mes_destino: Mês para o qual queremos calcular a estimativa
        
    Returns:
        Dicionário com estimativas para os três decêndios do mês
    """
    # Fatores de correção por mês (baseados em dados históricos)
    fatores = {
        'fevereiro': {'10': 0.92, '20': 0.95, '30': 0.88},
        'marco': {'10': 0.97, '20': 1.03, '30': 1.05},
        'abril': {'10': 1.08, '20': 0.98, '30': 0.95},
    }
    
    # Verificar se temos fatores para o mês solicitado
    if mes_destino not in fatores:
        return None
    
    # Calcular estimativas para cada decêndio
    estimativas = {}
    mes_abrev = mes_destino[:3]
    
    for decendio, fator in fatores[mes_destino].items():
        valor_estimado = valor_base * fator
        estimativas[f"{decendio}/{mes_abrev}/2025"] = valor_estimado
    
    return estimativas
