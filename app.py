import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps
from keras.models import load_model

# --- CSS para la estetica medieval y la imagen de fondo ---
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/ddvasquez421/cerradura_gestos/main/dragon.jpg"); /* ¡Asegúrate de reemplazar con la URL correcta de tu imagen! */
        background-size: cover;
        background-attachment: fixed;
        color: #e0e0e0; /* Color de texto para contrastar con el fondo */
        font-family: 'Georgia', serif; /* Una fuente que evoca lo antiguo */
    }
    .st-emotion-cache-1wv7rf0 e1nzp4z51 { /* Titulo */
        color: #FFD700; /* Oro */
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
        font-size: 3em;
        margin-bottom: 0.5em;
    }
    .st-emotion-cache-10qj01k e1nzp4z50 { /* Subtitulos */
        color: #C0C0C0; /* Plata */
        text-align: center;
        text-shadow: 1px 1px 2px #000000;
        font-size: 1.8em;
        margin-top: 1em;
        margin-bottom: 0.8em;
    }
    .st-emotion-cache-nahz7x e1nzp4z5 { /* Texto de entrada */
        background-color: rgba(40, 44, 52, 0.7); /* Fondo semi-transparente para el input */
        border: 2px solid #8B4513; /* Marrón para bordes de madera */
        color: #e0e0e0;
    }
    .st-emotion-cache-vk337c e1nzp4z5 { /* Botones */
        background-color: #A52A2A; /* Rojo oscuro para botones de sellado */
        color: white;
        border: 1px solid #8B0000;
        padding: 0.7em 1.5em;
        border-radius: 5px;
        font-weight: bold;
    }
    .st-emotion-cache-vk337c e1nzp4z5:hover { /* Botones hover */
        background-color: #8B0000;
    }
    /* Estilos para los mensajes de éxito, advertencia y error */
    .st-emotion-cache-p2w9n1 e1nzp4z5 { /* Mensajes de exito */
        background-color: rgba(34, 139, 34, 0.7); /* Verde bosque */
        color: white;
        padding: 1em;
        border-radius: 8px;
        margin-top: 1em;
        border: 2px solid #228B22;
    }
    .st-emotion-cache-1c70e5b e1nzp4z5 { /* Mensajes de advertencia */
        background-color: rgba(255, 140, 0, 0.7); /* Naranja oscuro */
        color: white;
        padding: 1em;
        border-radius: 8px;
        margin-top: 1em;
        border: 2px solid #FF8C00;
    }
    .st-emotion-cache-r423a2 e1nzp4z5 { /* Mensajes de error */
        background-color: rgba(178, 34, 34, 0.7); /* Rojo fuego */
        color: white;
        padding: 1em;
        border-radius: 8px;
        margin-top: 1em;
        border: 2px solid #B22222;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def on_publish(client, userdata, result):
    """
    Función de callback cuando un mensaje es publicado.
    Anuncia a los cielos que el edicto ha sido proclamado.
    """
    st.markdown("---")
    st.write("📜 *El heraldo ha proclamado el edicto al reino.*")
    st.markdown("---")
    pass

def on_message(client, userdata, message):
    """
    Función de callback cuando un mensaje es recibido.
    Escucha los susurros del éter, desentrañando el mensaje.
    """
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(f"👂 *Un eco resuena desde las profundidades: {message_received}*")

# --- Establecimiento de la conexión con el reino etéreo (MQTT Broker) ---
broker = "broker.hivemq.com"
port = 1883
client1 = paho.Client("APP_CERR")
client1.on_message = on_message
client1.on_publish = on_publish
try:
    client1.connect(broker, port)
    st.success("✨ *Conexión con el Reino Etéreo (MQTT Broker) establecida.*")
except Exception as e:
    st.error(f"💀 *Fracaso al conectar con el Reino Etéreo: {e}. Asegúrate de que los hilos del destino estén entrelazados correctamente.*")

# --- Carga del tomo de conocimiento arcaico (Modelo Keras) ---
try:
    model = load_model('keras_model.h5')
    st.success("📚 *El tomo de conocimiento arcaico (modelo) ha sido desenterrado y su sabiduría, cargada.*")
except Exception as e:
    st.error(f"🔥 *No se pudo invocar el tomo de conocimiento (modelo): {e}. ¿Acaso las runas no están en su lugar?*")

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

st.title("🏰 El Portal de la Fortaleza Antigua 🛡️")
st.markdown("---")
st.markdown("""
    *Bienvenido, viajero, a la entrada de esta venerable fortaleza. 
    Aquí, la magia de las imágenes y la elocuencia de las palabras 
    se unen para desvelar o sellar los antiguos portones.*
""")
st.markdown("---")

# --- HERRAMIENTA 1: Oráculo de la Visión (Camera Input) ---
st.subheader("👁️ Oráculo de la Visión - Reconocimiento de Gesto")
st.markdown("""
    *Alza tu mano ante el Oráculo de la Visión. Sus ojos místicas 
    percibirán tus gestos y decidirán si el portal se abrirá o permanecerá sellado.*
""")
img_file_buffer = st.camera_input("📸 *Capta tu imagen para la lectura del Oráculo...*")

if img_file_buffer is not None:
    st.markdown("---")
    st.write("🔮 *El Oráculo procesa tu semblante...*")
    # Para leer el buffer de imagen con OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Para leer el buffer de imagen como una Imagen PIL:
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    # Para convertir la imagen PIL a un array de numpy:
    img_array = np.array(img)

    # Normalizar la imagen para la lectura del Oráculo
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    # Cargar la imagen en el array
    data[0] = normalized_image_array

    # Ejecutar la inferencia (predicción)
    prediction = model.predict(data)
    # st.write(f"📜 *Lectura del Oráculo: {prediction}*") # Solo para depuración, puedes quitarlo
    
    if prediction[0][0] > 0.3:
        st.success('🔓 ¡Por la gracia de los Antiguos, el portal se abre ante ti!')
        client1.publish("PIPPO", "{'gesto': 'Abre'}", qos=0, retain=False)
        time.sleep(0.2)
    elif prediction[0][1] > 0.3:
        st.warning('🔒 ¡Las guardianes del portal se niegan! Permanece sellado.')
        client1.publish("PIPPO", "{'gesto': 'Cierra'}", qos=0, retain=False)
        time.sleep(0.2)
    else:
        st.info("🤷‍♀️ *El Oráculo no pudo discernir tu intención. Intenta de nuevo.*")
    st.markdown("---")

# --- HERRAMIENTA 2: Conjuro Escrito (Text Input) ---
st.subheader("📖 Hechizo Escrito - Sello por Palabra")
st.markdown("""
    *Si eres un maestro de la palabra, invoca los conjuros "abrir" o "cerrar" 
    para manipular el destino de esta entrada.*
""")
user_command = st.text_input("✍️ *Escribe tu conjuro en este pergamino mágico ('abrir' o 'cerrar'):*").strip().lower()

if st.button("🔮 *Invocar Hechizo*"):
    st.markdown("---")
    if user_command == "abrir":
        st.success("🔓 ¡Hechizo aceptado! La entrada se abre ante ti, revelando los secretos que aguardan.")
        client1.publish("PIPPO", "{'gesto': 'Abre'}", qos=0, retain=False)
    elif user_command == "cerrar":
        st.warning("🔒 ¡Puerta cerrada! El conjuro ha sido sellado, y el paso, negado.")
        client1.publish("PIPPO", "{'gesto': 'Cierra'}", qos=0, retain=False)
    else:
        st.error("🚫 *¡Palabra no reconocida por los grimorios ancestrales! Solo 'abrir' o 'cerrar' poseen tal poder.*")
    st.markdown("---")
