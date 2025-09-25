# -*- coding: utf-8 -*-
"""
Created on Sat on Apr 19 21:39:21 2025

@author: GEORGENAGWANTED

"""

# -*- coding: utf-8 -*-
"""
Semana 5 - Tecnologías Emergentes

Integrante:

- Taquiri Pillaca Jorge Ignacio	20200339

"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import io
from scipy.io import readsav
import re
import csv

# Configuración de página moderna
st.set_page_config(
    page_title="DataViz Pro Advanced - Análisis Visual Inteligente",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados mejorados
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        background: linear-gradient(45deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header moderno con columnas
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<h1 class="main-header">🔬 DataViz Pro Advanced</h1>', unsafe_allow_html=True)
    st.markdown("### *Plataforma Inteligente de Análisis Exploratorio de Datos*")
    st.markdown("---")

# Sidebar moderno con información útil
with st.sidebar:
    st.success("🎯 **DataViz Pro Advanced Activado**")
    st.markdown("---")
    st.markdown("### 🔧 Panel de Control Avanzado")
    
    # Selector de tema de visualización
    theme = st.selectbox("🎨 Tema de Visualización", 
                        ["default", "ggplot", "seaborn", "fivethirtyeight", "dark_background"])
    
    # Configuración de parámetros de visualización
    st.markdown("### ⚙️ Configuración de Gráficos")
    fig_width = st.slider("Ancho del gráfico", 8, 16, 12)
    fig_height = st.slider("Alto del gráfico", 6, 12, 8)
    
    st.markdown("---")
    st.markdown("### 📋 Información de Sesión")
    st.write(f"**Hora:** {datetime.now().strftime('%H:%M:%S')}")
    st.write(f"**Tema:** {theme}")

# Aplicar tema seleccionado
plt.style.use(theme)

# Función mejorada para detectar separador en archivos de texto
def detectar_separador(contenido):
    """
    Detecta el separador más probable en un archivo de texto
    """
    delimitadores = [',', ';', '\t', '|']
    resultados = {}
    
    # Probar con las primeras 20 líneas
    lineas = contenido.split('\n')[:20]
    lineas_validas = [linea.strip() for linea in lineas if linea.strip() and not linea.strip().startswith('#')]
    
    if not lineas_validas:
        return ','  # Valor por defecto
    
    for delim in delimitadores:
        try:
            # Contar el número de delimitadores en cada línea
            conteos = [linea.count(delim) for linea in lineas_validas]
            
            # Verificar consistencia (todas las líneas deberían tener el mismo número de delimitadores)
            if len(set(conteos)) == 1 and conteos[0] > 0:
                resultados[delim] = conteos[0]
            else:
                # Si no es consistente, usar el promedio
                resultados[delim] = sum(conteos) / len(conteos)
        except:
            resultados[delim] = 0
    
    # Si no encontramos buenos resultados, probar con espacios
    if max(resultados.values()) == 0:
        try:
            conteos_espacios = [len(linea.split()) for linea in lineas_validas]
            if len(set(conteos_espacios)) == 1 and conteos_espacios[0] > 1:
                return ' '
        except:
            pass
    
    mejor_delim = max(resultados, key=resultados.get)
    return mejor_delim if resultados[mejor_delim] > 0 else ','

# Función mejorada para leer archivos de texto con manejo de errores
def leer_archivo_texto(uploaded_file, separador):
    """
    Lee archivos de texto con manejo robusto de errores
    """
    try:
        contenido = uploaded_file.getvalue().decode('utf-8')
        
        # Opciones para pandas.read_csv con manejo de errores
        opciones_lectura = {
            'sep': separador,
            'engine': 'python',
            'on_bad_lines': 'skip',  # Saltar líneas problemáticas
            'quoting': csv.QUOTE_MINIMAL,
            'skipinitialspace': True
        }
        
        # Intentar leer con diferentes enfoques
        try:
            # Intento 1: Lectura normal
            df = pd.read_csv(io.StringIO(contenido), **opciones_lectura)
        except Exception as e:
            st.warning(f"Primer intento falló: {e}. Intentando con enfoque alternativo...")
            
            # Intento 2: Usar error_bad_lines=False (para versiones antiguas de pandas)
            try:
                df = pd.read_csv(io.StringIO(contenido), sep=separador, engine='python', error_bad_lines=False)
            except:
                # Intento 3: Leer manualmente y limpiar
                lineas = contenido.split('\n')
                lineas_limpias = []
                for linea in lineas:
                    if linea.count(separador) == lineas[0].count(separador):
                        lineas_limpias.append(linea)
                
                contenido_limpio = '\n'.join(lineas_limpias)
                df = pd.read_csv(io.StringIO(contenido_limpio), sep=separador)
        
        return df
        
    except Exception as e:
        st.error(f"Error crítico al leer archivo: {e}")
        return None

# Función para analizar la estructura del archivo
def analizar_estructura_archivo(contenido):
    """
    Analiza la estructura del archivo para diagnosticar problemas
    """
    lineas = contenido.split('\n')[:30]  # Analizar primeras 30 líneas
    resultados = {
        'total_lineas': len(lineas),
        'lineas_vacias': 0,
        'lineas_comentario': 0,
        'longitudes_campos': [],
        'problemas_detectados': []
    }
    
    for i, linea in enumerate(lineas):
        if not linea.strip():
            resultados['lineas_vacias'] += 1
            continue
            
        if linea.strip().startswith('#'):
            resultados['lineas_comentario'] += 1
            continue
            
        # Contar campos por línea
        campos = re.split(r'[,;\t|]', linea)
        resultados['longitudes_campos'].append(len(campos))
    
    # Analizar consistencia
    if resultados['longitudes_campos']:
        long_unica = len(set(resultados['longitudes_campos']))
        if long_unica > 1:
            resultados['problemas_detectados'].append(
                f"Inconsistencia en número de campos: {set(resultados['longitudes_campos'])}"
            )
    
    return resultados

# Función para leer archivos .sav (SPSS)
def leer_archivo_sav(uploaded_file):
    try:
        # Leer archivo .sav
        contenido = uploaded_file.read()
        data = readsav(io.BytesIO(contenido))
        
        # Convertir a DataFrame
        df = pd.DataFrame()
        for key, value in data.items():
            if isinstance(value, np.ndarray):
                if len(value.shape) == 1:
                    df[key] = value
                elif len(value.shape) == 2 and value.shape[1] == 1:
                    df[key] = value.flatten()
        
        return df
    except Exception as e:
        st.error(f"Error al leer archivo .sav: {e}")
        return None

# Contenedor principal mejorado
with st.container():
    # Tarjeta de métricas superiores
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 📤 Carga Avanzada de Datos")
    
    # Selector de tipo de archivo
    file_type = st.radio("**Tipo de archivo:**", 
                        ["CSV/Excel", "Texto (TXT)", "SPSS (SAV)", "Datos separados"],
                        horizontal=True)
    
    uploaded_file = None
    
    if file_type == "CSV/Excel":
        uploaded_file = st.file_uploader("**Sube tu archivo CSV o Excel**", 
                                       type=["csv", "xlsx"],
                                       help="Formatos soportados: CSV, Excel")
    
    elif file_type == "Texto (TXT)":
        uploaded_file = st.file_uploader("**Sube tu archivo de texto**", 
                                       type=["txt"],
                                       help="Archivos de texto plano")
        if uploaded_file:
            # Mostrar opciones avanzadas para archivos de texto
            st.markdown("### 🔧 Opciones Avanzadas para Archivos de Texto")
            col1, col2 = st.columns(2)
            with col1:
                separador_manual = st.selectbox("Separador (opcional)", 
                                              ["Auto-detectar", ",", ";", "\t", "|", " "],
                                              help="Puedes especificar manualmente el separador")
            with col2:
                encoding_manual = st.selectbox("Codificación", 
                                             ["utf-8", "latin-1", "iso-8859-1", "windows-1252"],
                                             help="Codificación del archivo")
    
    elif file_type == "SPSS (SAV)":
        uploaded_file = st.file_uploader("**Sube tu archivo SPSS**", 
                                       type=["sav"],
                                       help="Archivos .sav de SPSS")
    
    elif file_type == "Datos separados":
        uploaded_file = st.file_uploader("**Sube tu archivo de datos**", 
                                       type=["dat", "tsv", "data"],
                                       help="Archivos con datos separados")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Procesamiento de archivos cargados
if uploaded_file:
    try:
        df = None
        detalles_archivo = None
        
        if file_type == "CSV/Excel":
            if uploaded_file.name.endswith(".csv"):
                # Para CSV, usar manejo de errores robusto
                try:
                    df = pd.read_csv(uploaded_file, engine='python', on_bad_lines='skip')
                except Exception as e:
                    st.warning(f"Error en lectura CSV: {e}. Intentando con enfoque alternativo...")
                    # Volver a leer el archivo desde el principio
                    uploaded_file.seek(0)
                    contenido = uploaded_file.read().decode('utf-8')
                    separador = detectar_separador(contenido)
                    df = pd.read_csv(io.StringIO(contenido), sep=separador, engine='python', on_bad_lines='skip')
            else:
                df = pd.read_excel(uploaded_file)
                
        elif file_type == "Texto (TXT)":
            contenido = uploaded_file.getvalue().decode('utf-8')
            
            # Mostrar análisis de estructura
            with st.expander("🔍 Análisis de Estructura del Archivo"):
                estructura = analizar_estructura_archivo(contenido)
                st.write("**Diagnóstico del archivo:**")
                st.json(estructura)
                
                if estructura['problemas_detectados']:
                    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                    st.warning("**Problemas detectados en la estructura del archivo:**")
                    for problema in estructura['problemas_detectados']:
                        st.write(f"• {problema}")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Determinar separador
            if separador_manual == "Auto-detectar":
                separador = detectar_separador(contenido)
                st.info(f"🔍 Separador detectado automáticamente: '{separador}'")
            else:
                separador = separador_manual
                st.info(f"🔍 Separador manual seleccionado: '{separador}'")
            
            # Leer archivo con manejo de errores
            df = leer_archivo_texto(uploaded_file, separador)
            if df is None:
                st.error("No se pudo leer el archivo de texto. Por favor, verifica el formato.")
                st.stop()
                
        elif file_type == "SPSS (SAV)":
            df = leer_archivo_sav(uploaded_file)
            if df is None:
                st.error("No se pudo cargar el archivo .sav correctamente")
                st.stop()
                
        elif file_type == "Datos separados":
            contenido = uploaded_file.getvalue().decode('utf-8')
            separador = detectar_separador(contenido)
            st.info(f"🔍 Separador detectado: '{separador}'")
            df = pd.read_csv(io.StringIO(contenido), sep=separador, engine='python', on_bad_lines='skip')
            
        # Verificar si se pudo cargar el DataFrame
        if df is None or df.empty:
            st.error("❌ No se pudo cargar ningún dato del archivo. El archivo puede estar vacío o tener formato incorrecto.")
            st.stop()
            
        # Mostrar éxito en carga
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.success(f"✅ **Archivo cargado exitosamente:** {uploaded_file.name}")
        st.write(f"**Dimensiones:** {df.shape[0]} filas × {df.shape[1]} columnas")
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f"❌ **Error crítico al leer el archivo:** {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Ofrecer soluciones alternativas
        with st.expander("🛠️ Soluciones sugeridas"):
            st.write("""
            **Problemas comunes y soluciones:**
            
            1. **Inconsistencia en número de campos:**
               - Verifica que todas las filas tengan la misma cantidad de columnas
               - Revisa si hay comas o delimitadores adicionales en los datos
               
            2. **Problemas de codificación:**
               - Intenta guardar el archivo con codificación UTF-8
               - Evita caracteres especiales problemáticos
               
            3. **Formato incorrecto:**
               - Asegúrate de que el archivo tenga un formato consistente
               - Verifica que el separador sea el correcto
               
            4. **Archivo corrupto o incompleto:**
               - Intenta abrir el archivo en otro programa primero
               - Verifica que el archivo no esté dañado
            """)
            
            # Opción para cargar con parámetros manuales
            st.write("**O intenta cargar con parámetros manuales:**")
            col1, col2 = st.columns(2)
            with col1:
                separador_emergencia = st.selectbox("Separador de emergencia", [",", ";", "\t", "|"])
            with col2:
                if st.button("Intentar carga manual"):
                    try:
                        uploaded_file.seek(0)
                        contenido = uploaded_file.getvalue().decode('utf-8')
                        df = pd.read_csv(io.StringIO(contenido), sep=separador_emergencia, 
                                       engine='python', error_bad_lines=False)
                        st.success("¡Carga manual exitosa!")
                    except Exception as e2:
                        st.error(f"Error en carga manual: {e2}")
        
        st.stop()

    # [EL RESTO DEL CÓDIGO PERMANECE IGUAL...]
    # Análisis avanzado de tipos de variables
    def analizar_variables(df):
        variables_info = []
        
        for col in df.columns:
            col_info = {
                'nombre': col,
                'tipo_dato': str(df[col].dtype),
                'no_nulos': df[col].notna().sum(),
                'nulos': df[col].isna().sum(),
                'porcentaje_nulos': (df[col].isna().sum() / len(df)) * 100,
                'valores_unicos': df[col].nunique()
            }
            
            # Determinar tipo de variable (cualitativa/cuantitativa)
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info['tipo_variable'] = 'Cuantitativa'
                col_info['subtipo'] = 'Continua' if df[col].nunique() > 20 else 'Discreta'
                col_info['estadisticas'] = {
                    'media': df[col].mean(),
                    'mediana': df[col].median(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max()
                }
            else:
                col_info['tipo_variable'] = 'Cualitativa'
                col_info['subtipo'] = 'Nominal' if df[col].nunique() > 10 else 'Ordinal'
                col_info['categorias_frecuentes'] = df[col].value_counts().head(5).to_dict()
            
            variables_info.append(col_info)
        
        return variables_info

    # Aplicar análisis de variables
    variables_info = analizar_variables(df)
    
    # Métricas rápidas del dataset
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total de Registros", len(df))
    with col2:
        num_cols = len([v for v in variables_info if v['tipo_variable'] == 'Cuantitativa'])
        st.metric("📈 Variables Cuantitativas", num_cols)
    with col3:
        cat_cols = len([v for v in variables_info if v['tipo_variable'] == 'Cualitativa'])
        st.metric("📋 Variables Cualitativas", cat_cols)
    with col4:
        st.metric("🔍 Valores Nulos", df.isnull().sum().sum())

    # Vista previa mejorada con análisis de variables
    with st.expander("🔍 **Análisis Exploratorio Avanzado**", expanded=True):
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Datos", "📊 Estadísticas", "🔍 Estructura", "🎯 Tipos de Variables"])
        
        with tab1:
            st.dataframe(df.head(10), use_container_width=True)
        
        with tab2:
            if not df.select_dtypes(include=["number"]).empty:
                st.write("**Estadísticas Descriptivas:**")
                st.dataframe(df.describe(), use_container_width=True)
            else:
                st.info("No hay variables numéricas para mostrar estadísticas")
        
        with tab3:
            st.write("**Información del Dataset:**")
            buffer = io.StringIO()
            df.info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)
        
        with tab4:
            st.write("**Análisis de Tipos de Variables:**")
            for var in variables_info:
                with st.expander(f"📊 {var['nombre']} - {var['tipo_variable']} ({var['subtipo']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Tipo de dato:** {var['tipo_dato']}")
                        st.write(f"**No nulos:** {var['no_nulos']}")
                        st.write(f"**Nulos:** {var['nulos']} ({var['porcentaje_nulos']:.1f}%)")
                        st.write(f"**Valores únicos:** {var['valores_unicos']}")
                    
                    with col2:
                        if var['tipo_variable'] == 'Cuantitativa':
                            st.write("**Estadísticas:**")
                            for stat, value in var['estadisticas'].items():
                                if pd.notna(value):
                                    st.write(f"- {stat}: {value:.2f}")
                        else:
                            st.write("**Categorías más frecuentes:**")
                            for cat, freq in list(var.get('categorias_frecuentes', {}).items())[:3]:
                                st.write(f"- {cat}: {freq}")

    # Separar variables por tipo
    variables_cuantitativas = [v['nombre'] for v in variables_info if v['tipo_variable'] == 'Cuantitativa']
    variables_cualitativas = [v['nombre'] for v in variables_info if v['tipo_variable'] == 'Cualitativa']

    # Selector de modo mejorado
    st.markdown("---")
    st.markdown("## 🎯 **Selección de Modo de Análisis Inteligente**")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        modo = st.radio("**Tipo de análisis:**", 
                       ["Análisis Univariado", "Análisis Bivariado"],
                       help="Selecciona el tipo de análisis que deseas realizar")
    
    with col2:
        if modo == "Análisis Univariado":
            st.info("🔍 **Análisis de una variable:** Explora distribuciones y características individuales")
        else:
            st.info("🔗 **Análisis de dos variables:** Estudia relaciones entre pares de variables")

    # ==============================
    # ANÁLISIS UNIVARIADO
    # ==============================
    if modo == "Análisis Univariado":
        st.markdown("## 📈 **Análisis Univariado Avanzado**")
        
        # Selector de variable
        tipo_variable = st.radio("**Tipo de variable a analizar:**", 
                                ["Cuantitativa", "Cualitativa"], 
                                horizontal=True)
        
        if tipo_variable == "Cuantitativa" and variables_cuantitativas:
            variable = st.selectbox("**Selecciona variable cuantitativa:**", variables_cuantitativas)
            
            # Gráficos para variables cuantitativas - UN SOLO GRÁFICO
            chart_type = st.selectbox("**Tipo de gráfico:**", 
                                    ["Histograma", 
                                     "Boxplot", 
                                     "Gráfico de Densidad",
                                     "Gráfico de Violín",
                                     "Q-Q Plot"],
                                    help="Selecciona el gráfico más adecuado para tu análisis")
            
            if st.button("🚀 Generar Gráfico", type="primary"):
                with st.spinner("Generando visualización..."):
                    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                    data = df[variable].dropna()
                    
                    if chart_type == "Histograma":
                        # Histograma único con mejoras
                        n_bins = min(30, len(data) // 5)
                        n, bins, patches = ax.hist(data, bins=n_bins, alpha=0.7, color='skyblue', 
                                                 edgecolor='black', density=False)
                        ax.set_title(f'Histograma de {variable}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(variable, fontweight='bold')
                        ax.set_ylabel('Frecuencia', fontweight='bold')
                        ax.grid(True, alpha=0.3)
                        
                        # Añadir línea de densidad
                        from scipy.stats import gaussian_kde
                        kde = gaussian_kde(data)
                        x_vals = np.linspace(data.min(), data.max(), 100)
                        ax2 = ax.twinx()
                        ax2.plot(x_vals, kde(x_vals) * len(data) * (bins[1]-bins[0]), 
                                color='red', linewidth=2, label='Densidad')
                        ax2.set_ylabel('Densidad', fontweight='bold')
                        ax.legend(['Frecuencia'], loc='upper left')
                        ax2.legend(['Densidad'], loc='upper right')
                        
                    elif chart_type == "Boxplot":
                        # Boxplot mejorado
                        boxplot = ax.boxplot(data, vert=True, patch_artist=True, 
                                           boxprops=dict(facecolor='lightblue', color='black'),
                                           medianprops=dict(color='red', linewidth=2),
                                           whiskerprops=dict(color='black'),
                                           capprops=dict(color='black'),
                                           flierprops=dict(marker='o', markersize=4, 
                                                         markerfacecolor='red', alpha=0.5))
                        ax.set_title(f'Boxplot de {variable}', fontweight='bold', fontsize=14)
                        ax.set_ylabel(variable, fontweight='bold')
                        ax.grid(True, alpha=0.3)
                        
                        # Añadir estadísticas en el gráfico
                        stats_text = f"Mediana: {data.median():.2f}\nQ1: {data.quantile(0.25):.2f}\nQ3: {data.quantile(0.75):.2f}"
                        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top',
                               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
                        
                    elif chart_type == "Gráfico de Densidad":
                        # Gráfico de densidad único
                        data.plot.density(ax=ax, color='blue', linewidth=3)
                        ax.set_title(f'Función de Densidad de {variable}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(variable, fontweight='bold')
                        ax.set_ylabel('Densidad', fontweight='bold')
                        ax.fill_betweenx(ax.get_ylim(), data.min(), data.max(), alpha=0.2, color='blue')
                        ax.grid(True, alpha=0.3)
                        
                    elif chart_type == "Gráfico de Violín":
                        # Gráfico de violín simulado
                        from scipy.stats import gaussian_kde
                        kde = gaussian_kde(data)
                        x_vals = np.linspace(data.min(), data.max(), 100)
                        y_vals = kde(x_vals)
                        
                        # Crear efecto de violín
                        ax.fill_betweenx(x_vals, -y_vals/y_vals.max()*0.4, y_vals/y_vals.max()*0.4, 
                                       alpha=0.7, color='lightgreen')
                        ax.plot(y_vals/y_vals.max()*0.4, x_vals, color='green', linewidth=2)
                        ax.plot(-y_vals/y_vals.max()*0.4, x_vals, color='green', linewidth=2)
                        
                        # Añadir boxplot interno
                        q1, med, q3 = data.quantile([0.25, 0.5, 0.75])
                        ax.plot([-0.2, 0.2], [med, med], color='red', linewidth=3)
                        ax.plot([-0.1, 0.1], [q1, q1], color='black', linewidth=2)
                        ax.plot([-0.1, 0.1], [q3, q3], color='black', linewidth=2)
                        ax.plot([0, 0], [q1, q3], color='black', linewidth=2)
                        
                        ax.set_title(f'Gráfico de Violín de {variable}', fontweight='bold', fontsize=14)
                        ax.set_ylabel(variable, fontweight='bold')
                        ax.set_xlabel('Densidad', fontweight='bold')
                        
                    elif chart_type == "Q-Q Plot":
                        # Q-Q Plot para normalidad
                        from scipy.stats import probplot
                        probplot(data, dist="norm", plot=ax)
                        ax.set_title(f'Q-Q Plot de {variable}', fontweight='bold', fontsize=14)
                        ax.grid(True, alpha=0.3)
                        
                        # Añadir línea de referencia
                        ax.plot([data.min(), data.max()], [data.min(), data.max()], 'r--', alpha=0.8)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Estadísticas detalladas
                    with st.expander("📊 **Estadísticas Descriptivas Detalladas**"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write("**Medidas de Tendencia Central:**")
                            st.write(f"Media: {data.mean():.4f}")
                            st.write(f"Mediana: {data.median():.4f}")
                            st.write(f"Moda: {data.mode().iloc[0] if not data.mode().empty else 'N/A'}")
                            
                        with col2:
                            st.write("**Medidas de Dispersión:**")
                            st.write(f"Desviación: {data.std():.4f}")
                            st.write(f"Varianza: {data.var():.4f}")
                            st.write(f"Rango: {data.max() - data.min():.4f}")
                            st.write(f"IQR: {data.quantile(0.75) - data.quantile(0.25):.4f}")
                            
                        with col3:
                            st.write("**Medidas de Forma:**")
                            st.write(f"Sesgo: {data.skew():.4f}")
                            st.write(f"Curtosis: {data.kurtosis():.4f}")
                            st.write(f"Coef. Variación: {(data.std()/data.mean())*100:.2f}%")
        
        elif tipo_variable == "Cualitativa" and variables_cualitativas:
            variable = st.selectbox("**Selecciona variable cualitativa:**", variables_cualitativas)
            
            # Gráficos para variables cualitativas - UN SOLO GRÁFICO
            chart_type = st.selectbox("**Tipo de gráfico:**", 
                                    ["Gráfico de Barras", 
                                     "Gráfico Circular", 
                                     "Gráfico de Anillo",
                                     "Gráfico de Barras Horizontales",
                                     "Gráfico de Waffle"],
                                    help="Selecciona el gráfico más adecuado para tu análisis")
            
            if st.button("🚀 Generar Gráfico", type="primary"):
                with st.spinner("Generando visualización..."):
                    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                    
                    # Calcular frecuencias
                    counts = df[variable].value_counts()
                    percentages = (counts / len(df)) * 100
                    
                    if chart_type == "Gráfico de Barras":
                        # Gráfico de barras verticales mejorado
                        colors = plt.cm.Set3(np.linspace(0, 1, len(counts)))
                        bars = ax.bar(range(len(counts)), counts.values, color=colors, 
                                    edgecolor='black', alpha=0.8)
                        ax.set_title(f'Distribución de {variable}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(variable, fontweight='bold')
                        ax.set_ylabel('Frecuencia', fontweight='bold')
                        ax.set_xticks(range(len(counts)))
                        ax.set_xticklabels(counts.index, rotation=45, ha='right')
                        
                        # Añadir valores en las barras
                        for i, bar in enumerate(bars):
                            height = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                                   f'{int(height)}', ha='center', va='bottom', fontweight='bold')
                        
                        ax.grid(True, alpha=0.3, axis='y')
                        
                    elif chart_type == "Gráfico Circular":
                        # Gráfico circular mejorado
                        colors = plt.cm.Pastel1(np.linspace(0, 1, len(counts)))
                        wedges, texts, autotexts = ax.pie(counts.values, labels=counts.index, 
                                                         autopct='%1.1f%%', startangle=90,
                                                         colors=colors, textprops={'fontsize': 10})
                        
                        ax.set_title(f'Distribución de {variable}', fontweight='bold', fontsize=14)
                        
                        # Mejorar autotextos
                        for autotext in autotexts:
                            autotext.set_color('black')
                            autotext.set_fontweight('bold')
                            
                        # Añadir sombra
                        for wedge in wedges:
                            wedge.set_edgecolor('white')
                            wedge.set_linewidth(1)
                        
                    elif chart_type == "Gráfico de Anillo":
                        # Gráfico de anillo
                        colors = plt.cm.Set2(np.linspace(0, 1, len(counts)))
                        wedges, texts, autotexts = ax.pie(counts.values, labels=counts.index, 
                                                         autopct='%1.1f%%', startangle=90,
                                                         colors=colors, wedgeprops=dict(width=0.3))
                        
                        # Círculo central
                        centre_circle = plt.Circle((0,0), 0.70, fc='white')
                        ax.add_artist(centre_circle)
                        ax.set_title(f'Gráfico de Anillo de {variable}', fontweight='bold', fontsize=14)
                        
                    elif chart_type == "Gráfico de Barras Horizontales":
                        # Barras horizontales
                        colors = plt.cm.viridis(np.linspace(0, 1, len(counts)))
                        bars = ax.barh(range(len(counts)), counts.values, color=colors, 
                                     alpha=0.8, edgecolor='black')
                        ax.set_title(f'Distribución de {variable}', fontweight='bold', fontsize=14)
                        ax.set_xlabel('Frecuencia', fontweight='bold')
                        ax.set_ylabel(variable, fontweight='bold')
                        ax.set_yticks(range(len(counts)))
                        ax.set_yticklabels(counts.index)
                        
                        # Añadir valores
                        for i, bar in enumerate(bars):
                            width = bar.get_width()
                            ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2.,
                                   f'{int(width)}', ha='left', va='center', fontweight='bold')
                        
                        ax.grid(True, alpha=0.3, axis='x')
                        
                    elif chart_type == "Gráfico de Waffle":
                        # Waffle chart simplificado
                        total = counts.sum()
                        square_size = max(1, total // 100)  # Ajustar tamaño según datos
                        
                        # Crear matriz de waffle
                        waffle_data = []
                        for count in counts.values:
                            waffle_data.extend([1] * count + [0] * (total - count))
                        
                        # Tomar solo los necesarios para una visualización cuadrada
                        side = int(np.sqrt(total)) + 1
                        waffle_matrix = np.array(waffle_data[:side*side]).reshape(side, side)
                        
                        im = ax.imshow(waffle_matrix, cmap='Blues', aspect='auto')
                        ax.set_title(f'Waffle Chart de {variable}', fontweight='bold', fontsize=14)
                        ax.axis('off')
                        
                        # Añadir leyenda simple
                        for i, (cat, count) in enumerate(counts.items()):
                            if i < 4:  # Mostrar máximo 4 categorías en leyenda
                                ax.text(side + 1, i, f'{cat}: {count}', va='center')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Resumen categórico detallado
                    with st.expander("📋 **Resumen Categórico Detallado**"):
                        summary_df = pd.DataFrame({
                            'Categoría': counts.index,
                            'Frecuencia': counts.values,
                            'Porcentaje': percentages.values,
                            'Porcentaje Acumulado': percentages.cumsum().values
                        })
                        st.dataframe(summary_df, use_container_width=True)

    # ==============================
    # ANÁLISIS BIVARIADO
    # ==============================
    else:
        st.markdown("## 🔗 **Análisis Bivariado Avanzado**")
        
        # Selector de tipo de análisis bivariado
        tipo_analisis = st.selectbox("**Tipo de relación:**",
                                   ["Cuantitativa vs Cuantitativa",
                                    "Cualitativa vs Cuantitativa", 
                                    "Cualitativa vs Cualitativa"],
                                   help="Selecciona el tipo de variables a relacionar")
        
        if tipo_analisis == "Cuantitativa vs Cuantitativa" and len(variables_cuantitativas) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_var = st.selectbox("Variable X (cuantitativa)", variables_cuantitativas)
            with col2:
                y_var = st.selectbox("Variable Y (cuantitativa)", variables_cuantitativas)
            
            chart_type = st.selectbox("**Tipo de gráfico:**",
                                    ["Gráfico de Dispersión",
                                     "Gráfico de Líneas",
                                     "Gráfico de Área",
                                     "Heatmap 2D"],
                                    help="Selecciona el gráfico para la relación")
            
            if st.button("🚀 Generar Gráfico", type="primary"):
                with st.spinner("Generando visualización bivariada..."):
                    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                    data_x = df[x_var].dropna()
                    data_y = df[y_var].dropna()
                    
                    # Alinear datos eliminando NaN
                    valid_idx = data_x.index.intersection(data_y.index)
                    data_x = data_x.loc[valid_idx]
                    data_y = data_y.loc[valid_idx]
                    
                    if chart_type == "Gráfico de Dispersión":
                        scatter = ax.scatter(data_x, data_y, alpha=0.6, s=50, c='blue', edgecolors='white')
                        ax.set_xlabel(x_var, fontweight='bold')
                        ax.set_ylabel(y_var, fontweight='bold')
                        ax.set_title(f'Dispersión: {y_var} vs {x_var}', fontweight='bold', fontsize=14)
                        
                        # Línea de regresión
                        if len(data_x) > 1:
                            z = np.polyfit(data_x, data_y, 1)
                            p = np.poly1d(z)
                            ax.plot(data_x, p(data_x), "r--", alpha=0.8, linewidth=2, label='Regresión')
                            
                            # Coeficiente de correlación
                            corr = np.corrcoef(data_x, data_y)[0,1]
                            ax.text(0.05, 0.95, f'Correlación: {corr:.3f}', 
                                   transform=ax.transAxes, fontsize=12, fontweight='bold',
                                   bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.8))
                        
                        ax.legend()
                        ax.grid(True, alpha=0.3)
                        
                    elif chart_type == "Gráfico de Líneas":
                        # Ordenar por variable X
                        sorted_idx = data_x.argsort()
                        ax.plot(data_x.iloc[sorted_idx], data_y.iloc[sorted_idx], 
                               marker='o', linewidth=2, markersize=4, color='green')
                        ax.set_xlabel(x_var, fontweight='bold')
                        ax.set_ylabel(y_var, fontweight='bold')
                        ax.set_title(f'Relación: {y_var} vs {x_var}', fontweight='bold', fontsize=14)
                        ax.grid(True, alpha=0.3)
                        
                    elif chart_type == "Gráfico de Área":
                        sorted_idx = data_x.argsort()
                        ax.fill_between(data_x.iloc[sorted_idx], data_y.iloc[sorted_idx], 
                                      alpha=0.4, color='orange')
                        ax.plot(data_x.iloc[sorted_idx], data_y.iloc[sorted_idx], 
                               linewidth=2, color='red')
                        ax.set_xlabel(x_var, fontweight='bold')
                        ax.set_ylabel(y_var, fontweight='bold')
                        ax.set_title(f'Gráfico de Área: {y_var} vs {x_var}', fontweight='bold', fontsize=14)
                        ax.grid(True, alpha=0.3)
                        
                    elif chart_type == "Heatmap 2D":
                        # Crear heatmap 2D de la densidad
                        from scipy.stats import gaussian_kde
                        xy = np.vstack([data_x, data_y])
                        z = gaussian_kde(xy)(xy)
                        
                        scatter = ax.scatter(data_x, data_y, c=z, s=50, cmap='viridis', alpha=0.6)
                        ax.set_xlabel(x_var, fontweight='bold')
                        ax.set_ylabel(y_var, fontweight='bold')
                        ax.set_title(f'Heatmap 2D: {y_var} vs {x_var}', fontweight='bold', fontsize=14)
                        plt.colorbar(scatter, ax=ax, label='Densidad')
                        ax.grid(True, alpha=0.3)
                    
                    plt.tight_layout()
                    st.pyplot(fig)

# Footer moderno mejorado
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <h3>🔬 DataViz Pro Advanced</h3>
    <p><strong>Plataforma Inteligente de Análisis Exploratorio de Datos</strong></p>
    <p>Desarrollado con Streamlit 🚀 | Matplotlib 📊 | Análisis Estadístico Avanzado 📈</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>© 2024 DataViz Pro Advanced - Todos los derechos reservados</p>
</div>
""", unsafe_allow_html=True)