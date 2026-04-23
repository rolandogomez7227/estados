import boto3
import uuid
import csv
from datetime import datetime
from decimal import Decimal

# ── 1. SUBIR DATOS A DYNAMODB ──────────────────────────────────────────────
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('EstadosTabla')

def procesar_datos():
    archivo_entrada = 'Estados.txt'
    conteo = 0

    try:
        with open(archivo_entrada, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                if not fila['Estado'] or fila['Estado'] == 'Estado':
                    continue

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
                table.put_item(Item=item)
                conteo += 1
                print(f"Guardado: {fila['Estado']}")

        print(f"Total: {conteo} estados guardados.")

    except Exception as e:
        print(f"Error al procesar datos: {e}")
        exit(1)

# ── 2. LEER DYNAMODB Y GENERAR HTML ───────────────────────────────────────
def generar_html():
    try:
        response = table.scan()
        items = response['Items']

        # Construir filas de la tabla
        filas_html = ""
        for item in items:
            filas_html += f"""
            <tr>
                <td>{item.get('Estado', 'N/A')}</td>
                <td><span class="badge-temp">{item.get('Temperatura', '0')}°C</span></td>
                <td><span class="badge-hum">{item.get('Humedad', '0')}%</span></td>
                <td><span class="badge-cost">${item.get('Costo_Alojamiento', '0')}</span></td>
                <td>${item.get('Costo_Transporte', '0')}</td>
                <td>{item.get('Dias_Promedio', '0')} días</td>
                <td>{item.get('Tiempo_Traslado', 'N/A')}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Estados</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; padding: 30px; }}
        h1 {{ color: #1a1a2e; margin-bottom: 24px; font-size: 1.8rem; }}
        .card {{ background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden; }}
        table {{ width: 100%; border-collapse: collapse; }}
        thead {{ background: #1447a6; color: white; }}
        thead th {{ padding: 14px 20px; text-align: left; font-weight: 600; font-size: 0.9rem; }}
        tbody tr {{ border-bottom: 1px solid #f0f0f0; transition: background 0.2s; }}
        tbody tr:hover {{ background: #f7f9ff; }}
        tbody td {{ padding: 13px 20px; color: #333; font-size: 0.95rem; }}
        .badge-temp {{ background: #fff3cd; color: #856404; padding: 3px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }}
        .badge-hum {{ background: #d1ecf1; color: #0c5460; padding: 3px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }}
        .badge-cost {{ background: #d4edda; color: #155724; padding: 3px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }}
        .footer {{ margin-top: 16px; color: #888; font-size: 0.8rem; }}
    </style>
</head>
<body>
    <h1>📊 Información de Estados desde DynamoDB</h1>
    <div class="card">
        <table>
            <thead>
                <tr>
                    <th>Estado</th>
                    <th>Temperatura</th>
                    <th>Humedad</th>
                    <th>Costo Alojamiento</th>
                    <th>Costo Transporte</th>
                    <th>Días Promedio</th>
                    <th>Tiempo Traslado</th>
                </tr>
            </thead>
            <tbody>
                {filas_html}
            </tbody>
        </table>
    </div>
    <p class="footer">Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
</body>
</html>"""

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)

        print("index.html generado correctamente.")

    except Exception as e:
        print(f"Error al generar HTML: {e}")
        exit(1)

# ── 3. MAIN ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    procesar_datos()
    generar_html()

    with open('resultado.txt', 'w') as res:
        res.write(f"Proceso completado: {datetime.now().isoformat()}")