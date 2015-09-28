default_config = dict(
# templates
# =================
template_default_filters = ['h', 'unicode'],
template_helpers = [],
template_filesystem_check = True,
template_path = 'app/views',
cache_path = 'tmp/viewscache',
page_options = {},
# database
# =================
global_table_args = {},
schema_reflection = False,
database_engine_uri = 'sqlite:///:memory:',
database_engine_args = {},
# Asset Pipeline
# =================
BUNDLE_ASSETS = False,
BUNDLE_AUTO_BUILD = True,
# these are relative to the project path
BUNDLE_SOURCE_PATHS = ['/front_end', '/sass'],
# these are relative to the static file path (/public)
BUNDLE_OUTPUT_PATH = '/min',
BUNDLE_FILTER_OPTIONS = [],
# Email
# =================
smtp_config = {},
# Misc
# =================
project_name = "project",
debug = True,
email_errors = False,
env_name = "Default",
host_name = 'localhost',
path = '',
#  green = False,
)