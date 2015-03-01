#!/bin/sh
NUMBER_OF_HOURS=6;

if [ $(date +'%H') -gt 18 ]; then
    HOUR=18;
else
   if [ $(date +'%H') -gt 12 ]; then
        HOUR=12;
    else
        if [ $(date +'%H') -gt 6 ]; then
            HOUR=6;
        else
            HOUR=0;
        fi
    fi
fi

DATE_TIME_LABEL="$(date +'%F')-$HOUR";
if [ $HOUR == 0 ]; then
    DATE_TIME_START="$(date -d 'yesterday' +'%F')-18:00:00.0"
else
    DATE_TIME_START="$(date +'%F')-$(HOUR-6):00:00.0"
fi
DATE_TIME_NOW="$(date +'%F') $HOUR:00:00.0";

# DROP TEMP TABLE
SQL_CLEANUP_QUERY=$(sed ':a;N;$!ba;s/\n/ /g' ./report_cleanup.sql)
SQL_CLEANUP_QUERY="${SQL_CLEANUP_QUERY//'{{NUMBER_OF_HOURS}}'/$NUMBER_OF_HOURS}"
psql -c "$SQL_CLEANUP_QUERY"

# CREATE TEMP TABLE
SQL_QUERY=$(sed ':a;N;$!ba;s/\n/ /g' ./report_table_create.sql)
SQL_QUERY="${SQL_QUERY//'{{NUMBER_OF_HOURS}}'/$NUMBER_OF_HOURS}"
SQL_QUERY="${SQL_QUERY//'{{DATE_TIME_NOW}}'/$DATE_TIME_NOW}"
psql -c "$SQL_QUERY"

# CREATE SHP FROM TEMP TABLE
SQL_SELECT="SELECT * FROM FLOOD_MAPPER_FLOODSTATUS_{{NUMBER_OF_HOURS}}H;"
SQL_SELECT="${SQL_SELECT/'{{NUMBER_OF_HOURS}}'/$NUMBER_OF_HOURS}"
pgsql2shp -f /home/web/reports/shp/6h/$DATE_TIME_LABEL.shp gis "$SQL_SELECT"

# Zip all shp file files into one
find /home/web/reports/shp/6h/$DATE_TIME_LABEL.* -path -prune -o -type f -print | zip /home/web/reports/shp/6h/$DATE_TIME_LABEL.zip -@ -j

# GENERATE OTHER FORMATS
ogr2ogr -f "KML" /home/web/reports/kml/6h/$DATE_TIME_LABEL.kml /home/web/reports/shp/6h/$DATE_TIME_LABEL.shp
ogr2ogr -f "CSV" /home/web/reports/csv/6h/$DATE_TIME_LABEL.csv /home/web/reports/shp/6h/$DATE_TIME_LABEL.shp
ogr2ogr -f "SQLite" /home/web/reports/sqlite/6h/$DATE_TIME_LABEL.sqlite /home/web/reports/shp/6h/$DATE_TIME_LABEL.shp


# GENERATE THE PDF REPORT
DISPLAY=:99 python /home/web/cron-scripts/pdf_report_generator.py 6h $DATE_TIME_START $DATE_TIME_NOW $DATE_TIME_LABEL
