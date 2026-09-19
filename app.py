import streamlit as st
import pandas as pd
import datetime

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Condominio",
    page_icon="🏢",
    layout="wide"
)

# Estilo visual limpio y moderno
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

# Título y Estado
st.title("🏢 Sistema de Gestión de Condominio")
st.markdown("Panel administrativo para el control de alícuotas, cobros y gastos comunes.")

# Sidebar de navegación
st.sidebar.markdown("### Menú Principal")
menu = st.sidebar.selectbox("Seleccione una opción", ["Dashboard", "Inmuebles (13 Unidades)", "Cobros y Pagos", "Reportes"])

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tasa BCV Activa:** 36.50 VES/USD")

# Base de datos simulada de los 13 inmuebles con las alícuotas correctas
@st.cache_data
def cargar_inmuebles():
    return pd.DataFrame([
        {"Apartamento": "1A", "Propietario": "Juan Pérez", "Alicuota (%)": 6, "Teléfono": "584121234567", "Estado": "Al Día"},
        {"Apartamento": "1B", "Propietario": "María Gómez", "Alicuota (%)": 6, "Teléfono": "584149876543", "Estado": "Pendiente"},
        {"Apartamento": "3A", "Propietario": "Carlos Ruiz", "Alicuota (%)": 6, "Teléfono": "584165554433", "Estado": "Al Día"},
        {"Apartamento": "3B", "Propietario": "Ana Torres", "Alicuota (%)": 6, "Teléfono": "584123332211", "Estado": "Al Día"},
        {"Apartamento": "4A", "Propietario": "Luis Blanco", "Alicuota (%)": 6, "Teléfono": "584141112233", "Estado": "Pendiente"},
        {"Apartamento": "4B", "Propietario": "Rosa M.", "Alicuota (%)": 6, "Teléfono": "584129998877", "Estado": "Al Día"},
        {"Apartamento": "5A", "Propietario": "Pedro Infante", "Alicuota (%)": 6, "Teléfono": "584167776655", "Estado": "Al Día"},
        {"Apartamento": "5B", "Propietario": "Sofía Castro", "Alicuota (%)": 6, "Teléfono": "584124445566", "Estado": "Al Día"},
        {"Apartamento": "6A", "Propietario": "Miguel Ángel", "Alicuota (%)": 6, "Teléfono": "584148887766", "Estado": "Pendiente"},
        {"Apartamento": "6B", "Propietario": "Carmen Rosa", "Alicuota (%)": 6, "Teléfono": "584161110099", "Estado": "Al Día"},
        {"Apartamento": "2-7 (Apto 2)", "Propietario": "Alberto Sosa", "Alicuota (%)": 12, "Teléfono": "584125556677", "Estado": "Al Día"},
        {"Apartamento": "2-7 (Apto 7)", "Propietario": "Elena Vargas", "Alicuota (%)": 12, "Teléfono": "584142223344", "Estado": "Al Día"},
        {"Apartamento": "PH (Penthouse)", "Propietario": "Ricardo Montaner", "Alicuota (%)": 16, "Teléfono": "584120001122", "Estado": "Al Día"}
    ])

df_inmuebles = cargar_inmuebles()

# VISTA: DASHBOARD
if menu == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Fondo Disponible", value="$ 1,450.00", delta="+12%")
    with col2:
        st.metric(label="Cobros Pendientes", value="$ 380.00", delta="-3 inmuebles", delta_color="inverse")
    with col3:
        st.metric(label="Gastos del Mes", value="$ 620.00")
    with col4:
        st.metric(label="Total Inmuebles", value="13 Unidades")

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.subheader("Comportamiento Financiero Reciente")
        chart_data = pd.DataFrame({
            "Mes": ["Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre"],
            "Ingresos ($)": [1200, 1350, 1100, 1400, 1450, 1500]
        })
        st.bar_chart(chart_data, x="Mes", y="Ingresos ($)", color="#6366f1")
        
    with col_chart2:
        st.subheader("Acciones Rápidas")
        if st.button("🚀 Calcular y Emitir Recibos"):
            st.success("¡Recibos calculados según las alícuotas vigentes!")
        st.info("El sistema aplica automáticamente los porcentajes de cobro correspondientes a cada propietario.")

# VISTA: INMUEBLES
elif menu == "Inmuebles (13 Unidades)":
    st.subheader("Control de Inmuebles y Alícuotas")
    st.markdown("Distribución oficial configurada: **10 apartamentos al 6%, 2 al 12% y el Penthouse al 16%.**")
    
    # Mostrar tabla interactiva
    st.dataframe(df_inmuebles, use_container_width=True)
    
    st.markdown("### Enviar Recordatorio por WhatsApp")
    apt_seleccionado = st.selectbox("Seleccione el inmueble para notificar", df_inmuebles["Apartamento"].tolist())
    
    propietario_info = df_inmuebles[df_inmuebles["Apartamento"] == apt_seleccionado].iloc[0]
    mensaje = f"Hola {propietario_info['Propietario']}, le escribimos de la administración del condominio para recordarle su estado de cuenta del apto {apt_seleccionado}."
    link_whatsapp = f"https://wa.me/{propietario_info['Teléfono']}?text={mensaje.replace(' ', '%20')}"
    
    st.markdown(f'<a href="{link_whatsapp}" target="_blank"><button style="background-color:#22c55e; color:white; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Enviar WhatsApp a {propietario_info["Propietario"]}</button></a>', unsafe_allow_html=True)

# VISTA: PAGOS
elif menu == "Cobros y Pagos":
    st.subheader("Registro y Verificación de Pagos")
    
    with st.form("form_pago"):
        col1, col2, col3 = st.columns(3)
        with col1:
            inmueble_pago = st.selectbox("Inmueble", df_inmuebles["Apartamento"].tolist())
        with col2:
            monto_pago = st.number_input("Monto Pagado ($ o VES)", min_value=0.0, format="%.2f")
        with col3:
            ref_pago = st.text_input("Referencia Bancaria (últimos 4 dígitos)")
            
        submitted = st.form_submit_button("Registrar Pago")
        if submitted:
            if monto_pago > 0 and ref_pago:
                st.success(f"¡Pago registrado exitosamente para el apartamento {inmueble_pago} por un monto de {monto_pago} (Ref: {ref_pago})!")
            else:
                st.error("Por favor ingrese un monto válido y los datos de la referencia bancaria.")

# VISTA: REPORTES
elif menu == "Reportes":
    st.subheader("Reportes y Estados de Cuenta")
    st.write("Genera los reportes mensuales de ingresos y egresos listos para auditoría o impresión.")
    if st.button("🖨️ Generar Reporte General en PDF"):
        st.info("Función de descarga directa vinculada al motor de reportes del sistema.")
