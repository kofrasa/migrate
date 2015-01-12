# migrate

A simple generic database migration tool eschewing boilerplate and framework dependencies

Migrations are applied in a batch called a revision. A revision is represented with a folder named 
in consecutive numerical order, starting from **"1"**, and includes pairs of migration scripts
with extensions **.up.sql** and **.down.sql** for upgrading and downgrading the database respectively. 

Any migration operation will run with all files regardless of errors reported by the specified database engine.
Typically errors from the backing database engine will be sent to stderr as well as errors from the script.

## install
clone and install to user bin PATH
```sh
$ git clone https://github.com/kofrasa/migrate.git
$ cp migrate/migrate.py /usr/local/bin && cd /usr/local/bin
$ ln -s migrate.py migrate
```

## usage
```sh
$ ./migrate -h

usage: migrate.py [-h] [-e {postgres,mysql,sqlite3}] [-r REV] [-m MESSAGE]
                  [-u USER] [-p] [--host HOST] [--port PORT] [-d DATABASE]
                  [--path PATH] [-f CONFIG] [--env ENV] [-v]
                  {new,up,down,reset,refresh}
```

## examples
move into working directory and create default migrations folder
```sh
$ cd /path/to/working/directory
$ mkdir migrations
```

creating migrations with sqlite3
```sh
$ migrate new -e sqlite3 -d /path/to/test.db -m "create users table"
```

this generates the up and down files using the current timestamp and formatted description in the current revision folder
```
$ ls -R migrations/
1

migrations//1:
20141215134002.create-users-table.down.sql	20141215134002.create-users-table.up.sql
```

applying migrations
```sh
$ migrate up -e sqlite3 -d /path/to/test.db
```

rolling back
```sh
$ migrate down -e sqlite3 -d /path/to/test.db
```

running with sample configuration example: config.ini
```
[dev]
database = /path/to/test.db
engine = sqlite3

[prod]
migration_folder = /path/to/prod/migrations
database = superdb
user = francis
password = sUP@^8
host = localhost
engine = mysql
```

execute with configuration for a particular revision using a preferred environment
```sh
$ migrate refresh -f config.ini --env prod
```

## commands
| Command  | Description  |
| :--------| :----------- |
| new      | Add new migration files. specify "-r 0" to create a new revision |
| up       | Upgrade the latest revision  |
| down     | Downgrade the last or to the target revision |
| reset    | Downgrade all revisions |
| refresh  | Downgrade and re-run all revisions |


## license
The MIT License (MIT) Copyright (c) 2014 Francis Asante

