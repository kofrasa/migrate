# migrate

A simple generic database migration tool eschewing boilerplate and framework dependencies


## install
clone and install to reachable bin PATH
```
$ git clone https://github.com/kofrasa/migrate.git
$ cp migrate/migrate /usr/local/bin
```


## usage
```sh
$ ./migrate -h

usage: migrate [-h] [-c {create,migrate,rollback,reset,refresh}]
               [-e {postgres,mysql,sqlite3}] [-r REV] [-m MESSAGE] [-u USER]
               [-p] [--host HOST] [--port PORT] [-db DATABASE] [--path PATH]
               [-f CONFIG] [--env ENV] [-v]

Manage database migrations explicitly using SQL scripts

optional arguments:
  -h, --help            show this help message and exit
  -c {create,migrate,rollback,reset,refresh}
                        command to run (default: "create")
  -e {postgres,mysql,sqlite3}
                        database engine (default: "sqlite3")
  -r REV                revision to use. specify "0" for the next revision if
                        using the "create" command (default: last revision)
  -m MESSAGE            message description for creating new migrations with
                        "create" command
  -u USER               database user name (default: login_name)
  -p                    prompt for database password. if not supplied assumes
                        no password unless read from config
  --host HOST           database server host (default: "localhost")
  --port PORT           server port (defaults: postgres=5432, mysql=3306)
  -db DATABASE          database name to use. specify a /path/to/file if using
                        sqlite3
  --path PATH           path to the migration folder either absolute or
                        relative to the current directory. default to
                        migrations folder in current directory:
                        /path/to/current/migrations
  -f CONFIG             configuration file in ".ini" format. Sections
                        represent configurations for different environments.
                        Keys include (migration_folder, user, password, host,
                        port, database, engine)
  --env ENV             configuration environment. used only with config file
                        as the given sections (default: "default")
  -v                    show verbose output
```

move into working directory and create default migrations folder
```sh
$ cd /path/to/working/directory
$ mkdir migrations
```
creating migrations with sqlite3
```sh
$ ./migrate -e sqlite3 -c create -db /path/to/test.db -m "create users table"
```
this generates the up and down files using the current timestamp and formatted description in sub revision folder
```
$ ls -R migrations/
1

migrations//1:
20141215134002.create-users-table.down.sql	20141215134002.create-users-table.up.sql
```

applying migrations
```sh
$ ./migrate -e sqlite3 -c migrate -db /path/to/test.db
```

rolling back
```sh
$ ./migrate -e sqlite3 -c rollback -db /path/to/test.db
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

execute with configuration for a particular revision
```sh
$ ./migrate -f config.ini -c refresh --env prod
```

## commands
| Command  | Description  |
| :--------| :----------- |
| create   | create a new migration. specify "-r 0" for a new revision |
| migrate  | Run migration for the latest revision  |
| rollback | Rollback the migration for the last revision |
| reset    | Rollback all migrations |
| refresh  | Rollback all migrations and run them all again |


## license
The MIT License (MIT) Copyright (c) 2014 Francis Asante

