-- This function will return 4 x 6 hour time blocks for the last 24 hours
CREATE OR REPLACE FUNCTION time_slices_6hr(TIMESTAMP)
  RETURNS TABLE(start_time TIMESTAMP, end_time TIMESTAMP)
  AS $$ SELECT
      start_time, start_time + interval '6 hours' as end_time
      FROM (
          SELECT generate_series(
              $1 - INTERVAL '1 day',
              $1,
              '6 hours'
          ) AS start_time
      ) x order by end_time desc limit 4 offset 1 $$
     LANGUAGE SQL;
COMMENT ON FUNCTION time_slices_6hr(TIMESTAMP) IS '
This function will return 4 x 6 hour time blocks for the last 24 hours
preceding the time block you are currently in. So if you run the query at
9am you will get 6 hour blocks from
 mintime,                   maxtime
"2015-01-04 00:00:00.000000","2015-01-04 06:00:00.000000"
"2015-01-03 18:00:00.000000","2015-01-04 00:00:00.000000"
"2015-01-03 12:00:00.000000","2015-01-03 18:00:00.000000"
"2015-01-03 06:00:00.000000","2015-01-03 12:00:00.000000"';

-- Example query
select * from time_slices_6hr(cast(now() as TIMESTAMP));


-- This function will return the 24 hour time block for the last 24 hours
CREATE OR REPLACE FUNCTION time_slices_24hr(TIMESTAMP)
  RETURNS TABLE(start_time TIMESTAMP, end_time TIMESTAMP)
  AS $$
  SELECT min(start_time), max(end_time) FROM
    (
    SELECT
      start_time, start_time + interval '6 hours' as end_time
    FROM (
        SELECT generate_series(
            $1 - INTERVAL '1 day',
            $1,
            '6 hours'
        ) AS start_time
  ) x order by end_time desc limit 4 offset 1) y $$
     LANGUAGE SQL;

COMMENT ON FUNCTION time_slices_24hr(TIMESTAMP) IS '
This function will return the 24 hour time block for the last 24 hours
excluding the 6 hour time block you are currently in. So if you
run this query at 9am you will get
 mintime,                   maxtime
"2015-01-03 06:00:00.000000","2015-01-04 06:00:00.000000"
';

-- example query
select * from time_slices_24hr(cast(now() as TIMESTAMP));
