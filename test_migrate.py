# -*- coding: utf-8 -*-
import os
import shutil
import unittest
import glob
import subprocess
import tempfile
from migrate import Migrate


class MigrateTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(dir=os.getcwd())
        self.config = {
            'path': os.path.join(self.tmp_dir, 'migrations'),
            'database': os.path.join(self.tmp_dir, 'test.db'),
            'engine': 'sqlite3'
        }
        os.mkdir(self.config['path'])

    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def test_create_command(self):
        # need SQL commands so sqlite3 database file can be created
        sql = (
            """CREATE TABLE users (
              id INTEGER PRIMARY KEY ,
              name TEXT,
              email TEXT
            );
            """,
            "DROP TABLE users;"
        )
        self.config['command'] = 'create'
        self.config['message'] = 'users'
        Migrate(**self.config).run()
        rev_folder = os.path.join(self.config['path'], "1")
        # check that all folders have been created
        self.assertTrue(os.path.exists(rev_folder), "revision folder not created")
        # must create 2 files
        self.assertEqual(len(glob.glob(os.path.join(rev_folder, '*'))), 2,
                          "could not create migration files")
        # add some SQL
        for i, s in enumerate(('up', 'down')):
            filename = glob.glob(os.path.join(rev_folder, '*users.%s.sql' % s))[0]
            with open(filename, 'w') as w:
                w.write(sql[i])

    def test_up_command(self):
        self.test_create_command()
        self.config['command'] = 'up'
        Migrate(**self.config).run()
        self.assertTrue(os.path.exists(self.config['database']), 'no database file was created')
        # insert some data to confirm that scripts were applied
        subprocess.check_call(["sqlite3", self.config['database'],
                               "INSERT INTO users VALUES (NULL, 'francis', 'kofrasa@gmail.com');"])
        # query for inserted data
        res = subprocess.check_output(["sqlite3", self.config['database'],
                                       "SELECT COUNT(*) FROM users"])
        self.assertEqual(int(res.strip()), 1, "failed to apply migration scripts")

    def test_down_command(self):
        self.test_up_command()
        self.config['command'] = 'down'
        Migrate(**self.config).run()
        try:
            subprocess.check_call(["sqlite3", self.config['database'], "SELECT * FROM users"])
        except subprocess.CalledProcessError as e:
            self.assertEqual(e.returncode, 1, "failed to rollback database")

    def test_reset_command(self):
        self.test_up_command()
        self.config['command'] = 'reset'
        Migrate(**self.config).run()
        subprocess.check_call(["sqlite3", self.config['database'],
                               "INSERT INTO users VALUES (NULL, 'francis', 'kofrasa@gmail.com')"])
        # query for inserted data
        res = subprocess.check_output(["sqlite3", self.config['database'], "SELECT COUNT(*) FROM users"])
        self.assertEqual(int(res.strip()), 1, "failed to apply migration scripts")

    def test_config_file(self):
        filename = tempfile.mktemp(dir=self.tmp_dir)
        with open(filename, 'w') as f:
            f.write('\n'.join([
                '[test]',
                'migration_path = %s' % self.config['path'],
                'engine = sqlite3',
                'database = %s' % self.config['database']]))
        import migrate
        migrate.main('-f', filename, '--env', 'test', 'reset')


if __name__ == '__main__':
    unittest.main()