AUTHOR = 'Alex Liebscher'
SITENAME = 'Alex Liebscher'
SITEURL = 'http://127.0.0.1:8000'

PATH = 'content'
STATIC_PATHS = ['images', 'pdf', 'static']

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

THEME = 'themes/janson/'
TYPOGRIFY = True

AUTHOR_URL = ''
AUTHOR_SAVE_AS = ''

CATEGORY_URL = ''
CATEGORY_SAVE_AS = ''

ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{slug}/index.html'

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
DELETE_OUTPUT_DIRECTORY = True

# Exclude static directory from content processing
ARTICLE_EXCLUDES = ['static']
PAGE_EXCLUDES = ['static']

DIRECT_TEMPLATES = ['index', 'tags']

DEFAULT_METADATA = {
    'status': 'draft',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
