#!/usr/bin/env python
# encoding: utf-8
import os
import unittest
import mimetypes


class StaticServer(object):
    '''
    A *very* simple static asset server. Do not use in production, just
    for test or development use.

    StaticServer is a WSGI application that can be included in the WSGI
    pipeline to intercept static requests (and perform file system lookups).
    If the file lookup fails, the pipeline is allowed to continue to any
    dynamic components.
    '''
    def __init__(self, application, path):
        """
        :param application: is the remaining WSGI pipeline to connect to.
        :param path: is directory where static files are stored
        """
        self.path = path
        self.application = application

    def send_file(self, file_path, size):
        '''
        Read a file from the filesystem and yield 64k chunks of the file
        as a generator / iterable.
        '''
        BLOCK_SIZE = 64 * 1024
        f = open(file_path)  # as f:
        block = f.read(BLOCK_SIZE)
        while block:
            yield block
            block = f.read(BLOCK_SIZE)
        f.close()

    def __call__(self, environ, start_response):
        '''
        A simple static file server.

        Should not be used in production environments.
        '''
        file_path = os.path.join(self.path, environ['PATH_INFO'].lstrip('/'))
        if not os.path.isfile(file_path):
            return self.application(environ, start_response)

        mimetype, encoding = mimetypes.guess_type(file_path)

        size = os.path.getsize(file_path)
        headers = [
            ("Content-type", mimetype),
            ("Content-length", str(size)),
        ]
        start_response("200 OK", headers)
        return self.send_file(file_path, size)


class static_serveTests(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
