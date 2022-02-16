###############################################################################
# get weekly projections
#
# Gets weekly projections for each position from
# https://www.fantasypros.com/nfl/projections/.
#
# Usage example:
# ./get_weekly_projections.sh weeks
# ./get_weekly_projections.sh 18
###############################################################################

if [ -z "$1" ]
  then
    echo "Incorrect number of arguments."
fi

positions="qb rb wr te k dst"
for ((i = 1; i <= $1; i++))
  do
    for position in $positions
      do
        python ../scraper/projections_scraper.py $position $i
    done
done
