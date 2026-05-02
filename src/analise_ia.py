import os
import glob
import json
import pandas as pd
from google import genai

# Instancia o cliente da API do Google Gemini para processamento de linguagem natural (NLP)
CHAVE_API = "API_KEY"
client = genai.Client(api_key=CHAVE_API)


def analisar_emails_gerentes():
    print("Iniciando Módulo 3: Análise de Sentimento com Inteligência Artificial...")

    # Busca dinâmica de todos os e-mails (relatos narrativos) na pasta de input
    caminho_emails = '../data/input/emails/*.txt'
    arquivos_txt = glob.glob(caminho_emails)

    lista_resultados = []

    for arquivo in arquivos_txt:
        nome_arquivo = os.path.basename(arquivo)

        # Extração do identificador da filial a partir do nome do arquivo para garantir a rastreabilidade
        filial_id = nome_arquivo.split('_')[1]

        # Formatação dos identificadores para respeitar o padrão de saída exigido pela sede
        filial_nome = f"Posto {filial_id}"

        # Leitura do relato do gerente (usando UTF-8 para evitar problemas de codificação com caracteres em português)
        with open(arquivo, 'r', encoding='utf-8') as f:
            texto_email = f.read()

        print(f"Analisando {nome_arquivo}...")

        # Prompt Engineering: Instruções estritas (Zero-Shot) para forçar o LLM a retornar um JSON estruturado,
        # evitando respostas conversacionais que quebrariam o pipeline de dados.
        prompt = f"""
        Você é um analista de dados. Leia o e-mail enviado por um gerente de posto de combustível.

        Extraia as seguintes infomações e retorne a resposta EXATAMENTE neste formato JSON estrito, sem nenhuma formatação Markdown ou texto extra:
        {{
            "resumo": "Síntese do relato em 2 a 3 frases.",
            "destaques": ["ponto 1", "ponto 2", "ponto 3"],
            "alertas": "Problemas ou ocorrências que merecem atenção da sede (pode ser vazio).",
            "sentimento_geral": "Classifique APENAS como: positivo, neutro ou negativo"
        }}

        Email:
        {texto_email}
        """

        try:
            # Chamada à API utilizando o modelo flash, escolhido por ser o mais otimizado e veloz para tarefas de texto
            resposta = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )

            texto_resposta = resposta.text.strip()

            # Sanitização do Payload: Remoção preventiva de blocos de código Markdown (```json)
            # que as LLMs costumam adicionar por padrão, garantindo a conversão segura.
            if texto_resposta.startswith("```json"):
                texto_resposta = texto_resposta[7:-3]
            elif texto_resposta.startswith("```"):
                texto_resposta = texto_resposta[3:-3]

            # Desserialização do texto JSON para um Dicionário Python
            dados_ia = json.loads(texto_resposta.strip())

            # Injeção dos metadados da filial no resultado da IA para viabilizar a consolidação
            dados_ia['filial_id'] = filial_id
            dados_ia['filial_nome'] = filial_nome

            lista_resultados.append(dados_ia)

        except Exception as e:
            # Tratamento de exceção para garantir que uma falha na API não derrube a automação inteira
            print(f"Erro ao processar o arquivo {nome_arquivo} via IA. Detalhes: {e}")

    # Consolidação: Conversão da lista de dicionários enriquecidos em um DataFrame tabular
    if lista_resultados:
        df_ia = pd.DataFrame(lista_resultados)

        # Aplicação da máscara de colunas para garantir estritamente o esquema exigido na especificação (Item 3.4)
        colunas = ['filial_id', 'filial_nome', 'resumo', 'alertas', 'sentimento_geral']
        df_ia = df_ia[colunas]

        # Persistência dos dados analíticos estruturados na camada de saída
        caminho_saida = '../data/output/resumo_gerentes_marco2025.csv'
        df_ia.to_csv(caminho_saida, index=False)

        print("\n=== Prévia de Análise da IA ===")
        print(df_ia.head())
        print(f"\nArquivo de inteligência salvo em: {caminho_saida}")
    else:
        print("Nenhum dado foi extraído com sucesso.")


if __name__ == "__main__":
    analisar_emails_gerentes()