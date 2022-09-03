import sys
import time
def player_input():
  selc = input().upper().strip()
def print_slow(str, typingActive):
  if typingActive == "ON":
    for char in str:
      time.sleep(.01)
      sys.stdout.write(char)
      sys.stdout.flush()
    #print('')
  else:
    print(str)