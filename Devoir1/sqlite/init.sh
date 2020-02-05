rm devoir1.db
sqlite3 devoir1.db < create.sql
# cat -n data.sql | sort -uk2 | sort -nk1 | cut -f2- > data.sql
sqlite3 devoir1.db < data.sql
