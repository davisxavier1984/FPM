import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from algoritmo import estimar_fus, calcular_totais_mensais
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="FUS Ribeirão/PE",
    page_icon="💰",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para melhorar a apresentação visual
st.markdown("""
<style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 8px;
        margin-top: 25px;
    }
    .month-header {
        font-size: 20px;
        font-weight: bold;
        color: #3B82F6;
        background-color: #EFF6FF;
        padding: 5px 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .card {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        color: #6B7280;
        padding: 20px;
        border-top: 1px solid #E5E7EB;
    }
    .info-card {
        background-color: #F9FAFB;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Função para verificar se é dispositivo móvel
def is_mobile():
    """Verifica se o dispositivo é provavelmente um celular com base na largura"""
    return st.session_state.get('is_mobile', False)

# Define o estado inicial da sessão para detecção de mobile
if 'is_mobile' not in st.session_state:
    st.session_state.is_mobile = False

# Funções auxiliares
@st.cache_data
def carregar_dados():
    """Carrega os dados de todos os arquivos JSON"""
    with open('fus_2024.json', 'r') as f:
        fus_2024 = json.load(f)
    with open('fus_2025.json', 'r') as f:
        fus_2025 = json.load(f)
    with open('fns_2024.json', 'r') as f:
        fns_2024 = json.load(f)
    with open('fns_2025.json', 'r') as f:
        fns_2025 = json.load(f)
    return fus_2024, fus_2025, fns_2024, fns_2025

def formatar_valor_br(valor):
    """Formata valor para o padrão brasileiro"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def converter_fus_para_dataframe(dados_2024, dados_2025, previsoes_2025=None):
    """Converte os dados FUS para um DataFrame pandas"""
    resultados = []
    meses_nomes = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 
                   'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    
    # Adicionar dados reais de 2025
    for item in dados_2025["2025"]:
        decendio = item['data']
        for mes in meses_nomes:
            if mes in item:
                valor = item[mes]
                resultados.append({
                    'Decêndio': decendio,
                    'Mês': mes.capitalize(),
                    'Valor': valor,
                    'Ano': 2025,
                    'Tipo': 'Realizado'
                })
    
    # Adicionar previsões de 2025 se disponíveis
    if previsoes_2025:
        for chave, valor in previsoes_2025.items():
            partes = chave.split('/')
            decendio = partes[0]
            mes_abrev = partes[1]
            
            # Converter abreviação para nome completo do mês
            mes_mapeamento = {'jan': 'Janeiro', 'fev': 'Fevereiro', 'mar': 'Marco', 'abr': 'Abril'}
            mes = mes_mapeamento.get(mes_abrev, mes_abrev.capitalize())
            
            # Adicionar sempre a previsão, mesmo se já existir um valor realizado
            resultados.append({
                'Decêndio': decendio,
                'Mês': mes,
                'Valor': valor,
                'Ano': 2025,
                'Tipo': 'Previsto'
            })
    
    # Adicionar também os dados de 2024 para referência
    for item in dados_2024["2024"]:
        decendio = item['data']
        for mes in meses_nomes:
            if mes in item:
                valor = item[mes]
                if valor > 0:  # Só incluir valores positivos
                    resultados.append({
                        'Decêndio': decendio,
                        'Mês': mes.capitalize(),
                        'Valor': valor,
                        'Ano': 2024,
                        'Tipo': 'Realizado'
                    })
    
    return pd.DataFrame(resultados)

# Cabeçalho principal com estilo aprimorado
st.markdown('<div class="title">💰 FUS e FNS - Ribeirão/PE</div>', unsafe_allow_html=True)

# Modo mobile com tooltip explicativo
st.checkbox("📱 Modo Mobile", value=st.session_state.is_mobile, key="mobile_mode", help="Ative para melhor visualização em dispositivos móveis")
st.session_state.is_mobile = st.session_state.mobile_mode

# Introdução em forma de card
st.markdown('<div class="card">Sistema de Análise do FUS (Fundo Único de Saúde) e FNS (Piso de Atenção Primária) com valores realizados e previsão para 2025</div>', unsafe_allow_html=True)

# Carregar dados e calcular estimativas
try:
    # Carregar dados de 2024 e 2025
    fus_2024, fus_2025, fns_2024, fns_2025 = carregar_dados()
    
    # Calcular estimativas para 2025 usando o algoritmo
    previsoes_2025 = estimar_fus(fus_2024)
    
    # Converter para DataFrame combinado
    df_combined = converter_fus_para_dataframe(fus_2024, fus_2025, previsoes_2025)
    
    # Separar os dados para 2025
    df_2025 = df_combined[df_combined['Ano'] == 2025]
except Exception as e:
    st.error(f"Erro ao carregar ou calcular as previsões: {e}")
    st.stop()

# === EXIBIÇÃO DOS VALORES DO FUS DE JANEIRO A ABRIL DE 2025 ===
st.markdown('<div class="subtitle">📊 FUS 2025: Janeiro a Abril</div>', unsafe_allow_html=True)

# Meses para exibição
meses_exibicao = ['Janeiro', 'Fevereiro', 'Marco', 'Abril']
df_2025_filtrado = df_2025[df_2025['Mês'].isin(meses_exibicao)]

# Criar uma tabela para exibição detalhada por decêndios
st.markdown("### Detalhamento por Decêndios (Dia 10, 20 e 30)")

# Legenda de cores
legenda = """
<div style="display: flex; gap: 15px; margin-bottom: 15px; flex-wrap: wrap;">
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; background-color: #D1FAE5; margin-right: 5px;"></div>
        <span>Realizado</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; background-color: #FEF3C7; margin-right: 5px;"></div>
        <span>Previsto</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; background-color: #E0E7FF; margin-right: 5px;"></div>
        <span>Diferença</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; background-color: #DBEAFE; margin-right: 5px;"></div>
        <span>Total</span>
    </div>
</div>
"""
st.markdown(legenda, unsafe_allow_html=True)

for mes in meses_exibicao:
    st.markdown(f'<div class="month-header">📅 {mes} 2025</div>', unsafe_allow_html=True)
    
    # Filtrar dados para o mês atual
    df_mes_2025 = df_2025_filtrado[df_2025_filtrado['Mês'] == mes]
    
    # Criar dataframe para exibição dos decêndios
    dados_decendios = []
    
    # Obter valores para cada decêndio
    for decendio in ['10', '20', '30']:
        # Verificar valores realizados
        df_realizado = df_mes_2025[(df_mes_2025['Decêndio'] == decendio) & (df_mes_2025['Tipo'] == 'Realizado')]
        valor_realizado = df_realizado['Valor'].values[0] if len(df_realizado) > 0 else 0
        
        # Verificar valores previstos
        df_previsto = df_mes_2025[(df_mes_2025['Decêndio'] == decendio) & (df_mes_2025['Tipo'] == 'Previsto')]
        valor_previsto = df_previsto['Valor'].values[0] if len(df_previsto) > 0 else 0
        
        # Calculando a diferença (valor numérico para uso posterior)
        diferenca = valor_realizado - valor_previsto
        
        dados_decendios.append({
            'Decêndio': f"Dia {decendio}",
            'Valor Realizado': formatar_valor_br(valor_realizado),
            'Valor Previsto': formatar_valor_br(valor_previsto),
            'Diferença': formatar_valor_br(diferenca),
            '_diferenca_valor': diferenca  # Campo auxiliar para estilização
        })
    
    # Calcular os totais do mês
    total_realizado = df_mes_2025[df_mes_2025['Tipo'] == 'Realizado']['Valor'].sum()
    total_previsto = df_mes_2025[df_mes_2025['Tipo'] == 'Previsto']['Valor'].sum()
    
    # Calculando a diferença total (valor numérico para uso posterior)
    diferenca_total = total_realizado - total_previsto
    
    # Adicionar linha com o total do mês
    dados_decendios.append({
        'Decêndio': f"TOTAL {mes} 2025",
        'Valor Realizado': formatar_valor_br(total_realizado),
        'Valor Previsto': formatar_valor_br(total_previsto),
        'Diferença': formatar_valor_br(diferenca_total),
        '_diferenca_valor': diferenca_total  # Campo auxiliar para estilização
    })
    
    # Exibir tabela com os decêndios
    df_exibicao = pd.DataFrame(dados_decendios)
    
    # Formatar a tabela para destacar a linha de total e colorir colunas
    def highlight_cells(x):
        df_styled = pd.DataFrame('', index=x.index, columns=x.columns)
        df_styled.loc[:, 'Valor Realizado'] = 'background-color: #D1FAE5'
        df_styled.loc[:, 'Valor Previsto'] = 'background-color: #FEF3C7'
        df_styled.loc[:, 'Diferença'] = 'background-color: #E0E7FF'
        
        # Adicionar texto em vermelho para a coluna de diferença
        for i in range(len(x)):
            if '_diferenca_valor' in x.columns and x['_diferenca_valor'].iloc[i] < 0:
                df_styled.loc[i, 'Diferença'] = 'background-color: #E0E7FF; color: red'
        
        # Aplicar estilo à linha de total
        df_styled.iloc[-1] = 'background-color: #DBEAFE; font-weight: bold'
        
        # Manter o texto vermelho na linha de total se a diferença for negativa
        if '_diferenca_valor' in x.columns and x['_diferenca_valor'].iloc[-1] < 0:
            df_styled.iloc[-1, df_styled.columns.get_loc('Diferença')] = 'background-color: #DBEAFE; font-weight: bold; color: red'
        
        return df_styled
    
    # Remover a coluna auxiliar antes de exibir
    if '_diferenca_valor' in df_exibicao.columns:
        df_exibicao = df_exibicao.drop('_diferenca_valor', axis=1)
    
    # Aplicar o estilo e mostrar a tabela
    st.dataframe(df_exibicao.style.apply(highlight_cells, axis=None), use_container_width=True)

# Separador visual
st.markdown("<hr>", unsafe_allow_html=True)

# === EXIBIÇÃO DOS DADOS BRUTOS DO FNS ===
st.markdown('<div class="subtitle">📋 FNS: Dados Brutos</div>', unsafe_allow_html=True)

# Função para destacar a linha de total nas tabelas FNS
def highlight_total_row(df):
    def _highlight_total(s):
        styles = [''] * len(s)
        if 'Grupo' in df.columns and s.name == 'Grupo':
            styles = ['background-color: #DBEAFE; font-weight: bold' if v == 'Total' else '' for v in s]
        elif 'Grupo' in df.columns and 'Total' in df['Grupo'].values:
            total_idx = df[df['Grupo'] == 'Total'].index[0]
            styles = ['background-color: #DBEAFE; font-weight: bold' if i == total_idx else '' for i in range(len(s))]
        return styles

    return df.style.apply(_highlight_total)

# Exibir FNS 2025 com estilo melhorado
st.markdown('### 📅 FNS 2025')
df_fns_2025 = pd.DataFrame(fns_2025)

# Formatar valores numéricos
for col in df_fns_2025.columns:
    if col != 'Grupo':
        df_fns_2025[col] = df_fns_2025[col].apply(lambda x: formatar_valor_br(x) if x != 0 else "")

# Exibir tabela com linha de total destacada
st.dataframe(highlight_total_row(df_fns_2025), use_container_width=True)

# Exibir FNS 2024
st.markdown('### 📅 FNS 2024')
df_fns_2024 = pd.DataFrame(fns_2024)

# Formatar valores numéricos
for col in df_fns_2024.columns:
    if col != 'Grupo':
        df_fns_2024[col] = df_fns_2024[col].apply(lambda x: formatar_valor_br(x) if x != 0 else "")

# Exibir tabela com linha de total destacada
st.dataframe(highlight_total_row(df_fns_2024), use_container_width=True)

# Calcular valor de referência do FNS
total_fns_setembro_2024 = next(item['09/12 em 2024'] + (item['9 em 2024'] if '9 em 2024' in item else 0) 
                              for item in fns_2024 if item['Grupo'] == 'Total')

# Explicação da metodologia com estilo de card
st.markdown('<div class="subtitle">📝 Metodologia</div>', unsafe_allow_html=True)

# Informações sobre o FUS
st.markdown("""
<div class="info-card">
    <p><strong>🔹 Valores FUS realizados:</strong> Dados reais do FUS para 2025 já registrados</p>
    <p><strong>🔹 Valores FUS previstos:</strong> Estimativa baseada no seguinte método:</p>
    <ul>
        <li>Base de cálculo: Valores do FUS de 2024 como referência</li>
        <li>Variação percentual anual aplicada:
            <ul>
                <li>Fevereiro 2025: +3,7% em relação a fevereiro 2024</li>
                <li>Março 2025: +6,5% em relação a março 2024</li>
                <li>Abril 2025: +9,7% em relação a abril 2024</li>
            </ul>
        </li>
        <li>Distribuição por decêndio: Usando fatores de multiplicação de fevereiro 2025</li>
    </ul>
    <p><strong>🔹 Valores FNS:</strong> Dados reais para janeiro e fevereiro. Valores de março e abril são estimados com base no total de setembro/2024 (R$ {formatar_valor_br(total_fns_setembro_2024)})</p>
</div>
""", unsafe_allow_html=True)

# Nova seção com observações sobre padrões de liberação
st.markdown("""
<div class="info-card">
    <h4 style="color: #1E3A8A; margin-top: 0;">🔹 Padrões de Data Específicos para Liberações:</h4>
    <ol>
        <li><strong>Início do Mês (Dias 1-7):</strong> Concentração de liberações para ações como "ATENÇÃO À SAÚDE DA POPULAÇÃO PARA PROCEDIMENTOS NO MAC", "SAMU 192", "TRANSFERÊNCIA AOS ENTES FEDERATIVOS PARA O PAGAMENTO DOS VENCIMENTOS DOS AGENTES DE COMBATE ÀS ENDEMIAS" e "INCENTIVO FINANCEIRO AOS ESTADOS, DISTRITO FEDERAL E MUNICÍPIOS PARA A VIGILÂNCIA EM SAÚDE - DESPESAS DIVERSAS".</li>
        <li><strong>Segunda Semana do Mês (Dias 8-14):</strong> Concentração de liberações para "AGENTES COMUNITÁRIOS DE SAÚDE", "INCENTIVO FINANCEIRO PARA ATENÇÃO À SAÚDE BUCAL", "INCENTIVO FINANCEIRO DA APS - EQUIPES DE SAÚDE DA FAMÍLIA/ESF E EQUIPES DE ATENÇÃO PRIMÁRIA/EAP" e "INCENTIVO FINANCEIRO DA APS - MANUTENÇÃO DE PAGAMENTO DE VALOR NOMINAL COM BASE EM EXERCÍCIO ANTERIOR".</li>
        <li><strong>Final do Mês (Dias 25-31):</strong> Liberação da "ASSISTÊNCIA FINANCEIRA COMPLEMENTAR AOS ESTADOS, DF E MUNICÍPIOS P/ O PAG DO PISO SALARIAL DOS PROFISSIONAIS DA ENFERMAGEM".</li>
    </ol>
</div>
""", unsafe_allow_html=True)


# === TOTAIS MENSAIS ESTIMADOS (FUS + FNS) ===
st.markdown('<div class="subtitle">💵 Totais Mensais Estimados 2025</div>', unsafe_allow_html=True)

# Calcular totais previstos e realizados
total_row_fns = next(item for item in fns_2025 if item['Grupo'] == 'Total')

# CSS para cards com efeito de destaque
card_css = """
<style>
.valor-card {
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}
.valor-card:hover {
    transform: translateY(-2px);
}
.valor-label {
    font-size: 15px;
    margin-bottom: 5px;
    font-weight: 500;
}
.valor-total {
    font-size: 24px;
    font-weight: bold;
}
.estimativa-badge {
    font-size: 12px;
    padding: 3px 8px;
    border-radius: 12px;
    display: inline-block;
    margin-top: 5px;
}
</style>
"""
st.markdown(card_css, unsafe_allow_html=True)

for mes in meses_exibicao:
    st.markdown(f'<div class="month-header">📅 {mes} 2025</div>', unsafe_allow_html=True)
    
    # Calcular total FUS do mês
    df_mes = df_2025_filtrado[df_2025_filtrado['Mês'] == mes]
    total_fus_mes = df_mes[df_mes['Tipo'] == 'Realizado']['Valor'].sum()
    total_fus_previsto = df_mes[df_mes['Tipo'] == 'Previsto']['Valor'].sum()
    
    # Obter total FNS do mês
    mes_col_map = {
        'Janeiro': '01/12 em 2025',
        'Fevereiro': '02/12 em 2025',
        'Marco': '03/12 em 2025',
        'Janeiro': 'Jan/2025',
        'Fevereiro': 'Fev/2025',
        'Marco': 'Mar/2025',
        'Abril': 'Abr/2025' # Mapeamento para Abril, mesmo que não exista ainda no JSON
    }
    
    # Obter a chave correta para o mês atual no JSON FNS
    chave_fns_mes = mes_col_map.get(mes)
    
    # Buscar o valor FNS realizado do JSON
    # Se a chave não existir (ex: Abril), o valor será 0
    total_fns_mes_realizado = total_row_fns.get(chave_fns_mes, 0.0) 
    
    # Determinar se o valor FNS exibido no card "Recebido" é baseado em dados reais do JSON
    # Será False se a chave não existir no JSON (total_fns_mes_realizado será 0)
    eh_fns_real = chave_fns_mes in total_row_fns

    # Manter a estimativa FNS baseada em Set/2024 para o card "Estimado"
    total_fns_estimado = total_fns_setembro_2024
    
    # Calcular totais do mês
    total_recebido = total_fus_mes # FUS Realizado
    total_estimado = total_fus_previsto # FUS Previsto
    
    # Total geral recebido (FUS Realizado + FNS Realizado do JSON)
    total_geral_recebido = total_recebido + total_fns_mes_realizado
    # Total geral estimado (FUS Previsto + FNS Estimado de Set/2024)
    total_geral_estimado = total_estimado + total_fns_estimado
    
    # Exibir totais do mês
    col1, col2 = st.columns(2)
    
    # Coluna de Valores Recebidos
    with col1:
        st.markdown(f"""
        <div class="valor-card" style="background: linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%);">
            <div class="valor-label" style="color: #166534;">Valores Recebidos</div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <div>
                    <div style="font-size: 14px; color: #166534;">FUS</div>
                    <div style="font-size: 18px; color: #166534; font-weight: bold;">{formatar_valor_br(total_recebido)}</div>
                </div>
                <div>
                    <div style="font-size: 14px; color: #166534;">FNS {'' if eh_fns_real else '(N/D)'}</div>
                    <div style="font-size: 18px; color: #166534; font-weight: bold;">{formatar_valor_br(total_fns_mes_realizado) if eh_fns_real else '-'}</div>
                </div>
            </div>
            <div class="valor-total" style="color: #166534; border-top: 1px solid rgba(22, 101, 52, 0.2); padding-top: 10px;">
                {formatar_valor_br(total_geral_recebido)}
            </div>
            <div class="estimativa-badge" style="background-color: #86EFAC; color: #166534;">
                Total Recebido
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Coluna de Valores Estimados
    with col2:
        st.markdown(f"""
        <div class="valor-card" style="background: linear-gradient(135deg, #FEF9C3 0%, #FDE047 100%);">
            <div class="valor-label" style="color: #854D0E;">Valores Estimados</div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <div>
                    <div style="font-size: 14px; color: #854D0E;">FUS</div>
                    <div style="font-size: 18px; color: #854D0E; font-weight: bold;">{formatar_valor_br(total_estimado)}</div>
                </div>
                <div>
                    <div style="font-size: 14px; color: #854D0E;">FNS (Estimado)</div>
                    <div style="font-size: 18px; color: #854D0E; font-weight: bold;">{formatar_valor_br(total_fns_estimado)}</div>
                </div>
            </div>
            <div class="valor-total" style="color: #854D0E; border-top: 1px solid rgba(133, 77, 14, 0.2); padding-top: 10px;">
                {formatar_valor_br(total_geral_estimado)}
            </div>
            <div class="estimativa-badge" style="background-color: #FEF08A; color: #854D0E;">
                Total Estimado
            </div>
        </div>
        """, unsafe_allow_html=True)

# Rodapé com design melhorado
st.markdown(f'<div class="footer">SMS Ribeirão-PE | {datetime.now().year}</div>', unsafe_allow_html=True)
