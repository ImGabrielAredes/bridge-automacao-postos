import requests
from bs4 import BeautifulSoup


def coletar_precos_referencia():
    print("Iniciando a coleta de preços via RPA...")
    url = "https://bridgenoc.github.io/case-postos/precos_marco2025.html"

    # Tenta acessar o site da Bridge, onde está a tabela de preços médios.
    try:
        pagina = requests.get(url, timeout=10) # Espera 10 segundos para tentar acessar
    # Caso não consiga acessar, dispara uma exceção informando o erro.
    except requests.exceptions.RequestException as e:
        print(f"Erro critíco! Não foi possível conectar ao site da Bridge. Detalhes: {e}")
        return None

    if pagina.status_code == 200:
        print("Página acessada com sucesso! Extraindo e tratando os dados...")

        #  Faz o parsing do HTML da página, criando uma estrutura navegável para extrair dados.
        dados_pagina = BeautifulSoup(pagina.text, 'html.parser')

        # Encontra a tabela no site (table) e retorna o elemento.
        tabela = dados_pagina.find('table')

        if tabela is None:
            print("Erro estrutural! A tabela de preços não foi encontrada no HTML")
            return None

        # Encontra todos as linhas da tabela e retorna uma lista com esses elementos.
        linhas = tabela.find_all('tr')

        # Criamos um dicionário com os preços, até então vazio, para buscarmos na tabela.
        dicionario_precos = {}

        # Ignoramos o cabeçalho começando da linha 1, devido a primeira linha ser as descrições da tabela.
        for linha in linhas[1:]:
            colunas = linha.find_all('td') # Procura todos as células que existem por linha.

            # Validação de segurança: garante que a linha HTML extraída não está corrompida e possui os dados mínimos esperados.
            if len(colunas) >= 2:
                try:
                    # Extrai as informações brutas limpando espaços em branco (strip) das pontas.
                    produto = colunas[0].text.strip()
                    preco_texto = colunas[1].text.strip()

                # Tratamento de dados: Transformando String "6,15" em Float 6.15 para garantir o cálculo do volume no módulo 2.
                    preco_float = float(preco_texto.replace(',', '.'))

                # Vinculando ao dicionário o produto e preço captados.
                    dicionario_precos[produto] = preco_float
                except ValueError:
                 # Se vier uma letra no lugar do preço, ele ignora aquela linha e prossegue com a execução.
                    print(f"Aviso: Preço inválido ignorado para o produto: {produto}")

        print("Tabela de Preços Mapeada:")
        print(dicionario_precos)
        return dicionario_precos

    else:
        print(f"Erro ao acessar a página. Código: {pagina.status_code}")
        return None


if __name__ == "__main__":
    coletar_precos_referencia()