#!/opt/local/bin/bash
export LANG="${LANG:-en_AU.UTF-8}"
TMPALL=$(mktemp -t weather.XXXXXXXXXX)
TMPPER=$(mktemp -t perth.XXXXXXXXXX)

function clean_up {
	# Perform program exit housekeeping
	rm $TMPALL
	rm $TMPPER
	trap 0  # reset to default action
	exit
}
trap clean_up 0 1 2 3 15

curl "http://www.bom.gov.au/wa/observations/perth.shtml" 2>/dev/null 1>$TMPALL
grep "tPERTH-station-perth\"" $TMPALL > $TMPPER 
TIME=$(cat $TMPPER | grep tPERTH-datetime | sed 's/<[^>]*>//g' | tr -d ' ' | sed 's/[^ ]*\///')
TEMP=$(cat $TMPPER | grep tPERTH-tmp | sed 's/<[^>]*>//g' | tr -d ' ')
APPTEMP=$(cat $TMPPER | grep tPERTH-apptmp | sed 's/<[^>]*>//g' | tr -d ' ')
HUMID=$(cat $TMPPER | grep tPERTH-relhum | sed 's/<[^>]*>//g' | tr -d ' ')
PRESS=$(cat $TMPPER | grep tPERTH-press | sed 's/<[^>]*>//g' | tr -d ' ')
WINDDIR=$(cat $TMPPER | grep tPERTH-wind-dir | sed 's/<[^>]*>//g' | tr -d ' ')
WINDSPD=$(cat $TMPPER | grep tPERTH-wind-spd-kmh | sed 's/<[^>]*>//g' | tr -d ' ')
RAIN=$(cat $TMPPER | grep tPERTH-rainsince9am | sed 's/<[^>]*>//g' | tr -d ' ')
LOWT=$(cat $TMPPER | grep tPERTH-lowtmp | sed 's/<small>/\\u00b0C @ /' | sed 's/<[^>]*>//g' | sed -e 's/^[ \t]*//' )
HIGHT=$(cat $TMPPER | grep tPERTH-hightmp | sed 's/<small>/\\u00b0C @ /' | sed 's/<[^>]*>//g' | sed -e 's/^[ \t]*//' )
echo -e "${TEMP}\u00b0C"
echo "---"
echo "Perth Observations at ${TIME} | color=black"
echo -e "Current: ${TEMP}\u00b0C | color=dimgray"
echo -e "Feels like: ${APPTEMP}\u00b0C | color=dimgray"
echo -e "Humidity: ${HUMID}% | color=dimgray"
echo -e "Pressure: ${PRESS} hPa | color=dimgray"
echo -e "Wind: ${WINDDIR} @ ${WINDSPD} kmh | color=dimgray"
echo -e "Rain since 9am: ${RAIN} mm | color=dimgray"
echo -e "Minimum: ${LOWT} | color=dimgray"
echo -e "Maximum: ${HIGHT} | color=dimgray"


