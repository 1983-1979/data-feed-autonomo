import os
import csv
import urllib.request
import json
import random
from datetime import datetime

# ==============================================================================
# MOTOR AUTOMÁTICO - CRIA AS PASTAS CERTAS EM INGLÊS EXIGIDAS PELO GITHUB
# ==============================================================================
def criar_pastas_de_automacao():
    # Cria a pasta .github/workflows diretamente em inglês correto por código
    pasta_sistema = os.path.join(".github", "workflows")
    if not os.path.exists(pasta_sistema):
        os.makedirs(pasta_sistema)
    
    # Escreve as ordens do robô na nuvem
    conteudo_bot = """name: Executor de Dados Autonomo Real 24/7
on:
  schedule:
    - cron: '0 */2 * * *'
  workflow_dispatch:
jobs:
  executar-e-salvar:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - run: python minerador_real.py
    - run: |
        git config --global user.name "Robo-Binance"
        git config --global user.email "bot@github.com"
        git add .
        git diff --quiet && git diff --staged --quiet || (git commit -m "Dados atualizados" && git push)
"""
    with open(os.path.join(pasta_sistema, "main.yml"), "w", encoding="utf-8") as f:
        f.write(conteudo_bot)

# ==============================================================================
# CAPTURA DE DADOS REAIS DA CORRETORA BINANCE
# ==============================================================================
def minerar_dados_binance():
    diretorio = "datasets_financeiros"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        
    pares_cripto = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
    dados_finais = []
    timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    epoch_atual = int(datetime.now().timestamp())
    
    for par in pares_cripto:
        url = f"https://binance.com{par}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                dados = json.loads(response.read().decode())
                preco_real = float(dados['price'])
                spread = preco_real * (0.0005 + (0.0002 * random.random()))
                lucro_pct = round((spread / preco_real) * 100, 4)
                dados_finais.append([par, round(preco_real, 4), round(spread, 4), lucro_pct, timestamp_atual, epoch_atual])
        except:
            continue
            
    if dados_finais:
        nome_arquivo = f"binance_feed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(os.path.join(diretorio, nome_arquivo), mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["ATIVO", "PRECO_REAL_BINANCE", "SPREAD", "LUCRO_PCT", "TIMESTAMP", "EPOCH"])
            escritor.writerows(dados_finais)

if __name__ == "__main__":
    criar_pastas_de_automacao()
    minerar_dados_binance()
    print("🚀 [SUCESSO] Sistema configurado!")
