""" Module for S3 client wrapper and related tooling. """
import logging
import os
from manager.utils import debug, env, to_flag

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto import s3

logging.getLogger('libs3').setLevel(logging.INFO)

class S3(object):
    def __init__(self, envs=os.environ):
        self.secret_key = env('AWS_SECRET_KEY', None, envs)
        self.access_key = env('AWS_ACCESS_KEY', None, envs)
        self.bucket_name = env('AWS_S3_BUCKET', None, envs)
        self.region = env('AWS_S3_REGION', 'sa-east-1', envs)

        self.client = s3.connect_to_region(self.region,
                            aws_access_key_id=self.access_key,
                            aws_secret_access_key=self.secret_key,
                        )
        self.bucket = self.client.get_bucket(self.bucket_name)
    @debug
    def get_backup(self, backup_id):
        try:
            os.mkdir('/tmp/backup', 0770)
        except OSError:
            pass
        outfile = '/tmp/backup/{}'.format(backup_id)
        key = self.bucket.get_key(backup_id)
        key.get_contents_to_filename(outfile)

    def put_backup(self, backup_id, infile):
        print('Trying to save %s from %s' % (backup_id, infile))
        key = Key(bucket=self.bucket, name=backup_id)
        key.set_contents_from_filename(infile)
