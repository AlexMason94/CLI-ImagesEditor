import cv2
import tkinter as tk
from tkinter import filedialog

def seleccionar_archivo(prompt):
    print(prompt)
    root = tk.Tk()
    root.withdraw()
    ruta_archivo = filedialog.askopenfilename()
    root.destroy()
    return ruta_archivo

def copiar_imagen():
    origen = seleccionar_archivo("Selecciona la imagen original:")
    destino = seleccionar_archivo("Selecciona la ruta de destino para la copia:")
    img = cv2.imread(origen)
    if img is not None:
        cv2.imwrite(destino, img)
        print("Imagen copiada con éxito.")
    else:
        print("Error: No se pudo cargar la imagen.")

def mostrar_caracteristicas():
    origen = seleccionar_archivo("Selecciona la imagen:")
    img = cv2.imread(origen)
    if img is not None:
        altura, ancho, canales = img.shape
        print(f"Alto: {altura}, Ancho: {ancho}, Canales: {canales}")
    else:
        print("Error: No se pudo cargar la imagen.")

def sobrescribir_negros():
    origen = seleccionar_archivo("Selecciona la imagen:")
    img = cv2.imread(origen)
    x1, y1, x2, y2 = map(int, input("Introduce x1, y1, x2, y2 separados por comas: ").split(','))
    if img is not None:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)
        cv2.imshow('Imagen Modificada', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")

def invertir_imagen():
    origen = seleccionar_archivo("Selecciona la imagen:")
    img = cv2.imread(origen)
    if img is not None:
        vertical_flip = cv2.flip(img, 0)
        horizontal_flip = cv2.flip(img, 1)
        cv2.imshow('Vertical Flip', vertical_flip)
        cv2.imshow('Horizontal Flip', horizontal_flip)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")

def ampliar_reducir():
    origen = seleccionar_archivo("Selecciona la imagen:")
    factor = float(input("Introduce el factor de ampliación (por ejemplo, 0.5, 2, 3): "))
    img = cv2.imread(origen)
    if img is not None:
        width = int(img.shape[1] * factor)
        height = int(img.shape[0] * factor)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow('Imagen Redimensionada', resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")

def recortar_imagen():
    origen = seleccionar_archivo("Selecciona la imagen:")
    img = cv2.imread(origen)
    if img is not None:
        altura, ancho = img.shape[:2]
        print(f"Dimensiones originales: Alto = {altura}, Ancho = {ancho}")
        x1, y1, x2, y2 = map(int, input("Introduce x1, y1, x2, y2 separados por comas para recortar: ").split(','))
        crop_img = img[y1:y2, x1:x2]
        cv2.imshow('Imagen Recortada', crop_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")

def escribir_texto_en_imagen():
    origen = seleccionar_archivo("Selecciona la imagen:")
    texto = input("Introduce el texto a escribir en la imagen: ")
    img = cv2.imread(origen)
    if img is not None:
        cv2.putText(img, texto, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Imagen con Texto', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo cargar la imagen.")

def reconocimiento_facial():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Reconocimiento Facial', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    opciones = {
        '1': copiar_imagen,
        '2': mostrar_caracteristicas,
        '3': sobrescribir_negros,
        '4': invertir_imagen,
        '5': ampliar_reducir,
        '6': recortar_imagen,
        '7': escribir_texto_en_imagen,
        '8': reconocimiento_facial
    }
    while True:
        print("\nMenú de Opciones:")
        for k, v in opciones.items():
            print(f"{k}. {v.__name__.replace('_', ' ').title()}")
        print("0. Salir")
        opcion = input("Elige una opción: ")
        if opcion == '0':
            break
        elif opcion in opciones:
            opciones[opcion]()
        else:
            print("Opción no válida, por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
