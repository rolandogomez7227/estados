import os

def procesar_datos():
    if not os.path.exists('data.txt'):
        print("Error: data.txt no encontrado")
        return

    with open('data.txt', 'r') as f:
        lineas = f.readlines()[1:] # Omitir encabezado

    resultados = []
    for linea in lineas:
        datos = linea.strip().split(',')
        if len(datos) >= 2:
            estado = datos[0]
            temp = datos[1]
            humedad = datos[2]
            resultados.append(f"Estado: {estado} | Temp: {temp}°C | Humedad: {humedad}%")

    with open('resultado.txt', 'w') as f:
        f.write("\n".join(resultados))
    print("Archivo resultado.txt generado con éxito.")

if __name__ == "__main__":
    procesar_datos()