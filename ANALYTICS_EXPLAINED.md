# 🔬 El Lado de los Datos: Mi Análisis Paso a Paso

Aquí te cuento cómo fue que cuadré la parte analítica. Me puse a jugar con Pandas y otras librerías para ver qué tanto podía exprimir la data cripto, y este es el resultado de mi proceso de ingeniería. 📈✨

---

## 🏗️ 1. Preparando la Data (Ingesta ETL)

Antes de ver gráficos, tuve que poner en orden toda la data de entrada. No fue algo automático, sino que lo orquesté paso a paso:

*   **Conversión de Tiempo:** La data en la base de datos llega como texto. Usé `pd.to_datetime()` para que Pandas entienda que son fechas reales y así poder chequear las series temporales sin errores.
*   **Limpieza de Valores Nulos:** Al calcular indicadores (como el promedio de 20 días), los primeros registros quedan vacíos. Usé `.bfill()` (Backward Fill) para que no salieran huecos que me dañaran los gráficos en Power BI. Así quedó todo denso y bien cuadrado. 😎

---

## 📊 2. El Análisis Exploratorio de Datos (EDA)

Aquí es donde me pongo a usar Pandas de buena forma para entender el movimiento de los precios. No es solo mirar una línea, sino entender qué está pasando realmente:

### Resampling (Velas Japonesas) 🕯️
Agrupé miles de puntos de precio en velas de 1 hora. Es un truco genial de Pandas que me permite ver:
*   Dónde abrió el precio (**Open**), hasta dónde subió (**High**), lo más bajo que cayó (**Low**) y dónde cerró (**Close**). ¡Quedó impecable!

### Midiendo el Riesgo (Retornos y Volatilidad) 🌪️
Calculé cuánto cambia el precio de un momento a otro (`pct_change()`). Esto me dice qué tan volátil está el mercado. Con la desviación estándar (`std()`), mido qué tan rudo está el riesgo en ese activo. ¡Es pura ciencia del dato!

---

## 🧪 3. Los Indicadores que Utilicé

He implementado estos indicadores técnicos para que el bot y el dashboard sean más eficientes al dar alertas:

| Indicador | Función | Mi Lógica Técnica 🛠️ |
| :--- | :--- | :--- |
| **RSI (14)** | Momentum (La fuerza) | Si está arriba de 70, la gente está muy eufórica comprando. Si está bajo 30, ¡es un regalo! 🎁 |
| **SMA/EMA (20)** | La Tendencia | Limpio el "ruido" para ver si la tendencia del mercado va para arriba o para abajo de verdad. |
| **Bollinger Bands** | Volatilidad Visual | Me dice si el precio está muy apretado o si está por salir disparado. 💥 |

---

## ⚡ 4. El Puente Veloz hacia Power BI

Hice que mi script `export_powerbi.py` fuera súper eficiente. En lugar de hacer fórmulas difíciles dentro de Power BI con DAX (que es lento), hice que Python lo calculara todo de una vez. 🚀
Así, Power BI solo recibe una tabla limpia que puedo arrastrar a los gráficos sin que se pegue la computadora. ¡Quedó fino! ✨

---
*Si quieres saber más, puedes chequear el código. Está todo comentado paso a paso.* 👨‍💻🛰️ 
