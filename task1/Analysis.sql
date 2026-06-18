SELECT
    al.title AS album,
    ar.name AS artist,
    COUNT(*) AS listens
FROM listening_logs l
JOIN songs s ON s.song_id = l.song_id
JOIN albums al ON al.album_id = s.album_id
JOIN song_artists sa ON sa.song_id = s.song_id
JOIN artists ar ON ar.artist_id = sa.artist_id
JOIN song_genres sg ON sg.song_id = s.song_id
JOIN genres g ON g.genre_id = sg.genre_id
WHERE g.name = 'Rock'
GROUP BY al.album_id, ar.artist_id
ORDER BY listens DESC LIMIT 1;

SELECT
    a.name AS artist,
    COUNT(*) AS top_songs
FROM artists a
JOIN song_artists sa ON a.artist_id = sa.artist_id
WHERE sa.song_id IN (
    SELECT song_id
    FROM listening_logs
    GROUP BY song_id
    ORDER BY COUNT(*) DESC
    LIMIT (
        SELECT COUNT(DISTINCT song_id) / 5
        FROM songs
    )
)
GROUP BY a.artist_id, a.name
ORDER BY top_songs DESC
LIMIT 1;


SELECT
    al.title AS album,
    ar.name AS artist,
    COUNT(*) AS collab_count
FROM albums al
JOIN artists ar ON al.artist_id = ar.artist_id
JOIN songs s ON al.album_id = s.album_id
WHERE s.song_id IN (
    SELECT song_id
    FROM song_artists
    GROUP BY song_id
    HAVING COUNT(*) > 1
)
GROUP BY al.album_id, al.title, ar.name
ORDER BY collab_count DESC
LIMIT 1;

SELECT
    strftime('%Y-%m', listen_time) AS year_month,
    COUNT(*) AS total_listens
FROM listening_logs
GROUP BY strftime('%Y-%m', listen_time)
ORDER BY year_month;

SELECT
    g.name AS genre,
    l.region AS region,
    COUNT(*) AS total_listens
FROM listening_logs l
JOIN song_genres sg ON l.song_id = sg.song_id
JOIN genres g ON sg.genre_id = g.genre_id
GROUP BY g.name, l.region
ORDER BY genre, region;
