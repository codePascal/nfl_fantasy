###############################################################################
# get weekly stats
#
# Gets weekly stats from https://www.fantasypros.com/nfl/stats/ for all
# positions QB, RB, WR, TE, K, DST.
#
# Usage example:
# ./get_weekly_stats.sh year weeks
# ./get_weekly_stats.sh 2021 18
###############################################################################

if [ -z "$2" ]
  then
    echo "Incorrect number of arguments."
fi

positions="qb rb wr te k dst"
for ((i = 1; i <= $2; i++))
  do
    for position in $positions
      do
        python ../scraper/stats_scraper.py $1 $position --week $i
    done
done
