import csv
import datetime

import requests

# import os


LAT = -37.813061
LONGITUDE = 144.944214
API_KEY = "d342e18efa48c85976dbaa3493b34dd4"
FILE_NAME = "climaMelbourne.csv"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# https://iabigdata-soka-4ae9e223e32444ac5ae3d78afbd55fd9aa6da1c19d9679bf.gitlab.io/post/2024-06-06-pia_openweathermap_ex/#:~:text=Este%20sistema%20consulta%20la%20API,clim%C3%A1ticos%20de%20diferentes%20ubicaciones%20y


def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=es"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error al obtener clima:", e)
        return None


def verificar_alertas(data):
    alertas = []  # Lista para almacenar alertas

    # Verifica si la temperatura supera los 35°C
    if data["main"]["temp"] > 35:
        alertas.append("Alerta de calor extremo")

    # Verifica si la velocidad del viento supera los 20 m/s
    if data["wind"]["speed"] > 20:
        alertas.append("Alerta de viento fuerte")

    # Segun entendi pidio para eso, estaba en el json de la pagina para esas horas
    # Verifica si hay datos de lluvia
    """if "rain" in data and ("1h" in data["rain"]):
        alertas.append("Alerta de lluvia")"""
    if "rain" in data and data["rain"].get("1h", 0) > 0:
        alertas.append("Alerta de lluvia")

    # Verificar nieve
    """if "snow" in data and ("1h" in data["snow"]):
        alertas.append("Alerta de nieve")"""
    if "snow" in data and data["snow"].get("1h", 0) > 0:
        alertas.append("Alerta de nieve")

    return alertas


# https://www.geeksforgeeks.org/python/python-find-current-weather-of-any-city-using-openweathermap-api/


def writeCSV(data, alertas):
    # Encabezados para el archivo CSV
    campos = [
        "ciudad",
        "lat",
        "lon",
        "temp",
        "humedad",
        "viento",
        "description",
        "lluvia",
        "nieve",
        "fecha",
        "alertas",
    ]

    # Crear archivo con encabezado si aún no existe
    try:
        with open(FILE_NAME, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(campos)
    except FileExistsError:
        pass

    # Agregar los datos y alertas en una nueva fila del archivo
    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                data["name"],
                LAT,
                LONGITUDE,
                data["main"]["temp"],
                data["main"]["humidity"],
                data["wind"]["speed"],
                data["weather"][0]["description"],
                data.get("rain", {}).get("1h", 0),
                data.get("snow", {}).get("1h", 0),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "; ".join(alertas),
            ]
        )


def main():
    print("===== Clima Melbourne =====")
    melbourne_weather = get_weather(LAT, LONGITUDE)
    if melbourne_weather and melbourne_weather.get("cod") == 200:
        alertas = verificar_alertas(melbourne_weather)
        writeCSV(melbourne_weather, alertas)
        print(f"Datos guardados para {melbourne_weather['name']}")
        if alertas:
            print("Alertas activadas:", ", ".join(alertas))
    else:
        print("Error: Ciudad no disponible o API KEY inválida")


if __name__ == "__main__":
    main()
