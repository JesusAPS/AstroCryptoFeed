# 🔬 El Laboratorio de Datos: Mi Análisis Paso a Paso

Aquí te cuento el lado técnico pero contado por mí, osea, sin rollos aburridos. Me puse a jugar con Pandas y otras librerías para ver qué tanto podía exprimir los datos de cripto. ¡Esta es la parte donde me siento como un mini científico loco! ajajaja. 📈🧪

---

## 🏗️ 1. Preparando la Pócima (Limpieza ETL)

Antes de ver gráficos bonitos, tuve que limpiar el desastre de los datos crudos. No es tan fácil como parece, ¡pero aquí hice mi magia! 💪

*   **Poner las fechas en orden:** Los datos de la base de datos vienen como simples textos. Usé `pd.to_datetime()` para que Pandas entienda que son fechas reales. ¡Sin esto, mis gráficos estarían perdidos en el espacio!
*   **Arreglando los huecos (Manejo de NaNs):** Cuando calculas cosas como el promedio de 20 días, ¡los primeros 19 no existen! Usé `.bfill()` (Backward Fill) para que no me salieran celdas vacías que rompen el dashboard de Power BI. Todo densamente lleno y balanceado. 😎

---

## 📊 2. Mi Laboratorio de Datos (EDA en Streamlit)

Aquí es donde me pongo a inventar con Pandas para ver qué está pasando con el precio. No es solo mirar una línea; es entender el movimiento:

### El Truco de las Velas (Resampling) 🕯️
Agrupé miles de puntos de precio en velas de 1 hora. Es un truco genial de Pandas que me permite ver:
*   Donde empezó (**Open**), hasta donde subió (**High**), lo más bajo que cayó (**Low**) y como terminó (**Close**).

### Midiendo el Nerviosismo (Retornos y Volatilidad) 🌪️
Calculé cuánto cambia el precio de un momento a otro (`pct_change()`). Esto me dice qué tan loco está el mercado. Con la desviación estándar (`std()`), mido qué tan peligroso es meter dinero ahí. ¡Es pura ciencia del riesgo!

---

## 🧪 3. Mis Indicadores de "Científico Loco"

Metí estos indicadores técnicos para que el bot y el dashboard sean más inteligentes:

| Herramienta | ¿Para qué sirve? | Mi Toque Técnico 🛠️ |
| :--- | :--- | :--- |
| **RSI (14)** | Momentum (La fuerza) | Si está arriba de 70, la gente se volvió loca comprando. Si está bajo 30, ¡es un regalo! 🎁 |
| **SMA/EMA (20)** | La Tendencia | Limpio el "ruido" para ver si vamos para arriba o para abajo de forma real. |
| **Bollinger Bands** | Volatilidad Visual | Me dice si el precio está muy apretado o está a punto de explotar. 💥 |

---

## ⚡ 4. El Puente Veloz a Power BI

Hice que mi script `export_powerbi.py` fuera como un cohete. En lugar de hacer fórmulas difíciles dentro de Power BI (que es lentísimo), hice que Python calculara todo de una vez. 🚀
Asi, Power BI solo recibe una tabla limpia lista para usar. ¡Ahorra tiempo y recursos!

---
*Si quieres saber más, ¡revisa el código! Está todo comentado con mi estilo.* 👨‍🔬🧠 
