# Portfolio Metrics Analyzer Pro

## Descripción

**Portfolio Metrics Analyzer Pro** es un script en Python diseñado para analizar portafolios de inversión compuestos por acciones, ETFs y criptomonedas. Utiliza datos históricos descargados desde Yahoo Finance para calcular métricas clave y generar visualizaciones que ayudan a evaluar el rendimiento y el riesgo del portafolio.

## Características

1. **Métricas Clave**:
   - **Rendimiento Promedio Anualizado (%):** Media anual de los rendimientos diarios.
   - **Volatilidad Anualizada (%):** Variabilidad anualizada de los rendimientos diarios.
   - **Rendimiento Acumulado (%):** Crecimiento total del portafolio durante el período analizado.
   - **Ratio Sharpe:** Medida del rendimiento ajustado al riesgo.
   
2. **Soporte para múltiples activos**:
   - Acciones y ETFs (ejemplo: `AAPL`, `SPY`).
   - Criptomonedas (ejemplo: `BTC-USD`, `ETH-USD`).
   
3. **Análisis multi-período**:
   - Métricas calculadas para rangos de 1, 3, 5 y 10 años.

4. **Visualización**:
   - Genera un gráfico de la cotización histórica ponderada del portafolio para los últimos 10 años.

5. **Resultados en HTML**:
   - Presenta las métricas en formato tabla para facilitar su visualización y uso.

---

## Requisitos

1. **Python 3.7 o superior**
2. Instalación de las librerías necesarias:
   ```bash
   pip install yfinance pandas numpy matplotlib
