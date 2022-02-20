# Machine Learning meets NFL Fantasy Football

This repository deals with NFL fantasy football and its connection to
machine learning and data analysis.

Most of the code is based on the course *Learn Python with Fantasy Football*
written by Ben Dominguez and hosted by Fantasy Football Data Pros (FFDP). 
It deals with simple data analysis techniques and machine learning approaches
to
* predict fantasy performance of players,
* play-by-play analysis and
* in-season analysis.

Based on this code snippets, more powerful analysis tools should be developed
and hopefully applied for my team in our dynasty fantasy league.

## TODO

### Draft 

- Establish ranking scheme for QB, RB, WR, TE based on recent progress 
  - Rookies: take ECR
  - Experienced: three years experience, weight recent years more
  - Veterans: more than three years experience, weight recent years more
  - Scheme:
    - Define stats for each position
    - Weight each stat different
    - Try to minimize, e.g. rushing attempts + rushing yards = yards/attempt
  - Cluster ranking and check with expert ranking

### In season
