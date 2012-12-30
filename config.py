class Config(object):
  DEBUG=False
  HOST='0.0.0.0'

class DebugConfig(Config):
  DEBUG=True

class Hosts(object):
  STATUS_UP       = 1
  STATUS_REDIRECT = 2
  STATUS_DOWN     = 3

  nodes = [
    ('archimedes.epochfail.com',  STATUS_DOWN)
  , ('cherrybrook.epochfail.com', STATUS_REDIRECT)
  , ('kensington.epochfail.com',  STATUS_DOWN)
  ]

  services = [
    ('epochfail.com',             STATUS_REDIRECT)
  , ('evgenymartynov.com',        STATUS_REDIRECT)
  , ('aiocdb.epochfail.com',      STATUS_UP)
  , ('anic.epochfail.com',        STATUS_UP)
  , ('blog.epochfail.com',        STATUS_DOWN)
  , ('circles.epochfail.com',     STATUS_UP)
  , ('jrit.epochfail.com',        STATUS_DOWN)
  , ('passthru.epochfail.com',    STATUS_DOWN)
  , ('shouty.epochfail.com',      STATUS_UP)
  ]
