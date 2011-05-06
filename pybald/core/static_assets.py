#!/usr/bin/env python
# encoding: utf-8

from pybald.core.helpers import img
import project

asset_tag_cache = {}
class StaticAssetManager(object):
    def __init__(self, req):
        self.static_prefix=""
        self.set_req(req)
        
    def set_req(self, req):
        if project.s3:
            if 'gzip' in req.accept_encoding:
                self.static_prefix = "http://staticz.smarterer.com"
            else:
                self.static_prefix = "http://static.smarterer.com"
    
    def js(self, filename):
        return '''<script type="text/javascript" src="{0}"></script>'''.format(self.gen_url(filename))

    def css(self, filename, media="screen"):
        return '''<link type="text/css" href="{0}" media="{1}" rel="stylesheet" />'''.format(self.gen_url(filename), str(media))

    
    def img(self, src, *pargs, **kargs):
        src = ''.join((self.static_prefix, str(src)))
        return img(src, *pargs, **kargs)
        
    def _compute_asset_tag(self, filename):
         asset_tag = asset_tag_cache.get(filename, None)
         if not asset_tag:
             asset_tag = str(int(round(os.path.getmtime(os.path.join(project_path,"content",filename.lstrip("/"))) )) ) 
             asset_tag_cache[filename] = asset_tag
         return asset_tag

    def gen_url(self, filename):
         return ''.join((static_prefix, filename, "?v=", self._compute_asset_tag(filename) ))