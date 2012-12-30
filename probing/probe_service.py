import probe
import lib.theta as theta, threading, time

class ProbeService(object):
  def __init__(self, hosts):
    # Probe-related data.
    self.results = {}
    self.hosts = hosts
    for host, _, _ in hosts:
      self.results[host] = (False, 'unknown', 'not yet queried')

    # Results-related data and locks.
    self.results_lock = threading.Lock()
    self.probe_thread = theta.ResilientThread(
        target=self.__probe_worker,
        name='probe_thread')
    self.probe_thread.daemon = True

  def __probe_worker(self):
    while True:
      # Run through and update all hosts/services.
      for tup in self.hosts:
        host = tup[0]

        with self.results_lock:
          self.results[host] = probe.probe_host(*tup)

      # Slep for a lot.
      time.sleep(60)

  def start(self):
    self.probe_thread.start()

  def query(self, host):
    with self.results_lock:
      if host in self.results:
        return self.results[host]
      else:
        return (False, 'unknown', 'host not listed for monitoring')
