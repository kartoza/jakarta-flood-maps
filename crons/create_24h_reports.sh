NUMBER_OF_HOURS=24
DATE_TIME_LABEL="$(date -d 'yesterday' +'%F')"
DATE_TIME_NOW="$(date +'%F') 00:00:00.0"

# DROP TEMP TABLE
SQL_CLEANUP_QUERY=$(sed ':a;N;$!ba;s/\n/ /g' ../sql/report_cleanup.sql)
SQL_CLEANUP_QUERY="${SQL_CLEANUP_QUERY//'{{NUMBER_OF_HOURS}}'/$NUMBER_OF_HOURS}"
psql -p 6543 -U docker -h localhost gis -c "$SQL_CLEANUP_QUERY"

# CREATE TEMP TABLE
SQL_QUERY=$(sed ':a;N;$!ba;s/\n/ /g' ../sql/report_table_create.sql)
SQL_QUERY="${SQL_QUERY//'{{NUMBER_OF_HOURS}}'/$NUMBER_OF_HOURS}"
SQL_QUERY="${SQL_QUERY//'{{DATE_TIME_NOW}}'/$DATE_TIME_NOW}"
psql -p 6543 -U docker -h localhost gis -c "$SQL_QUERY"

# CREATE SHP FROM TEMP TABLE
SQL_SELECT="SELECT * FROM report_{{NUMBER_OF_HOURS}}_hour_temp;"
SQL_SELECT="${SQL_SELECT/'{{NUMBER_OF_HOURS}}'/$NUMBER_OF_HOURS}"
pgsql2shp -f ../reports/shp/24h/$DATE_TIME_LABEL.shp \
    -p 6543 -P docker -u docker -h localhost \
    -r gis "$SQL_SELECT"

# Zip all shp file files into one
find ../reports/shp/24h/$DATE_TIME_LABEL.* -path -prune -o -type f -print | zip ../reports/shp/24h/$DATE_TIME_LABEL.zip -@ -j

# GENERATE OTHER FORMATS
ogr2ogr -f "KML" ../reports/kml/24h/$DATE_TIME_LABEL.kml ../reports/shp/24h/$DATE_TIME_LABEL.shp
ogr2ogr -f "CSV" ../reports/csv/24h/$DATE_TIME_LABEL.csv ../reports/shp/24h/$DATE_TIME_LABEL.shp
ogr2ogr -f "SQLite" ../reports/sqlite/24h/$DATE_TIME_LABEL.sqlite ../reports/shp/24h/$DATE_TIME_LABEL.shp
