# Pagerank
My implementation of the Google pagerank algorithm using a mongoDB map reduce

`import.sh` contains a mongoimport command importing `pages.json` to the `pages` collection in the `Devoir1-pagerank` mongoDB database.

`map_reduce.js` contains the mongo commands to apply the pagerank algorithm 20 times.
It defines the mapping and reducing functions, then it calls `map_reduce` 20 times, replacing the `pages` collection each time.