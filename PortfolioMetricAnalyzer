import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Función para obtener el rango de fechas basado en el período
def get_date_range(years):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

# Función para calcular la cotización ponderada del portafolio
def calculate_weighted_portfolio(data, weights):
    weights = [w / 100 for w in weights]  # Convertir pesos a proporciones
    weighted_portfolio = (data * weights).sum(axis=1)  # Calcular la cotización ponderada
    return weighted_portfolio

# Función para calcular métricas del portafolio
def calculate_portfolio_metrics(portfolio):
    # Calcular rendimientos diarios
    returns = portfolio.pct_change().dropna()

    # Calcular métricas
    metrics = {
        "Rendimiento Promedio (%)": returns.mean() * 252 * 100,  # Promedio anualizado
        "Volatilidad (%)": returns.std() * np.sqrt(252) * 100,  # Volatilidad anualizada
        "Rendimiento Acumulado (%)": ((portfolio[-1] / portfolio[0]) - 1) * 100,  # Rendimiento acumulado
        "Ratio Sharpe": (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else np.nan  # Ratio Sharpe
    }
    return pd.Series(metrics)

# Entrada del usuario
tickers = input("Ingrese los tickers separados por comas (ej: AAPL,BTC-USD,ETH-USD): ").strip()
weights = input("Ingrese los pesos correspondientes separados por comas (ej: 50,25,25): ").strip()

try:
    # Procesar entradas
    ticker_list = [ticker.strip() for ticker in tickers.split(",")]
    weight_list = [float(weight.strip()) for weight in weights.split(",")]

    if len(ticker_list) != len(weight_list):
        raise ValueError("El número de tickers no coincide con el número de pesos.")

    # Validar que los pesos sumen 100
    if sum(weight_list) != 100:
        raise ValueError("Los pesos no suman 100%. Por favor, ajuste los valores.")

    # Períodos de análisis
    time_periods = {"1A": 1, "3A": 3, "5A": 5, "10A": 10}
    results = []

    # Calcular métricas para cada período
    for label, years in time_periods.items():
        start_date, end_date = get_date_range(years)
        data = yf.download(ticker_list, start=start_date, end=end_date)['Adj Close']

        if data.empty:
            raise ValueError(f"No se encontraron datos para el período {label}.")

        portfolio = calculate_weighted_portfolio(data, weight_list)
        metrics = calculate_portfolio_metrics(portfolio)
        metrics["Período"] = label
        results.append(metrics)

    # Crear DataFrame con los resultados
    metrics_df = pd.DataFrame(results)

    # Mostrar la tabla en HTML
    print("\nTabla de métricas del portafolio (HTML):\n")
    print(metrics_df.to_html(index=False))

    # Generar gráfico para el período de 10 años
    start_date, end_date = get_date_range(10)
    data_10y = yf.download(ticker_list, start=start_date, end=end_date)['Adj Close']
    portfolio_10y = calculate_weighted_portfolio(data_10y, weight_list)

    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_10y.index, portfolio_10y, label="Portafolio Ponderado (10A)", color="blue")
    plt.title("Cotización Histórica del Portafolio Ponderado (10 Años)")
    plt.xlabel("Fecha")
    plt.ylabel("Cotización")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Ocurrió un error: {e}")
