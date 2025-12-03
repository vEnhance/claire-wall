AUTHOR = "Claire Zhang"
SITENAME = "lost thoughts"
SITESUBTITLE = "a casual blog"

PATH = "content"
TIMEZONE = "US/Eastern"
DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = "theme"
DEFAULT_PAGINATION = 5

# Monthly archives configuration
DIRECT_TEMPLATES = ["index", "archives"]
TAG_SAVE_AS = ""
TAGS_SAVE_AS = ""
CATEGORY_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
STATIC_PATHS = ["images", "extra"]
PAGE_URL = r"{slug}.html"
PAGE_SAVE_AS = r"{slug}.html"
PLUGINS = ["pelican_katex"]
