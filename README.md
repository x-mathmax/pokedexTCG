# 📇 Pokédex TCG — Catálogo de Colección Personal

## Objetivo
Aplicación interactiva para gestionar y analizar una colección personal de cartas de Pokémon TCG integrando la API de pokemontcg.io, persistencia de datos en JSON y análisis visual mediante Pandas y Matplotlib.

## Estructura del Proyecto
- `main.py`: Menú principal e interfaz de consola.
- `funciones.py`: Módulo con la lógica de negocio, llamados a la API, validaciones e indicadores.
- `analisis.ipynb`: Notebook para la visualización de la galería de cartas y gráficos de barras/torta.
- `datos.json`: Archivo local para persistencia de la colección.
- `requirements.txt`: Dependencias del proyecto.

## Cómo Ejecutarlo
1. Instalar dependencias:
   `pip install -r requirements.txt`
2. Ejecutar la app por consola:
   `python main.py`
3. Abrir `analisis.ipynb` en Jupyter Notebook o VS Code para visualizar las estadísticas y la galería de imágenes.

## Registro de Prompts de IA (Requisito TP)
1. **Prompt 1 (Diseño de lógica de precios en API):** 
   - *Consulta:* "¿Cómo extraer de forma segura el precio 'market' de la API pokemontcg.io considerando que la estructura de `tcgplayer.prices` cambia según si la carta es holofoil, reverseHolofoil o normal?"
   - *Decisión:* Aceptada la implementación con un bucle dinámico y bloque `try/except` para no romper la ejecución si el precio no está disponible.
2. **Prompt 2 (Descarga e inclusión de imágenes en Matplotlib):**
   - *Consulta:* "¿Cómo convertir la URL de la imagen recibida por la API en un objeto dibujable por `matplotlib.imshow`?"
   - *Decisión:* Aceptada la propuesta utilizando `PIL.Image` y `io.BytesIO`.
3. **Prompt 3 (Filtrado de DataFrames):**
   - *Consulta:* "¿Cómo calcular el precio total acumulado por set si la cantidad de cartas de cada fila varía?"
   - *Decisión:* Aceptada la solución creando una columna calculada `df['valor_total_usd'] = df['precio_usd'] * df['cantidad']` previo al `groupby`.
