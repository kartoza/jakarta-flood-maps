CREATE OR REPLACE FUNCTION time_slices_{{NUMBER_OF_HOURS}}_hours(now TIMESTAMP)
RETURNS TABLE(start_time TIMESTAMP, end_time TIMESTAMP)
AS $$
SELECT min(start_time), max(end_time) FROM
    (
    SELECT
      start_time, start_time + INTERVAL '{{NUMBER_OF_HOURS}} hours' as end_time
    FROM (
        SELECT generate_series(
            now - INTERVAL '{{NUMBER_OF_HOURS}} hours',
            now,
            '{{NUMBER_OF_HOURS}} hours'
        ) AS start_time
  ) x order by end_time desc limit 4 offset 1) y
  $$ LANGUAGE SQL;

WITH currently_reported AS (
  SELECT
    flood_mapper_rw.geometry AS geo,
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
    select start_time from time_slices_{{NUMBER_OF_HOURS}}_hours(cast('{{DATE_TIME_NOW}}' as TIMESTAMP)))
  AND
    flood_mapper_floodstatus.date_time <= (
    select end_time from time_slices_{{NUMBER_OF_HOURS}}_hours(cast('{{DATE_TIME_NOW}}' as TIMESTAMP)))
)
  SELECT temp.*
  INTO REPORT_{{NUMBER_OF_HOURS}}_HOUR_TEMP
  FROM currently_reported temp
  INNER JOIN
      (SELECT rw_id, MAX(date_time) AS max_date_time
      FROM currently_reported
      GROUP BY rw_id) grouped_temp
  ON temp.rw_id = grouped_temp.rw_id
  AND temp.date_time = grouped_temp.max_date_time;

