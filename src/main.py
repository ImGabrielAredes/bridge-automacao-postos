import pandas as pd
from rpa_scraper import coletar_precos_referencia
from dados_etl import processar_vendas
from analise_ia import analisar_emails_gerentes
from gerar_ranking import criar_ranking

# --- CONFIGURAÇÃO DO AMBIENTE CLI ---
# Ajustes de display do Pandas para garantir a renderização integral dos relatórios e resumos textuais da IA no terminal
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 80)
# ---------------------------------------

def executar_pipeline_completo():
    print("="*60)
    print("🚀 INICIANDO AUTOMAÇÃO COMPLETA - CASE BRIDGE 🚀")
    print("="*60)

    # FASE 1: Extração (RPA) - Coleta os preços de referência dinâmicos na web para injeção de dependência no ETL
    precos_reais = coletar_precos_referencia()

    if precos_reais is None:
        # Fail-fast: Interrompe a orquestração imediatamente se a fonte de dados externa estiver indisponível
        print("Erro Crítico: Não foi possível obter os preços de referência.")
        print("Encerrando automação para evitar processamento de dados inconsistentes.")
        return

    print("\n" + "="*60)
    # FASE 2: Processamento (ETL) - Executa a normalização dos CSVs cruzando os dados locais com os preços capturados via RPA
    processar_vendas(precos_reais)

    print("\n" + "="*60)
    # FASE 3: Agregação Analítica - Consome a base unificada para gerar os rankings de performance (Faturamento e Volumetria)
    criar_ranking()

    print("\n" + "="*60)
    # FASE 4: Enriquecimento com IA - Processamento de Linguagem Natural (NLP) nos relatos textuais para extração estruturada (JSON)
    analisar_emails_gerentes()

    print("\n" + "="*60)
    print("✨ PIPELINE CONCLUÍDO! TODOS OS ENTREGÁVEIS ESTÃO NA PASTA OUTPUT ✨")
    print("=" * 60)


if __name__ == "__main__":
    executar_pipeline_completo()