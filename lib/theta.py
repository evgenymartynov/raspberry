import threading
import sys, traceback, time

__all__ = ['Thread', 'ResilientThread']

# Basic wrapper around the standard threading.Thread class.
# Makes join(None) pick up KeyboardInterrupt properly.
class Thread(threading.Thread):
  def join(self, timeout=None):
    if timeout is None:
      while self.isAlive():
        super(Thread, self).join(0)
        time.sleep(0.1)
    else:
      super(Thread, self).join(timeout)

# Restarts the worker function in case of an exception.
# Logs the exception to sys.stdout and sleeps for a bit before rebooting.
class ResilientThread(Thread):
  def __init__(self, *args, **kwargs):
    if 'target' in kwargs:
      kwargs['target'] = self._resilient_worker_wrapper(kwargs['target'])

    super(ResilientThread, self).__init__(*args, **kwargs)

  def _resilient_worker_wrapper(self, worker):
    def wrapped(*args, **kwargs):
      while True:
        try:
          worker(*args, **kwargs)
        except Exception as e:
          print '8<' + ' -' * 39
          print 'Exception in thread', threading.currentThread().getName()
          traceback.print_exc(file=sys.stdout)
          print '- ' * 39 + '>8'
          time.sleep(1)
    return wrapped
