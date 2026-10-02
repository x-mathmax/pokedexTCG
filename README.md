# 📇 Pokédex TCG — Catálogo & Análisis de Colección Personal

## Objetivo del Proyecto

**Pokédex TCG** es una aplicación interactiva desarrollada en Python para coleccionistas y entusiastas del juego de cartas coleccionables Pokémon (TCG). La herramienta permite centralizar la búsqueda en tiempo real mediante la API pública de `pokemontcg.io`, gestionar un inventario personal de forma persistente en un archivo local `JSON`, calcular indicadores financieros y estadísticos, y generar análisis gráficos interactivos.

---

## Estructura del Proyecto

- **`app.py`**: Interfaz gráfica e interactiva de la aplicación web desarrollada con Streamlit.
- **`main.py`**: Interfaz interactiva para ejecución por consola / terminal basada en menús.
- **`funciones.py`**: Módulo central con la lógica de negocio, consumo de la API, persistencia en JSON, validaciones de datos con `type hints` e indicadores estadísticos.
- **`analisis.ipynb`**: Notebook de Jupyter para exploración de datos con Pandas, gráficos de barras de Matplotlib (con paleta de colores temáticos por tipo elemental) y renderizado de la galería de imágenes.
- **`datos.json`**: Archivo local utilizado para la persistencia de los datos de la colección entre ejecuciones.
- **`requirements.txt`**: Listado de dependencias y librerías externas necesarias para el funcionamiento del proyecto.

---

## Instrucciones de Instalación y Ejecución

### 1. Instalación de Dependencias

Antes de ejecutar cualquiera de los módulos, instalar las librerías requeridas desde la terminal:

```bash
pip install -r requirements.txt
```

### 2. Modo A: Ejecución de la Interfaz Visual Web (Recomendado)

Para iniciar la aplicación gráfica e interactiva en el navegador mediante Streamlit, ejecutar en la consola:

```bash
streamlit run app.py
```

Se abrirá automáticamente una pestaña en el navegador en la dirección `http://localhost:8501`.

### 3. Modo B: Ejecución por Consola (Terminal)

Para utilizar la versión de menú interactivo por texto en la terminal, ejecutar:

```bash
python main.py
```

### 4. Modo C: Ejecución del Análisis (`analisis.ipynb`) en Visual Studio Code

1. Abrir el archivo `analisis.ipynb` en VS Code.
2. En la esquina superior derecha del editor, hacer clic en **"Select Kernel"** (o **"Seleccionar Kernel"**).
3. Seleccionar **Python Environments...** y elegir la versión del intérprete de Python instalada en el sistema.
4. Hacer clic en **"Run All"** (o **"Ejecutar todo"**) en la barra superior de la notebook para procesar las celdas y generar las figuras.

---

## Validación de Funcionamiento

El código generado y modificado se validó mediante los siguientes casos de prueba:

- **Búsquedas con distinto formato de texto:** cadenas en mayúsculas, minúsculas y caracteres mixtos (`gEnGaR`, `lugia`, `LUGIA`).
- **Resultados vacíos:** ingreso de nombres inexistentes o búsquedas en blanco, para comprobar la respuesta de la interfaz.
- **Precios no disponibles:** carga de cartas con precio `None` o `0.0`, para asegurar la solidez del cálculo del valor total acumulado.
- **Empate en cantidad máxima:** colecciones en las que dos o más cartas comparten la misma cantidad máxima, para validar que se muestren todas y no solo una.