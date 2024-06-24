import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime


def seleccionar_carpeta(prompt):
    print(prompt)
    root = tk.Tk()
    root.withdraw()  
    carpeta_destino = None
    try:
        carpeta_destino = filedialog.askdirectory()  
        if not carpeta_destino:
            print("No se seleccionó ninguna carpeta.")
        else:
            print(f"Carpeta seleccionada: {carpeta_destino}")
    except Exception as e:
        print(f"Error al seleccionar la carpeta: {e}")
    finally:
        root.destroy()
    return carpeta_destino

def seleccionar_archivo(prompt):
    print(prompt)
    root = tk.Tk()
    root.withdraw()  
    try:
        ruta_archivo = filedialog.askopenfilename()
        if ruta_archivo:
            print(f"Archivo seleccionado: {ruta_archivo}")
        else:
            print("No se seleccionó ningún archivo.")
    finally:
        root.destroy()  
    return ruta_archivo


def copiar_imagen(origen, destino, numero_copias, nombre_base):
    img = cv2.imread(origen)
    if img is not None:
        altura, ancho, canales = img.shape
        print(f"Dimensiones de la imagen original: {ancho}x{altura} píxeles. Canales de color: {canales}.")

        for i in range(numero_copias):
            nombre_archivo = f"{nombre_base}_{i+1}.jpg" if numero_copias > 1 else f"{nombre_base}.jpg"
            ruta_completa = os.path.join(destino, nombre_archivo)
            cv2.imwrite(ruta_completa, img)
            print(f"Imagen copiada con éxito a {ruta_completa}.")

    else:
        print("Error: No se pudo cargar la imagen desde la ruta proporcionada.")
        
def mostrar_caracteristicas(origen):
    img = cv2.imread(origen)
    if img is not None:
        altura, ancho, canales = img.shape
        
       
        tamaño_en_bytes = os.path.getsize(origen)
        tamaño_en_kb = tamaño_en_bytes / 1024
        
        # Mostrar información sobre la imagen
        print("Características de la imagen:")
        print(f"  - Alto (altura): {altura} píxeles")
        print(f"  - Ancho: {ancho} píxeles")
        print(f"  - Número de canales de color: {canales}")
        
        
        dpi_estandar = 96
        print(f"  - Resolución aproximada: {ancho // dpi_estandar} x {altura // dpi_estandar} pulgadas (asumiendo {dpi_estandar} DPI)")
        
        
        print(f"  - Tamaño del archivo: {tamaño_en_kb:.2f} KB")
    else:
        print("Error: No se pudo cargar la imagen.")


def sobrescribir_negros(origen, x1, y1, x2, y2):
    img = cv2.imread(origen)
    if img is not None:
        
        x1, y1, x2, y2 = max(0, x1), max(0, y1), min(img.shape[1], x2), min(img.shape[0], y2)
        
        
        color = solicitar_color()

        
        img[y1:y2, x1:x2] = color
        cv2.imshow('Imagen modificada', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")

def invertir_imagen(origen, num_copias, tipo):
    img = cv2.imread(origen)
    if img is not None:
        # Establecer el código de flip adecuado
        flip_code = 0 if tipo == 'horizontal' else 1 if tipo == 'vertical' else None
        
        if flip_code is None:
            print("Error: Tipo de inversión no válido.")
            return

        for i in range(num_copias):
            flipped_image = cv2.flip(img, flip_code)
            cv2.imshow(f'{tipo.capitalize()} flip {i+1}', flipped_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")
        
def ampliar_reducir(origen, factor):
    img = cv2.imread(origen)
    if img is not None:
       
        try:
            factor = float(factor)  
            if factor <= 0:
                print("El factor de escala debe ser un número positivo mayor que cero.")
                return
        except ValueError:
            print("Debes introducir un número decimal válido. Por ejemplo, 1.2 o 0.5.")
            return

       
        width = int(img.shape[1] * factor)
        height = int(img.shape[0] * factor)
        dim = (width, height)

        
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow(f'Imagen {"ampliada" if factor > 1 else "reducida"}', resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")

def recortar_imagen(origen, x1, y1, x2, y2):
    img = cv2.imread(origen)
    if img is not None:
        
        if 0 <= x1 < x2 <= img.shape[1] and 0 <= y1 < y2 <= img.shape[0]:
            crop_img = img[y1:y2, x1:x2]
            cv2.imshow('Cropped Image', crop_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Las coordenadas proporcionadas están fuera de los límites de la imagen.")
    else:
        print("Error: No se pudo cargar la imagen.")



def escribir_texto_en_imagen(origen, texto):
    img = cv2.imread(origen)
    if img is not None:
        color = solicitar_color()
        tamaño_fuente = float(input("Introduce el tamaño de la fuente (ej: 1.0, 0.5, etc.): "))
        ubicacion_x = int(input("Introduce la coordenada X para el texto (esquina izquierda del texto): "))
        ubicacion_y = int(input("Introduce la coordenada Y para el texto (altura del texto): "))
        orientacion = input("¿Deseas el texto horizontal o vertical? (horizontal/vertical): ").lower()
        
        if orientacion == "vertical":
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            
            ubicacion_x, ubicacion_y = ubicacion_y, img.shape[0] - ubicacion_x

       
        cv2.putText(img, texto, (ubicacion_x, ubicacion_y), cv2.FONT_HERSHEY_SIMPLEX, tamaño_fuente, color, 2, cv2.LINE_AA)
        
        if orientacion == "vertical":
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

        cv2.imshow('Text on Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")

def dibujar_forma(origen, forma):
    img = cv2.imread(origen)
    if img is not None:
        color = solicitar_color()
        
        if forma == "circulo":
            radio = int(input("Introduce el radio del círculo: "))
            centro_x = int(input("Introduce la coordenada X del centro del círculo: "))
            centro_y = int(input("Introduce la coordenada Y del centro del círculo: "))
            cv2.circle(img, (centro_x, centro_y), radio, color, -1)
        
        elif forma == "rectangulo":
            x1 = int(input("Introduce la coordenada X de la esquina superior izquierda: "))
            y1 = int(input("Introduce la coordenada Y de la esquina superior izquierda: "))
            x2 = int(input("Introduce la coordenada X de la esquina inferior derecha: "))
            y2 = int(input("Introduce la coordenada Y de la esquina inferior derecha: "))
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
        
        else:
            print("Forma no reconocida. Solo se permite 'circulo' o 'rectangulo'.")
            return
        
        cv2.imshow('Form on Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")

def leer_camara_y_reconocer_rostro():
    if not os.path.exists("fotos"):
        os.makedirs("fotos")
    if not os.path.exists("videos"):
        os.makedirs("videos")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return

    net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000_fp16.caffemodel")
    conf_threshold = 0.7
    recording = False
    video_writer = None
    frame_index = 0
    video_index = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se pudo leer de la cámara.")
                break

            frame_height, frame_width = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], swapRB=False, crop=False)
            net.setInput(blob)
            detections = net.forward()

            found_face = False

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > conf_threshold:
                    found_face = True
                    x1 = int(detections[0, 0, i, 3] * frame_width)
                    y1 = int(detections[0, 0, i, 4] * frame_height)
                    x2 = int(detections[0, 0, i, 5] * frame_width)
                    y2 = int(detections[0, 0, i, 6] * frame_height)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if found_face:
                if not recording:
                    video_index += 1
                    video_path = f"videos/video_{video_index}.avi"
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    video_writer = cv2.VideoWriter(video_path, fourcc, 20.0, (frame_width, frame_height))
                    recording = True

                video_writer.write(frame)

                if frame_index % 10 == 0:
                    photo_path = f"fotos/photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{frame_index}.jpg"
                    cv2.imwrite(photo_path, frame)

            else:
                if recording:
                    recording = False
                    video_writer.release()

            frame_index += 1
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        if recording:
            video_writer.release()
        cv2.destroyAllWindows()

def solicitar_coordenadas():
    print("Necesitarás proporcionar las coordenadas del rectángulo a sobrescribir en negro sobre la imagen.")
    print("Imagina que la imagen es un plano cartesiano donde el punto (0, 0) está en la esquina superior izquierda.")
    print("Deberás indicar dos puntos: la esquina superior izquierda y la esquina inferior derecha del rectángulo.")
    x1 = int(input("Introduce la coordenada X de la esquina superior izquierda: "))
    y1 = int(input("Introduce la coordenada Y de la esquina superior izquierda: "))
    x2 = int(input("Introduce la coordenada X de la esquina inferior derecha: "))
    y2 = int(input("Introduce la coordenada Y de la esquina inferior derecha: "))
    return x1, y1, x2, y2

def solicitar_coordenadas_para_recorte(img):
    altura, ancho = img.shape[:2]
    print("Necesitas proporcionar las coordenadas del rectángulo a recortar.")
    print("Asegúrate de que x1 < x2 y y1 < y2 y que todas las coordenadas estén dentro de los límites de la imagen.")
    print(f"La imagen tiene {ancho} píxeles de ancho y {altura} píxeles de alto.")
    print("Deberás introducir las coordenadas de dos puntos: la esquina superior izquierda y la esquina inferior derecha del rectángulo a recortar.")
    x1 = int(input("Introduce la coordenada X de la esquina superior izquierda: "))
    y1 = int(input("Introduce la coordenada Y de la esquina superior izquierda: "))
    x2 = int(input("Introduce la coordenada X de la esquina inferior derecha: "))
    y2 = int(input("Introduce la coordenada Y de la esquina inferior derecha: "))
    
    return x1, y1, x2, y2

def solicitar_color():
    print("Introduce los valores RGB para el color del texto.")
    r = int(input("Valor de Rojo (0-255): "))
    g = int(input("Valor de Verde (0-255): "))
    b = int(input("Valor de Azul (0-255): "))
    return (b, g, r)  


def main():
    while True:
        print("\nMenú de opciones:")
        print("1. Copiar imagen")
        print("2. Mostrar características de la imagen")
        print("3. Sobrescribir pixeles")
        print("4. Invertir imagen")
        print("5. Ampliar/reducir imagen")
        print("6. Recortar imagen")
        print("7. Escribir texto en imagen")
        print("8. Dibujar forma en imagen")
        print("9. Leer cámara, reconocer rostro, grabar rostro y tomar fotos")
        print("0. Salir")
        
        opcion = input("Introduce una opción: ")
        
        if opcion == "1":
            origen = seleccionar_archivo("Selecciona la imagen original:")
            if not origen:
                print("No se seleccionó ningún archivo.")
                continue
            destino = seleccionar_carpeta("Selecciona la carpeta de destino para la copia:")
            if not destino:
                print("No se seleccionó ningún archivo.")
                continue
            try:
                numero_copias = int(input("Introduce el número de copias que deseas realizar: "))
            except ValueError:
                print("Debes introducir un número entero válido para el número de copias.")
                continue
            nombre_base = input("Introduce el nombre base para las nuevas imágenes (sin extensión): ")
            copiar_imagen(origen, destino, numero_copias, nombre_base)
        
        elif opcion == "2":
            origen = seleccionar_archivo("Selecciona la imagen original:")
            if not origen:
                print("No se seleccionó ningún archivo.")
                continue
            mostrar_caracteristicas(origen)
        
        elif opcion == "3":
            origen = seleccionar_archivo("Selecciona la imagen original:")
            if not origen:
                print("No se seleccionó ningún archivo.")
                continue
            x1, y1, x2, y2 = solicitar_coordenadas()
            sobrescribir_negros(origen, x1, y1, x2, y2)
        
        elif opcion == "4":
            origen = seleccionar_archivo("Selecciona la imagen original:")
            if not origen:
                print("No se seleccionó ningún archivo.")
                continue
            num_copias = int(input("Número de copias a crear: "))
            tipo = input("Introduce el tipo de inversión ('vertical' o 'horizontal'): ").lower()
            if tipo not in ['vertical', 'horizontal']:
                print("Tipo de inversión no reconocido. Debe ser 'vertical' o 'horizontal'.")
            else:
                invertir_imagen(origen, num_copias, tipo)
        
        elif opcion == "5":
            origen = seleccionar_archivo("Selecciona la imagen original:")
            if not origen:
                print("No se seleccionó ningún archivo.")
                continue
            try:
                factor = float(input("Factor de multiplicación (por ejemplo, 0.50 para el 50%, 1.20 para el 120%, etc.): "))
                ampliar_reducir(origen, factor)
            except ValueError:
                print("Debes introducir un número decimal válido.")
        
        elif opcion == "6":
                origen = seleccionar_archivo("Selecciona la imagen original:")
                if not origen:
                    print("No se seleccionó ningún archivo.")
                    continue
                img = cv2.imread(origen)  
                if img is None:
                    print("Error al cargar la imagen.")
                    continue
                x1, y1, x2, y2 = solicitar_coordenadas_para_recorte(img)
                recortar_imagen(origen, x1, y1, x2, y2)
        
        elif opcion == "7":
            origen = seleccionar_archivo("Selecciona la imagen original:")
            if not origen:
                print("No se seleccionó ningún archivo.")
                continue
            texto = input("Texto a escribir: ")
            escribir_texto_en_imagen(origen, texto)
        
        elif opcion == "8":
            origen = seleccionar_archivo("Selecciona la imagen original:")
            if not origen:
                print("No se seleccionó ningún archivo.")
                continue
            forma = input("Tipo de forma ('circulo' o 'rectangulo'): ").lower()
            if forma in ["circulo", "rectangulo"]:
                dibujar_forma(origen, forma)
            else:
                print("Forma no reconocida. Solo se permite 'circulo' o 'rectangulo'.")
        
        elif opcion == "9":
            leer_camara_y_reconocer_rostro()
        
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción no reconocida, intenta de nuevo.")

if __name__ == "__main__":
    main()


