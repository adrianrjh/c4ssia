import requests

def obtener_coordenadas_osm(ciudad):
    url = "https://nominatim.openstreetmap.org/search"
    headers = {'User-Agent': 'adrianfime27@gmail.com'}
    params = {"q": ciudad,"format": "json"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        resultados = response.json()
        if resultados:
            latitud = resultados[0]['lat']
            longitud = resultados[0]['lon']
            return latitud, longitud
        else:
            return "No se encontraron resultados"
    else:
        return "Error en la solicitud: " + str(response.status_code)
ciudad = "LA PLACITA DE MORELOS"
coordenadas = obtener_coordenadas_osm(ciudad)
print(coordenadas[0])