import boto3
import json
import uuid

# Configuración de DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
tabla = dynamodb.Table('EstadosTabla')

def procesar_archivo_a_dynamo():
    archivo_entrada = 'Estados.txt'
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            
        for linea in lineas:
            dato = linea.strip()
            if not dato: continue
            
            # Crear el formato JSON para la tabla
            item = {
                'EstadoID': str(uuid.uuid4()),
                'NombreEstado': dato,
                'FechaRegistro': datetime.now().isoformat()
            }
            
            # Subir a DynamoDB
            tabla.put_item(Item=item)
            print(f"Subido con éxito: {dato}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    procesar_archivo_a_dynamo()
