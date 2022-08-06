import random
from character import *
from combat import *
from world import *
from script import line2004
from slowprint import *
global current_room



def setup():
  global gameSetup
  global p1
  
  typeSetup()    
  while gameSetup == 1:
    print_slow("Please enter your character's NAME: \n", typingActive)
    player_name = input().strip()
    gameSetup = 2
    while gameSetup == 2:
      print_slow("Please choose your CLASS: WARRIOR, WIZARD, or THIEF. Type HELP for assistance. \n", typingActive) 
      player_job = input().upper().strip()
      print_slow('', typingActive)
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
        p1 = player(player_name, player_job, ['LANTERN', 'AXE'], 1, 999999, 0, 999, 999, 99, 99, 99, 3, 10, 5000, 10, 10, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 'alive')
        gameSetup = 3
      elif player_job == "INFO":
        stat_check_menu(typingActive)
  
      elif player_job == 'HELP':
          print_slow(
              'Type your CLASS selection to choose your CLASS. Type INFO for CLASS details.\n', typingActive
          )
      else:
          print_slow('Please select a valid command or type HELP.\n', typingActive)
      while gameSetup == 3:
        p1.stat_check(typingActive)
        gameSetup = 0

def typeSetup():
  global typingActive
  textSetup = 1
  while textSetup == 1:
    print_slow("\nWould you like to activate typing effect? Type ON or OFF.\n", typingActive)
    selc = input().upper().strip()
    i = ["ON", 'OFF',]
    if selc == "ON":
      typingActive = "ON"
      textSetup = 0
    if selc == "OFF":
      typingActive = "OFF"
      textSetup = 0
    elif selc not in i:
       print_slow('Please select a valid command', typingActive)

def move_rooms():
  global current_room 
  global player_choice
  while True:
    if selc in rooms[current_room] and rooms[current_room][selc] == 'LOCKED':
        rooms[current_room]['LOCK'](p1, selc)
        break
    elif selc in rooms[current_room] and rooms[current_room][selc] != 'LOCKED':
        current_room = rooms[current_room][selc]
        if selc != "CLIMB":
          print_slow(f'\nYou move to the {selc}.\n', typingActive)
        if selc == "CLIMB":
          print_slow(line2004, typingActive)
        encounter_initiaiton(current_room, typingActive)
        player_choice = 1
        if 'boss_ambush' in rooms[current_room]:
          rooms[current_room]['boss_ambush'](p1)
          break
        break
    else:
        print_slow (f'\nYou can\'t go to the {selc.lower()}\n', typingActive)
        break

      
def take_actions():
  global current_room
  global player_choice
  while True:

    if selc == "EXPLORE":
      print_slow(rooms[current_room][selc], typingActive)
      break
    elif selc == "EXAMINE" and selc in rooms[current_room]:
      rooms[current_room]['EXAMINE'](p1)
      break
    elif selc == "SPEAK" and selc in rooms[current_room]:
      rooms[current_room]['SPEAK'](p1)
      break  
    elif selc == "HEAL":
      if p1.POTS > 0:
        potion_healing(p1, typingActive)  
        break
      else:
          print_slow(
              f'{p1.name} is out of POTIONS and unable to heal at this time\n', typingActive)
    elif selc == 'BUY' and selc in rooms[current_room]:
      city_shop(p1, typingActive)
      break
    elif selc == 'REST' and selc in rooms[current_room]:
      if rooms[current_room]['name'] == 'Camp Site':
        camp_healing(p1, typingActive)
        break
      elif rooms[current_room]['name'] in inns:
        city_inn(p1, typingActive)
        break
    elif selc == 'PRAY' and selc in rooms[current_room]:
      shrine_pray(p1, typingActive)
      break
    elif selc == "UPGRADE" and selc in rooms[current_room]:
      village_smith(p1, typingActive)
      break
    elif selc == "TEST" and selc in rooms[current_room]:
      rooms[current_room]['TEST']()
      break
    else:
      print_slow('Unable to do that here.\n', typingActive)
      break

      
def helper_actions():
  global current_room
  global player_choice

  while True:
    if selc == "HELP":
      world_menu(typingActive)
      break
    elif selc == "STATS":
      p1.stat_check(typingActive)
      break
    elif selc == "ITEMS":
      item_check(p1, typingActive)
      break 
    elif selc == "TYPE":
      typeSetup()
      break 

def item_check(p1):
      while True:
        print_slow(f'\nInventory: {p1.inventory}', typingActive)
        print_slow('Type item name for more info or BACK to exit menu.\n', typingActive)
        selc = input().upper().strip()
        if selc in p1.inventory:
          print_slow(f"\n{key_items[selc]['description']}", typingActive)
        elif selc == 'BACK':
          break
        else:
          print_slow('Invalid selection. Try again.', typingActive)


def encounter_initiaiton(current_room, typingActive):
    encounter = random.randrange(1, 6)
    if encounter <= rooms[current_room]['spawn_rate']:
        foe = random.choice(rooms[current_room]['enemy_spawn_set'])
        standard_battle(p1, foe, typingActive)     
      
def ambush_initiaiton(current_room, typingActive):
    encounter = random.randrange(1, 6)
    if encounter >= rooms[current_room]['spawn_rate'] * 2:
        print_slow(f'{p1.name} is ambushed by an enemy!', typingActive)
        foe = random.choice(enemy_spawn_set)
        standard_battle(p1, foe, typingActive)
      


def world_menu(typingActive):
    print_slow(
        '\nWorld commands:\nNORTH: Move NORTH.\nEAST: Move EAST.\nSOUTH: Move SOUTH.\nWEST: Move WEST.\nEXIT: Move to EXIT\nEXPLORE: Check your surroundings.\nEXAMINE: Investigate area of interest\nSPEAK: Talk to NPCs\nHEAL: Use potion to restore HP.\nSTATS: View your current level and stats.\nITEMS: Check current inventory\nTYPE: Change text display settings\nSome commands may be presented to you or hidden.\n',typingActive
    )

directions = ['NORTH', 'EAST', 'SOUTH', 'WEST', 'EXIT', 'CLIMB']
actions = ['EXPLORE', 'EXAMINE', 'SPEAK', 'HEAL', 'REST', 'PRAY', 'BUY', "UPGRADE"]
helper = ['HELP', 'STATS', 'ITEMS', 'TYPE']

inns = ['Inn', 'Tavern & Inn']
current_room = 'Camp'

typingActive = "OFF"
gameSetup = 1
while True:
  while gameSetup == 1:
    setup()
  print_slow(f"\n**********[ {rooms[current_room]['name']} ]**********\n", typingActive)
  print_slow(rooms[current_room]['intro'], typingActive)
  player_choice = 0
  while player_choice == 0:
    print_slow('\nEnter command:\n', typingActive)
    selc = input().upper().strip()
    if selc in directions:
      move_rooms()
    
    elif selc in actions:
      take_actions()

    elif selc in helper:
      helper_actions()
      
    else:
      print_slow('invalid', typingActive)