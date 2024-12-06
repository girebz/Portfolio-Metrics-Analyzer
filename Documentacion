# Documentación del Script de Gestión de Portafolio

## Descripción General
Este script calcula, analiza y visualiza un portafolio de activos financieros utilizando datos históricos. Permite al usuario:
1. Ingresar los tickers de los activos y sus pesos.
2. Definir un rango de tiempo para el análisis.
3. Calcular métricas del portafolio ponderado y visualizar tendencias de precios.

## Documentación del Código

```python
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Función para determinar el rango de fechas según los años definidos por el usuario
def get_date_range(years):
    """
    Calcula las fechas de inicio y fin basadas en el número de años ingresado.

    Args:
        years (int): Número de años para el rango de fechas.

    Returns:
        tuple: Fechas de inicio y fin en formato 'YYYY-MM-DD'.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

# Función para calcular los precios ponderados del portafolio
def calculate_weighted_portfolio(data, weights):
    """
    Calcula los precios ponderados del portafolio según los pesos de los activos.

    Args:
        data (DataFrame): Precios históricos ajustados de los activos.
        weights (list): Lista de pesos correspondientes a cada activo.

    Returns:
        Series: Precios ponderados del portafolio.
    """
    weights = [w / 100 for w in weights]  # Convertir los pesos a proporciones
    weighted_portfolio = (data * weights).sum(axis=1)
    return weighted_portfolio

# Función para calcular métricas de rendimiento del portafolio
def calculate_portfolio_metrics(portfolio):
    """
    Calcula las métricas clave de rendimiento para un portafolio.

    Args:
        portfolio (Series): Precios ponderados del portafolio.

    Returns:
        Series: Métricas del portafolio, incluyendo retorno anualizado, volatilidad y ratio Sharpe.
    """
    returns = portfolio.pct_change().dropna()
    metrics = {
        "Rendimiento Promedio (%)": returns.mean() * 252 * 100,
        "Volatilidad (%)": returns.std() * np.sqrt(252) * 100,
        "Rendimiento Acumulado (%)": ((portfolio[-1] / portfolio[0]) - 1) * 100,
        "Ratio Sharpe": (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else np.nan
    }
    return pd.Series(metrics)

# Función para solicitar al usuario el tipo de escala del eje Y
def select_y_scale():
    """
    Solicita al usuario que seleccione el tipo de escala para el eje Y.

    Returns:
        int: Opción de escala (1 para lineal, 2 para logarítmica, 3 para exponencial).
    """
    print("\nSeleccione el tipo de escala para el eje Y:")
    print("1) Escala lineal")
    print("2) Escala logarítmica")
    print("3) Escala exponencial")
    while True:
        try:
            choice = int(input("Ingrese su elección (1, 2 o 3): ").strip())
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Por favor, elija una opción válida.")
        except ValueError:
            print("Entrada no válida. Intente de nuevo.")

# Función para solicitar al usuario un rango de tiempo para el análisis
def select_time_scale():
    """
    Solicita al usuario que seleccione un rango de tiempo para el análisis.

    Returns:
        int: Número de años correspondiente al rango de tiempo seleccionado.
    """
    print("\nSeleccione el rango de tiempo para el gráfico:")
    print("1) 1 año")
    print("2) 3 años")
    print("3) 5 años")
    print("4) 10 años")
    while True:
        try:
            choice = int(input("Ingrese su elección (1, 2, 3 o 4): ").strip())
            if choice in [1, 2, 3, 4]:
                return [1, 3, 5, 10][choice - 1]
            else:
                print("Por favor, elija una opción válida.")
        except ValueError:
            print("Entrada no válida. Intente de nuevo.")

# Entrada principal del usuario y procesamiento de datos
tickers = input("Ingrese los tickers separados por comas (ej: AAPL,MSFT): ").strip()
weights = input("Ingrese los pesos correspondientes separados por comas (ej: 50,50): ").strip()

try:
    ticker_list = [ticker.strip() for ticker in tickers.split(",")]
    weight_list = [float(weight.strip()) for weight in weights.split(",")]

    if len(ticker_list) != len(weight_list):
        raise ValueError("El número de tickers no coincide con el número de pesos.")

    if sum(weight_list) != 100:
        raise ValueError("Los pesos no suman 100%. Por favor, ajuste los valores.")

    y_scale_choice = select_y_scale()
    scale_labels = {1: "Escala Lineal", 2: "Escala Logarítmica", 3: "Escala Exponencial"}
    time_scale = select_time_scale()

    start_date, end_date = get_date_range(time_scale)
    data_selected = yf.download(ticker_list, start=start_date, end=end_date)['Adj Close']

    if data_selected.empty:
        raise ValueError("No se encontraron datos históricos para los tickers especificados.")

    plt.figure(figsize=(12, 6))
    for ticker, weight in zip(ticker_list, weight_list):
        plt.plot(data_selected.index, data_selected[ticker], label=f"{ticker} ({weight}%)", linestyle="--")

    if len(ticker_list) > 1:
        portfolio_selected = calculate_weighted_portfolio(data_selected, weight_list)
        plt.plot(portfolio_selected.index, portfolio_selected, label="Subcartera", color="blue", linewidth=2)

    if y_scale_choice == 1:
        plt.yscale("linear")
    elif y_scale_choice == 2:
        plt.yscale("log")
    elif y_scale_choice == 3:
        plt.yscale("symlog")

    plt.title(f"Cotización Histórica del Portafolio ({time_scale} Año(s)) - {scale_labels[y_scale_choice]}")
    plt.xlabel("Time")
    plt.ylabel("USD")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    if len(ticker_list) > 1:
        results = []
        for label, years in {"1A": 1, "3A": 3, "5A": 5, "10A": 10}.items():
            start_date, end_date = get_date_range(years)
            data = yf.download(ticker_list, start=start_date, end=end_date)['Adj Close']
            portfolio = calculate_weighted_portfolio(data, weight_list)
            metrics = calculate_portfolio_metrics(portfolio)
            metrics["Período"] = label
            results.append(metrics)

        metrics_df = pd.DataFrame(results)
        columns_order = ["Período"] + [col for col in metrics_df.columns if col != "Período"]
        metrics_df = metrics_df[columns_order].round(2)

        html_table = metrics_df.to_html(index=False)
        html_table = html_table.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" style="text-align: left;">')
        html_table = html_table.replace('<thead>', '<thead style="font-size: 14px;">')

        print("\nTabla de métricas del portafolio (HTML):\n")
        print(html_table)

except Exception as e:
    print(f"Ocurrió un error: {e}")
