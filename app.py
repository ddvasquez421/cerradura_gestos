import paho.mqtt.client as paho
import time
import streamlit as st
import numpy as np
from PIL import Image
from keras.models import load_model

# ---- CONFIGURACIÓN DE PÁGINA ----
st.set_page_config(page_title="🔐 Portal de la Fortaleza", page_icon="🛡️", layout="centered")

# ---- ESTILO MEDIEVAL ----
st.markdown("""
    <style>
    /* El cuerpo del documento (no siempre visible directamente en Streamlit) */
    body {
        background-color: #fdf6e3; /* Color de fallback */
        color: #3e2f1c; /* Color de texto general */
    }

    /* El contenedor principal de Streamlit donde se renderiza toda la aplicación */
    .stApp {
        background-image: url('https://raw.githubusercontent.com/ddvasquez421/cerradura_gestos/main/dragon.jpg'); /* URL CORRECTA de tu imagen de dragón */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Ocultar la cabecera predeterminada de Streamlit, que a menudo se superpone */
    .stApp > header {
        display: none;
    }

    /* EL RECUADRO NEGRO SEMITRANSPARENTE */
    /* Este selector apunta al div que Streamlit usa para envolver el contenido principal.
       Puede ser susceptible a cambios en futuras versiones de Streamlit,
       pero es la forma más efectiva de lograrlo ahora. */
    .stApp > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) {
        background-color: rgba(0, 0, 0, 0.6); /* Negro semitransparente (0.6 de opacidad) */
        padding: 2em; /* Espaciado interno */
        border-radius: 10px; /* Bordes redondeados */
        margin: 2em auto; /* Centrar horizontalmente y dar margen superior/inferior */
        max-width: 800px; /* Ancho máximo del recuadro para centrar mejor */
        box-shadow: 0 0 25px rgba(0, 0, 0, 0.8); /* Sombra para profundidad */
        border: 2px solid #5e3929; /* Borde sutil para el recuadro */
    }

    /* Ajustes para los títulos y subtítulos (para que se vean sobre el negro) */
    h1, h2, h3 {
        color: #FFD700; /* Oro para los títulos */
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px 4px #000000; /* Sombra más pronunciada para legibilidad */
        text-align: center; /* Centrar títulos */
    }

    /* Estilos generales para el texto dentro del recuadro */
    p, label, .stMarkdown {
        color: #f3e9dc; /* Blanco crema para el texto normal */
    }

    /* Ajustes específicos para los elementos de entrada y botones */
    .stButton>button {
        background-color: #A52A2A !important; /* Rojo oscuro medieval para botones */
        color: #f3e9dc !important; /* Texto blanco en el botón */
        border-radius: 10px;
        border: 2px solid #8B0000; /* Borde más oscuro */
        font-weight: bold;
        transition: background-color 0.3s ease; /* Transición suave al pasar el mouse */
    }
    .stButton>button:hover {
        background-color: #8B0000 !important; /* Color más oscuro al pasar el mouse */
        border-color: #FF4500; /* Borde brillante al pasar el mouse */
    }

    /* Input de texto */
    .stTextInput > div > div > input {
        background-color: rgba(60, 60, 60, 0.7); /* Fondo más oscuro y semitransparente para inputs */
        color: #f3e9dc; /* Texto blanco crema */
        border: 2px solid #8B4513; /* Borde marrón para el pergamino */
        border-radius: 5px;
        padding: 0.5em;
    }

    /* Camera Input (puede que necesite un selector más específico si hay conflictos) */
    .stCameraInput > div:first-child {
        background-color: rgba(60, 60, 60, 0.7); /* Fondo semitransparente para la cámara */
        border: 2px solid #8B4513;
        border-radius: 5px;
        padding: 1em; /* Espaciado dentro del recuadro de la cámara */
    }

    /* Mensajes de éxito/advertencia/error */
    .stSuccess > div {
        background-color: rgba(34, 139, 34, 0.7) !important; /* Verde bosque semi-transparente */
        color: white !important;
        border: 2px solid #228B22 !important;
        border-radius: 8px;
        padding: 1em;
        margin-top: 1em;
    }
    .stWarning > div {
        background-color: rgba(255, 140, 0, 0.7) !important; /* Naranja oscuro semi-transparente */
        color: white !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 8px;
        padding: 1em;
        margin-top: 1em;
    }
    .stError > div {
        background-color: rgba(178, 34, 34, 0.7) !important; /* Rojo fuego semi-transparente */
        color: white !important;
        border: 2px solid #B22222 !important;
        border-radius: 8px;
        padding: 1em;
        margin-top: 1em;
    }

    /* Leyendas de las imágenes y otros textos descriptivos */
    .stImage > figcaption {
        color: #f3e9dc; /* Color para la leyenda de la imagen */
        text-align: center;
        margin-top: 0.5em;
    }
    </style>
""", unsafe_allow_html=True)

# ---- MQTT ----
def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")
    pass

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.write("📜 Mensaje recibido:", message_received)

broker = "broker.hivemq.com"
port = 1883
client1 = paho.Client("APP_yyyyy")
client1.on_message = on_message
client1.on_publish = on_publish
try:
    client1.connect(broker, port)
    st.success("✨ *Conexión con el Reino Etéreo (MQTT Broker) establecida.*")
except Exception as e:
    st.error(f"💀 *Fracaso al conectar con el Reino Etéreo: {e}. Asegúrate de que los hilos del destino estén entrelazados correctamente.*")

# ---- CARGA DEL MODELO ----
try:
    model = load_model('keras_model.h5')
    st.success("📚 *El tomo de conocimiento arcaico (modelo) ha sido desenterrado y su sabiduría, cargada.*")
except Exception as e:
    st.error(f"🔥 *No se pudo invocar el tomo de conocimiento (modelo): {e}. ¿Acaso las runas no están en su lugar?*")

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# ---- INTERFAZ ----
st.title("🛡️ Portal Encantado de la Fortaleza")

# ---- IMAGEN DEL DRAGÓN DESDE GITHUB ----
# Asegúrate de que esta URL sea la 'Raw' de tu imagen en GitHub
st.image("https://raw.githubusercontent.com/ddvasquez421/cerradura_gestos/main/dragon.jpg", # Reemplazado a .jpg
          caption="🐉 Guardián del Portal", use_column_width=True)

st.markdown("### ✨ *Invoca con tu gesto o palabra el poder de abrir o sellar la puerta mágica...*")

# ---- HERRAMIENTA 1: GESTO CON CÁMARA ----
st.subheader("📜 Magia Visual - Sello por Gesto")
img_file_buffer = st.camera_input("📸 Muestra tu gesto sagrado frente al espejo encantado")

if img_file_buffer is not None:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    img = Image.open(img_file_buffer)
    img = img.resize((224, 224))
    img_array = np.array(img)
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)

    if prediction[0][0] > 0.3:
        st.success("🔓 ¡La puerta de roble se abre con tu gesto mágico!")
        client1.publish("PIPPO", "{'gesto': 'Abre'}", qos=0, retain=False)
    elif prediction[0][1] > 0.3:
        st.warning("🔒 ¡El portón se cierra con el poder de tu sello ancestral!")
        client1.publish("PIPPO", "{'gesto': 'Cierra'}", qos=0, retain=False)
    else:
        st.info("🤷‍♀️ *El Oráculo no pudo discernir tu intención. Intenta de nuevo.*") # Agregado para cuando no hay prediccion clara

# ---- HERRAMIENTA 2: COMANDO ESCRITO ----
st.subheader("📖 Hechizo Escrito - Sello por Palabra")
user_command = st.text_input("✍️ Escribe 'abrir' o 'cerrar' como si fueran conjuros").strip().lower()

if st.button("🔮 Invocar Hechizo"):
    if user_command == "abrir":
        st.success("🔓 ¡Hechizo aceptado! La entrada se abre ante ti.")
        client1.publish("PIPPO", "{'gesto': 'Abre'}", qos=0, retain=False)
    elif user_command == "cerrar":
        st.warning("🔒 ¡Puerta cerrada! El conjuro ha sido sellado.")
        client1.publish("PIPPO", "{'gesto': 'Cierra'}", qos=0, retain=False)
    else:
        st.error("🚫 Palabra no reconocida por los grimorios. Usa 'abrir' o 'cerrar'.")
