# Análisis de Datos de Temperatura de Melbourne, Australia

**Coders:**

- Uriel Dueñas 
- Felipe Merino

Este repositorio contiene la implementación un sistema automatizado para la recopilación y análisis de datos meteorológicos en tiempo real. Los componentes clave incluyen:

1. La configuración de la API:
    - Obtención de un API en **OpenWeatherMap** (ya no es valido)
    - Determinación de las coordenadas geográficas para Melbourne, Australia

2. Automatización de los datos:
    - *Script* Python para consulta de API y escritura en CSV (*climaMelbourne.csv*)
    - Ejecutable get-weather.sh para gestionar procesos
    - Configuración de **Crontab** para muestreo 

3. Gestión de registros:
    - Almacenamiento sistemático en *registro.log*
    - Validación de la integridad de los datos
    - Respaldar ejecuciones en *output.log*
