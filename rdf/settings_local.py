import settings

DEBUG_INSTALLED_APPS = (
    'debug_toolbar',
)

DEBUG_MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

if settings.DEBUG:
    INSTALLED_APPS = DEBUG_INSTALLED_APPS + settings.INSTALLED_APPS

    INTERNAL_IPS = (
        '127.0.0.1',
    )

    MIDDLEWARE_CLASSES = DEBUG_MIDDLEWARE_CLASSES + settings.MIDDLEWARE_CLASSES
