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
import seaborn as sns  # Para acceder a datasets populares

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
    .dataset-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .dataset-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
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
                        ["default", "ggplot", "fivethirtyeight", "dark_background"])
    
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

# =============================================================================
# FUNCIONES PARA DATASETS POR DEFECTO
# =============================================================================

def cargar_dataset_por_defecto(nombre_dataset):
    """
    Carga datasets populares por defecto
    """
    datasets = {
        'iris': {
            'data': sns.load_dataset('iris'),
            'descripcion': 'Dataset clásico de flores Iris con medidas de sépalos y pétalos',
            'tipo': 'Clasificación',
            'filas': 150,
            'columnas': 5
        },
        'tips': {
            'data': sns.load_dataset('tips'),
            'descripcion': 'Datos de propinas en un restaurante con información de clientes',
            'tipo': 'Regresión/Clasificación',
            'filas': 244,
            'columnas': 7
        },
        'titanic': {
            'data': sns.load_dataset('titanic'),
            'descripcion': 'Información de pasajeros del Titanic y supervivencia',
            'tipo': 'Clasificación',
            'filas': 891,
            'columnas': 15
        },
        'penguins': {
            'data': sns.load_dataset('penguins'),
            'descripcion': 'Medidas corporales de pingüinos en la Antártida',
            'tipo': 'Clasificación',
            'filas': 344,
            'columnas': 7
        },
        'diamonds': {
            'data': sns.load_dataset('diamonds'),
            'descripcion': 'Precios y atributos de 54,000 diamantes',
            'tipo': 'Regresión',
            'filas': 53940,
            'columnas': 10
        },
        'mpg': {
            'data': sns.load_dataset('mpg'),
            'descripcion': 'Datos de consumo de combustible de automóviles',
            'tipo': 'Regresión',
            'filas': 398,
            'columnas': 9
        },
        'planets': {
            'data': sns.load_dataset('planets'),
            'descripcion': 'Datos de exoplanetas descubiertos hasta 2016',
            'tipo': 'Regresión',
            'filas': 1035,
            'columnas': 6
        },
        'flights': {
            'data': sns.load_dataset('flights'),
            'descripcion': 'Número de pasajeros de aerolíneas por mes (1949-1960)',
            'tipo': 'Series de Tiempo',
            'filas': 144,
            'columnas': 3
        },
        'exercise': {
            'data': sns.load_dataset('exercise'),
            'descripcion': 'Datos de ejercicio físico y oxígeno consumido',
            'tipo': 'Experimental',
            'filas': 90,
            'columnas': 5
        },
        'car_crashes': {
            'data': sns.load_dataset('car_crashes'),
            'descripcion': 'Estadísticas de accidentes automovilísticos por estado de EE.UU.',
            'tipo': 'Regresión',
            'filas': 51,
            'columnas': 8
        }
    }
    
    return datasets.get(nombre_dataset, None)

def crear_dataset_sintetico(tipo_datos="Comercial", n_filas=1000):
    """
    Crea un dataset sintético personalizado según el tipo de datos
    """
    np.random.seed(42)
    
    if tipo_datos == "Comercial":
        data = {
            'edad': np.random.normal(35, 10, n_filas).astype(int),
            'ingresos': np.random.normal(50000, 15000, n_filas).astype(int),
            'gasto_mensual': np.random.normal(2000, 500, n_filas),
            'puntuacion_crediticia': np.random.normal(700, 50, n_filas).astype(int),
            'nivel_educacion': np.random.choice(['Bachiller', 'Universitario', 'Maestría', 'Doctorado'], n_filas, p=[0.3, 0.4, 0.2, 0.1]),
            'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], n_filas),
            'compras_online': np.random.poisson(5, n_filas),
            'satisfaccion': np.random.randint(1, 11, n_filas)
        }
        
        # Crear correlaciones para datos comerciales
        data['gasto_mensual'] = data['gasto_mensual'] + data['ingresos'] * 0.001
        data['puntuacion_crediticia'] = np.clip(data['puntuacion_crediticia'] + data['ingresos'] // 1000, 300, 850)
        
    elif tipo_datos == "Financiero":
        data = {
            'edad': np.random.normal(45, 12, n_filas).astype(int),
            'ingresos_anuales': np.random.lognormal(10.5, 0.8, n_filas).astype(int),
            'ahorros': np.random.lognormal(9, 1.2, n_filas).astype(int),
            'deuda_total': np.random.lognormal(8, 1.5, n_filas).astype(int),
            'score_credito': np.random.normal(650, 100, n_filas).astype(int),
            'tipo_inversion': np.random.choice(['Conservadora', 'Moderada', 'Agresiva'], n_filas, p=[0.4, 0.4, 0.2]),
            'nivel_riesgo': np.random.choice(['Bajo', 'Medio', 'Alto'], n_filas, p=[0.5, 0.3, 0.2]),
            'cantidad_inversiones': np.random.poisson(3, n_filas),
            'años_experiencia': np.random.normal(15, 8, n_filas).astype(int)
        }
        
        # Correlaciones financieras
        data['score_credito'] = np.clip(data['score_credito'] + (data['ingresos_anuales'] // 10000), 300, 850)
        data['ahorros'] = data['ahorros'] * (1 + data['ingresos_anuales'] / 100000)
        
    elif tipo_datos == "Salud":
        data = {
            'edad': np.random.normal(40, 15, n_filas).astype(int),
            'peso': np.random.normal(70, 15, n_filas),
            'altura': np.random.normal(170, 10, n_filas),
            'presion_arterial_sistolica': np.random.normal(120, 15, n_filas),
            'presion_arterial_diastolica': np.random.normal(80, 10, n_filas),
            'colesterol': np.random.normal(200, 40, n_filas),
            'nivel_azucar': np.random.normal(100, 20, n_filas),
            'fuma': np.random.choice(['Sí', 'No'], n_filas, p=[0.2, 0.8]),
            'ejercicio_semanal': np.random.choice(['Nada', '1-2 veces', '3-5 veces', 'Diario'], n_filas, p=[0.3, 0.4, 0.2, 0.1]),
            'condicion_salud': np.random.choice(['Excelente', 'Buena', 'Regular', 'Mala'], n_filas, p=[0.2, 0.5, 0.2, 0.1])
        }
        
        # Calcular IMC
        data['imc'] = data['peso'] / ((data['altura'] / 100) ** 2)
        
        # Correlaciones de salud
        data['presion_arterial_sistolica'] = data['presion_arterial_sistolica'] + (data['imc'] - 25) * 0.5
        data['colesterol'] = np.clip(data['colesterol'] + (data['imc'] - 25) * 2, 100, 300)
        
    elif tipo_datos == "Educación":
        data = {
            'edad_estudiante': np.random.normal(20, 5, n_filas).astype(int),
            'nota_promedio': np.random.normal(7.5, 1.5, n_filas),
            'horas_estudio_semana': np.random.normal(15, 8, n_filas),
            'asistencia_clases': np.random.normal(85, 15, n_filas),
            'puntaje_prueba_entrada': np.random.normal(500, 100, n_filas),
            'nivel_educativo': np.random.choice(['Bachillerato', 'Pregrado', 'Posgrado'], n_filas, p=[0.3, 0.5, 0.2]),
            'area_estudio': np.random.choice(['Ciencias', 'Humanidades', 'Ingeniería', 'Artes'], n_filas, p=[0.3, 0.2, 0.4, 0.1]),
            'tipo_institucion': np.random.choice(['Pública', 'Privada'], n_filas, p=[0.6, 0.4]),
            'beca': np.random.choice(['Sí', 'No'], n_filas, p=[0.3, 0.7]),
            'trabaja': np.random.choice(['Sí', 'No'], n_filas, p=[0.4, 0.6])
        }
        
        # Correlaciones educativas
        data['nota_promedio'] = np.clip(data['nota_promedio'] + (data['horas_estudio_semana'] - 15) * 0.05, 0, 10)
        data['nota_promedio'] = np.clip(data['nota_promedio'] + (data['asistencia_clases'] - 85) * 0.01, 0, 10)
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Asegurar que no haya valores negativos en variables que no deberían tenerlos
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            if 'edad' in col or 'años' in col or 'horas' in col:
                df[col] = df[col].clip(lower=0)
            elif 'nota' in col:
                df[col] = df[col].clip(lower=0, upper=10)
            elif 'porcentaje' in col or 'asistencia' in col:
                df[col] = df[col].clip(lower=0, upper=100)
    
    return df

# =============================================================================
# INTERFAZ DE SELECCIÓN DE DATASETS
# =============================================================================

# Inicializar variables en session_state si no existen
if 'df' not in st.session_state:
    st.session_state.df = None
if 'dataset_cargado' not in st.session_state:
    st.session_state.dataset_cargado = None
if 'dataset_info' not in st.session_state:
    st.session_state.dataset_info = None

# Contenedor principal mejorado
with st.container():
    # Tarjeta de métricas superiores
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 📤 Carga Avanzada de Datos")
    
    # Selector de modo de carga
    modo_carga = st.radio("**Selecciona el modo de carga:**", 
                         ["📁 Cargar archivo propio", "🎯 Usar dataset por defecto", "🧪 Generar datos sintéticos"],
                         horizontal=True)
    
    df = None
    uploaded_file = None
    
    if modo_carga == "📁 Cargar archivo propio":
        st.info("📁 **Modo: Cargar archivo propio** - Sube tu archivo CSV, Excel o TXT")
        
        # Selector de tipo de archivo
        file_type = st.radio("**Tipo de archivo:**", 
                            ["CSV/Excel", "Texto (TXT)", "SPSS (SAV)", "Datos separados"],
                            horizontal=True)
        
        if file_type == "CSV/Excel":
            uploaded_file = st.file_uploader("**Sube tu archivo CSV o Excel**", 
                                           type=["csv", "xlsx"],
                                           help="Formatos soportados: CSV, Excel")
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith('.xlsx'):
                        df = pd.read_excel(uploaded_file)
                    st.session_state.df = df
                    st.session_state.dataset_cargado = 'archivo_propio'
                    st.success(f"✅ Archivo {uploaded_file.name} cargado exitosamente!")
                except Exception as e:
                    st.error(f"❌ Error al cargar archivo: {e}")
        


        elif file_type == "Texto (TXT)":
            uploaded_file = st.file_uploader("**Sube tu archivo de texto**", 
                                        type=["txt"],
                                        help="Archivos de texto plano")
            
            if uploaded_file is not None:
                # Función para detección automática
                def detectar_separador_y_cabecera(contenido):
                    """
                    Detecta automáticamente el separador y si hay cabecera
                    """
                    lineas = contenido.split('\n')[:10]  # Analizar primeras 10 líneas
                    lineas = [linea.strip() for linea in lineas if linea.strip()]
                    
                    if len(lineas) < 2:
                        return "Espacio", False  # Por defecto espacio y sin cabecera
                    
                    # Probables separadores
                    separadores = ["\t", ",", ";", "|", " "]
                    mejor_separador = " "
                    mejor_puntaje = 0
                    
                    for sep in separadores:
                        # Contar consistencia en número de columnas
                        num_columnas = []
                        for linea in lineas:
                            partes = linea.split(sep)
                            # Filtrar partes vacías
                            partes_validas = [p for p in partes if p.strip()]
                            num_columnas.append(len(partes_validas))
                        
                        if len(set(num_columnas)) == 1:  # Todas las líneas tienen mismo número de columnas
                            puntaje = len(lineas) * 10
                        else:
                            # Calcular variación
                            if num_columnas:
                                media_cols = np.mean(num_columnas)
                                var_cols = np.std(num_columnas)
                                puntaje = len(lineas) * (10 - min(var_cols, 10))
                            else:
                                puntaje = 0
                        
                        if puntaje > mejor_puntaje:
                            mejor_puntaje = puntaje
                            mejor_separador = sep
                    
                    # Detectar cabecera
                    primera_linea = [p for p in lineas[0].split(mejor_separador) if p.strip()]
                    segunda_linea = [p for p in lineas[1].split(mejor_separador) if p.strip()] if len(lineas) > 1 else []
                    
                    def parece_texto(elementos):
                        textos = 0
                        for elem in elementos:
                            elem_limpio = elem.strip()
                            if not elem_limpio:
                                continue
                            try:
                                float(elem_limpio)
                                # Si puede convertirse a número, probablemente es dato
                            except:
                                textos += 1
                        return textos
                    
                    textos_linea1 = parece_texto(primera_linea) if primera_linea else 0
                    textos_linea2 = parece_texto(segunda_linea) if segunda_linea else 0
                    
                    tiene_cabecera = (textos_linea1 > textos_linea2 * 1.5) if textos_linea2 > 0 else (textos_linea1 > 0)
                    
                    # Mapear separador a nombre
                    sep_nombres = {
                        "\t": "Tab",
                        ",": "Coma", 
                        ";": "Punto y coma",
                        "|": "Pipe",
                        " ": "Espacio"
                    }
                    
                    return sep_nombres.get(mejor_separador, "Espacio"), tiene_cabecera

                # Obtener contenido para detección automática
                contenido_preview = uploaded_file.getvalue().decode("utf-8")
                separador_auto, cabecera_auto = detectar_separador_y_cabecera(contenido_preview)
                
                # Mostrar preview para ayudar al usuario
                with st.expander("🔍 Vista previa de las primeras líneas"):
                    primeras_lineas = contenido_preview.split('\n')[:5]
                    for i, linea in enumerate(primeras_lineas[:3]):
                        if linea.strip():
                            st.text(f"Línea {i+1}: {linea[:100]}{'...' if len(linea) > 100 else ''}")
                
                # Configuración de procesamiento
                col1, col2 = st.columns(2)
                with col1:
                    separador = st.selectbox("Separador", 
                                        ["Espacio", "Tab", "Coma", "Punto y coma", "Pipe"],
                                        index=["Espacio", "Tab", "Coma", "Punto y coma", "Pipe"].index(separador_auto))
                
                with col2:
                    cabecera = st.radio("¿La primera fila es cabecera?",
                                    ["Sí (primera fila son nombres de columnas)", 
                                    "No (primera fila son datos)"],
                                    index=0 if cabecera_auto else 1)
                
                if st.button("📊 Procesar archivo TXT", type="primary"):
                    try:
                        # Reiniciar el archivo para leer desde el inicio
                        uploaded_file.seek(0)
                        content = uploaded_file.getvalue().decode("utf-8")
                        lines = [line.strip() for line in content.split('\n') if line.strip()]
                        
                        # Mapear separadores
                        separadores_dict = {
                            "Espacio": " ",
                            "Tab": "\t", 
                            "Coma": ",",
                            "Punto y coma": ";",
                            "Pipe": "|"
                        }
                        sep_char = separadores_dict[separador]
                        
                        if cabecera == "Sí (primera fila son nombres de columnas)":
                            # Primera línea como cabecera
                            header_line = lines[0]
                            header = [col.strip() for col in header_line.split(sep_char) if col.strip()]
                            data_lines = lines[1:]
                            
                            # Procesar datos
                            data = []
                            for line in data_lines:
                                if line.strip():  # Ignorar líneas vacías
                                    values = [val.strip() for val in line.split(sep_char) if val.strip()]
                                    # Asegurar que tenga el mismo número de columnas que el header
                                    if len(values) == len(header):
                                        data.append(values)
                                    elif len(values) > len(header):
                                        # Tomar solo las primeras columnas que coincidan con el header
                                        data.append(values[:len(header)])
                                    else:
                                        # Rellenar con valores vacíos las columnas faltantes
                                        values_extended = values + [''] * (len(header) - len(values))
                                        data.append(values_extended)
                            
                            df = pd.DataFrame(data, columns=header)
                            
                        else:
                            # Sin cabecera, generar nombres automáticos
                            data = []
                            for line in lines:
                                if line.strip():
                                    values = [val.strip() for val in line.split(sep_char) if val.strip()]
                                    data.append(values)
                            
                            # Determinar número máximo de columnas
                            max_cols = max(len(row) for row in data) if data else 0
                            
                            # Crear nombres de columnas automáticos
                            column_names = [f"Columna_{i+1}" for i in range(max_cols)]
                            
                            # Asegurar que todas las filas tengan el mismo número de columnas
                            data_padded = []
                            for row in data:
                                if len(row) < max_cols:
                                    # Rellenar con valores vacíos
                                    row_extended = row + [''] * (max_cols - len(row))
                                    data_padded.append(row_extended)
                                else:
                                    # Tomar solo las columnas necesarias
                                    data_padded.append(row[:max_cols])
                            
                            df = pd.DataFrame(data_padded, columns=column_names)
                        
                        # Intentar convertir columnas a tipos numéricos cuando sea posible
                        for col in df.columns:
                            # Solo intentar convertir si la columna no está vacía y tiene algunos valores numéricos
                            if not df[col].empty:
                                # Verificar si la columna parece ser numérica
                                valores_numericos = 0
                                total_valores = len(df[col])
                                
                                for valor in df[col]:
                                    if str(valor).strip():  # Si no está vacío
                                        try:
                                            float(str(valor))
                                            valores_numericos += 1
                                        except:
                                            pass
                                
                                # Si más del 70% de los valores son numéricos, convertir la columna
                                if valores_numericos / total_valores > 0.7:
                                    df[col] = pd.to_numeric(df[col], errors='coerce')
                        
                        st.session_state.df = df
                        st.session_state.dataset_cargado = 'archivo_propio'
                        st.success(f"✅ Archivo TXT procesado exitosamente!")
                        st.info(f"📊 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
                        
                        # Mostrar preview del DataFrame resultante
                        with st.expander("🔍 Vista previa del DataFrame procesado"):
                            st.dataframe(df.head(10), use_container_width=True)
                            st.write(f"**Tipos de datos detectados:**")
                            tipos = df.dtypes.astype(str)
                            for col, tipo in tipos.items():
                                st.write(f"- {col}: {tipo}")
                        
                    except Exception as e:
                        st.error(f"❌ Error al procesar archivo TXT: {str(e)}")
                        st.info("💡 **Sugerencias:**")
                        st.info("- Verifica que el separador seleccionado sea correcto")
                        st.info("- Revisa que todas las filas tengan estructura similar")
                        st.info("- Si el archivo tiene formato especial, considera convertirlo a CSV primero")

    
    elif modo_carga == "🎯 Usar dataset por defecto":
        st.info("🎯 **Modo: Dataset por defecto** - Selecciona un dataset popular para analizar")
        
        st.markdown("### 🔥 Datasets Populares Disponibles")
        
        # Organizar datasets en columnas
        col1, col2 = st.columns(2)
        
        datasets_info = {
            'iris': {'emoji': '🌺', 'color': 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'},
            'titanic': {'emoji': '🚢', 'color': 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)'},
            'tips': {'emoji': '💵', 'color': 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'},
            'penguins': {'emoji': '🐧', 'color': 'linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)'},
            'diamonds': {'emoji': '💎', 'color': 'linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)'},
            'mpg': {'emoji': '🚗', 'color': 'linear-gradient(135deg, #fccb90 0%, #d57eeb 100%)'},
            'flights': {'emoji': '✈️', 'color': 'linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)'},
            'planets': {'emoji': '🪐', 'color': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'}
        }
        
        dataset_seleccionado = None
        
        with col1:
            for i, (dataset_name, info) in enumerate(list(datasets_info.items())[:4]):
                if st.button(f"{info['emoji']} {dataset_name.upper()}", 
                           key=f"btn_{dataset_name}",
                           use_container_width=True):
                    dataset_seleccionado = dataset_name
        
        with col2:
            for i, (dataset_name, info) in enumerate(list(datasets_info.items())[4:]):
                if st.button(f"{info['emoji']} {dataset_name.upper()}", 
                           key=f"btn_{dataset_name}",
                           use_container_width=True):
                    dataset_seleccionado = dataset_name
        
        # Cargar dataset seleccionado
        if dataset_seleccionado:
            dataset_info = cargar_dataset_por_defecto(dataset_seleccionado)
            if dataset_info:
                df = dataset_info['data']
                st.session_state.df = df
                st.session_state.dataset_cargado = dataset_seleccionado
                st.session_state.dataset_info = dataset_info
                st.success(f"✅ Dataset {dataset_seleccionado.upper()} cargado exitosamente!")
    
    elif modo_carga == "🧪 Generar datos sintéticos":
        st.info("🧪 **Modo: Datos sintéticos** - Genera un dataset artificial para pruebas")
        
        st.markdown("### 🔬 Dataset Sintético Personalizado")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            n_filas = st.slider("Número de filas", 100, 5000, 1000)
        with col2:
            tipo_datos = st.selectbox("Tipo de datos", ["Comercial", "Financiero", "Salud", "Educación"])
        with col3:
            if st.button("🎲 Generar Dataset", type="primary", use_container_width=True):
                # Pasar el tipo de datos y número de filas a la función
                df = crear_dataset_sintetico(tipo_datos=tipo_datos, n_filas=n_filas)
                
                st.session_state.df = df
                st.session_state.dataset_cargado = 'sintetico'
                st.session_state.dataset_info = {
                    'descripcion': f'Dataset sintético de {tipo_datos.lower()} con {len(df)} registros',
                    'tipo': 'Sintético',
                    'filas': len(df),
                    'columnas': df.shape[1]
                }
                st.success(f"✅ Dataset {tipo_datos} sintético generado exitosamente!")
                st.rerun()  # Esto fuerza la actualización de la interfaz



# =============================================================================
# PROCESAMIENTO DE DATOS Y ANÁLISIS
# =============================================================================

# Usar el DataFrame de session_state
df = st.session_state.df

# Si tenemos un DataFrame cargado
if df is not None and not df.empty:
    # Mostrar información del dataset
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.success(f"✅ **Dataset cargado exitosamente**")
    
    if st.session_state.dataset_cargado == 'archivo_propio':
        st.write(f"**Fuente:** Archivo propio")
    elif st.session_state.dataset_cargado == 'sintetico':
        st.write(f"**Fuente:** Datos sintéticos")
    else:
        st.write(f"**Fuente:** Dataset {st.session_state.dataset_cargado.upper()}")
    
    st.write(f"**Dimensiones:** {df.shape[0]} filas × {df.shape[1]} columnas")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Análisis avanzado de tipos de variables
    # Análisis avanzado de tipos de variables - VERSIÓN MEJORADA
    def analizar_variables(df):
        """
        Analiza variables considerando no solo el tipo de dato sino también
        el significado semántico (variables numéricas que son categóricas)
        """
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
            
            # Detectar si es numérica
            es_numerica = pd.api.types.is_numeric_dtype(df[col])
            
            # Lista de variables comúnmente categóricas aunque sean numéricas
            variables_categoricas_numericas = [
                'survived', 'pclass', 'sex', 'embarked', 'who', 'adult_male',
                'deck', 'embark_town', 'alone', 'class', 'sex_male', 'sex_female',
                'alive', 'sex_female', 'sex_male'
            ]
            
            # Variables con pocos valores únicos (probablemente categóricas)
            pocos_valores_unicos = df[col].nunique() <= 10
            
            # Determinar tipo de variable considerando contexto semántico
            if es_numerica:
                if col.lower() in variables_categoricas_numericas or pocos_valores_unicos:
                    # Es numérica pero categórica
                    col_info['tipo_variable'] = 'Cualitativa'
                    col_info['subtipo'] = 'Binaria' if df[col].nunique() == 2 else 'Ordinal'
                    col_info['categorias_frecuentes'] = df[col].value_counts().head(5).to_dict()
                else:
                    # Es verdaderamente cuantitativa
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
                # Es categórica (string/object)
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
            st.write("**Vista previa de los datos:**")
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
            
            # Gráficos para variables cuantitativas
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
            
            # Gráficos para variables cualitativas
            chart_type = st.selectbox("**Tipo de gráfico:**", 
                                    ["Gráfico de Barras", 
                                     "Gráfico Circular", 
                                     "Gráfico de Anillo",
                                     "Gráfico de Barras Horizontales"],
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

        #else:
            #st.warning("⚠️ No hay variables disponibles del tipo seleccionado")

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
                x_var = st.selectbox("Variable X (cuantitativa)", variables_cuantitativas, key="x_cuant")
            with col2:
                y_var = st.selectbox("Variable Y (cuantitativa)", variables_cuantitativas, key="y_cuant")
            
            chart_type = st.selectbox("**Tipo de gráfico:**",
                                    ["Gráfico de Dispersión",
                                    "Gráfico de Líneas",
                                    "Gráfico de Área"],
                                    help="Selecciona el gráfico para la relación")
            
            if st.button("🚀 Generar Gráfico", type="primary", key="btn_cuant_cuant"):
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
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Análisis estadístico de correlación
                    with st.expander("📊 **Análisis de Correlación**"):
                        if len(data_x) > 1:
                            corr_pearson = np.corrcoef(data_x, data_y)[0,1]
                            from scipy.stats import spearmanr, kendalltau
                            
                            try:
                                corr_spearman = spearmanr(data_x, data_y)[0]
                                corr_kendall = kendalltau(data_x, data_y)[0]
                            except:
                                corr_spearman = "N/A"
                                corr_kendall = "N/A"
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Correlación Pearson", f"{corr_pearson:.4f}")
                            with col2:
                                st.metric("Correlación Spearman", f"{corr_spearman:.4f}" if isinstance(corr_spearman, (int, float)) else "N/A")
                            with col3:
                                st.metric("Correlación Kendall", f"{corr_kendall:.4f}" if isinstance(corr_kendall, (int, float)) else "N/A")
                            
                            # Interpretación
                            st.write("**Interpretación de la correlación:**")
                            abs_corr = abs(corr_pearson)
                            if abs_corr < 0.3:
                                st.info("Correlación débil")
                            elif abs_corr < 0.7:
                                st.info("Correlación moderada")
                            else:
                                st.info("Correlación fuerte")
        
        elif tipo_analisis == "Cualitativa vs Cuantitativa" and variables_cualitativas and variables_cuantitativas:
            col1, col2 = st.columns(2)
            with col1:
                cat_var = st.selectbox("Variable categórica", variables_cualitativas, key="cat_var")
            with col2:
                num_var = st.selectbox("Variable numérica", variables_cuantitativas, key="num_var")
            
            chart_type = st.selectbox("**Tipo de gráfico:**",
                                    ["Boxplot por Categoría",
                                    "Gráfico de Barras",
                                    "Gráfico de Violín",
                                    "Gráfico de Puntos"],
                                    help="Selecciona el gráfico para comparar categorías",
                                    key="chart_cat_cuant")
            
            if st.button("🚀 Generar Gráfico", type="primary", key="btn_cat_cuant"):
                with st.spinner("Generando comparación categórica..."):
                    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                    
                    # Filtrar datos válidos
                    valid_data = df[[cat_var, num_var]].dropna()
                    categorias = valid_data[cat_var].unique()
                    
                    if chart_type == "Boxplot por Categoría":
                        data_to_plot = [valid_data[valid_data[cat_var] == cat][num_var] for cat in categorias]
                        boxplot = ax.boxplot(data_to_plot, labels=categorias, patch_artist=True)
                        
                        # Colorear boxes
                        colors = plt.cm.Set3(np.linspace(0, 1, len(categorias)))
                        for patch, color in zip(boxplot['boxes'], colors):
                            patch.set_facecolor(color)
                        
                        ax.set_title(f'Boxplot de {num_var} por {cat_var}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(cat_var, fontweight='bold')
                        ax.set_ylabel(num_var, fontweight='bold')
                        ax.grid(True, alpha=0.3)
                        
                    elif chart_type == "Gráfico de Barras":
                        medias = valid_data.groupby(cat_var)[num_var].mean()
                        errores = valid_data.groupby(cat_var)[num_var].std()
                        
                        colors = plt.cm.viridis(np.linspace(0, 1, len(medias)))
                        bars = ax.bar(range(len(medias)), medias.values, yerr=errores.values,
                                    capsize=5, color=colors, alpha=0.8, edgecolor='black')
                        
                        ax.set_title(f'Media de {num_var} por {cat_var}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(cat_var, fontweight='bold')
                        ax.set_ylabel(f'Media de {num_var}', fontweight='bold')
                        ax.set_xticks(range(len(medias)))
                        ax.set_xticklabels(medias.index, rotation=45, ha='right')
                        ax.grid(True, alpha=0.3, axis='y')
                        
                    elif chart_type == "Gráfico de Violín":
                        data_to_plot = [valid_data[valid_data[cat_var] == cat][num_var] for cat in categorias]
                        violin = ax.violinplot(data_to_plot, showmeans=True, showmedians=True)
                        
                        ax.set_title(f'Distribución de {num_var} por {cat_var}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(cat_var, fontweight='bold')
                        ax.set_ylabel(num_var, fontweight='bold')
                        ax.set_xticks(range(1, len(categorias) + 1))
                        ax.set_xticklabels(categorias, rotation=45, ha='right')
                        ax.grid(True, alpha=0.3)
                        
                    elif chart_type == "Gráfico de Puntos":
                        for i, cat in enumerate(categorias):
                            cat_data = valid_data[valid_data[cat_var] == cat][num_var]
                            y_vals = np.random.normal(i + 1, 0.04, size=len(cat_data))
                            ax.scatter(cat_data, y_vals, alpha=0.6, s=50, label=cat)
                        
                        ax.set_title(f'Distribución de Puntos de {num_var} por {cat_var}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(num_var, fontweight='bold')
                        ax.set_ylabel(cat_var, fontweight='bold')
                        ax.set_yticks(range(1, len(categorias) + 1))
                        ax.set_yticklabels(categorias)
                        ax.legend()
                        ax.grid(True, alpha=0.3)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Análisis estadístico por categoría
                    with st.expander("📊 **Estadísticas por Categoría**"):
                        stats_by_cat = valid_data.groupby(cat_var)[num_var].agg(['count', 'mean', 'median', 'std', 'min', 'max']).round(4)
                        st.dataframe(stats_by_cat, use_container_width=True)
        
        elif tipo_analisis == "Cualitativa vs Cualitativa" and len(variables_cualitativas) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                var1 = st.selectbox("Variable 1 (categórica)", variables_cualitativas, key="var1")
            with col2:
                var2 = st.selectbox("Variable 2 (categórica)", variables_cualitativas, key="var2")
            
            chart_type = st.selectbox("**Tipo de gráfico:**",
                                    ["Tabla de Contingencia",
                                    "Gráfico de Barras Agrupadas",
                                    "Heatmap de Frecuencias",
                                    "Gráfico de Mosaico"],
                                    help="Selecciona el gráfico para relaciones categóricas",
                                    key="chart_cat_cat")
            
            if st.button("🚀 Generar Análisis", type="primary", key="btn_cat_cat"):
                with st.spinner("Analizando relación categórica..."):
                    # Tabla de contingencia
                    contingency_table = pd.crosstab(df[var1], df[var2])
                    
                    if chart_type == "Tabla de Contingencia":
                        st.write("**Tabla de Contingencia:**")
                        st.dataframe(contingency_table, use_container_width=True)
                        
                        # Porcentajes
                        st.write("**Porcentajes por Fila:**")
                        st.dataframe((contingency_table.div(contingency_table.sum(axis=1), axis=0) * 100).round(2), 
                                use_container_width=True)
                    
                    elif chart_type == "Gráfico de Barras Agrupadas":
                        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                        
                        contingency_table.plot(kind='bar', ax=ax, alpha=0.8)
                        ax.set_title(f'Relación entre {var1} y {var2}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(var1, fontweight='bold')
                        ax.set_ylabel('Frecuencia', fontweight='bold')
                        ax.legend(title=var2)
                        ax.grid(True, alpha=0.3)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    elif chart_type == "Heatmap de Frecuencias":
                        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                        
                        im = ax.imshow(contingency_table.values, cmap='YlOrRd', aspect='auto')
                        ax.set_title(f'Heatmap: {var1} vs {var2}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(var2, fontweight='bold')
                        ax.set_ylabel(var1, fontweight='bold')
                        ax.set_xticks(range(len(contingency_table.columns)))
                        ax.set_yticks(range(len(contingency_table.index)))
                        ax.set_xticklabels(contingency_table.columns, rotation=45, ha='right')
                        ax.set_yticklabels(contingency_table.index)
                        
                        # Añadir valores en las celdas
                        for i in range(len(contingency_table.index)):
                            for j in range(len(contingency_table.columns)):
                                ax.text(j, i, f'{contingency_table.iloc[i, j]}', 
                                    ha="center", va="center", color="black", fontweight='bold')
                        
                        plt.colorbar(im, ax=ax, label='Frecuencia')
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    elif chart_type == "Gráfico de Mosaico":
                        # Gráfico de mosaico simplificado usando barras apiladas
                        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                        
                        contingency_table_percent = contingency_table.div(contingency_table.sum(axis=1), axis=0)
                        
                        bottom_vals = np.zeros(len(contingency_table_percent))
                        colors = plt.cm.Set3(np.linspace(0, 1, len(contingency_table_percent.columns)))
                        
                        for i, col in enumerate(contingency_table_percent.columns):
                            ax.bar(range(len(contingency_table_percent)), 
                                contingency_table_percent[col], 
                                bottom=bottom_vals, 
                                label=col, 
                                color=colors[i],
                                alpha=0.8)
                            bottom_vals += contingency_table_percent[col].values
                        
                        ax.set_title(f'Gráfico de Mosaico: {var1} vs {var2}', fontweight='bold', fontsize=14)
                        ax.set_xlabel(var1, fontweight='bold')
                        ax.set_ylabel('Proporción', fontweight='bold')
                        ax.set_xticks(range(len(contingency_table_percent)))
                        ax.set_xticklabels(contingency_table_percent.index, rotation=45, ha='right')
                        ax.legend(title=var2, bbox_to_anchor=(1.05, 1), loc='upper left')
                        ax.grid(True, alpha=0.3, axis='y')
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    # Prueba de independencia Chi-cuadrado
                    with st.expander("📊 **Prueba de Independencia Chi-Cuadrado**"):
                        from scipy.stats import chi2_contingency
                        
                        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Chi-cuadrado", f"{chi2:.4f}")
                        with col2:
                            st.metric("Valor p", f"{p_value:.4f}")
                        with col3:
                            st.metric("Grados Libertad", dof)
                        
                        # Interpretación
                        st.write("**Interpretación:**")
                        if p_value < 0.05:
                            st.success("✅ **Existe relación significativa** entre las variables (p < 0.05)")
                        else:
                            st.info("❌ **No existe relación significativa** entre las variables (p ≥ 0.05)")
        
        else:
            if tipo_analisis == "Cuantitativa vs Cuantitativa":
                st.warning(f"⚠️ **Se necesitan al menos 2 variables cuantitativas. Disponibles: {len(variables_cuantitativas)}**")
            elif tipo_analisis == "Cualitativa vs Cuantitativa":
                st.warning(f"⚠️ **Se necesita al menos 1 variable cualitativa y 1 cuantitativa. Disponibles: Cualitativas={len(variables_cualitativas)}, Cuantitativas={len(variables_cuantitativas)}**")
            elif tipo_analisis == "Cualitativa vs Cualitativa":
                st.warning(f"⚠️ **Se necesitan al menos 2 variables cualitativas. Disponibles: {len(variables_cualitativas)}**")

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

