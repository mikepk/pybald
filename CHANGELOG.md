# Pybald Changelog

## Release 0.5.8 (Sep 10, 2024)

  - Remove use of 'imp' module
  - Update travis CI/CD to just test python 3.10 and above

## Release 0.5.7 (August 23, 2019)

  - Change dependencies to minimums instead of pinned
  versions

## Release 0.5.6 (April 29, 2019)

  - Update SQLAlchemy dependency to 1.3.3 to mitigate a 
    security issue with SQLAlchemy verstions <= 1.3.0

## Release 0.5.4 (February 18, 2019)

  - Update dependencies: WTForms, alembic, SQLALchemy, WebOb
  - Change docs from ReStructured text to Markdown

## Release 0.5.3 (February 14, 2019)

  - Fix Python 3 compatibility issue in Proxy.\_\_dir\_\_

## Release 0.5.2 (January 2, 2019)

  - Fix bug with stacktrace template for default Error handler
  - Improve the context model binding function

## Release 0.5.0 (August 19, 2017)

  - **Warning** - this release may not be compatible with previous
    pybald releases *if* you were making use of the asset pipeline
    (bundles, bundle filters, JSX compilation), utilizing the celery
    loader or the newrelic adapter
  - This removes the webasset pipeline from core pybald. The webasset
    pipeline was only used in a few projects and added complexity and
    numerous requirements to pybald.
  - The webasset pipeline will be re-designed and released as a
    supporting pybald package instead of included in the core.
  - The newrelic adapter and celery support code will also be
    re-designed and released as supporting pybald packages instead of
    included in the core.
  - This release also bumps the supporting library versions: Mako,
    SqlAlchemy, WTForms
  - Remove requirement for forked routes library, required behaviors
    have been included in the main routes project
  - Improve tests and test coverage

## Release 0.4.1 (February 26, 2016)

  - Fix a bug with the default error controller. Now the raw exception
    can be passed in and the order of the arguments was changed but not
    updated in the default.

## Release 0.4.0 (January 28, 2016)

  - **Warning** - this release is not compatible with previous pybald
    releases.
  - Major configuration changes, deprecate the use of importing
    'project.py' directly.
  - New application context that lives globally is the config passing
    mechanism.
  - Replace FormAlchemy with WTForms as the primary mechanism for form
    processing and validation
  - Utilize controller and model registry.
  - Global context is on a threadlocal stacked proxy to allow multiple
    pybald applications in one interpreter.
  - Database session is now attached to the app context.
  - Shared application resources (caches etc..) are now registered with
    the context
  - ErrorMiddleware now has a more consistent interface with error
    controllers, passing the raw exception as a \*parg, followed by
    context-specific \*\*kargs

## Release 0.3.2 (March 25, 2015)

  - Add jsx filters for react components

## Release 0.3.1 (February 19, 2015)

  - Fix webassets dependencies and bugs
  - Added browser caching headers to the simple static server

## Release 0.3.0 (November 2, 2014)

  - Change the default behavior of all templates to include the html
    escape filter
  - New helper: HTMLLiteral. Allows explicit html escape bypassing
  - Add csrf decorator
  - New newrelic instrumentation code to improve controller/action
    visibility

## Release 0.2.8 (June 26, 2014)

  - Update the webasset-based asset bundler to take input and output
    paths from the project config file. The new arguments are
    BUNDLE\_SOURCE\_PATHS and BUNDLE\_OUTPUT\_PATH. So in the project.py
    file you might have a config

that looks like:

    BUNDLE_SOURCE_PATHS = ['alternate_source_path', 'public']
    BUNDLE_OUTPUT_PATH = '/some_path/public_files/'


