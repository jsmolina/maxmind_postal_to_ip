import logging
import urllib.request
import datetime
import time
import tarfile
import sys
import os
from orjson import dumps
from quart import (
    Quart, current_app
)

from quart.views import MethodView
import maxminddb

DOWNLOAD_GZ_PATH = os.getenv('DOWNLOAD_GZ_PATH', '/tmp/db.tar.gz')
DESTINATION_PATH = os.getenv('DECOMPRESS_GZ_PATH', '/tmp/maxmind')
MAXMINDB = os.getenv('MAXMIND_URL', None)
LOGLEVEL = os.getenv('LOGLEVEL', 'INFO')

logger = logging.getLogger('quart.serving')
logger.setLevel(LOGLEVEL)

app = Quart(__name__)


def remove_download_gz(gz_file):
    try:
        os.remove(gz_file)
    except:
        print("file was not there...")


def download_db(url, gz_file):
    file_time = 0
    try:
        file_time = os.path.getmtime(gz_file)
        print("File exists and created on {0}".format(datetime.datetime.fromtimestamp(file_time)))
    except Exception as e:
        pass

    if time.time() - file_time > 86400:
        remove_download_gz(gz_file)
        result = urllib.request.urlretrieve(url, gz_file)
        content_length = result[1]['Content-Length']
        print("file has {0} size".format(content_length))
    return gz_file


def extract_db(gz_file, destination_path):
    tar = tarfile.open(gz_file, "r:gz")
    try:
        os.mkdir(destination_path)
    except Exception as e:
        print(e)
    members = tar.getmembers()
    for member in members:
        if 'GeoLite2-City.mmdb' in member.name:
            # remove own path part
            member.name = 'GeoLite2-City.mmdb'
            tar.extract(member, destination_path)
            tar.close()
            return os.path.join(destination_path, 'GeoLite2-City.mmdb')


class IpToPostalCode(MethodView):
    async def get(self, ip):
        start_t = time.time()
        status = 200
        info = current_app.maxmind_reader.get(ip)
        if not info:
            info = {}
            status = 404

        result = {
            'zip_code': info.get('postal', {}).get('code', None),
            'location': info.get('location', {}),
        }
        logger.debug("response took %s seconds", time.time() - start_t)
        return dumps(result), status, {'Content-Type': 'application/json'}


def create_app():
    app.add_url_rule('/json/<ip>', view_func=IpToPostalCode.as_view('iptopostal'))
    return app


def application():
    @app.before_serving
    async def init():
        print("Download db...")
        if MAXMINDB is None:
            print("Error! Please specify MAXMIND_URL environment variable")
            exit(1)
        gz_file = download_db(MAXMINDB, DOWNLOAD_GZ_PATH)
        print("Extract db...")
        db = extract_db(gz_file, DESTINATION_PATH)
        app.maxmind_reader = maxminddb.open_database(db, mode=maxminddb.MODE_MEMORY)

    return create_app()


if __name__ == '__main__':
    application().cli(obj={})
