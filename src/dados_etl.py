import pandas as pd
import os
import glob

# Passamos o dicionario_precos como parâmetro para que o Pandas combine o produto normalizado com o preço extraído do RPA e realize a estimativa de volume.
def processar_vendas(dicionario_precos):
    print("Iniciando Módulo 2: Processamento e Normalização de Dados...")

    # Mapeamento de De/Para: garante a conformidade e padronização dos nomes variantes para os 3 produtos canônicos da rede.
    mapa_produtos = {
        'Gasolina C': 'Gasolina Comum',
        'Gasolina Comum': 'Gasolina Comum',
        'GC': 'Gasolina Comum',
        'Gasolina Comun': 'Gasolina Comum',
        'Gas. Comum': 'Gasolina Comum',

        'Etanol Hid.': 'Etanol',
        'Etanol Comum': 'Etanol',
        'Etanol': 'Etanol',
        'Etanol Hidratado': 'Etanol',

        'Diesel S-10': 'Diesel S10',
        'DSL S10': 'Diesel S10',
        'Diesel S10 Aditivado': 'Diesel S10',
        'Diesel S10': 'Diesel S10'
    }

    # Busca dinâmica de todos os lotes de vendas na pasta de input
    caminho_arquivos = '../data/input/vendas_*.csv'
    arquivos_csv = glob.glob(caminho_arquivos)

    # Lista para armazenar os DataFrames em memória antes da consolidação unificada
    lista_dataframes = []

    for arquivo in arquivos_csv:
        nome_arquivo = os.path.basename(arquivo)

        # Extração dinâmica do ID da filial a partir do padrão de nomenclatura do arquivo (ex: vendas_F001_marco2025.csv)
        filial_id = nome_arquivo.split('_')[1]

        df = pd.read_csv(arquivo)

        # Adição das colunas de identificação obrigatórias exigidas pela sede
        df['filial_id'] = filial_id
        df['filial_nome'] = f"Posto {filial_id}"

        # Aplicação da regra de normalização de produtos de forma vetorizada
        df['produto_canonico'] = df['produto'].map(mapa_produtos)

        # Cruzamento dos preços de referência (RPA) com os produtos normalizados para viabilizar o cálculo da volumetria
        df['preco_unitario'] = df['produto_canonico'].map(dicionario_precos)
        df['volume_estimado_litros'] = (df['valor_total_brl'] / df['preco_unitario']).round(2)

        lista_dataframes.append(df)

    # Consolidação: empilha os DataFrames de todas as filiais em uma única estrutura tabular
    df_consolidado = pd.concat(lista_dataframes, ignore_index=True)

    # Filtro de colunas para garantir que a saída contenha estritamente o formato solicitado no case
    colunas_finais = ['data', 'filial_id', 'filial_nome', 'produto_canonico',
                      'valor_total_brl', 'volume_estimado_litros']

    df_consolidado = df_consolidado[colunas_finais]

    print("\nVisualização rápida da tabela final consolidada (preview):")
    print(df_consolidado.head())

    caminho_saida = '../data/output/vendas_consolidadas_marco2025.csv'
    df_consolidado.to_csv(caminho_saida, index=False)

    print(f"\nArquivo salvo com sucesso em: {caminho_saida}")
    return df_consolidado