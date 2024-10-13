import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
loc1 = "Santiago"
loc2 = "Buenos Aires"
key = "b0775702-665a-4c66-b203-243b29f434a9" ## Reemplazar con su clave de API

url = geocode_url + urllib.parse.urlencode ({"q": loc1, "limit": "1", "key": key})
url2 = geocode_url + urllib.parse.urlencode ({"q": loc2, "limit": "2", "key": key})

replydata = requests.get(url)
replydata2 = requests.get(url2)
json_data = replydata.json()
json_data2 = replydata2.json()
json_status = replydata.status_code
print(json_data)
print(json_data2)
####################
#Parte 2 del codigo#
####################
import requests

def obtener_coordenadas(nombre_ciudad, clave_api):
    """Obtiene las coordenadas (latitud, longitud) de una ciudad usando la API de GraphHopper."""
    url = f"https://graphhopper.com/api/1/geocode?q={nombre_ciudad}&key={clave_api}"
    respuesta = requests.get(url)
    datos = respuesta.json()
    if datos.get('hits'):
        latitud = datos['hits'][0]['point']['lat']
        longitud = datos['hits'][0]['point']['lng']
        return latitud, longitud
    else:
        return None, None

def obtener_info_ruta(lat1, lon1, lat2, lon2, clave_api, vehiculo):
    """Obtiene la distancia y el tiempo estimado entre dos coordenadas usando un tipo de vehículo."""
    url = f"https://graphhopper.com/api/1/route?point={lat1},{lon1}&point={lat2},{lon2}&vehicle={vehiculo}&key={clave_api}&calc_points=false"
    respuesta = requests.get(url)
    datos = respuesta.json()
    if 'paths' in datos:
        distancia_km = datos['paths'][0]['distance'] / 1000  # convertir de metros a kilómetros
        tiempo_ms = datos['paths'][0]['time']  # tiempo en milisegundos
        tiempo_horas = tiempo_ms / (1000 * 60 * 60)  # convertir de milisegundos a horas
        return distancia_km, tiempo_horas
    else:
        return None, None

def calcular_tiempo_vuelo(distancia_km):
    """Calcula el tiempo de vuelo aproximado considerando una velocidad promedio de 800 km/h."""
    velocidad_promedio_avion = 800  # km/h
    return distancia_km / velocidad_promedio_avion

def convertir_km_a_millas(distancia_km):
    """Convierte la distancia de kilómetros a millas."""
    return distancia_km * 0.621371

def main():
    clave_api = "b0775702-665a-4c66-b203-243b29f434a9"  # Reemplaza con tu API Key de GraphHopper
    print()
    ciudad1 = input("Ingrese la ciudad 1: ")
    ciudad2 = input("Ingrese la ciudad 2: ")

    lat1, lon1 = obtener_coordenadas(ciudad1, clave_api)
    lat2, lon2 = obtener_coordenadas(ciudad2, clave_api)

    if lat1 is None or lat2 is None:
        print("No se pudieron obtener las coordenadas de una de las ciudades. Intente con otro nombre.")
        return

    # Calcular en auto
    distancia_km, tiempo_auto_horas = obtener_info_ruta(lat1, lon1, lat2, lon2, clave_api, "car")
    if distancia_km:
        distancia_millas = convertir_km_a_millas(distancia_km)
        print(f"Distancia entre {ciudad1} y {ciudad2}: {distancia_km:.2f} km ({distancia_millas:.2f} millas)")
        print(f"Tiempo en auto: {tiempo_auto_horas:.2f} horas")
    
        # Calcular en bicicleta
        _, tiempo_bici_horas = obtener_info_ruta(lat1, lon1, lat2, lon2, clave_api, "bike")
        if tiempo_bici_horas:
            print(f"Tiempo en bicicleta: {tiempo_bici_horas:.2f} horas")
    
        # Calcular en avión
        tiempo_vuelo_horas = calcular_tiempo_vuelo(distancia_km)
        print(f"Tiempo en avión (estimado): {tiempo_vuelo_horas:.2f} horas")
    else:
        print("No se pudo calcular la distancia entre las ciudades.")

if __name__ == "__main__":
    main()
