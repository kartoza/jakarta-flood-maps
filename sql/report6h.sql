CREATE OR REPLACE FUNCTION time_slices(now TIMESTAMP, hours int)
RETURNS TABLE(start_time TIMESTAMP, end_time TIMESTAMP)
AS $$
SELECT min(start_time), max(end_time) FROM
    (
    SELECT
      start_time, start_time + (hours || ' hours')::INTERVAL as end_time
    FROM (
        SELECT generate_series(
            now - (hours || ' hours')::INTERVAL,
            now,
            (hours || ' hours')::INTERVAL
        ) AS start_time
  ) x order by end_time desc limit 4 offset 1) y
  $$ LANGUAGE SQL;

WITH currently_reported AS (
  SELECT
    flood_mapper_rw.geometry AS geometry,
    flood_mapper_floodstatus.depth AS depth,
    flood_mapper_floodstatus.date_time AS date_time,
    flood_mapper_rw.id AS rw_id
  FROM
    flood_mapper_floodstatus
  JOIN
    flood_mapper_rt
  ON
    flood_mapper_floodstatus.rt_id=flood_mapper_rt.id
  JOIN
    flood_mapper_rw
  ON
    flood_mapper_rt.rw_id=flood_mapper_rw.id
  WHERE
    flood_mapper_floodstatus.date_time >= (
    select start_time from time_slices (cast(now() as TIMESTAMP), 6))
  AND
    flood_mapper_floodstatus.date_time <= (
    select end_time from time_slices(cast(now() as TIMESTAMP), 6))
)
SELECT temp.*
FROM currently_reported temp
INNER JOIN
    (SELECT rw_id, MAX(date_time) AS max_date_time
    FROM currently_reported
    GROUP BY rw_id) grouped_temp
ON temp.rw_id = grouped_temp.rw_id
AND temp.date_time = grouped_temp.max_date_time;
