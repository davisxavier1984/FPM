# Dashboard Financeiro da Saúde - Ribeirão/PE

Este aplicativo Streamlit apresenta uma análise completa dos recursos financeiros da saúde do município de Ribeirão - PE, incluindo dados do Fundo Único de Saúde (FUS), do Fundo de Participação dos Municípios (FPM) e dos repasses do Fundo Nacional de Saúde (PAP).

## Recursos do Dashboard

- **Visão Geral**: Resumo gráfico dos recursos financeiros
- **FUS/FPM**: Análise detalhada dos valores por mês e decêndio
- **PAP**: Análise dos repasses Fundo a Fundo por grupo e período
- **Projeções**: Estimativas de valores futuros baseadas em algoritmo de projeção
- **Responsivo**: Interface adaptada para visualização em dispositivos móveis

## Como executar

1. Instale as dependências:
```
pip install -r requirements.txt
```

2. Execute o aplicativo:
```
streamlit run app.py
```

## Dispositivos móveis

O dashboard foi otimizado para funcionar em smartphones e tablets, com:
- Layout adaptativo que muda com base no tamanho da tela
- Gráficos redimensionados para melhor visualização em telas pequenas
- Opção "Modo Mobile" para forçar a visualização móvel em qualquer dispositivo

## Estrutura de arquivos

- `app.py`: Aplicativo principal Streamlit
- `algoritmo.py`: Funções para cálculo de projeções
- `fus_2024.json`, `fus_2025.json`: Dados do Fundo Único de Saúde
- `pap_2024.json`, `pap_2025.json`: Dados dos repasses PAP/FNS

## Notas sobre as projeções

As projeções são baseadas em modelos estimativos e fatores de multiplicação históricos. 
Os valores apresentados são apenas para referência e planejamento, e podem não refletir os valores reais futuros.
