"""
Django tables on other schema quick fix
~~~~~~~~~~~~~~~~~~
"""
VERSION = (0, 5)
__version__ = VERSION

from time import time

import django
from django.conf import settings
if django.VERSION < (1, 7):
    from django.db.backends import util
else:
    from django.db.backends import utils as util

def _override_cursor():
    return getattr(settings, 'CURSOR_OVERRIDE', False)


class ReadOnlyCursorWrapper(object):
    """
    This is a wrapper for a database cursor.

    This sits between django's own wrapper at
    `django.db.backends.util.CursorWrapper` and the database specific cursor at
    `django.db.backends.*.base.*CursorWrapper`. It overrides two specific
    methods: `execute` and `executemany`. If the site is in read-only mode,
    then the SQL is examined to see if it contains any write actions. If a
    write is detected, an exception is raised.

    A site is in read only mode by setting the SITE_READ_ONLY setting. For
    obvious reasons, this is False by default.

    Raises a DatabaseWriteDenied exception if writes are disabled.
    """

    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db
        # self.readonly = _readonly()
        # self.readonly_dbs = _get_readonly_dbs()

    def execute(self, sql, params=()):
        # Check the SQL
        # if (self.readonly
        #         and self._write_sql(sql)
        #         and self._write_to_readonly_db()):
        #     raise DatabaseWriteDenied
        # return self.cursor.execute(sql, params)
        self.db.validate_no_broken_transaction()
        with self.db.wrap_database_errors:
            # print('Cursor Override SQL: ' + sql)
            sql = sql.replace("_salesforce\".\"","_salesforce_")
            if params is None:
                return self.cursor.execute(sql)
            else:
                return self.cursor.execute(sql, params)

    def executemany(self, sql, param_list):
        # Check the SQL
        # if self.readonly and self._write_sql(sql):
        #     raise DatabaseWriteDenied
        # print('Cursor Override SQL: ' + sql)
        sql = sql.replace("_salesforce\".\"","_salesforce_")
        return self.cursor.executemany(sql, param_list)

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)


class CursorWrapper(util.CursorWrapper):
    def __init__(self, cursor, db):
        self.cursor = ReadOnlyCursorWrapper(cursor, db)
        self.db = db


# Redefine CursorDebugWrapper because we want it to inherit from *our*
# CursorWrapper instead of django.db.backends.util.CursorWrapper
class CursorDebugWrapper(CursorWrapper):

    def execute(self, sql, params=()):
        start = time()
        try:
            return self.cursor.execute(sql, params)
        finally:
            stop = time()
            duration = stop - start
            sql = self.db.ops.last_executed_query(self.cursor, sql, params)
            self.db.queries.append({
                'sql': sql,
                'time': "%.3f" % duration,
            })
            # logger.debug(
            #     '(%.3f) %s; args=%s',
            #     duration, sql, params,
            #     extra={'duration': duration, 'sql': sql, 'params': params}
            # )

    def executemany(self, sql, param_list):
        start = time()
        try:
            return self.cursor.executemany(sql, param_list)
        finally:
            stop = time()
            duration = stop - start
            self.db.queries.append({
                'sql': '%s times: %s' % (len(param_list), sql),
                'time': "%.3f" % duration,
            })
            # logger.debug(
            #     '(%.3f) %s; args=%s',
            #     duration, sql, param_list,
            #     extra={'duration': duration, 'sql': sql, 'params': param_list}
            # )

if _override_cursor():
    # Monkey Patching!
    util.CursorWrapper = CursorWrapper
    util.CursorDebugWrapper = CursorDebugWrapper
