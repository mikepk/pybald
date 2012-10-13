from celery.loaders.base import BaseLoader
import project

def wanted_module_item(item):
    # check if the config item starts with any of the celery config start keys
    # run startswith against each, and then or the results to return True
    # if any match
    # this could probably be done with a dynamic regex too.
    celery_config_start_keys = ('CELERY', 'BROKER')
    return reduce(lambda x, y: x or y,
                  map(item.startswith,
                      celery_config_start_keys))


class PybaldLoader(BaseLoader):
    """Pybald celery loader.

        * Maps the pybald.project config onto the celery config dict

    """
    def read_configuration(self):
        self.configured = True
        # generate a config dictionary from project.py
        return dict((key, getattr(project, key))
            for key in filter(wanted_module_item, dir(project)))