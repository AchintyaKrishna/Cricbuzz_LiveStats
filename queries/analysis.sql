-- Total matches
SELECT COUNT(*) FROM matches;

-- Matches per venue
SELECT venue_id, COUNT(*) as total_matches
FROM matches
GROUP BY venue_id
ORDER BY total_matches DESC;

-- Matches per team (team1)
SELECT t.team_name, COUNT(*) as matches_played
FROM matches m
JOIN teams t ON m.team1_id = t.team_id
GROUP BY t.team_name;

-- Matches per team (team2)
SELECT t.team_name, COUNT(*) as matches_played
FROM matches m
JOIN teams t ON m.team2_id = t.team_id
GROUP BY t.team_name;

-- Rank of Team by Matches count
SELECT 
    team_name,
    COUNT(*) as matches_played,
    RANK() OVER (ORDER BY COUNT(*) DESC) as rank
FROM (
    SELECT team1_id as team_id FROM matches
    UNION ALL
    SELECT team2_id FROM matches
) m
JOIN teams t ON m.team_id = t.team_id
GROUP BY team_name;

-- Difference when no gap
SELECT 
    team_name,
    COUNT(*) as matches_played,
    DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) as rank
FROM (
    SELECT team1_id as team_id FROM matches
    UNION ALL
    SELECT team2_id FROM matches
) m
JOIN teams t ON m.team_id = t.team_id
GROUP BY team_name;

-- Unique Order for Pagination
SELECT 
    match_id,
    ROW_NUMBER() OVER (ORDER BY match_id) as row_num
FROM matches;

-- Matches count total running
SELECT 
    match_id,
    COUNT(*) OVER (ORDER BY match_id) as running_total
FROM matches;

-- Top match per team
SELECT *
FROM (
    SELECT 
        t.team_name,
        m.match_id,
        ROW_NUMBER() OVER (PARTITION BY t.team_name ORDER BY m.match_id DESC) as rn
    FROM matches m
    JOIN teams t ON m.team1_id = t.team_id
) sub
WHERE rn = 1;

-- Recent Performance
SELECT player_name,
       AVG(runs) AS avg_runs,
       AVG(strike_rate) AS avg_sr
FROM performance
WHERE match_type = 'T20'
GROUP BY player_name
ORDER BY avg_runs DESC;

-- Consistency Score
SELECT player_name,
       COUNT(*) AS matches,
       AVG(runs) AS avg_runs,
       (AVG(runs) * COUNT(*)) AS consistency_score
FROM performance
GROUP BY player_name
ORDER BY consistency_score DESC;

-- Format Specialist
SELECT player_name,
       match_type,
       AVG(runs) AS avg_runs
FROM performance
GROUP BY player_name, match_type;

-- Top Finishers
SELECT player_name,
       AVG(runs) AS avg_runs
FROM performance
GROUP BY player_name
HAVING avg_runs > 30
ORDER BY avg_runs DESC;

-- Best Strike Rate
SELECT player_name,
       AVG(strike_rate) AS sr
FROM performance
GROUP BY player_name
ORDER BY sr DESC;