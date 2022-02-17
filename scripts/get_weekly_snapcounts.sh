###############################################################################
# get weekly snapcounts
#
# Gets weekly snapcounts from
# https://www.fantasypros.com/nfl/reports/snap-count-analysis/ for the offense.
#
# Usage example:
# ./get_weekly_snapcounts.sh year weeks
# ./get_weekly_snapcounts.sh 2021 18
###############################################################################

if [ -z "$2" ]
  then
    echo "Incorrect number of arguments."
fi

for ((i = 1; i <= $2; i++))
  do
    python ../scraper/snapcounts_scraper.py $1 --week $i
done
