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
            """create table users (
              id int primary key,
              name text,
              email text
            );
            """,
            "drop table users;"
        )
        self.config['command'] = 'create'
        self.config['message'] = 'users'
        Migrate(self.config).run()
        rev_folder = os.path.join(self.config['path'], "1")
        # check that all folders have been created
        self.assertTrue(os.path.exists(rev_folder), "revision folder not created")
        # must create 2 files
        self.assertEquals(len(glob.glob(os.path.join(rev_folder, '*'))), 2,
                          "could not create migration files")
        # add some SQL
        for i, s in enumerate(('up', 'down')):
            filename = glob.glob(os.path.join(rev_folder, '*.users.%s.sql' % s))[0]
            with open(filename, 'w') as w:
                w.write(sql[i])

    def test_up_command(self):
        self.test_create_command()
        self.config['command'] = 'up'
        Migrate(self.config).run()
        self.assertTrue(os.path.exists(self.config['database']), 'no database file was created')
        # insert some data to confirm that scripts were applied
        subprocess.check_call(["sqlite3", self.config['database'],
                               "insert into users values (1, 'francis', 'kofrasa@gmail.com');"])
        # query for inserted data
        res = subprocess.check_output(["sqlite3", self.config['database'],
                                       "select count(*) from users"])
        self.assertEqual(int(res.strip()), 1, "failed to apply migration scripts")

    def test_down_command(self):
        self.test_up_command()
        self.config['command'] = 'down'
        Migrate(self.config).run()
        try:
            subprocess.check_call(["sqlite3", self.config['database'], "select * from users"])
        except subprocess.CalledProcessError as e:
            self.assertEqual(e.returncode, 1, "failed to rollback database")

    def test_refresh_command(self):
        self.test_up_command()
        self.config['command'] = 'refresh'
        Migrate(self.config).run()
        subprocess.check_call(["sqlite3", self.config['database'],
                               "insert into users values (1, 'francis', 'kofrasa@gmail.com');"])
        # query for inserted data
        res = subprocess.check_output(["sqlite3", self.config['database'],
                                       "select count(*) from users"])
        self.assertEqual(int(res.strip()), 1, "failed to apply migration scripts")

    def test_config_file(self):
        filename = tempfile.mktemp(dir=self.tmp_dir)
        with open(filename, 'w') as f:
            f.write('\n'.join([
                '[test]',
                'migration_path = %s' % self.config['path'],
                'engine = sqlite3',
                'database = %s' % self.config['database']]))
        # other tests use values from config dict
        self.config['file'] = filename
        self.config['env'] = 'test'
        self.test_refresh_command()


if __name__ == '__main__':
    unittest.main()