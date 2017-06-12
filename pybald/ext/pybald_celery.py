from celery import Celery


def celery_config_item(item):
    # check if the config item starts with any of the celery config start keys
    celery_config_start_keys = ('CELERY', 'BROKER')
    return any(item.startswith(key) for key in celery_config_start_keys)


def make_celery(app):
    celery = Celery(app.name)
    celery.conf.update(dict((key, getattr(app.config, key)) for key in
        filter(celery_config_item, dir(app.config))))
    return celery
