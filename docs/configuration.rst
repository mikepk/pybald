Configuration
===============

The `project.py` file
---------------------

A pybald application is configured by the project.py file in the root of the project. This is a regular python module. This module will contain configuration variable declarations. Generally the project.py file will be where you define things like:

 * whether the project is in debugging mode or not
 * logging directives
 * the database kind, host, port, username and password
 * any additional template helpers to load into all tempaltes
 * other server configurations, like SMTP servers, search servers, etc...

The default project.py file has some example configuration variables along with comments.

Common config arguments
------------------------

For example database configuration is done via a URL following `RFC-1738 <http://rfc.net/rfc1738.html>`_. In the project.py file, the config variable `database_engine_uri` is used to define the URL to be used for database configuration. Generally pybald projects use some string interpolation to create these URLs from configuration dictionaries.

The default project.py has the following block to define a simple sqllite database as the database URL:


.. code-block:: python

  # sqlalchemy engine string examples:
  # mysql -         "mysql://{user}:{password}@{host}/{database}"
  # postgres - postgresql://{username}:{password}@{host}:{port}/{database}'
  # sqllite -       "sqlite:///{filename}"
  # sqllite mem -   "sqlite:///:memory:"
  
  # local database connection settings
  # default to a sqllite file database based on the project name
  database_engine_uri_format = 'sqlite:///{filename}'
  db_config = {'filename': os.path.join(path,
               '{project}.sqlite'.format(project=project_name))}
  
  # create the db engine uri
  database_engine_uri = database_engine_uri_format.format(**db_config)

