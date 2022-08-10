import sys
import time
def player_input():
  selc = input().upper().strip()
def print_slow(str, typingActive):
  if typingActive == "ON":
    for char in str:
      time.sleep(.015)
      sys.stdout.write(char)
      sys.stdout.flush()
    #print('')
  else:
    print(str)