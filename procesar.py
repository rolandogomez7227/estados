import boto3
import uuid
import csv
from datetime import datetime

# Configuración de AWS
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('EstadosTabla')

def procesar_datos():
    archivo_entrada = 'Estados.txt'
    
    try:
        with open(archivo_entrada, mode='r', encoding='utf-8') as f:
            # Usamos DictReader para que use la primera línea como nombres de columnas
            lector = csv.DictReader(f)
            
            conteo = 0
            for fila in lector:
                # Si la fila está vacía o es un encabezado repetido, la saltamos
                if not fila['Estado'] or fila['Estado'] == 'Estado':
                    continue
                
                # Creamos el item para DynamoDB
                item = {
                    'EstadoID': str(uuid.uuid4()),
                    'Estado': fila['Estado'],
                    'Temperatura': fila.get('Temperatura', '0'),
                    'Humedad': fila.get('Humedad', '0'),
                    'Costo_Alojamiento': fila.get('Costo_Alojamiento', '0'),
                    'Costo_Transporte': fila.get('Costo_Transporte', '0'),
                    'Dias_Promedio': fila.get('Dias_Promedio', '0'),
                    'Tiempo_Traslado': fila.get('Tiempo_Traslado', '0'),
                    'FechaProcesado': datetime.now().isoformat()
                }
                
                # Subir a la tabla
                table.put_item(Item=item)
                conteo += 1
                print(f"Registro guardado: {fila['Estado']}")
            
            # Crear archivo de control para el buildspec
            with open('resultado.txt', 'w') as res:
                res.write(f"Se procesaron {conteo} estados exitosamente.")
                
    except Exception as e:
        print(f"Error durante el proceso: {e}")
        # Importante: si hay error, el script debe fallar para que el pipeline avise
        exit(1) 

if __name__ == "__main__":
    procesar_datos()
