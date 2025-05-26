import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="HeartLeaves AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para enviar los datos a la API y obtener la predicción
def predict_with_api(troponin, ck_mb, age):
    url = "https://flask-api-model.onrender.com/predict"  # Cambia esta URL si tu API está desplegada en un servidor
    payload = {
        "Troponin": troponin,
        "CK-MB": ck_mb,
        "Age": age
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Error al contactar la API: {e}")
        return None

def main():
    # Cabecera con logos y título
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.image("Escudo_UAZ.png", width=100)
    with col2:
        st.title("HeartLeaves AI - Predictor de Infarto con Inteligencia Artificial")
        st.caption("Herramienta de apoyo clínico basada en aprendizaje automático")
    with col3:
        st.image("logo2.png", width=100)

    st.markdown("---")

    # Entrada de datos
    with st.container():
        st.header("📊 Datos del Paciente")
        st.write("Ingrese los valores biomarcadores y la edad del paciente:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            troponin = st.number_input(
                "Nivel de Troponina (ng/mL)", min_value=0.0, max_value=100.0,
                value=0.01, step=0.01, help="Valor normal típico: <0.04 ng/mL"
            )
        with col2:
            ck_mb = st.number_input(
                "Nivel de CK-MB (U/L)", min_value=0.0, max_value=1000.0,
                value=5.0, step=0.1, help="Valor normal típico: <5 U/L"
            )
        with col3:
            age = st.number_input(
                "Edad del Paciente", min_value=18, max_value=120,
                value=50, help="Edad en años completos"
            )

    # Botón de predicción
    st.markdown("---")
    if st.button("🔍 Calcular Riesgo de Infarto", use_container_width=True):
        with st.spinner("Consultando modelo..."):
            result = predict_with_api(troponin, ck_mb, age)
            if result:
                pred = result["prediction"]
                prob = float(result.get("probability", 0.0))

                st.subheader("📋 Resultados de la Predicción")
                if pred == 1:
                    st.error("**Predicción:** Riesgo de Infarto detectado")
                else:
                    st.success("**Predicción:** Sin evidencia de infarto")

                st.write(f"**Probabilidad de Infarto:** {prob*100:.2f}%")
                st.progress(prob)

                # Interpretación clínica
                st.markdown("---")
                st.subheader("📝 Interpretación Clínica")
                if prob < 0.2:
                    st.info("**Bajo riesgo:** Considerar otras causas de los síntomas.")
                elif prob < 0.5:
                    st.warning("**Riesgo moderado:** Monitoreo continuo y posible repetición de pruebas.")
                else:
                    st.error("**Alto riesgo:** Requiere intervención inmediata y evaluación cardiológica.")

                st.markdown("---")
                st.warning("""
                **Nota importante:**  
                Este resultado es una predicción automatizada y no debe ser considerado como diagnóstico médico definitivo. 
                Siempre debe ser interpretado por un profesional de la salud calificado.
                """)

# Información adicional en la barra lateral
with st.sidebar:
    st.header("ℹ️ Acerca de esta herramienta")
    st.write("""
    Este predictor utiliza un modelo de Random Forest entrenado con datos clínicos 
    para estimar el riesgo de infarto cardíaco basado en:
    - Nivel de Troponina
    - Nivel de CK-MB
    - Edad del paciente
    """)
    
    st.markdown("---")
    st.subheader("📈 Rangos de Referencia")
    st.write("""
    **Troponina:**
    - Normal: <0.04 ng/mL
    - Elevación leve: 0.04–0.39 ng/mL
    - Elevación significativa: ≥0.4 ng/mL

    **CK-MB:**
    - Normal: <5 U/L
    - Elevado: ≥5 U/L
    """)
    
    st.markdown("---")
    st.write("Desarrollado por: Jesús Alejandro Montes Medina")
    st.caption("Maestría en Ciencias del Procesamiento de la Información | Universidad Autónoma de Zacatecas")

if __name__ == "__main__":
    main()
