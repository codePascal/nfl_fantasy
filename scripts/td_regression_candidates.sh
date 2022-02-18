###############################################################################
# touchdown regression candidates
#
# Calculates regression candidates for touchdowns for given year on all
# offense positions in terms of receiving, passing and rushing.
#
# Usage example:
# td_regression_candidates.sh year
# td_regression_candidates.sh 2021
###############################################################################

# check args
if [ -z "$1" ]
  then
    echo "Incorrect number of arguments."
fi

# QB: passing, rushing
for play in pass rush
  do
    python ../tools/td_regression_candidates.py $1 $play QB
done

# RB: rushing, receiving
for play in pass rec
  do
    python ../tools/td_regression_candidates.py $1 $play RB
done

# WR: receiving
for play in rec
  do
    python ../tools/td_regression_candidates.py $1 $play WR
done

# TE: receiving
for play in rec
  do
    python ../tools/td_regression_candidates.py $1 $play TE
done