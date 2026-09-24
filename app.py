import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO

# Importamos las funciones que ya tenías desarrolladas
from funciones import (
    cargar_coleccion, guardar_coleccion, buscar_carta_api,
    extraer_datos_carta, agregar_a_coleccion, modificar_cantidad,
    calcular_valor_total, carta_mas_repetida, tipo_mas_frecuente, promedio_hp
)

# Configuración de página
st.set_page_config(
    page_title="Pokédex TCG — Colección Personal",
    page_icon="📇",
    layout="wide"
)

# Título Principal
st.title("📇 Pokédex TCG — Catálogo & Análisis")
st.markdown("Gestión y análisis estadístico de tu colección personal de cartas Pokémon.")

# Carga de la colección
coleccion = cargar_coleccion()

# Menú Lateral (Sidebar)
st.sidebar.header("Navegación")
menu = st.sidebar.radio(
    "Seleccioná una sección:",
    ["📊 Mi Colección & Indicadores", "🔍 Buscar & Agregar Cartas", "✏️ Gestionar Colección", "📈 Análisis Visual (Gráficos)"]
)

# ---------------------------------------------------------
# SECCIÓN 1: MI COLECCIÓN & INDICADORES
# ---------------------------------------------------------
if menu == "📊 Mi Colección & Indicadores":
    st.header("Resumen de tu Colección")
    
    if not coleccion:
        st.info("📭 Tu colección está vacía. Ir a 'Buscar & Agregar Cartas' para empezar.")
    else:
        # Fila de Metricas e Indicadores
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Valor Total Estimado", f"${calcular_valor_total(coleccion):.2f} USD")
        col2.metric("Tipo Dominante", tipo_mas_frecuente(coleccion))
        col3.metric("Promedio de HP", f"{promedio_hp(coleccion):.1f}")
        
        c_rep = carta_mas_repetida(coleccion)
        if c_rep:
            col4.metric("Carta más Repetida", f"{c_rep['nombre']} ({c_rep['cantidad']}x)")

        st.divider()

        # Tabla de Datos con Pandas
        st.subheader("Lista de Cartas")
        df = pd.DataFrame(coleccion)
        df['valor_total_usd'] = df['precio_usd'] * df['cantidad']
        
        # Filtros rápidos en la interfaz
        tipo_filtro = st.multiselect("Filtrar por Tipo:", options=df['tipo'].unique())
        if tipo_filtro:
            df_mostrar = df[df['tipo'].isin(tipo_filtro)]
        else:
            df_mostrar = df

        st.dataframe(
            df_mostrar[["id", "nombre", "tipo", "rareza", "set", "hp", "precio_usd", "cantidad", "valor_total_usd"]],
            use_container_width=True
        )

# ---------------------------------------------------------
# SECCIÓN 2: BUSCAR & AGREGAR CARTAS (CON PAGINACIÓN)
# ---------------------------------------------------------
elif menu == "🔍 Buscar & Agregar Cartas":
    st.header("Buscador de Cartas en la API")
    
    col_busqueda, col_btn = st.columns([3, 1])
    with col_busqueda:
        nombre_buscar = st.text_input("Nombre de la carta (en inglés, ej: Pikachu, Charizard):")
    
    if st.button("Buscar en Pokémon TCG API"):
        if nombre_buscar:
            with st.spinner("Conectando con la API..."):
                resultados = buscar_carta_api(nombre_buscar)
                
            if not resultados:
                st.error("❌ No se encontraron cartas con ese nombre o hubo un problema de conexión.")
                st.session_state['resultados_busqueda'] = []
            else:
                st.session_state['resultados_busqueda'] = resultados
                st.session_state['pagina_actual'] = 0  # Reiniciar a la primera página
        else:
            st.warning("Por favor, ingresá un nombre para buscar.")

    # Manejo y visualización con paginación
    if 'resultados_busqueda' in st.session_state and st.session_state['resultados_busqueda']:
        resultados = st.session_state['resultados_busqueda']
        total_resultados = len(resultados)
        
        # Configuración de elementos por página
        CARTAS_POR_PAGINA = 6
        total_paginas = (total_resultados + CARTAS_POR_PAGINA - 1) // CARTAS_POR_PAGINA
        
        # Inicializar página en session_state si no existe
        if 'pagina_actual' not in st.session_state:
            st.session_state['pagina_actual'] = 0
            
        pagina_actual = st.session_state['pagina_actual']
        
        # Calcular índices de corte para la página actual
        inicio = pagina_actual * CARTAS_POR_PAGINA
        fin = min(inicio + CARTAS_POR_PAGINA, total_resultados)
        cartas_pagina = resultados[inicio:fin]
        
        st.success(f"Se encontraron **{total_resultados}** cartas en total. Mostrando página **{pagina_actual + 1}** de **{total_paginas}**:")
        
        # Mostrar cartas de la página en grilla de 3 columnas
        cols = st.columns(3)
        for i, carta_raw in enumerate(cartas_pagina):
            carta = extraer_datos_carta(carta_raw)
            with cols[i % 3]:
                st.markdown(f"### {carta['nombre']}")
                if carta['imagen_url']:
                    st.image(carta['imagen_url'], use_container_width=True)
                st.caption(f"**ID:** `{carta['id']}` | **Set:** {carta['set']}")
                st.caption(f"**Rareza:** {carta['rareza']} | **Precio:** ${carta['precio_usd']:.2f} USD")
                
                cant = st.number_input(
                    f"Cantidad copias:", 
                    min_value=1, 
                    value=1, 
                    step=1, 
                    key=f"num_{carta['id']}_{pagina_actual}"
                )
                if st.button(f"➕ Agregar", key=f"btn_{carta['id']}_{pagina_actual}"):
                    coleccion = agregar_a_coleccion(coleccion, carta, cant)
                    guardar_coleccion(coleccion)
                    st.toast(f"¡{cant} copia(s) de {carta['nombre']} ({carta['set']}) agregada(s)!", icon="✅")

        st.divider()

        # Controles de navegación de páginas (Anterior / Siguiente)
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if st.button("⬅️ Anterior", disabled=(pagina_actual == 0)):
                st.session_state['pagina_actual'] -= 1
                st.rerun()

        with col_info:
            st.markdown(f"<p style='text-align: center;'>Página <b>{pagina_actual + 1}</b> de <b>{total_paginas}</b></p>", unsafe_allow_html=True)

        with col_next:
            if st.button("Siguiente ➡️", disabled=(pagina_actual >= total_paginas - 1)):
                st.session_state['pagina_actual'] += 1
                st.rerun()

# ---------------------------------------------------------
# SECCIÓN 3: GESTIONAR COLECCIÓN
# ---------------------------------------------------------
elif menu == "✏️ Gestionar Colección":
    st.header("Modificar o Eliminar Cartas")
    
    if not coleccion:
        st.info("📭 Tu colección está vacía.")
    else:
        opciones_cartas = {f"{c['nombre']} ({c['id']}) - Copias actuales: {c['cantidad']}": c['id'] for c in coleccion}
        seleccion = st.selectbox("Seleccioná la carta que querés modificar:", list(opciones_cartas.keys()))
        
        card_id = opciones_cartas[seleccion]
        nueva_cant = st.number_input("Nueva cantidad de copias (0 para eliminar):", min_value=0, value=1, step=1)
        
        if st.button("Guardar Cambios"):
            if modificar_cantidad(coleccion, card_id, nueva_cant):
                guardar_coleccion(coleccion)
                st.success("✅ Colección actualizada correctamente.")
                st.rerun()

# ---------------------------------------------------------
# SECCIÓN 4: ANÁLISIS VISUAL (GRÁFICOS)
# ---------------------------------------------------------
elif menu == "📈 Análisis Visual (Gráficos)":
    st.header("Estadísticas y Galería Visual")
    
    if not coleccion:
        st.info("📭 Agregá cartas a tu colección para ver el análisis gráfico.")
    else:
        df = pd.DataFrame(coleccion)
        df['valor_total_usd'] = df['precio_usd'] * df['cantidad']
        
        # Gráficos con Matplotlib
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.subheader("Cantidad de Cartas por Tipo")
            fig1, ax1 = plt.subplots()
            df_tipo = df.groupby('tipo')['cantidad'].sum()
            df_tipo.plot(kind='bar', ax=ax1, color='#ffcb05', edgecolor='#3657a0', linewidth=1.5)
            ax1.set_ylabel("Copias")
            st.pyplot(fig1)

        with col_g2:
            st.subheader("Valor ($ USD) por Rareza")
            fig2, ax2 = plt.subplots()
            df_rareza = df.groupby('rareza')['valor_total_usd'].sum()
            df_rareza.plot(kind='barh', ax=ax2, color='#e3350d', edgecolor='black')
            ax2.set_xlabel("USD Total")
            st.pyplot(fig2)

        st.divider()
        st.subheader("🖼️ Galería Visual de Cartas")
        
        cartas_con_img = df[df['imagen_url'] != ''].head(12)
        cols_gal = st.columns(4)
        for idx, (_, row) in enumerate(cartas_con_img.iterrows()):
            with cols_gal[idx % 4]:
                st.image(row['imagen_url'], caption=f"{row['nombre']} (x{row['cantidad']})")