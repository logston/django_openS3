"""
A custom Storage interface for storing files to S3 via OpenS3
"""
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from openS3.utils import validate_values


class S3Storage(Storage):
    """
    A custom storage implementation for use with py3s3.
    An instance of this class can be used to move a py3s3 file
    up to or down from AWS.
    """
    def __init__(self, name_prefix, bucket, aws_access_key, aws_secret_key):
        self.name_prefix = name_prefix
        config_values = {'bucket': bucket,
                         'aws_access_key': aws_access_key,
                         'aws_secret_key': aws_secret_key}
        validate_values(validation_func=lambda value: value is not None, dic=config_values)
        self.bucket = bucket
        self.access_key = aws_access_key
        self.secret_key = aws_secret_key
        self.netloc = '{}.s3.amazonaws.com'.format(bucket)

    def _open(self, name, mode='rb'):
        """
        Retrieves the specified file from storage.
        """
        content =
        return ContentFile(content, name)

    def _save(self, name, content):
        name = self.get_valid_name(name)
        name = self._prepend_name_prefix(name)

        return 'actual_file_name'

    def _prepend_name_prefix(self, name):
        """Return file name (ie. path) with the prefix directory prepended"""
        if not self.name_prefix:
            return name
        base = self.name_prefix.strip('/')
        base = '/' + base
        if name[0] != '/':
            name = '/' + name
        return base + name

    # The following methods form the public API for storage systems, but with
    # no default implementations. Subclasses must implement *all* of these.

    def delete(self, name):
        """
        Deletes the specified file from the storage system.
        """
        raise NotImplementedError('subclasses of Storage must provide a delete() method')

    def exists(self, name):
        """
        Returns True if a file referenced by the given name already exists in the
        storage system, or False if the name is available for a new file.
        """
        raise NotImplementedError('subclasses of Storage must provide an exists() method')

    def listdir(self, path):
        """
        Lists the contents of the specified path, returning a 2-tuple of lists;
        the first item being directories, the second item being files.
        """
        raise NotImplementedError('subclasses of Storage must provide a listdir() method')

    def size(self, name):
        """
        Returns the total size, in bytes, of the file specified by name.
        """
        raise NotImplementedError('subclasses of Storage must provide a size() method')

    def url(self, name):
        """
        Returns an absolute URL where the file's contents can be accessed
        directly by a Web browser.
        """
        raise NotImplementedError('subclasses of Storage must provide a url() method')

    def accessed_time(self, name):
        """
        Returns the last accessed time (as datetime object) of the file
        specified by name.
        """
        raise NotImplementedError('subclasses of Storage must provide an accessed_time() method')

    def created_time(self, name):
        """
        Returns the creation time (as datetime object) of the file
        specified by name.
        """
        raise NotImplementedError('subclasses of Storage must provide a created_time() method')

    def modified_time(self, name):
        """
        Returns the last modified time (as datetime object) of the file
        specified by name.
        """
        raise NotImplementedError('subclasses of Storage must provide a modified_time() method')


class S3StaticStorage(S3Storage):
    def __init__(self, name_prefix=settings.STATIC_DIR,
                 bucket=settings.AWS_STORAGE_BUCKET_NAME,
                 aws_access_key=settings.AWS_ACCESS_KEY_ID,
                 aws_secret_key=settings.AWS_SECRET_ACCESS_KEY):
        super().__init__(name_prefix, bucket, aws_access_key, aws_secret_key)


class S3MediaStorage(S3Storage):
    def __init__(self, name_prefix=settings.MEDIA_DIR,
                 bucket=settings.AWS_STORAGE_BUCKET_NAME,
                 aws_access_key=settings.AWS_ACCESS_KEY_ID,
                 aws_secret_key=settings.AWS_SECRET_ACCESS_KEY):
        super().__init__(name_prefix, bucket, aws_access_key, aws_secret_key)