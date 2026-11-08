import os
import csv
import urllib.request
import json
from datetime import datetime

def capturar_preco_binance(ticker):
    """Busca o preço em tempo real diretamente na API pública da Binance."""
    url = f"https://binance.com{ticker}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            dados = json.loads(response.read().decode())
            return float(dados['price'])
    except Exception as e:
        print(f"⚠️ Erro ao conectar com a API para o ativo {ticker}: {e}")
        return None

def executar_mineracao_real():
    """Minera preços reais, calcula spreads sintéticos de arbitragem e sela o arquivo."""
    diretorio = "datasets_financeiros"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        
    # Pares de moedas de alta liquidez para monitoramento
    pares_cripto = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
    dados_finais = []
    
    timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    epoch_atual = int(datetime.now().timestamp())
    
    print(f"🔄 Iniciando coleta de dados reais da API da Binance às {timestamp_atual}...")
    
    for par in pares_cripto:
        preco_real = capturar_preco_binance(par)
        
        if preco_real is not None:
            # Algoritmo matemático para simular detecção de spreads de arbitragem entre corretoras de balcão
            # Variação típica de mercado flutua entre 0.05% e 0.3%
            spread_simulado = preco_real * round(random_spread := (0.0005 + (0.0025 * (preco_real % 1))), 4)
            lucro_estimado_pct = round((spread_simulado / preco_real) * 100, 4)
            
            dados_finais.append([
                par, 
                round(preco_real, 4), 
                round(spread_simulado, 4), 
                lucro_estimado_pct, 
                timestamp_atual, 
                epoch_atual
            ])
            
    if dados_finais:
        # Nome único baseado no timestamp para criar um histórico cronológico perfeito
        nome_arquivo = f"binance_feed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        caminho_completo = os.path.join(diretorio, nome_arquivo)
        
        with open(caminho_completo, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["ATIVO", "PRECO_REAL_BINANCE", "SPREAD_ARBITRAGEM", "LUCRO_PCT", "TIMESTAMP", "EPOCH"])
            escritor.writerows(dados_finais)
            
        print(f"📊 [SUCESSO] Bloco de dados reais gerado e selado em: {caminho_completo}")
    else:
        print("❌ [FALHA] Nenhum dado pôde ser coletado neste ciclo.")

if __name__ == "__main__":
    # Importação interna para garantir execução limpa na nuvem
    import random
    executar_mineracao_real()
