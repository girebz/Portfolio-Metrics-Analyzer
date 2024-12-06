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

# Función para seleccionar escala del eje Y
def select_y_scale():
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

# Función para seleccionar escala de tiempo
def select_time_scale():
    print("\nSeleccione el rango de tiempo para el gráfico:")
    print("1) 1 año")
    print("2) 3 años")
    print("3) 5 años")
    print("4) 10 años")
    
    while True:
        try:
            choice = int(input("Ingrese su elección (1, 2, 3 o 4): ").strip())
            if choice in [1, 2, 3, 4]:
                return [1, 3, 5, 10][choice - 1]  # Retorna el valor de años según la elección
            else:
                print("Por favor, elija una opción válida.")
        except ValueError:
            print("Entrada no válida. Intente de nuevo.")

# Entrada del usuario
tickers = input("Ingrese los tickers separados por comas (ej: AAPL,MSFT): ").strip()
weights = input("Ingrese los pesos correspondientes separados por comas (ej: 50,50): ").strip()

try:
    # Procesar entradas
    ticker_list = [ticker.strip() for ticker in tickers.split(",")]
    weight_list = [float(weight.strip()) for weight in weights.split(",")]

    if len(ticker_list) != len(weight_list):
        raise ValueError("El número de tickers no coincide con el número de pesos.")

    # Validar que los pesos sumen 100
    if sum(weight_list) != 100:
        raise ValueError("Los pesos no suman 100%. Por favor, ajuste los valores.")

    # Preguntar por la escala del eje Y y el rango de tiempo
    y_scale_choice = select_y_scale()
    scale_labels = {1: "Escala Lineal", 2: "Escala Logarítmica", 3: "Escala Exponencial"}
    time_scale = select_time_scale()

    # Generar datos históricos para el rango de tiempo seleccionado
    start_date, end_date = get_date_range(time_scale)
    data_selected = yf.download(ticker_list, start=start_date, end=end_date)['Adj Close']

    if data_selected.empty:
        raise ValueError("No se encontraron datos históricos para los tickers especificados.")

    plt.figure(figsize=(12, 6))

    # Graficar cada instrumento individualmente
    for ticker, weight in zip(ticker_list, weight_list):
        plt.plot(data_selected.index, data_selected[ticker], label=f"{ticker} ({weight}%)", linestyle="--")

    # Si hay más de un instrumento, calcular y graficar el promedio ponderado
    portfolio_selected = None
    if len(ticker_list) > 1:
        portfolio_selected = calculate_weighted_portfolio(data_selected, weight_list)
        plt.plot(portfolio_selected.index, portfolio_selected, label="Subcartera", color="blue", linewidth=2)

    # Configuración de la escala del eje Y
    if y_scale_choice == 1:
        plt.yscale("linear")
    elif y_scale_choice == 2:
        plt.yscale("log")
    elif y_scale_choice == 3:
        plt.yscale("symlog")  # Escala exponencial aproximada

    # Título del gráfico con la escala y el rango de tiempo utilizados
    plt.title(f"Cotización Histórica del Portafolio ({time_scale} Año(s)) - {scale_labels[y_scale_choice]}")
    plt.xlabel("Time" )
    plt.ylabel("USD")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    # Calcular métricas del portafolio ponderado (siempre para 1A, 3A, 5A y 10A)
    if len(ticker_list) > 1:
        results = []
        for label, years in {"1A": 1, "3A": 3, "5A": 5, "10A": 10}.items():
            start_date, end_date = get_date_range(years)
            data = yf.download(ticker_list, start=start_date, end=end_date)['Adj Close']
            portfolio = calculate_weighted_portfolio(data, weight_list)
            metrics = calculate_portfolio_metrics(portfolio)
            metrics["Período"] = label
            results.append(metrics)

        # Crear DataFrame con las métricas
        metrics_df = pd.DataFrame(results)

        # Reordenar columnas para que "Período" sea la primera
        columns_order = ["Período"] + [col for col in metrics_df.columns if col != "Período"]
        metrics_df = metrics_df[columns_order]

        # Ajustar precisión a 2 dígitos
        metrics_df = metrics_df.round(2)

        # Generar la tabla HTML con estilo personalizado
        html_table = metrics_df.to_html(index=False)
        html_table = html_table.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" style="text-align: left;">')
        html_table = html_table.replace('<thead>', '<thead style="font-size: 14px;">')

        print("\nTabla de métricas del portafolio (HTML):\n")
        print(html_table)

except Exception as e:
    print(f"Ocurrió un error: {e}")
