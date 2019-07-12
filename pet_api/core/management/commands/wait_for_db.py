import time

from django.db import connections
from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until databse is available"""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                connection.ensure_connection()
                db_conn = True
            except OperationalError:
                self.stdout.write("DATABASE UNAVAILABLE, try reconnect in 2 seconds...")
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS("DATABASE AVAILABLE! :-)"))

        conn_obj = connections["default"]
        tables = conn_obj.introspection.table_names()
        print('-------')
        print('Tables available:')
        print(tables)
        print('-------')

        #print('Models available:\n')
        #seen_models = conn_obj.introspection.installed_models(tables)
        #print(seen_models)