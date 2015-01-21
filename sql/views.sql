DROP VIEW vw_events;
CREATE OR REPLACE VIEW vw_events AS
SELECT
  flood_mapper_floodstatus.id,
  flood_mapper_village.name as village,
  flood_mapper_rw.name as rw,
  flood_mapper_rw.geometry as rw_geom,
  flood_mapper_rt.name as rt,
  flood_mapper_rt.geometry as rt_geom,
  flood_mapper_floodstatus.date_time as event_date,
  flood_mapper_floodstatus.reporter_name,
  flood_mapper_floodstatus.notes,
  flood_mapper_floodstatus.name,
  flood_mapper_floodstatus.depth
FROM
  public.flood_mapper_rt,
  public.flood_mapper_rw,
  public.flood_mapper_floodstatus,
  public.flood_mapper_village
WHERE
  flood_mapper_rt.rw_id = flood_mapper_rw.id AND
  flood_mapper_rw.village_id = flood_mapper_village.id AND
  flood_mapper_floodstatus.rt_id = flood_mapper_rt.id;
