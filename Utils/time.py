import time

sleep_memory = {}
def sleep(ms):
  if not ms in sleep_memory:
    sleep_memory[ms] = ms / 1000
  return time.sleep(sleep_memory[ms])

def now():
  return time.time() * 1000

def diff(start, end=None):
  if end == None:
    end = now()
  return end - start
