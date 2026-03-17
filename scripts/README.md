# ⚙️ Scripts ETL - Jugando con herramientas externas

¡Bienvenido a los engranajes detrás de escena! El panel web y el bot en Telegram están geniales trabajando 100% en Python, pero me entró la duda: ¿qué pasaría si quiero llevar todos estos datos calculados y jugar con ellos en Power BI o Tableau?

Esta carpeta contiene scripts independientes (Pipeline **ETL**: *Extract, Transform, Load*) que operan tras bastidores para hacerle la vida más fácil a herramientas externas que quieran consumir los datos limpios de **AstroCryptoFeed**.

## 🧩 Herramientas Destacadas

- `export_powerbi.py` - Un script mágico que transforma cientos de mediciones complejas desde SQL y orquesta un `.csv` plano que cualquier software de Business Intelligence adora beber.

---

## 🏗️ Los Problemas que Enfrenté y Cómo los Resolví

### Problema 1: "Power BI no es bueno calculando series temporales complejas a gran escala"
Imaginemos que le lanzo los datos de precio crudos de varias criptos a Power BI. Si yo le pido a Power BI que calcule "RSI" o "Promedios Móviles Ponderados (EMA)", hacerlo a través de sentencias **DAX** no solo es un infierno de lidiar, sino que cuando la data crezca, va a colapsar el archivo `.pbix`.
✅ **Mi solución:** Delegué ese dolor de cabeza a Python. **Pandas** está increíblemente optimizado (gracias a sus bases en C++) para procesar "ventanas" (rolling windows). Usé `export_powerbi.py` para leer toda mi base de datos SQLite y pre-calcular en batch **RSI, SMA, EMA, y Bandas de Bollinger** para cada fila antes de exportarlo. Así, Power BI sólo recibe métricas planas listas para simplemente arrastrar a un gráfico visual; es **extremadamente** más rápido.

### Problema 2: "Los valores NaN rompen todo el Pipeline Visual"
Al calcular una Media Móvil Simple de 20 periodos (`SMA_20`), ¡los primeros 19 registros de la base de datos no tienen suficientes días atrás y devuelven valores en blanco (`NaN`)! **El problema:** Exportar `NaN` o valores parciales a una tabla corporativa genera campos vacíos feos o da errores en la ingesta automátizada de Power BI.
✅ **Mi solución (`bfill`):** En el ciclo de transformación del script, apliqué estratégicamente la técnica de *Backward Fill* (`df_processed.bfill()`) con Pandas tras el cálculo técnico. Esto hace que si las primeras filas no tenían manera estadística de generar sus métricas, copian el primer dato válido más cercano, manteniendo mi archivo CSV exportado denso, robusto y 100% libre de espacios en blanco sin perturbar grandemente las matemáticas reales de cara a futuros análisis. 

### Problema 3: "Mezclando Perros con Gatos al analizar el histórico"
Si saco toda la lista larga de precios sin distinciones y les aplico el promedio móvil global con Pandas, Pandas iba a calcular el promedio de Bitcoin cruzándolo con Ethereum simplemente por estar en fechas continuas dentro de un solo lote. **El problema:** Estaba a punto de causar un desastre estadístico financiero.
✅ **Mi solución:** Dentro del script ETL, usé filtros booleanos anidados e iteré dinámicamente:
```python
# Itero por cada activo individual evitando la mezcla letal
for symbol in df['symbol'].unique():
    df_sym = df[df['symbol'] == symbol].copy()
    # Recién aquí calculo...
```
¡Esto aseguró que el "RSI" de Bitcoin sea única y exclusivamente influído por los retornos de Bitcoin, produciendo la más alta calidad posible de Datos Desnormalizados Listos para BI!

---
*⚠️ **Nota:** Los datos generados por este ETL son estrictamente experimentales y educativos. **Bajo ningún motivo debes considerarlos una bola de cristal** o usarlos al pie de la letra para operar con dinero real. Protege tus finanzas.*
