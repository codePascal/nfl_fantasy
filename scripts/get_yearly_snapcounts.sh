###############################################################################
# get yearly snapcounts
#
# Gets yearly snapcounts from
# https://www.fantasypros.com/nfl/reports/snap-count-analysis/ for the offense.
#
# Usage example:
# ./get_yearly_snapcounts.sh year
# ./get_yearly_snapcounts.sh 2021
###############################################################################

if [ -z "$1" ]
  then
    echo "Incorrect number of arguments."
fi

python ../scraper/snapcounts_scraper.py $1
