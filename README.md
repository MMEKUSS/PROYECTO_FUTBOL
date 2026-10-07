RESUMEN DEL PROYECTO — ANÁLISIS DE FÚTBOL EUROPEO

OBJETIVO

El proyecto busca construir una base de datos de fútbol combinando información de diferentes fuentes para analizar posteriormente el rendimiento de jugadores, clubes y el posible impacto de las lesiones.

FUENTES DE DATOS

1. Web scraping
Se utiliza Sport-Histoire para obtener las clasificaciones de las cinco grandes ligas europeas:
- Premier League
- La Liga
- Bundesliga
- Serie A
- Ligue 1

Se recogen las temporadas 2023-24 y 2024-25, por lo que se trabajan diez páginas.

De cada competición se extraen:
- liga
- equipo
- puntos
- goles a favor
- goles en contra

La información se encuentra dentro de un objeto JSON incluido en los scripts HTML de las páginas. Por ello, el proyecto utiliza BeautifulSoup para localizar el script y json.loads() para convertir los datos a estructuras Python.

2. CSV european_football_players.csv

Se conservan las variables:
- Player
- Pos
- Squad
- Comp
- MP
- Starts
- Min

Estas variables permiten trabajar con el jugador, posición, club, competición, partidos, titularidades y minutos.

3. CSV injuries24_25.csv

Se filtra la temporada 24/25 y se conservan:
- Season
- Injury
- Days
- Games missed
- player_name
- player_position
- club
- league

Los registros de lesiones se agrupan por jugador y club para obtener el total de días de baja y partidos perdidos.

PROCESO DE LIMPIEZA

Uno de los problemas principales es que los nombres de competiciones y clubes no son exactamente iguales entre las fuentes.

Por ejemplo, algunos nombres de clubes aparecen abreviados en el dataset de jugadores. Se utiliza un diccionario de equivalencias para normalizarlos antes del merge.

También se normalizan los nombres de las competiciones para facilitar su comparación.

INTEGRACIÓN

El DataFrame de jugadores se combina con el DataFrame agregado de lesiones mediante:
- Player ↔ player_name
- Squad ↔ club

Se utiliza un left merge para conservar todos los jugadores del dataset de jugadores.

Cuando un jugador no tiene un registro de lesión, Days y Games missed se convierten en 0.

RESULTADO

El resultado principal de esta fase es df_final, que reúne información de jugadores y lesiones.

La estructura queda preparada para continuar el proyecto en SQL.

PRÓXIMA FASE

El siguiente paso será llevar los datos a SQL y construir consultas que permitan analizar relaciones entre:
- minutos jugados
- titularidades
- lesiones
- días de baja
- partidos perdidos
- clubes
- competiciones
- temporadas

La clasificación de las ligas obtenida mediante scraping se mantiene como una fuente independiente hasta definir la relación exacta entre clubes, temporadas y jugadores.

CORRECCIONES PRINCIPALES REALIZADAS

- Se eliminaron comprobaciones duplicadas que servían para explorar la página pero no son necesarias en la versión final.
- Se separó la exploración del scraping definitivo.
- Se automatizó la extracción de las diez competiciones.
- Se mantuvo la función original obtener_soup(url) sin modificar nombre ni parámetro.
- Se crearon funciones reutilizables para las partes repetitivas.
- Se mantuvieron las columnas y nombres de variables principales del proyecto.
- Se ordenó el flujo para que siga una lógica de extracción → limpieza → normalización → integración → comprobación → SQL.
- Se añadió una comprobación de nulos, duplicados y tipos antes de pasar a SQL.

NOTA SOBRE LOS CAMBIOS

El único cambio conceptual relevante está en la normalización de la columna liga. En la primera parte del proyecto aparecían códigos como FL1, BL1, PD, PL y SA, mientras que la extracción automática posterior genera nombres como “Premier League 2024-2025”. La normalización de la versión ordenada se adapta al valor que realmente genera el método automatizado.

No se ha cambiado la función original del usuario.
