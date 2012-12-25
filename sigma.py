import flask

app = flask.Flask(__name__)
app.config.from_object('config.DebugConfig')

from probe import *
from config import Hosts

def probe_hosts(hosts):
  stats = []

  for node, stat in hosts:
    okay, status, description = probe_host(
        node,
        stat == Hosts.STATUS_DOWN,
        stat == Hosts.STATUS_REDIRECT)
    stats.append({
      'host': node
    , 'as_expected': okay
    , 'status': status
    , 'description': description
    })

  return stats

@app.route('/nodes')
def nodes_status_as_json():
  return flask.jsonify(stats=probe_hosts(Hosts.nodes))

@app.route('/services')
def services_status_as_json():
  return flask.jsonify(stats=probe_hosts(Hosts.services))

@app.route('/')
def main_page():
  return flask.render_template('main.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
