# migrate

A simple generic database migration tool eschewing boilerplate and framework dependencies

Migrations are applied in batches called a revision. A revision is represented by a folder named
in consecutive numerical order, starting from **"1"**. Each revision contains pairs of migration scripts
with extensions **.up.sql** and **.down.sql** for upgrading and downgrading the database respectively. 

Any migration operation will run with all files regardless of errors reported by the specified database engine.
All errors including the ones from the database engine are sent to **stderr**.

## install
clone and install
```sh
$ git clone https://github.com/kofrasa/migrate.git
$ cp migrate
$ make install
```

uninstall with
```sh
$ make uninstall
```

## usage
```sh
$ migrate -h

usage: migrate.py [-h] [-e {postgres,mysql,sqlite3}] [-r REV] [-m MESSAGE]
                  [-u USER] [-p] [--host HOST] [--port PORT] [-d DATABASE]
                  [--path PATH] [-f CONFIG] [--env ENV] [-v]
                  {create,up,down,reset,refresh}
```

## examples
move into working directory and create default migrations folder
```sh
$ cd /path/to/working/directory
$ mkdir migrations
```

creating migrations with sqlite3
```sh
$ migrate create -e sqlite3 -d /path/to/test.db -m "create users table"
```

this generates the up and down files using the current timestamp and formatted description in the current revision folder
```
$ ls -R migrations/
1

migrations//1:
20141215134002.create-users-table.down.sql	20141215134002.create-users-table.up.sql
```

upgrading from current revision
```sh
$ migrate up -e sqlite3 -d /path/to/test.db
```

rolling back current revision
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
| create   | Create a migration. Specify "-r 0" to add a new revision |
| up       | Upgrade the latest revision  |
| down     | Downgrade the last or to the target revision |
| reset    | Downgrade all revisions |
| refresh  | Downgrade and re-run all revisions |


## license
MIT

