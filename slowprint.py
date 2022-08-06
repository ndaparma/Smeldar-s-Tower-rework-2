import sys
import time

def print_slow(str, typingActive):
  if typingActive == "ON":
    for char in str:
      time.sleep(.02)
      sys.stdout.write(char)
      sys.stdout.flush()
  else:
    print(str)