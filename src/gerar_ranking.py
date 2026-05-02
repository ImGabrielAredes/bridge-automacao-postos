import pandas as pd

def criar_ranking():
    print("Iniciando Módulo 4: Geração de Rankings de Faturamento...")

    # Carregamento da base de dados consolidada e normalizada gerada no pipeline de ETL (Módulo 2)
    caminho_dados = '../data/output/vendas_consolidadas_marco2025.csv'

    try:
        df = pd.read_csv(caminho_dados)
    except FileNotFoundError:
        # Validação de dependência: impede o processamento se a etapa anterior do pipeline não tiver sido executada
        print("Erro: Arquivo consolidado não encontrado. Rode o Módulo 2 primeiro!")
        return

    # Agregação de faturamento bruto por filial para identificar as unidades com melhor performance financeira
    ranking_filiais = df.groupby('filial_nome')['valor_total_brl'].sum().reset_index()

    # Ordenação decrescente para estabelecer o ranking definitivo de faturamento
    ranking_filiais = ranking_filiais.sort_values(by='valor_total_brl', ascending=False)

    # Agregação de volumetria de vendas (litros) por produto canônico, focando na vazão física do estoque
    ranking_produtos = df.groupby('produto_canonico')['volume_estimado_litros'].sum().reset_index()

    # Ordenação decrescente para o ranking de volume
    ranking_produtos = ranking_produtos.sort_values(by='volume_estimado_litros', ascending=False)

    # Persistência dos relatórios analíticos em formato tabular (CSV) para consumo das áreas de negócio
    caminho_rank_filiais = '../data/output/ranking_filiais.csv'
    caminho_rank_produtos = '../data/output/ranking_produtos.csv'

    ranking_filiais.to_csv(caminho_rank_filiais, index=False)
    ranking_produtos.to_csv(caminho_rank_produtos, index=False)

    # Exibição dos indicadores via console (CLI) para validação rápida da orquestração
    print("\n RANKING DE FATURAMENTO POR FILIAL")
    print(ranking_filiais.to_string(index=False))

    print("\n RANKING DE VOLUME POR PRODUTO (Litros)")
    print(ranking_produtos.to_string(index=False))

    print("\nArquivos de ranking salvos com sucesso na pasta output!")

if __name__ == "__main__":
    criar_ranking()