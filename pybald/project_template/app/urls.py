import project
import sys

def map(urls):
    '''
    Defines the url to controller mapping for the application. A 
    routes mapper or submapper object must be passed in.
    '''
    urls.connect('home', r'/', controller="home")

    # generic pattern
    urls.connect('base', r'/{controller}/{action}/{id}')
    urls.connect(r'/{controller}/{action}')
    urls.connect(r'/{controller}')

    # REDIRECT ALL URLS TERMINATING IN a slash, '/', to no slash
    urls.redirect('/*(url)/', '/{url}',
                  _redirect_code='301 Moved Permanently')


    # when in debug mode, print the whole URL mapping
    if project.debug:
        sys.stderr.write(str(urls)+"\n")