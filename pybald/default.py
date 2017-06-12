default_config = dict(
    # templates
    # =================
    template_default_helpers=[
        'from pybald.core.helpers import img, link, humanize, HTMLLiteral as literal, url_for',
        'from pybald.core import page'],
    # order important, html filter always first!
    template_default_filters=['h', 'unicode'],
    template_helpers=[],
    template_filesystem_check=True,
    template_path='app/views',
    cache_path='tmp/viewscache',
    page_options={},
    # database
    # =================
    global_table_args={},
    schema_reflection=False,
    database_engine_uri='',
    database_engine_args={},
    # Asset Pipeline
    # =================
    USE_CDN=False,
    # Email
    # =================
    smtp_config={},
    # Misc
    # =================
    project_name=None,
    static_path="public",
    debug=True,
    email_errors=False,
    env_name="Default",
    host_name='localhost',
    path='',
    STATIC_SOURCES=None
)
