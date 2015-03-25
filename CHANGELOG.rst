Release 0.2.8 (June 26, 2014)
=============================

* Update the webasset-based asset bundler to take input and output paths from 
  the project config file. The new arguments are BUNDLE_SOURCE_PATHS and
  BUNDLE_OUTPUT_PATH. So in the project.py file you might have a config
  that looks like:

      BUNDLE_SOURCE_PATHS = ['alternate_source_path', 'public']
      BUNDLE_OUTPUT_PATH = '/some_path/public_files/'


Release 0.3.0 (November 2, 2014)
================================

* Change the default behavior of all templates to include the html escape filter
* New helper: HTMLLiteral. Allows explicit html escape bypassing
* Add csrf decorator
* New newrelic instrumentation code to improve controller/action visibility

Release 0.3.1 (February 19, 2015)
================================

* Fix webassets dependencies and bugs
* Added browser caching headers to the simple static server

Release 0.3.2 (March 25, 2015)
================================

* Add jsx filters for react components
