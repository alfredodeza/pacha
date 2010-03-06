# Author: Alfredo Deza
# Email: alfredodeza [at] gmail dot com
# License: MIT
# Copyright 2009-2010 Alfredo Deza
#
"""Simple database work. We do not need an ORM to do this for us."""
import sqlite3
import os

class Worker(object):
    """All database operations happen here"""

    def __init__(self,
            db = '/opt/pacha/db/pacha.db'):
        self.db = db 
        if os.path.isfile(self.db):
            self.conn = sqlite3.connect(self.db)
            self.c = self.conn.cursor()
        else:
            self.conn = sqlite3.connect(self.db)
            table_1 = 'CREATE TABLE repos(id integer primary key, path TEXT, file TEXT, permissions TEXT)'
            table_2 = 'CREATE TABLE users(id integer primary key, user TEXT, key TEXT)'
            self.c = self.conn.cursor()
            self.c.execute(table_1)
            self.c.execute(table_2)

    def insert_host(self, host=None, user=None, port=None):
        """Puts a new host in the database"""
        values = (host, user, port)
        command = "INSERT INTO hosts(host, user, port) VALUES(?,?,?)"
        self.c.execute(command, values)
        self.conn.commit()
        self.conn.close()

    def insert_user(self, user=None, key=None):
        """Puts a new user/key in the database"""
        values = (user, key)
        command = "INSERT INTO users(user, key) VALUES(?,?)"
        self.c.execute(command, values)
        self.conn.commit()
        self.conn.close()

    def remove(self, host):
        """Removes a host from the database"""
        values = (host,)
        command = "DELETE FROM hosts WHERE host = (?)"
        self.c.execute(command, values)
        self.conn.commit()

    def get_hosts(self):
        """Gets all the hosts"""
        command = "SELECT * FROM hosts"
        return self.c.execute(command)

    def get_host(self, host):
        """Gets attributes for a specific host"""
        values = (host,)
        command = "SELECT * FROM hosts WHERE host = (?)"
        return self.c.execute(command, values)

    def get_users(self):
        """Gets all the users"""
        command = "SELECT * FROM users"
        return self.c.execute(command)

