# %% [markdown]
# # Funciones del proyecto — Análisis de fútbol
# 
# Este notebook reúne las funciones reutilizables necesarias para ejecutar el proyecto.
# 
# **Importante:** la función `obtener_soup(url)` se mantiene con el mismo nombre, parámetro y código que en el notebook original.

# %%
import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# %% [markdown]
# ## 1. Función original del proyecto
# Se conserva sin cambios.

# %%
def obtener_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    return soup

# %% [markdown]
# ## 2. Extraer los datos `standingsData`
# 
# Esta función evita repetir en cada liga el mismo bloque que busca el `script`, extrae el JSON y lo convierte en una lista de diccionarios.
# 
# No sustituye ni modifica `obtener_soup()`.

# %%
def extraer_standings(soup):
    for script in soup.find_all("script"):
        texto = script.get_text()

        if "window.standingsData" in texto:
            datos_json = texto.split("window.standingsData", 1)[1]
            datos_json = datos_json.split("=", 1)[1]
            datos_json = datos_json.split(";", 1)[0].strip()

            return json.loads(datos_json)

    return []

# %% [markdown]
# ## 3. Convertir standings en registros
# 
# Recibe el nombre de la liga/temporada y los datos extraídos y devuelve las filas que después utilizaremos para crear el DataFrame.

# %%
def convertir_standings(liga, standings):
    datos = []

    for equipo in standings:
        datos.append([
            liga,
            equipo["team"],
            equipo["pts"],
            equipo["gf"],
            equipo["ga"]
        ])

    return datos

# %% [markdown]
# ## 4. Crear el DataFrame de las competiciones
# 
# Esta función centraliza el proceso de recorrer las URLs, obtener el HTML, extraer el JSON y construir el DataFrame final de clasificación.

# %%
def crear_dataframe_ligas(ligas):
    datos = []

    for liga, url_liga in ligas.items():
        soup_liga = obtener_soup(url_liga)
        standings = extraer_standings(soup_liga)

        datos.extend(convertir_standings(liga, standings))

    return pd.DataFrame(
        datos,
        columns=["liga", "equipo", "puntos", "goles_favor", "goles_contra"]
    )

# %% [markdown]
# ## 5. Seleccionar columnas de jugadores

# %%
def seleccionar_columnas_players(df_players):
    columnas_players = [
        "Player",
        "Pos",
        "Squad",
        "Comp",
        "MP",
        "Starts",
        "Min"
    ]

    return df_players[columnas_players].copy()

# %% [markdown]
# ## 6. Filtrar y seleccionar columnas de lesiones
# 
# Se mantiene la lógica utilizada en el proyecto: trabajar únicamente con la temporada `24/25`.

# %%
def preparar_injuries(df_injuries):
    df_injuries = df_injuries[df_injuries["Season"] == "24/25"].copy()

    columnas_injuries = [
        "Season",
        "Injury",
        "Days",
        "Games missed",
        "player_name",
        "player_position",
        "club",
        "league"
    ]

    return df_injuries[columnas_injuries].copy()

# %% [markdown]
# ## 7.Limpiar y agrupar la columna injury
# 
# Se limpia con un regex la columna de injury para luego calcular cuál es la lesión más frecuente.

# %%
def limpiar_lesiones(df_injuries):

    df_injuries["injury"] = (
        df_injuries["injury"]
        .str.lower()
        .str.strip()
    )

    df_injuries["injury_category"] = np.select(
        [
            df_injuries["injury"].str.contains(
                r"muscle|muscular|calf|hamstring|thigh|adductor|quadriceps|groin",
                regex=True,
                na=False
            ),

            df_injuries["injury"].str.contains(
                r"ankle|foot|achilles",
                regex=True,
                na=False
            ),

            df_injuries["injury"].str.contains(
                r"knee|meniscus|patella",
                regex=True,
                na=False
            ),

            df_injuries["injury"].str.contains(
                r"back|lumbar|spine",
                regex=True,
                na=False
            ),

            df_injuries["injury"].str.contains(
                r"shoulder|arm|elbow|wrist|hand|finger",
                regex=True,
                na=False
            ),

            df_injuries["injury"].str.contains(
                r"hip|pelvis",
                regex=True,
                na=False
            ),

            df_injuries["injury"].str.contains(
                r"head|concussion|face",
                regex=True,
                na=False
            ),

            df_injuries["injury"].str.contains(
                r"ill|illness|flu|virus|infection|fever",
                regex=True,
                na=False
            )
        ],
        [
            "Muscular",
            "Ankle/Foot",
            "Knee",
            "Back",
            "Arm/Hand",
            "Hip/Pelvis",
            "Head/Face",
            "Illness"
        ],
        default="Other"
    )

    return df_injuries

# %% [markdown]
# ## 7. Normalizar competiciones

# %%
def normalizar_competencias(df_players):
    equivalencias = {
        "eng Premier League": "Premier League",
        "es La Liga": "La Liga",
        "it Serie A": "Serie A",
        "fr Ligue 1": "Ligue 1",
        "de Bundesliga": "Bundesliga"
    }

    df_players = df_players.copy()
    df_players["Comp"] = df_players["Comp"].replace(equivalencias)

    return df_players

# %% [markdown]
# ## 8. Normalizar nombres de clubes
# 
# Utiliza el diccionario construido durante la comprobación del proyecto.

# %%
def normalizar_clubes(df_players, clubes):
    df_players = df_players.copy()
    df_players["Squad"] = df_players["Squad"].replace(clubes)

    return df_players

# %% [markdown]
# ## 9. Preparar las columnas numéricas de lesiones
# 
# `Days` llega como texto, por ejemplo `14 days`, y se convierte a entero para poder sumar los días de baja.

# %%
def preparar_datos_lesiones(df_injuries):
    df_injuries = df_injuries.copy()

    df_injuries["Days"] = (
        df_injuries["Days"]
        .str.replace(" days", "", regex=False)
        .astype(int)
    )

    return df_injuries

# %% [markdown]
# ## 10. Agrupar lesiones por jugador y club

# %%
def agrupar_lesiones(df_injuries):
    return (
        df_injuries
        .groupby(["player_name", "club"])[["Days", "Games missed"]]
        .sum()
        .reset_index()
    )

# %% [markdown]
# ## 11. Unir jugadores y lesiones
# 
# Se utiliza un `left merge` para conservar todos los jugadores aunque no tengan registros de lesiones.

# %%
def unir_players_lesiones(df_players, df_injuries_agg):
    df_final = df_players.merge(
        df_injuries_agg,
        left_on=["Player", "Squad"],
        right_on=["player_name", "club"],
        how="left"
    )

    df_final[["Days", "Games missed"]] = (
        df_final[["Days", "Games missed"]].fillna(0)
    )

    return df_final.drop(columns=["club", "player_name"])

# %% [markdown]
# ## 12. Diccionario de normalización de clubes
# 
# Se mantiene separado para que sea fácil ampliarlo si aparecen nuevos nombres diferentes.

# %%
clubes = {
    "Saint-Étienne": "Saint-Etienne",
    "Alavés": "Deportivo Alaves",
    "Milan": "AC Milan",
    "Freiburg": "SC Freiburg",
    "Dortmund": "Borussia Dortmund",
    "Leverkusen": "Bayer Leverkusen",
    "St Pauli": "FC St. Pauli",
    "Athletic Club": "Athletic Bilbao",
    "Nottingham": "Nottingham Forest",
    "Newcastle": "Newcastle United",
    "Leganés": "Leganes",
    "West Ham": "West Ham United",
    "Atlético Madrid": "Atletico Madrid",
    "Manchester Utd": "Manchester United",
    "Frankfurt": "Eintracht Frankfurt",
    "Wolfsburg": "VfL Wolfsburg",
    "Paris SG": "Paris Saint-Germain",
    "Tottenham": "Tottenham Hotspur",
    "Bochum": "VfL Bochum",
    "Heidenheim": "FC Heidenheim",
    "Stuttgart": "VfB Stuttgart",
    "Gladbach": "Borussia Monchengladbach"
}


