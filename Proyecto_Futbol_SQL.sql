USE estadísticas_futbol;

SET SQL_SAFE_UPDATES = 0;

UPDATE liga
SET season = '24/25'
WHERE season = '2024-25';

UPDATE liga
SET season = '23/24'
WHERE season = '2023-24';

SET SQL_SAFE_UPDATES = 1;


DESCRIBE liga;

-- 1. ¿Cuáles son los 5 mejores equipos de las temporadas 2023-24 y 2024-25?

SELECT
    l1.season,
    l1.club,
    l1.points,
    l1.goals_for,
    l1.goals_against
FROM liga AS l1
WHERE (
    SELECT COUNT(*)
    FROM liga AS l2
    WHERE l2.season = l1.season
      AND l2.points > l1.points
) < 5
ORDER BY l1.season, l1.points DESC;

-- 2. Calculamos los equipos con mayor avarage de goles

SELECT
    season,
    club,
    points,
    goals_for,
    goals_against,
    goals_for - goals_against AS goal_average
FROM liga
ORDER BY goal_average DESC
LIMIT 20;

-- 3.¿Cuál es la posicion que juega mas minutos?

SELECT
    year AS temporada,
    position AS posicion,
    SUM(Minutes) AS total_minutos
FROM players
GROUP BY year, position
ORDER BY year, total_minutos DESC;

-- 4.¿Qué cinco jugadores acumulan más minutos?
-- TEMPORADA 23/24
SELECT
    year,
    player,
    position,
    club,
    SUM(Minutes) AS total_minutos
FROM players
WHERE year = '23/24'
  AND position <> 'Goalkeeper'
GROUP BY year, player, position,club
ORDER BY total_minutos DESC
LIMIT 5;

-- TEMPORADA 24/25
SELECT
    year,
    player,
    position,
    club,
    SUM(Minutes) AS total_minutos
FROM players
WHERE year = '24/25'
  AND position <> 'Goalkeeper'
GROUP BY year, player, position, club
ORDER BY total_minutos DESC
LIMIT 5;
    
-- 5.¿Qué jugador ha marcado mas goles?
SELECT *
FROM ((SELECT year, player,
SUM(Goals) AS total_goles
FROM players
WHERE year = '23/24'
GROUP BY year, player
ORDER BY total_goles DESC
LIMIT 5
)
UNION ALL
(
SELECT year, player,
SUM(Goals) AS total_goles
FROM players
WHERE year = '24/25'
GROUP BY year, player
ORDER BY total_goles DESC
LIMIT 5
)
) AS maximos_goleadores
ORDER BY total_goles DESC;

-- 6. ¿Qué liga acumula mas lesiones durante las temporadas?
SELECT
    league,
    COUNT(*) AS total_lesiones
FROM injuries
WHERE season IN ('23/24', '24/25')
GROUP BY league
ORDER BY total_lesiones DESC;

-- 7. ¿Qué equipo acumula mas lesiones durante las temporadas?
    
    SELECT
    p.year AS temporada,
    p.club,
    SUM(p.Minutes) AS total_minutos,
    COUNT(i.club) AS total_lesiones
FROM players p
LEFT JOIN injuries i
    ON p.club = i.club
    AND p.year = i.season
GROUP BY
    p.year,
    p.club
ORDER BY
    temporada,
    total_minutos DESC;
    
    
-- 8.¿Los jugadores que disputan más minutos sufren más lesiones?
-- LEFT JOIN: mantiene también a los jugadores que no tienen lesiones registradas.

SELECT
    p.year AS temporada,
    p.player AS jugador,
    SUM(p.Minutes) AS total_minutos,
    COUNT(i.player) AS total_lesiones
FROM players p
LEFT JOIN injuries i
    ON p.player = i.player
    AND p.year = i.season
GROUP BY
    p.year,
    p.player
ORDER BY
    total_minutos DESC;


    
--  9. ¿Cual es la lesión mas frecuente y en qué posición?  
SELECT
    i.injury,
    p.position,
    COUNT(*) AS total_lesiones
FROM injuries i
JOIN players p
    ON i.player = p.player
    AND i.season = p.year
WHERE i.season IN ('23/24', '24/25')
GROUP BY
    i.injury,
    p.position
ORDER BY total_lesiones DESC
LIMIT 10;




-- 10. El ganador de cada liga y luego la cantidad de lesiones que han sufrido

WITH liga_normalizada AS (
    SELECT
        CASE
            WHEN club IN ('Bayer 04 Leverkusen', 'Bayer Leverkusen')
                THEN 'Bayer Leverkusen'
            WHEN club IN ('FC Bayern München', 'Bayern Munich',
                          'Bayern de Múnich', 'Bayern München')
                THEN 'Bayern Munich'
            WHEN club IN ('Paris Saint-Germain FC', 'Paris Saint-Germain',
                          'PSG')
                THEN 'Paris Saint-Germain'
            WHEN club IN ('FC Barcelona', 'Barcelona',
                          'Fútbol Club Barcelona')
                THEN 'Barcelona'
            WHEN club IN ('Manchester City FC', 'Manchester City')
                THEN 'Manchester City'
            WHEN club IN ('Real Madrid CF', 'Real Madrid')
                THEN 'Real Madrid'
            WHEN club IN ('FC Internazionale Milano', 'Inter',
                          'Inter Milan', 'Internazionale')
                THEN 'Inter'
            WHEN club IN ('Liverpool FC', 'Liverpool')
                THEN 'Liverpool'
            WHEN club IN ('SSC Napoli', 'Napoli')
                THEN 'Napoli'
            ELSE club
        END AS club_normalizado,
        league,
        season,
        points
    FROM liga
),
lesiones_normalizadas AS (
    SELECT
        CASE
            WHEN club IN ('Bayer 04 Leverkusen', 'Bayer Leverkusen')
                THEN 'Bayer Leverkusen'
            WHEN club IN ('FC Bayern München', 'Bayern Munich',
                          'Bayern de Múnich', 'Bayern München')
                THEN 'Bayern Munich'
            WHEN club IN ('Paris Saint-Germain FC', 'Paris Saint-Germain',
                          'PSG')
                THEN 'Paris Saint-Germain'
            WHEN club IN ('FC Barcelona', 'Barcelona',
                          'Fútbol Club Barcelona')
                THEN 'Barcelona'
            WHEN club IN ('Manchester City FC', 'Manchester City')
                THEN 'Manchester City'
            WHEN club IN ('Real Madrid CF', 'Real Madrid')
                THEN 'Real Madrid'
            WHEN club IN ('FC Internazionale Milano', 'Inter',
                          'Inter Milan', 'Internazionale')
                THEN 'Inter'
            WHEN club IN ('Liverpool FC', 'Liverpool')
                THEN 'Liverpool'
            WHEN club IN ('SSC Napoli', 'Napoli')
                THEN 'Napoli'
            ELSE club
        END AS club_normalizado,
        season,
        COUNT(*) AS cantidad_lesiones
    FROM injuries
    GROUP BY club_normalizado, season
)

-- COALESCE sirve para devolver el primer valor que no sea NULL de una lista de valores.
SELECT
    l.club_normalizado AS club,
    l.league AS liga,
    l.season AS temporada,
    l.points AS puntos,
    COALESCE(i.cantidad_lesiones, 0) AS cantidad_lesiones
FROM liga_normalizada AS l
LEFT JOIN lesiones_normalizadas AS i
    ON l.club_normalizado = i.club_normalizado
    AND l.season = i.season
WHERE l.club_normalizado IN (
    'Bayer Leverkusen',
    'Bayern Munich',
    'Paris Saint-Germain',
    'Barcelona',
    'Manchester City',
    'Real Madrid',
    'Inter',
    'Liverpool',
    'Napoli'
)
AND l.season IN ('23/24', '24/25')
ORDER BY l.club_normalizado, l.season;