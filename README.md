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

usage: migrate [-h] [-e {postgres,mysql,sqlite3}] [-r REV] [-m MESSAGE]
               [-u USER] [-p] [--host HOST] [--port PORT] [-db DATABASE]
               [--path PATH] [-f CONFIG] [--env ENV] [-v]
               {new,run,rollback,reset,refresh}

Manage database migrations explicitly using SQL scripts

positional arguments:
  {new,run,rollback,reset,refresh}
                        command to run (default: "new")

optional arguments:
  -h, --help            show this help message and exit
  -e {postgres,mysql,sqlite3}
                        database engine (default: "sqlite3")
  -r REV                revision to use. specify "0" for the next revision if
                        using the "new" command. this option applies to only
                        the "new" and (default: last revision)
  -m MESSAGE            message description for creating new migrations with
                        "new" command
  -u USER               database user name (default: login name)
  -p                    prompt for database password. if not supplied assumes
                        no password unless read from config
  --host HOST           database server host (default: "localhost")
  --port PORT           server port (defaults: postgres=5432, mysql=3306)
  -d DATABASE           database name to use. specify a /path/to/file if using
                        sqlite3. (default: login name)
  --path PATH           path to the migration folder either absolute or
                        relative to the current directory. defaults to
                        "migrations" in current working directory
  -f CONFIG             configuration file in ".ini" format. Sections
                        represent configurations for different environments.
                        Keys include (migration_path, user, password, host,
                        port, database, engine)
  --env ENV             configuration environment. used only with config file
                        as the given sections (default: "default")
  -v                    show verbose output. use multiple times for different
                        verbosity levels
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
$ migrate run -e sqlite3 -d /path/to/test.db
```

rolling back
```sh
$ migrate rollback -e sqlite3 -d /path/to/test.db
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
| new      | add a new migration. specify "-r 0" to create a new revision |
| run      | Run the migration for the latest revision  |
| rollback | Rollback migration for the last or a target revision |
| reset    | Rollback all migrations |
| refresh  | Rollback all migrations and run them all again |


## license
The MIT License (MIT) Copyright (c) 2014 Francis Asante

