import os

def procesar():
    print("Iniciando el procesamiento de datos...")
    # Creamos datos de prueba si no existe data.txt para que no falle
    datos_ejemplo = "Estado,Temp\nAguascalientes,24\nCDMX,20\nEdomex,19\nJalisco,26\nNuevo Leon,28"
    
    if not os.path.exists('data.txt'):
        with open('data.txt', 'w') as f:
            f.write(datos_ejemplo)

    try:
        with open('data.txt', 'r') as f:
            lineas = f.readlines()
        
        # Generamos el archivo de resultados
        with open('resultado.txt', 'w') as f_out:
            f_out.write("Resultados del procesamiento AWS\n")
            f_out.write("------------------------------\n")
            for linea in lineas[1:]: # Saltamos encabezado
                f_out.write(f"Procesado: {linea}")
        
        print("Archivo resultado.txt creado exitosamente.")
    except Exception as e:
        print(f"Error procesando: {e}")
        exit(1)

if __name__ == "__main__":
    procesar() 