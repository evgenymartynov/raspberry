import theta
import time

def exception_worker():
  raise Exception('blah')

t = theta.ResilientThread(name='TestThread', target=exception_worker)
t.daemon = True

t.start()
t.join(3)
