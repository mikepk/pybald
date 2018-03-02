#!/usr/bin/env python
# encoding: utf-8
import os
import mimetypes
from datetime import datetime, timedelta
import io
from functools import partial


class StaticServer(object):
    '''
    A *very* simple static asset server. Do not use in production, just
    for test or development use.

    StaticServer is a WSGI application that can be included in the WSGI
    pipeline to intercept static requests (and perform file system lookups).
    If the file lookup fails, the pipeline is allowed to continue to any
    dynamic components.
    '''
    def __init__(self, application, path, browser_caching=False):
        """
        :param application: is the remaining WSGI pipeline to connect to.
        :param path: is directory where static files are stored
        :param browser_caching: whether to send 30d expires future headers
        """
        self.path = path
        self.application = application
        self.browser_caching = browser_caching

    def send_file(self, file_path, size):
        '''
        Read a file from the filesystem and yield 64k chunks of the file
        as a generator / iterable.
        '''
        BLOCK_SIZE = 64 * 1024
        with io.open(file_path, mode="rb") as f:
            file_read = partial(f.read, BLOCK_SIZE)
            for block in iter(file_read, b''):
                yield block

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
            ("Content-Type", mimetype),
            ("Content-Length", str(size)),
        ]
        if self.browser_caching:
            expires = datetime.utcnow() + timedelta(days=30)
            headers.extend([
            ("Cache-Control", "public, max-age={0}".format(60 * 60 * 24 * 30)),
            ("Expires", "{0}".format(expires.strftime("%a, %e %b %Y %H:%M:%S GMT")))
                ])

        start_response("200 OK", headers)
        return self.send_file(file_path, size)

