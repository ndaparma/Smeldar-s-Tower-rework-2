import random
from character import *
from combat import *
from world import *


def setup():
  global gameSetup
  global p1
  
  while gameSetup == 1:
    print("Please enter your character's NAME: \n")
    player_name = input().strip()
    gameSetup = 2
    while gameSetup == 2:
      print("Please choose your CLASS: WARRIOR, WIZARD, or THIEF. Type HELP for assistance \n") 
      player_job = input().upper().strip()
      print('')
      if player_job == "WARRIOR":
        p1 = player(player_name, player_job, [], 1, 100, 0, 70, 70, 3, 3, 11, 7, 10, 100, 10, 4, 5, 1, 5, 0, 5, 1, 0, 0, 0, 0,'alive')
        gameSetup = 3
      elif player_job == "WIZARD":
        p1 = player(player_name, player_job, [], 1, 100, 0, 40, 40, 8, 8, 18, 9, 10, 100, 10, 3, 5, 1, 5, 1, 5, 1, 0, 0, 0, 0, 'alive')
        gameSetup = 3
      elif player_job == "THIEF":
        p1 = player(player_name, player_job, [], 1, 100, 0, 55, 55, 5, 5, 13, 8, 10, 100, 10, 3, 5, 2, 5, 1, 5, 3, 0, 0, 0, 0, 'alive')
        gameSetup = 3
      elif player_job == "GOD":
        p1 = player(player_name, player_job, ['AXE'], 1, 999999, 0, 999, 999, 99, 99, 99, 3, 10, 5000, 10, 10, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 'alive')
        gameSetup = 3
      elif player_job == "INFO":
        stat_check_menu()
  
      elif player_job == 'HELP':
          print(
              'Type your CLASS selection to choose your CLASS. Type INFO for CLASS details.\n'
          )
      else:
          print('Please select a valid command or type HELP.\n')
      while gameSetup == 3:
        p1.stat_check()
        gameSetup = 0


def move_rooms():
  global current_room 
  global player_choice
  while True:
    if selc in rooms[current_room] and rooms[current_room][selc] == 'LOCKED':
        rooms[current_room]['LOCK']()
        break
    elif selc in rooms[current_room] and rooms[current_room][selc] != 'LOCKED':
        current_room = rooms[current_room][selc]
        print(f'\nYou move to the {selc}.\n')
        encounter_initiaiton(current_room)
        player_choice = 1
        if 'boss_ambush' in rooms[current_room]:
          rooms[current_room]['boss_ambush']()
          break
        break
    else:
        print (f'\nYou can\'t go to the {selc.lower()}\n')
        break
      
def take_actions():
  global current_room
  global player_choice
  while True:

    if selc == "EXPLORE":
      print(rooms[current_room][selc])
      break
    elif selc == "EXAMINE" and selc in rooms[current_room]:
      rooms[current_room]['EXAMINE'](p1)
      break
    elif selc == "SPEAK" and selc in rooms[current_room]:
      rooms[current_room]['SPEAK'](p1)
      break  
    elif selc == "HEAL":
      if p1.POTS > 0:
        potion_healing(p1)  
        break
      else:
          print(
              f'{p1.name} is out of POTIONS and unable to heal at this time')
    elif selc == 'BUY' and selc in rooms[current_room]:
      city_shop(p1)
      break
    elif selc == 'REST' and selc in rooms[current_room]:
      if rooms[current_room]['name'] == 'Camp Site':
        camp_healing(p1)
        break
      elif rooms[current_room]['name'] in inns:
        city_inn(p1)
        break
    elif selc == 'PRAY' and selc in rooms[current_room]:
      shrine_pray(p1)
      break
    elif selc == "UPGRADE" and selc in rooms[current_room]:
      village_smith(p1)
      break
    elif selc == "TEST" and selc in rooms[current_room]:
      rooms[current_room]['TEST']()
      break
    else:
      print('Unable to do that here.')
      break
        
def helper_actions():
  global current_room
  global player_choice

  while True:
    if selc == "HELP":
      world_menu()
      break
    elif selc == "STATS":
      p1.stat_check()
      break
    elif selc == "ITEMS":
      p1.item_check()
      break 

def encounter_initiaiton(current_room):
    encounter = random.randrange(1, 6)
    if encounter <= rooms[current_room]['spawn_rate']:
        foe = random.choice(rooms[current_room]['enemy_spawn_set'])
        standard_battle(p1, foe)

directions = ['NORTH', 'EAST', 'SOUTH', 'WEST', 'EXIT']
actions = ['EXPLORE', 'EXAMINE', 'SPEAK', 'HEAL', 'REST', 'PRAY', 'BUY', "UPGRADE"]
helper = ['HELP', 'STATS', 'ITEMS']

game_setup = 0
inns = ['Inn', 'Tavern & Inn']
current_room = 'Camp'


gameSetup = 1
while True:
  while gameSetup == 1:
    setup()
  print(f"**********[ {rooms[current_room]['name']} ]**********\n")
  print(rooms[current_room]['intro'])
  player_choice = 0
  while player_choice == 0:
    print('\nEnter command:')
    selc = input().upper().strip()
    if selc in directions:
      move_rooms()
    
    elif selc in actions:
      take_actions()

    elif selc in helper:
      helper_actions()
      
    else:
      print('invalid')