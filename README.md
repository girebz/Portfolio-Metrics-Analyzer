# Portfolio Metrics Analyzer

## Descripción General

Este proyecto es un script de Python diseñado para gestionar, analizar y visualizar un portafolio financiero. El usuario puede proporcionar una lista de activos (tickers) y asignarles pesos para calcular métricas clave de rendimiento, como el retorno anualizado, la volatilidad y el ratio Sharpe. Además, el script genera gráficos de las tendencias de precios históricos, permitiendo elegir entre varias escalas y rangos de tiempo.

---

## Características

1. **Cálculo de métricas del portafolio**:
   - Retorno promedio anualizado.
   - Volatilidad anualizada.
   - Retorno acumulado.
   - Ratio Sharpe.

2. **Visualización gráfica**:
   - Soporte para escalas lineales, logarítmicas y exponenciales.
   - Elección de rangos de tiempo predefinidos (1, 3, 5 o 10 años).
   - Superposición de datos individuales y del portafolio ponderado.

3. **Interfaz interactiva**:
   - Solicita al usuario información clave, como tickers, pesos, escala del eje Y y rango de tiempo.

---

## Requisitos del Sistema

1. **Python**: Versión 3.7 o superior.
2. **Bibliotecas necesarias**:
   - `yfinance`
   - `pandas`
   - `numpy`
   - `matplotlib`

Instale las bibliotecas requeridas ejecutando:

```bash
pip install yfinance pandas numpy matplotlib
