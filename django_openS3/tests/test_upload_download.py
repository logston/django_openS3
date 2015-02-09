import unittest
from django.conf import settings
from django.core.management import call_command
from openS3 import OpenS3


class ManagementCommandTC(unittest.TestCase):
    def test_collectstatic(self):
        opener = OpenS3(settings.AWS_STORAGE_BUCKET_NAME,
                        settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY)
        files = ('/static/css/test.css',
                 '/static/js/test.js')
        for file in files:
            with opener(file) as fd:
                fd.delete()
            with opener(file) as fd:
                self.assertFalse(fd.exists())

        call_command('collectstatic', interactive=False, verbosity=0)

        for file in files:
            with opener(file) as fd:
                self.assertTrue(fd.exists())
                fd.delete()


if __name__ == '__main__':
    unittest.main()