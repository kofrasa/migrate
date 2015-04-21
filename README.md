migrate
=======

A simple language agnostic database migration tool

Migrations are applied in batches called a revision. A revision is represented by a folder named
in consecutive numerical order, starting from **"1"**. Each revision contains pairs of migration scripts
with extensions **.up.sql** and **.down.sql** for upgrading and downgrading the database respectively.

install
-------
```sh
$ pip install migrate
```

usage
-----

```sh
usage: migrate [options] <command>
```

examples
--------
move into working directory and create default migrations folder

```sh
$ cd /path/to/project
$ mkdir migrations
```

creating a migration

```sh
$ migrate create -e sqlite3 -d /path/to/test.db -m "create users table"
```

this generates the up and down files using the current timestamp and message in the current revision folder
```sh
$ ls -R migrations/
1

migrations//1:
20141215134002_create_users_table.down.sql	20141215134002_create_users_table.up.sql
```

upgrading from current revision

```sh
    $ migrate up -e sqlite3 -d test.db
```

rolling back current revision

```sh
$ migrate down -e sqlite3 -d test.db
```

running with sample configuration example: config.ini

```
[dev]
database = /path/to/test.db
engine = sqlite3

[prod]
migration_path = /path/to/prod/migrations
database = DB_NAME
user = DB_USER
password = DB_PASSWORD
host = DB_HOST
engine = ENGINE
```

execute with configuration for a particular revision using a preferred environment

```sh
$ migrate reset -f config.ini --env prod
```

you may put a *.migrate* configuration file in INI format in your project directory to be used by default

commands
--------
| Command | Description |
| ------- | ----------- |
| create  | Create a migration. Specify "--rev 0" to add a new revision |
| up      | Upgrade from a revision to the latest |
| down    | Downgrade from the latest to a lower revision |
| reset   | Rollback and re-run to the current revision |

Any migration operation will stop when errors are encountered in any of the scripts. To ignore errors use the
*--skip-errors* option.

For more options

```sh
$ migrate -h
```

license
-------
MIT