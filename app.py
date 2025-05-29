import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image

# ---- CONFIGURACIÓN DE PÁGINA ----
st.set_page_config(page_title="🔐 Portal de la Fortaleza", page_icon="🛡️", layout="centered")

# ---- ESTILO MEDIEVAL ----
st.markdown("""
    <style>
    body {
        background-color: #fdf6e3;
        color: #3e2f1c;
    }
    .stApp {
        background-image: url('https://i.imgur.com/1ZQZ1Zv.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    h1, h2, h3 {
        color: #5e3929;
        font-family: 'Georgia', serif;
        text-shadow: 1px 1px #decbb7;
    }
    .stButton>button {
        background-color: #5e3929 !important;
        color: #f3e9dc !important;
        border-radius: 10px;
        border: 2px solid #e0c097;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: #fffbe6;
        color: #3e2f1c;
        border: 1px solid #bfa27f;
    }
    </style>
""", unsafe_allow_html=True)

def on_publish(client,userdata,result):           #create function for callback
    print("El dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write("📜 Mensaje recibido:", message_received) # Cambiado para el estilo medieval

broker="broker.hivemq.com"
port=1883
client1= paho.Client("APP_CERR")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker,port)

# Se asume que 'keras_model.h5' está disponible en el entorno donde se ejecuta este código.
# Si no lo tienes, este código no funcionará, ya que el modelo es esencial para la funcionalidad.
# Para evitar errores si el modelo no existe, puedes añadir un bloque try-except.
try:
    from keras.models import load_model
    model = load_model('keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
except ImportError:
    st.error("Error: La librería 'keras' no está instalada. Por favor, instálala usando 'pip install keras'.")
    st.stop() # Detiene la ejecución de Streamlit si keras no está disponible
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}. Asegúrate de que 'keras_model.h5' existe y es un modelo válido.")
    st.stop()

# ---- INTERFAZ ----
st.title("🛡️ Portal Encantado de la Fortaleza")

# ---- IMAGEN DEL DRAGÓN DESDE GITHUB ----
# Asegúrate de reemplazar 'TU_USUARIO' y 'TU_REPO' con los valores correctos de tu repositorio de GitHub.
st.image("https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/dragon.jpeg",
          caption="🐉 Guardián del Portal", use_column_width=True)

st.markdown("### ✨ *Invoca con tu gesto o palabra el poder de abrir o sellar la puerta mágica...*")

# ---- HERRAMIENTA 1: GESTO CON CÁMARA ----
st.subheader("📜 Magia Visual - Sello por Gesto")
img_file_buffer = st.camera_input("📸 Muestra tu gesto sagrado frente al espejo encantado")

if img_file_buffer is not None:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    img_array = np.array(img)

    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    print(prediction) # Mantengo el print para depuración si es necesario.

    if prediction[0][0] > 0.3:
        st.success("🔓 ¡La puerta de roble se abre con tu gesto mágico!")
        client1.publish("PIPPO","{'gesto': 'Abre'}",qos=0, retain=False)
        time.sleep(0.2)
    elif prediction[0][1] > 0.3: # Usamos elif para evitar que ambas condiciones se activen simultáneamente
        st.warning("🔒 ¡El portón se cierra con el poder de tu sello ancestral!")
        client1.publish("PIPPO","{'gesto': 'Cierra'}",qos=0, retain=False)
        time.sleep(0.2)

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
