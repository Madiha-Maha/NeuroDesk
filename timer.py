import time

def start_timer(seconds, callback):
    while seconds:
          mins, secs = divmod(seconds, 60)
          timer = f'{mins:02d}:{secs:02d}'
          callback(timer)
          time.sleep(1)
          seconds -= 1