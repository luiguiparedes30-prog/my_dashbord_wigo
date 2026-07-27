import streamlit as st
from conexion import cargar_datos
from indicadores import *
from graficos import *
# ==========================
# AUTENTICACIÓN
# ==========================

USUARIOS = {
    "admin": "123456",
    "profesor": "wigo2025"
}

if "logueado" not in st.session_state:
    st.session_state.logueado = False

def login():
    st.title("🔐 Inicio de sesión")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario in USUARIOS and USUARIOS[usuario] == password:
            st.session_state.logueado = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

if not st.session_state.logueado:
    login()
    st.stop()
df = cargar_datos()

# CONFIGURACIÓN DE DASHBOARD CON STREAMLIT:


st.set_page_config(page_title = "Wigo Motors", 
                   layout="wide")      


st.markdown(
    """
    <h1 style='text-align:center; color:#0E4C92;'>
    🚗 WIGO MOTORS S.A.C.
    </h1>
    <h3 style='text-align:center; color:gray;'>
    Dashboard Comercial
    </h3>
    <hr>
    """,
    unsafe_allow_html=True
)

st.info("📊 Bienvenido al panel de control comercial de Wigo Motors.")

st.sidebar.title("🚗 WIGO MOTORS")
st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Buscador")
tipo_busqueda = st.sidebar.selectbox("Seleccione tipo de búsqueda", ["Marca", "Asesor comercial", "Sede"])  


df_filtrado = df.copy()     # Haciendo una copia del DataFrame 



# FILTRO POR MARCA:


if tipo_busqueda == "Marca":
    valor = st.sidebar.selectbox("Seleccionar marca", df["marca"].unique()) # Mostrar las marcas disponibles y sin repetir
    df_filtrado = df[df["marca"] == valor]                                   # Filtrar búsqueda por marca  
    
elif tipo_busqueda == "Asesor comercial":
    valor = st.sidebar.selectbox("Seleccionar asesor", df["asesor_comercial"].unique()) # Mostrar las marcas disponibles y sin repetir
    df_filtrado = df[df["asesor_comercial"] == valor]                                   # Filtrar búsqueda por marca  
    
elif tipo_busqueda == "Sede":
    valor = st.sidebar.selectbox("Seleccionar sede", df["tienda"].unique()) # Mostrar las marcas disponibles y sin repetir
    df_filtrado = df[df["tienda"] == valor]                                   # Filtrar búsqueda por marca  
    


# MOSTRAR RESULTADOS:


st.success(f"Registros encontrados: {len(df_filtrado)}")        # Mostrar la cantidad de filas encontradas (color verde)
st.markdown("### 📋 Resultados encontrados")
st.dataframe(df_filtrado, use_container_width=True)

# INDICADORES GENERALES: 


st.subheader("Indicadores:")


c1, c2, c3, c4 = st.columns(4)          # CREANDO 4 COLUMNAS  


c1.metric("💰 Ventas Totales", f"S/{precio_total(df_filtrado):,.2f}")

c2.metric("🚘 Unidades", unidades_vendidas(df_filtrado))

c3.metric("📈 Precio Promedio", f"S/{precio_promedio(df_filtrado):,.2f}")

c4.metric("📄 Operaciones", operaciones(df_filtrado))

c5.metric("🔺 Precio Máximo", f"S/{df_filtrado['precio_venta'].max():,.2f}")

c6.metric("🔻 Precio Mínimo", f"S/{df_filtrado['precio_venta'].min():,.2f}")

st.markdown("## 📈 Ventas por Marca")
st.plotly_chart(grafico_ventas(df_filtrado), use_container_width=True)

st.markdown("## 📊 Precio Promedio")
st.plotly_chart(grafico_promedio(df_filtrado), use_container_width=True)

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Cerrar sesión"):
    st.session_state.logueado = False
    st.rerun()

st.markdown("---")
st.markdown(
    "<center><b>WIGO MOTORS S.A.C.</b><br>Dashboard Comercial - 2025</center>",
    unsafe_allow_html=True
)
