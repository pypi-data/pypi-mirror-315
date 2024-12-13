from pathlib import Path

from environs import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# read os.environ or .env file
env = Env()
env.read_env()

# log levels for django and BMA
DJANGO_LOG_LEVEL = env.str("DJANGO_LOG_LEVEL", default="INFO")
BMA_LOG_LEVEL = env.str("DJANGO_BMA_LOG_LEVEL", default="DEBUG")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="{{ django_secret_key }}")

# debug settings - remember to set allowed_hosts if debug is disabled
DEBUG = True
DEBUG_TOOLBAR = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Database settings
DATABASES = {
"default": env.dj_db_url(
    "DJANGO_DATABASE_URL", default="postgres://bma:bma@127.0.0.1/bmadb"
)
}

# admin site url prefix, set to 'admin' for /admin/
ADMIN_PREFIX = "admin"

# secure cookies and proxy header
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# uploaded or generated files are placed below MEDIA_ROOT
MEDIA_ROOT = Path("/home/user/bma/django_media_root")

OAUTH_SERVER_BASEURL="http://127.0.0.1:8000"

NGINX_PROXY=False

# permit these image mimetypes, and use this extension for them
ALLOWED_IMAGE_TYPES={
    "image/jpeg": "jpg",
    "image/bmp": "bmp",
    "image/gif": "gif",
    "image/svg+xml": "svg",
    "image/tiff": "tif",
    "image/png": "png",
    "image/webp": "webp",
}

# permit these video mimetypes, and use this extension for them
ALLOWED_VIDEO_TYPES={
    "video/mpeg": "mp2",
    "video/mp4": "mp4",
    "video/quicktime": "mov",
    "video/x-ms-asf": "asf",
}

# permit these audio mimetypes, and use this extension for them
ALLOWED_AUDIO_TYPES={
    "audio/basic": "au",
    "audio/mid": "mid",
    "audio/mpeg": "mp3",
    "audio/x-aiff": "aif",
    "audio/x-pn-realaudio": "ram",
    "audio/x-wav": "wav",
}

# permit these document mimetypes, and use this extension for them
ALLOWED_DOCUMENT_TYPES={
    "text/plain": "txt",
    "application/pdf": "pdf",
}

# filetype icons
FILETYPE_ICONS = {
    "basefile": "fas fa-file",
    "image": "fas fa-file-image",
    "video": "fas fa-file-video",
    "audio": "fas fa-file-audio",
    "document": "fas fa-file-lines",
}

DEFAULT_THUMBNAIL_URLS = {
    "basefile": "/static/images/file-solid.png",
    "image": "/static/images/file-image-solid.png",
    "video": "/static/images/file-video-solid.png",
    "audio": "/static/images/file-audio-solid.png",
    "document": "/static/images/file-alt-solid.png",
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
]

BMA_CREATOR_GROUP_NAME = "creators"
BMA_MODERATOR_GROUP_NAME = "moderators"
BMA_CURATOR_GROUP_NAME = "curators"
BMA_WORKER_GROUP_NAME = "workers"
BMA_INITIAL_GROUPS=[BMA_CREATOR_GROUP_NAME,BMA_CURATOR_GROUP_NAME,BMA_MODERATOR_GROUP_NAME,BMA_WORKER_GROUP_NAME] # new users are always added to these groups on first login


# how long to wait before registering another hit
HITCOUNT_KEEP_HIT_ACTIVE = { 'minutes': 10 }

# Limit the number of active Hits from a single IP address. 0 means that it is unlimited.:
HITCOUNT_HITS_PER_IP_LIMIT = 0

# Exclude Hits from all users in the specified user groups
HITCOUNT_EXCLUDE_USER_GROUP = ()

# Any Hit older than the time specified will be removed from the Hits table when the cleanup management command is run
HITCOUNT_KEEP_HIT_IN_DATABASE = { 'days': 365 }

IMAGE_ENCODING = {
    "image/webp": {
        "lossless": False,
        "quality": 90,
    },
}
