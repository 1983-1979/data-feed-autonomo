
import os
import csv
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

# CONFIGURAÇÃO
DIRETORIO = "datasets_financeiros"
ARQUIVO = os.path.join(DIRETORIO, "historico_binance.csv")

ATIVOS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT"
]

URL_API = "https://api.binance.com/api/v3/ticker/bookTicker"


def capturar_dados_binance(ativo):
    """Consulta preços reais de compra e venda na Binance."""

    url = f"{URL_API}?symbol={ativo}"
    requisicao = urllib.request.Request(
        url,
        headers={"User-Agent": "FeedDadosAutonomo/1.0"}
    )

    try:
        with urllib.request.urlopen(requisicao, timeout=20) as resposta:
            dados = json.loads(resposta.read().decode("utf-8"))

        compra = float(dados["bidPrice"])
        venda = float(dados["askPrice"])

        if compra <= 0 or venda <= 0:
            raise ValueError("Preço inválido recebido")

        spread = venda - compra
        spread_pct = (spread / compra) * 100

        return {
            "ativo": ativo,
            "compra": compra,
            "venda": venda,
            "spread": spread,
            "spread_pct": spread_pct
        }

    except (urllib.error.URLError, urllib.error.HTTPError,
            TimeoutError, ValueError, KeyError) as erro:
        print(f"Erro ao consultar {ativo}: {erro}")
        return None


def executar_coleta():
    """Coleta e armazena dados históricos."""

    os.makedirs(DIRETORIO, exist_ok=True)

    arquivo_existe = os.path.exists(ARQUIVO)

    agora = datetime.now(timezone.utc)
    timestamp = agora.strftime("%Y-%m-%dT%H:%M:%SZ")
    epoch = int(agora.timestamp())

    resultados = []

    print(f"Iniciando coleta: {timestamp}")

    for ativo in ATIVOS:
        dados = capturar_dados_binance(ativo)

        if dados:
            resultados.append([
                dados["ativo"],
                dados["compra"],
                dados["venda"],
                dados["spread"],
                round(dados["spread_pct"], 6),
                timestamp,
                epoch
            ])

            print(
                f'{ativo}: compra={dados["compra"]} '
                f'venda={dados["venda"]} '
                f'spread={dados["spread_pct"]:.6f}%'
            )

    if resultados:
        with open(
            ARQUIVO,
            "a",
            newline="",
            encoding="utf-8"
        ) as arquivo:

            escritor = csv.writer(arquivo)

            if not arquivo_existe:
                escritor.writerow([
                    "ATIVO",
                    "PRECO_COMPRA",
                    "PRECO_VENDA",
                    "SPREAD",
                    "SPREAD_PCT",
                    "TIMESTAMP_UTC",
                    "EPOCH"
                ])

            escritor.writerows(resultados)

        print(f"Coleta concluída: {len(resultados)} ativos registrados.")
    else:
        print("Nenhum dado válido coletado neste ciclo.")
        raise RuntimeError("Falha na coleta de todos os ativos.")


if __name__ == "__main__":
    executar_coleta()
