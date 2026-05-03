# ⛽ Automação e Pipeline de Dados: Rede de Postos Bridge & Co.

Este repositório contém a resolução do case técnico para a estruturação de um pipeline de dados automatizado. A solução integra processos de Web Scraping (RPA), consolidação e tratamento de dados (ETL), análise de performance financeira e extração de sentimentos estruturados utilizando Processamento de Linguagem Natural (NLP/LLM).

## 📑 Sumário
- [1. Como Executar o Projeto (Instruções de Setup)](#️-1-como-executar-o-projeto-instruções-de-setup)
- [2. Visão Geral e Decisões de Arquitetura](#-2-visão-geral-e-decisões-de-arquitetura)
- [3. Limitações da Solução Atual](#-3-limitações-da-solução-atual)
- [4. Próximos Passos e Evolução](#-4-próximos-passos-e-evolução)

## ⚙️ 1. Como Executar o Projeto (Instruções de Setup)

Este projeto foi desenvolvido utilizando Python puro, garantindo fácil portabilidade e execução.

**Pré-requisitos:** 
* Python 3.10 ou superior.
* Gerenciador de pacotes `pip`.

**Passo a passo:**

1. **Clone o repositório para a sua máquina local:**
   ```bash
   git clone [https://github.com/ImGabrielAredes/bridge-automacao-postos.git](https://github.com/ImGabrielAredes/bridge-automacao-postos.git)
   cd bridge-automacao-postos
   
2. **Instale as dependências necessárias do projeto:**
    ```bash
   pip install pandas beautifulsoup4 requests google-genai

3. **Configuração de Credenciais (API Gemini):**
    * Gere uma chave de API gratuita no [Google AI Studio](https://aistudio.google.com/).
    * Abra o arquivo `src/analise_ia.py` e substitua a string `"API_KEY"` na variável `CHAVE_API` pela sua credencial real.

4. **Inicie a Orquestração:**
    Navegue até a pasta do código-fonte e execute o orquestrador principal:
    ```bash
    cd src
    python main.py
    ```

> **Nota:** Os arquivos processados (`vendas_consolidadas_marco2025.csv`, `resumo_gerentes_marco2025.csv` e relatórios de ranking) serão gerados automaticamente na pasta `data/output/`.

## 🧠 2. Visão Geral e Decisões de Arquitetura

O foco principal do desenvolvimento foi trabalhar em um **pipeline automatizado** que roda do início ao fim, sem a necessidade de intervenção manual. O ponto de entrada (`main.py`) garante que todo o pipeline seja executado, e todas as etapas do processo sejam concluídas automaticamente, conectando os módulos de forma independente através da injeção de dados de um estágio para o outro.

A solução foi organizada em 4 módulos isolados para garantir manutenibilidade e escalabilidade:

1. **Módulo RPA (`rpa_scraper.py`):** Utilizei a biblioteca `BeautifulSoup` em conjunto com `requests` (em vez de frameworks pesados como o Selenium). Como a página que continha os preços médios era estática, o parse direto do HTML nativo garante uma execução rápida e reduz consideravelmente o consumo de memória. Além disso, é realizada a conversão imediata dos preços para o formato numérico (float).
2. **Módulo ETL (`dados_etl.py`):** O tratamento de dados inconsistentes (nomes de produtos variados) foi resolvido através de um **Dicionário de Mapeamento (De/Para)** em conjunto com a função `.map()` do Pandas. Essa decisão evita laços de repetição (`for` loops) iterando linha a linha, deixando o processamento mais eficiente.
3. **Módulo de Agregação (`gerar_ranking.py`):** Utilizou-se agrupamento de dados através do `.groupby()` para separar a análise de desempenho das filiais em dois eixos de negócio: Faturamento Bruto (Financeiro) e Volume de Vendas (Estoque físico), gerando rankings ordenados de forma decrescente.
4. **Módulo de IA (`analise_ia.py`):** Para o processamento dos relatos não estruturados dos gerentes, utilizou-se a API do Google Gemini (modelo `gemini-2.5-flash` pela sua velocidade de inferência em texto). A principal decisão técnica aqui foi o uso de **Prompt Engineering estrito (Zero-Shot)** para forçar o retorno do LLM em formato JSON puro, aliado a uma garantia via código para remover possíveis blocos Markdown, viabilizando a conversão segura do texto para um DataFrame Pandas.

## 🚧 3. Limitações da Solução Atual

Embora o pipeline atenda perfeitamente às necessidades das 5 filiais, ao analisar a solução com mais profundidade, surgem alguns pontos de atenção para cenários de alta escalabilidade:

* **Gerenciamento de Memória (ETL):** Atualmente, o Pandas consolida todos os CSVs em memória RAM antes do processamento. Em um cenário real com centenas de filiais ou anos de histórico, seria necessário implementar processamento em lotes ou migrar o processamento para PySpark.
* **Resiliência do RPA:** O scraper possui um `timeout` de segurança, mas ainda não possui um mecanismo automático de repetição (ex: biblioteca `Tenacity` para Retry/Backoff) caso o servidor alvo apresente instabilidade temporária.
* **Gestão de Credenciais:** O código atual exige que a API Key seja informada no momento da execução em um formato de string. O ideal para um ambiente produtivo é isolar essa dependência.
* **Limites de Requisição (Rate Limit):** O envio sequencial de múltiplas requisições para a API de IA pode atingir limites de uso, especialmente em planos gratuitos. Para cenários maiores, seria interessante implementar controle de requisições, filas ou processamento assíncrono para evitar bloqueios.

## 🚀 4. Próximos Passos e Evolução
Para cenários futuros, pensando em um cenário de produção com maior volume de dados, algumas evoluções importantes seriam:

1. **Isolamento de Variáveis de Ambiente:** Implementação da biblioteca `python-dotenv` para o carregamento seguro das chaves de API a partir de um arquivo `.env` ignorado pelo repositório.
2. **Sistema de Logging Profissional:** Substituição das saídas via console (`print`) por logs estruturados usando a biblioteca nativa `logging`, gerando arquivos de registro com marcações de data/hora e níveis de severidade (INFO, WARNING, ERROR).
3. **Orquestração em Nuvem:** Em vez de depender da execução local, o script poderia ser conteinerizado (Docker) e agendado em uma ferramenta corporativa como o **Apache Airflow**, ou configurado em uma arquitetura Serverless (como AWS Lambda / Google Cloud Functions) acionada automaticamente sempre que novos arquivos CSV chegassem a um Bucket de entrada no S3.
4. **Visualização de Dados:** Conectar o arquivo final `vendas_consolidadas_marco2025.csv` e `resumo_gerentes_marco2025.csv` a uma ferramenta de B.I. (como Power BI ou Looker Studio) para geração de dashboards interativos.
