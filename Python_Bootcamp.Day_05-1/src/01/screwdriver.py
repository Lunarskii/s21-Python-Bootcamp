from django.utils import timezone
from django.conf import settings
import psycopg2
import os
import shutil
import magic
import sys


settings.configure(
    TIME_ZONE='Europe/Moscow',
    USE_TZ=True
)

dbname = 'postgres'
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'


class DB:

    def __init__(self, dbname, user, password, host, port):
        self.db = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def send_get_request(self, request):
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def send_post_request(self, request, *args):
        self.cursor.execute(request, *args)
        self.db.commit()


def upload_file(db, file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            mime = magic.Magic(mime=True)
            mime_type = mime.from_buffer(file.read(1024))
            if not mime_type.startswith('audio/'):
                print('The uploaded file is not an audio file.')
            else:
                base_name = os.path.basename(file_path)
                name_without_extension = os.path.splitext(base_name)[0]
                db.send_post_request('INSERT INTO app_audio (publication_date, name, file) VALUES (%s, %s, %s);',
                                     (timezone.now(), name_without_extension, 'audio/' + base_name))
                shutil.copy(file_path, 'django_module/media/audio')
    else:
        print(f'\'{file_path}\' is not a file')


def list_files(db):
    for file in db.send_get_request('SELECT file FROM app_audio'):
        print(f'{file=}')


if __name__ == '__main__':
    db = DB(dbname, user, password, host, port)
    args = sys.argv
    if 'upload' in args:
        file_index = args.index('upload') + 1
        if file_index < len(args):
            upload_file(db, args[file_index])
    elif 'list' in args:
        list_files(db)
