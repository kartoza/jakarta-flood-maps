
SQL_QUERY=$(sed ':a;N;$!ba;s/\n/ /g' ../sql/report6h.sql)
echo $SQL_QUERY
# SQL_QUERY="select * from flood_mapper_rw"
pgsql2shp -f test.shp -p 6543 -P docker -u docker -h localhost gis "$SQL_QUERY"

## Log into psql
# psql -p 6543 -U docker -h localhost gis
