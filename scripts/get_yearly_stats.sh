###############################################################################
# get yearly stats
#
# Gets yearly stats from https://www.fantasypros.com/nfl/stats/ for all
# positions QB, RB, WR, TE, K, DST.
#
# Usage example:
# ./get_weekly_stats.sh year
# ./get_weekly_stats.sh 2021
###############################################################################

if [ -z "$1" ]
  then
    echo "Incorrect number of arguments."
fi

positions="qb rb wr te k dst"
for position in $positions
  do
    python ../utils/stats_scraper.py $1 $position
done
