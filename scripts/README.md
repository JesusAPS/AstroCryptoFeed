# ⚙️ Scripts ETL - Los Engranajes de los Datos

¡Bienvenido a la parte de atrás de mi laboratorio! El bot en Telegram y el dashboard están muy cool corriendo solitos en Python, pero me puse a pensar: ¿qué pasaría si quiero llevar todos estos datos a Power BI o Tableau? 🤔📈

Esta carpeta tiene los scripts que corren tras bastidores para prepararle la vida a herramientas externas que quieran "beber" mis datos limpios de **AstroCryptoFeed**.

---

## 🧩 Herramientas Pro

*   **`export_powerbi.py`**: Es un script mágico que transforma cientos de mediciones complejas desde SQL y les da forma de un `.csv` plano que cualquier BI adora. ✨📊

---

## 🏗️ Retos que me hicieron pensar como un mini científico loco 🧠

### 1. Power BI no es muy rápido calculando cosas raras 😵‍⚖️
No quería lanzarle los precios crudos a Power BI y que él calculara el "RSI" o las "Medias Móviles". Hacer eso en **DAX** es un dolor de cabeza rudo y cuando la data crezca, se va a poner súper lento. 🐢
*   **Mi solución:** Le delegué ese problema a Python. Usando la potencia de **Pandas**, calculé todo el **RSI, SMA, EMA y Bandas de Bollinger** antes de exportar el archivo. ¡Así Power BI solo recibe datos planos listos para arrastrar a un gráfico y vuela! 🚀⚡

### 2. ¡Los valores vacíos (NaN) lo rompían todo! 🛠️
Al calcular la media de 20 periodos, ¡los primeros 19 quedan vacíos! Eso daba errores feos en la tabla final de Power BI.
*   **Mi solución (`bfill`):** Apliqué una técnica de Pandas llamada *Backward Fill* (`bfill`). Si un dato no tiene cálculo al inicio, copia el primer dato válido más cercano. Así el archivo final está 100% denso y sin "huecos" horribles. 😎💎

### 3. ¡Cuidado con mezclar peras con manzanas! 🍎🍐
Si sacaba una lista gigante de precios para todas las criptos a la vez, Pandas iba a calcular el promedio móvil mezclando Bitcoin con Ethereum por estar en fechas seguidas. ¡Eso hubiera sido un desastre estadístico! 😵💨
*   **Mi solución:** Hice un filtro inteligente para que el script analice cada criptomoneda por separado antes de juntarlas al final. ¡Garantía de calidad total!

---
*Nota: Los datos aquí son experimentales y educativos. No los uses como bola de cristal para tu dinero. ¡Cuida tus finanzas!* 👨‍🔬🧠 
