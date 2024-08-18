import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

def crear_imagen_partido(fondo, escudo_local, escudo_visitante, nombre_torneo, fecha_partido):
  """
  Crea una imagen con los escudos de dos equipos sobre un fondo,
  agrega el nombre del torneo y la fecha a la imagen.

  Args:
    fondo (Image): Imagen de fondo.
    escudo_local (Image): Escudo del equipo local.
    escudo_visitante (Image): Escudo del equipo visitante.
    nombre_torneo (str): Nombre del torneo.
    fecha_partido (str): Fecha del partido.

  Returns:
    Image: Imagen generada.
  """

  try:
    # Redimensionar la imagen de fondo al tamaño deseado
    fondo = fondo.resize((1290, 760))

    # Calcular la posición central para cada escudo
    posicion_local = ((fondo.width // 4) - (escudo_local.width // 2),
                     (fondo.height // 2) - (escudo_local.height // 2))
    posicion_visitante = ((fondo.width * 3 // 4) - (escudo_visitante.width // 2),
                         (fondo.height // 2) - (escudo_visitante.height // 2))

    # Pegar los escudos en la imagen de fondo
    fondo.paste(escudo_local, posicion_local, escudo_local)
    fondo.paste(escudo_visitante, posicion_visitante, escudo_visitante)

    # Agregar el nombre del torneo a la imagen
    draw = ImageDraw.Draw(fondo)
    font_torneo = ImageFont.truetype("DejaVuSans.ttf", 70)  # Asegúrate de tener la fuente disponible
    text_width, text_height = draw.textsize(nombre_torneo, font=font_torneo)
    text_position = ((fondo.width - text_width) // 2, 50)
    draw.text(text_position, nombre_torneo, font=font_torneo, fill=(255, 255, 255))

    # Agregar la fecha del partido a la imagen
    font_fecha = ImageFont.truetype("DejaVuSans.ttf", 55)  # Asegúrate de tener la fuente disponible
    text_width, text_height = draw.textsize(fecha_partido, font=font_fecha)
    text_position = ((fondo.width - text_width) // 2, fondo.height - text_height - 100)
    draw.text(text_position, fecha_partido, font=font_fecha, fill=(255, 255, 255))

    return fondo

  except Exception as e:
    print(f"Error al generar la imagen: {e}")
    return None

def main():
  st.title("Generador de imágenes de partidos")

  # Subir la imagen de fondo
  fondo_file = st.file_uploader("Suba la imagen de fondo", type=["jpg", "jpeg", "png"])
  if fondo_file is not None:
    fondo = Image.open(fondo_file)

    # Subir los escudos de los equipos
    escudo_local_file = st.file_uploader("Suba el escudo del equipo 1", type=["jpg", "jpeg", "png"])
    escudo_visitante_file = st.file_uploader("Suba el escudo del equipo 2", type=["jpg", "jpeg", "png"])

    if escudo_local_file is not None and escudo_visitante_file is not None:
      escudo_local = Image.open(escudo_local_file)
      escudo_visitante = Image.open(escudo_visitante_file)

      # Pedir al usuario que ingrese el nombre del torneo y la fecha
      nombre_torneo = st.text_input("Ingrese el nombre del torneo: ").upper()
      fecha_partido = st.text_input("Ingrese la fecha del partido (ej. 25 de Agosto): ")

      if st.button("Generar imagen"):
    imagen_partido = crear_imagen_partido(fondo, escudo_local, escudo_visitante, nombre_torneo, fecha_partido)
        if imagen_partido is not None:
        # Mostrar la imagen
        st.image(imagen_partido, caption="Imagen generada", use_column_width=True)
        # Descargar la imagen
        buffer = io.BytesIO()
        imagen_partido.save(buffer, format='JPEG')
        buffer.seek(0)
        st.download_button("Descargar imagen", data=buffer, file_name="partido.jpg", mime="image/jpeg")
           
     
          # Descargar la imagen
          buffer = io.BytesIO()
          imagen_partido.save(buffer, format='JPEG')
          buffer.seek(0)
          st.download_button("Descargar imagen", data=buffer, file_name="partido.jpg", mime="image/jpeg")

if __name__ == "__main__":
  main()
