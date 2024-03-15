import streamlit as st
import time
import os
from dotenv import load_dotenv
import openai

def preguntar_openAI(info, pregunta, pregunta_anterior,respuesta_anterior):
  contexto = "\nEres un asistente de una compañia de energia, por lo que responde de manera breve, y casi siempre las nuevas preguntas hacen referencia a la pregunta anterior, dispones unicamente de un texto con la informacion de la empresa"
  prompt = contexto + "La nueva pregunta suele hacer referencia a:" + pregunta_anterior + respuesta_anterior +'\nEl texto con la informacion es: \n' + info + "\nResponde breve y claramente a: " + pregunta + '\n'
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0613",
      messages=[
          {"role": "system", "content": "Users are older people who need simpler information with less text in the response. Please note that the question may be related to the previous question"},
          {"role": "user", "content": prompt}
      ],
      temperature=0.5,
      max_tokens=340
  )
  return (response['choices'][0]['message']['content'])


def iniciar_sesion():
    if 'mensajes' not in st.session_state:
        st.session_state.mensajes = []

def main():
  
  load_dotenv()
  openai.api_key = os.getenv("OPENAI_API_KEY")

  #se divide la pantalla en 3 partes
  col1, col2, col3 = st.columns([1, 3, 1])

  #Insertamos los logos
  with col1:
    st.image("https://miro.medium.com/v2/resize:fit:4800/format:webp/1*fRYU2gXNPg8Q5wq8LLmQVw.png")

  with col3:
    st.image("https://totalenergies.com.ar/es/system/files/styles/large/private/atoms/image/totalenergies_logo_rgb.png?itok=0fstyGuH",width=150)


  with col2:
    # Se aumenta el tamaño del titulo y se centra
    st.markdown(
        """
        <style>
        /* Selector de título h1 */
        h1 {
            font-size: 56px; /* Tamaño del texto del título */
            text-align: center; /* Centra horizontalmente el título */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("ChatBot")

    #Creamos un contenedor donde se va a mostrar la informacion
    messages = st.container(height=500,border=True)

    # Llama a la función para inicializar el estado de la sesión
    iniciar_sesion()

    #Cargamos los ficheros donde esta la informacion
    dir = 'Info_TotalEnergi_parte_1.txt'
    with open(dir, 'r') as f:
        datos1 = f.read()
    dir = 'Info_TotalEnergi_parte_2.txt'
    with open(dir, 'r') as f:
        datos2 = f.read()

    #inicializamos la respuesta y pregunta anterior a vacio
    pregunta_anterior=""
    respuesta_anterior=""

    #cada vez que se escriba algo en el prompt se va a guardar en la sesion
    if prompt := st.chat_input("Say something"):
        if len(st.session_state.mensajes) >= 2:
          pregunta_anterior = st.session_state.mensajes[len(st.session_state.mensajes) - 2]
          respuesta_anterior = st.session_state.mensajes[len(st.session_state.mensajes) - 1]
        st.session_state.mensajes.append(prompt)
        response = preguntar_openAI(datos1, prompt,pregunta_anterior, respuesta_anterior)
        st.session_state.mensajes.append(response)
    #para cada uno de los mensajes guardados en la sesion se van a mostrar dentro del contenedor
    for i,mensaje in enumerate(st.session_state.mensajes):
      #si el mensaje se encuentra en una posicion par quiere decir que es la pregunta que hemos realizado y si esta en uan posicion impar se trata de la respuesta
      if i%2==0:
        messages.chat_message("user").write(mensaje)
      else:
        messages.chat_message("assistant").write(mensaje)

    #se crea este boton si se desea eliminar el contenido de la sesion, es decir, se quiere eliminar las preguntas y respuestas realizadas anteriormente
    if st.button("Eliminar mensajes"):
        messages.empty()
        del st.session_state.mensajes

# Llama a la función main para ejecutar la aplicación
if __name__ == "__main__":
    main()
