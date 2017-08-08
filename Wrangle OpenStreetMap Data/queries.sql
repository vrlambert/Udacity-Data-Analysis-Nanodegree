-- Total number of nodes
SELECT COUNT(*) FROM nodes

-- Total number of ways
SELECT COUNT(*) FROM ways

-- Return distinct number of users
SELECT COUNT(DISTINCT(combined.uid))
  FROM
    (SELECT uid FROM nodes
    UNION ALL
    SELECT uid FROM ways) combined;

-- total number of shops
SELECT COUNT(*)
  FROM (SELECT key FROM nodes_tags
        UNION ALL
        SELECT key FROM ways_tags) combined
  WHERE key = "shop";

-- top several keys
SELECT key, count(*) as num
FROM nodes_tags
GROUP BY key
ORDER BY num DESC
LIMIT 20;

-- top 10 amenities
SELECT nodes_tags.value, COUNT(*) as num
  FROM nodes_tags
  WHERE key = 'amenity'
  GROUP BY value
  ORDER BY num DESC
  LIMIT 10;

-- top fast_food
SELECT nodes_tags.value, count(*) as num
  FROM nodes_tags
  JOIN (SELECT DISTINCT(id)
        FROM nodes_tags
        WHERE value = 'fast_food') as ff
        ON nodes_tags.id = ff.id
  WHERE nodes_tags.key = 'name'
  GROUP BY nodes_tags.value
  ORDER BY num DESC
  LIMIT 10;

-- most common nature things
SELECT value, count(*) as num
  FROM nodes_tags
  WHERE key = 'natural'
  GROUP BY value
  ORDER BY num DESC;

-- Find the name of the rock
SELECT nodes_tags.value
  FROM nodes_tags
  JOIN (SELECT DISTINCT(id)
        FROM nodes_tags
        WHERE value = 'rock') as rock
        ON nodes_tags.id = rock.id
  WHERE nodes_tags.key = 'name';

-- top users in nodes
SELECT user, count(*) AS num
FROM nodes
GROUP BY uid
ORDER BY num DESC
LIMIT 10;
