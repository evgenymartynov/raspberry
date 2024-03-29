import flask

app = flask.Flask(__name__)
CONF='config.Config'
try:
  app.config.from_object('sigma.' + CONF)
except:
  app.config.from_object(CONF)

from probing.probe_service import ProbeService
from config import Hosts

import platform
hostname = platform.node()

probe_service = None

def probe_hosts(hosts):
  stats = []

  for host in hosts:
    okay, status, description = probe_service.query(host)
    stats.append({
      'host': host
    , 'as_expected': okay
    , 'status': status
    , 'description': description
    })

  return stats

@app.route('/nodes')
def nodes_status_as_json():
  hosts = map(lambda x: x[0], Hosts.nodes)
  stats = probe_hosts(hosts)

  # We check health of nodes by looking at /node-status, so URL has to be
  # cleaned up before displaying.
  for stat in stats:
    stat['host'] = stat['host'].split('/', 1)[0]

  return flask.jsonify(stats=stats)

@app.route('/services')
def services_status_as_json():
  hosts = map(lambda x: x[0], Hosts.services)
  return flask.jsonify(stats=probe_hosts(hosts))

@app.route('/')
def main_page():
  return flask.render_template('main.html', hostname=hostname)

#
# Call this before running the app!
#
def Init():
  global probe_service
  probe_service = ProbeService(map(
      lambda tup:
          ( tup[0]
          , tup[1] == Hosts.STATUS_DOWN
          , tup[1] == Hosts.STATUS_REDIRECT
          ),
      Hosts.nodes + Hosts.services))
  probe_service.start()

if __name__ == '__main__':
  Init()
  app.run(host='0.0.0.0')
