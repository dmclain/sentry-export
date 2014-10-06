try:
    VERSION = __import__('pkg_resources').get_distribution('sentry-export').version
except Exception, e:
    VERSION = "dev"
