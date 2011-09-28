from celery.loaders.base import BaseLoader
import project

def wanted_module_item(item):
    return item[0].isupper() and not item.startswith("_")


class PybaldLoader(BaseLoader):
    """Pybald celery loader.

        * Maps the celery config onto pybald.project

    """
    def read_configuration(self):
        self.configured = True
        usercfg = dict((key, getattr(project, key))
            for key in dir(project)
            if wanted_module_item(key))

        return usercfg