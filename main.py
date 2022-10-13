import random
import os
import sys
import shelve
import character 
import combat 
import world 
from script import line2004
from slowprint import print_slow
from pathlib import Path



def intro_load():
    global gameSetup
    while gameSetup == 2:
        print(
            'Would you like to load saved data? Type YES to load or NO to continue to setup and character creation.'
        )
        selc = input().upper().strip()
        if selc == 'YES':
            load()
            break
        elif selc == 'NO':
            gameSetup = 1
            break
        else:
            print('Please select a valid command.')


def setup():
    global gameSetup
    global p1

    typeSetup()
    while gameSetup == 1:
        print_slow("Please enter your character's NAME: \n", typingActive)
        player_name = input().strip()
        gameSetup = 2
        while gameSetup == 2:
            print_slow(
                "Please choose your CLASS: WARRIOR, WIZARD, or THIEF. Type HELP for assistance. \n",
                typingActive)
            player_job = input().upper().strip()
            print_slow('', typingActive)
            if player_job == "WARRIOR":
                p1 = character.player(player_name, player_job, ['HARDEN',], ['RUSTY DAGGER'],
                            [], 1, 100, 0, 70, 70, 3, 3, 16, 70, 0, 100, 95, 100, 10, 4,
                            5, 1, 5, 0, 5, 1, 0, 1, 'RUSTY DAGGER', None, None, None, None, None, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            'alive')
                gameSetup = 3
            elif player_job == "WIZARD" or player_job == "WITCH":
                p1 = character.player(player_name, player_job, ['FOCUS',], ['RUSTY DAGGER',], [],
                            1, 100, 0, 45, 45, 6, 6, 22, 89, 0, 100, 95, 100, 10, 3, 5,
                            1, 5, 1, 5, 1, 0, 1, 'RUSTY DAGGER', None, None, None, None, None, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'alive')
                gameSetup = 3
            elif player_job == "THIEF":
                p1 = character.player(player_name, player_job, ['STEAL',], ['RUSTY DAGGER'],
                            [], 1, 100, 0, 55, 55, 5, 5, 19, 78, 0, 100, 95, 100, 10, 3,
                            5, 2, 5, 1, 5, 3, 0, 1, 'RUSTY DAGGER', None, None, None, None, None, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            'alive')
                gameSetup = 3
            elif player_job == "GOD":
                p1 = character.player(
                    player_name, player_job,
                    ['HARDEN', 'STRIKE', 'BERSERK', 'FOCUS', 'BOLT', 'STORM', 'BLAST', 'STEAL', 'THROW', 'MUG', 'HASTE'], ['MAP', 'SHARP AXE', 'LANTERN', 'MESSER', 'ADAMANTITE SWORD', 'BUCKLER', 'MYTHRIL MAIL', 'BRIGANDINE', 'AETHON', 'FULGUR', 'MIDAS'], [], 1, 999999, 0, 999, 999, 99, 99, 99, 30, 0, 100, 100, 5000, 10, 10, 5, 5, 5, 5, 5, 5, 0, 1, None, None, None, None, None, None, None, 0, 1, 20, 10, 10, 10, 10, 10, 0, 0, 'alive')
                gameSetup = 3
            elif player_job == "INFO":
                character.stat_check_menu(typingActive)

            elif player_job == 'HELP':
                print_slow(
                    'Type your CLASS selection to choose your CLASS. Type INFO for CLASS details.\n',
                    typingActive)
            else:
                print_slow('Please select a valid command or type HELP.\n',
                           typingActive)
            while gameSetup == 3:
                p1.stat_check(typingActive)
                gameSetup = 0


def typeSetup():
    global typingActive
    textSetup = 1
    while textSetup == 1:
        print_slow(
            "\nWould you like to activate typing effect? Type ON or OFF.\n",
            typingActive)
        selc = input().upper().strip()
        i = [
            "ON",
            'OFF',
        ]
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
    global previous_room
    global player_choice
  
    while True:
        if 'secret_path' in world.rooms[current_room]:
          if world.rooms[current_room]['secret_path'] == 1:
            previous_room = current_room
            current_room = world.rooms[current_room]['SECRET_ROUTE']
            world.rooms[previous_room]['secret_path']  = 0
            player_choice = 1
            break
        if (selc in world.rooms[current_room] and selc in directions) and world.rooms[current_room][
                selc] == 'LOCKED':
            world.rooms[current_room]['LOCK'](p1, selc, world.rooms, typingActive)
        if (selc in world.rooms[
                current_room] and selc in directions) and world.rooms[current_room][selc] != 'LOCKED' and selc != 'SECRET_ROUTE':
            if world.rooms[current_room][selc] not in world.rooms[current_room][
                    'discovered']:
                world.rooms[current_room]['discovered'].append(
                    world.rooms[current_room][selc])
            previous_room = current_room
            current_room = world.rooms[current_room][selc]
            if previous_room not in world.rooms[current_room]['discovered']:
                world.rooms[current_room]['discovered'].append(previous_room)
            if selc in directions and selc != "CLIMB":
                print_slow(f'\nYou move to the {selc}.\n', typingActive)
            if selc == "CLIMB":
                print_slow(line2004, typingActive)
            encounter_initiaiton(current_room, typingActive)
            player_choice = 1
            if 'boss_ambush' in world.rooms[current_room]:
                world.rooms[current_room]['boss_ambush'](p1, typingActive)
                break
            break
        elif selc in directions and selc != "CLIMB":
            print_slow(f"\nYou cannot go to the {selc.lower()}.\n", typingActive)
            break
        else:
          break

def special_actions():
    global current_room
    while True:
      if 'secrets' in world.rooms[current_room]:
        if selc in world.rooms[current_room]['secrets']:
          world.rooms[current_room]['special'](p1, selc, typingActive)
          move_rooms()
        else:
          print_slow('\nInvalid selection. Try again.', typingActive)
      else:
          print_slow('\nInvalid selection. Try again.', typingActive)
      break
        
  
def take_actions():
    global current_room
    global player_choice
    while True:

        if selc == "EXPLORE":
              print_slow(world.rooms[current_room][selc], typingActive)
              break
        elif selc == "EXAMINE" and selc in world.rooms[current_room]:
              world.rooms[current_room]['EXAMINE'](p1, world.rooms, typingActive)
              move_rooms()
              break
        elif selc == "SPEAK" and selc in world.rooms[current_room]:
              world.rooms[current_room]['SPEAK'](p1, world.rooms, typingActive)
              break
        elif selc == "HEAL":
            if p1.POTS > 0:
                world.potion_healing(p1, typingActive)
                break
            else:
                print_slow(
                  f'{p1.name} is out of POTIONS and unable to heal at this time\n',
                  typingActive)
        elif selc == 'BUY' and selc in world.rooms[current_room]:
              world.rooms[current_room]['BUY'](p1, world.rooms, current_room, typingActive)
              break
        elif selc == 'TRADE' and selc in world.rooms[current_room]:
              world.rooms[current_room]['TRADE'](p1, world.rooms, current_room, typingActive)
              break
        elif selc == 'REST' and selc in world.rooms[current_room]:
              world.rooms[current_room]['REST'](p1, current_room, typingActive)
              break
        elif selc == 'PRAY' and selc in world.rooms[current_room]:
              world.rooms[current_room]['PRAY'](p1, typingActive)
              break
        elif selc == "UPGRADE" and selc in world.rooms[current_room]:
              world.rooms[current_room]['UPGRADE'](p1, current_room, typingActive)
              break
        elif (selc == "CRAFT" and selc in world.rooms[current_room]
              ) and world.rooms[current_room]['crafting'] == 'ACTIVE':
              world.rooms[current_room]['CRAFT'](p1, typingActive)
              break
        elif selc == "TEST" and selc in world.rooms[current_room]:
              world.rooms[current_room]['TEST']()
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
        elif selc == 'EQUIPMENT': 
            equipment_check(p1, typingActive)
            break
        elif selc == "LOCATION" or selc == "MAP":
            if 'MAP' in p1.inventory:
                print_slow(
                    f"\n**********[ {world.rooms[current_room]['name']} ]**********\n",
                    typingActive)
                print(world.rooms[current_room]['map'])
                if 'NORTH' in world.rooms[current_room]:
                    if world.rooms[current_room]['NORTH'] in world.rooms[current_room][
                            'discovered']:
                        print(f"N. {world.rooms[current_room]['NORTH']}")
                    else:
                        print('N. ???')
                if 'EAST' in world.rooms[current_room]:
                    if world.rooms[current_room]['EAST'] in world.rooms[current_room][
                            'discovered']:
                        print(f"E. {world.rooms[current_room]['EAST']}")
                    else:
                        print('E. ???')
                if 'SOUTH' in world.rooms[current_room]:
                    if world.rooms[current_room]['SOUTH'] in world.rooms[current_room][
                            'discovered']:
                        print(f"S. {world.rooms[current_room]['SOUTH']}")
                    else:
                        print('S. ???')
                if 'WEST' in world.rooms[current_room]:
                    if world.rooms[current_room]['WEST'] in world.rooms[current_room][
                            'discovered']:
                        print(f"W. {world.rooms[current_room]['WEST']}")
                    else:
                        print('W. ???')
                if 'CLIMB' in world.rooms[current_room]:
                    if world.rooms[current_room]['CLIMB'] in world.rooms[current_room][
                            'discovered']:
                        print(f"C. {world.rooms[current_room]['CLIMB']}")
                    else:
                        print('C. ???')
                
            else:
                print_slow(
                    f"\n**********[ {world.rooms[current_room]['name']} ]**********\n",
                    typingActive)
            break
        elif selc == "TYPE":
            typeSetup()
            break
        elif selc == "SAVE":
            save()
            break
        elif selc == "LOAD":
            load()
            break
        elif selc == "QUIT":
            quit_game()
            break
        elif selc == "PRINT":
            print(world.rooms[current_room])
            break


def item_check(p1, typingActive):
    while True:
        print_slow(
            f'\nPOTIONS: {p1.POTS}/{p1.MaxPOTS}\nANTIDOTES: {p1.ANT}/{p1.MaxANT}\nETHERS: {p1.ETR}/{p1.MaxETR}\nSMOKE BOMBS: {p1.SMB}/{p1.MaxSMB}',
            typingActive)
        print_slow(f'\nKey Items: {p1.inventory}\n', typingActive)
        print_slow('Type Key Item name for more info or BACK to exit menu.\n',
                   typingActive)
        selc = input().upper().strip()
        if selc in p1.inventory:
            print_slow(f"\n{world.key_items[selc]['description']}", typingActive)
            if 'description2' in world.key_items[selc]:
              print_slow(f"\n{world.key_items[selc]['description2']}", typingActive)
            if selc == 'CRAFTING POUCH':
                while True:
                    p1.materials_list()
                    print_slow(f"\n Crafting Items:\n", typingActive)
                    p1.material_print(typingActive)
                    print_slow(
                        'Type crafting material name for more info or BACK to return to previous menu.\n',
                        typingActive)
                    selc = input().upper().strip()
                    if selc == 'BACK':
                        break
                    elif selc in p1.materials:
                        print_slow("test", typingActive)
                        print_slow(f"\n{world.crafting_items[selc]['description']}",
                                   typingActive)
                    else:
                        print_slow('\nInvalid selection. Try again.',
                                   typingActive)
        elif selc == 'BACK':
            break
        else:
            print_slow('\nInvalid selection. Try again.', typingActive)


def encounter_initiaiton(current_room, typingActive):
    encounter = random.randrange(1, 6)
    if encounter <= world.rooms[current_room]['spawn_rate']:
        foe = random.choice(world.rooms[current_room]['enemy_spawn_set'])
        if foe == character.p28:
          world.traveling_merchant(p1, foe, current_room, typingActive)
        elif foe == character.p34:
          combat.standard_battle(p1, foe, typingActive)
          character.enemy_spawn14.remove(p34)
        else:
          combat.standard_battle(p1, foe, typingActive)


def ambush_initiaiton(current_room, typingActive):
    encounter = random.randrange(1, 6)
    if encounter <= world.rooms[current_room]['spawn_rate']:
        print_slow(f'{p1.name} is ambushed by an enemy!', typingActive)
        foe = random.choice(world.rooms[current_room]['enemy_spawn_set'])
        combat.standard_battle(p1, foe, typingActive)


def save():
    global p1
    #global world.rooms
    global current_room
    saveMenu = "OPEN"
    while saveMenu == "OPEN":
      print_slow('\nWould you like to save? YES or NO:\n', typingActive)
      selc = input().upper().strip()
      if selc == 'YES':
        print_slow('\nType name for your save:\n', typingActive)
        savefile1 = input().lower().strip()
        savePath = Path(sys.argv[0]).parent / Path(f'saves/{savefile1}')
        shelfFile = shelve.open(f'{savePath}')
        shelfFile['playerVar'] = p1 
        shelfFile['croomVar'] = current_room 
        shelfFile['roomVar'] = world.rooms 
        shelfFile.close()
        print_slow('\n*****[Save Complete]*****', typingActive)
        saveMenu = "CLOSED"
        break
      elif selc == 'NO':
        saveMenu = "CLOSED"
        break
      else:
        print_slow('\nInvalid selection. Try again.', typingActive)

def load():
  #"""sys.argv[0] is used to """
    global p1
    #global world.rooms
    global current_room
    global gameSetup
    print_slow('\nType name for your save file you wish to load, SHOW to see saves, or BACK to exit menu:', typingActive)
    loadMenu = "OPEN"
    while loadMenu == "OPEN":
        selc = input().lower().strip()
        savefile1 = selc      
        loadPath = Path(sys.argv[0]).parent / Path(f'saves/{savefile1}')
        if loadPath.is_file():
            shelfFile = shelve.open(f'{loadPath}')
            p1 = shelfFile['playerVar'] 
            current_room = shelfFile['croomVar'] 
            world.rooms = shelfFile['roomVar']
            shelfFile.close()
            loadMenu = "CLOSED"
            gameSetup = 0
            print_slow('\n*****[Load Complete]*****', typingActive)
            break
        if selc == 'show':
            path = Path('saves/')
            files = [file.stem for file in path.rglob('*')]
            print(sorted(files))
        elif selc == 'back':
            loadMenu = "CLOSED"
            break
        else:
            print_slow('\nInvalid selection. Try again.', typingActive)

def quit_game():
  while True:
    print_slow('\nAre you sure you wish to exit? YES or NO:\n', typingActive)
    selc = input().upper().strip()
    print('\n')
    if selc == 'YES':
      while True:
        print_slow('\nWould you like to save first? YES or NO:\n', typingActive)
        selc = input().upper().strip()
        print('\n')
        if selc == 'YES':
          save()
          quit()
        elif selc =='NO':
          quit()
        else:
          print_slow('\nInvalid selection. Try again.', typingActive)
    elif selc =='NO':
      break
    else:
      print_slow('\nInvalid selection. Try again.', typingActive)
def world_menu(typingActive):
    print_slow(
        '\nWorld commands:\nNORTH: Move NORTH.\nEAST: Move EAST.\nSOUTH: Move SOUTH.\nWEST: Move WEST.\nEXIT: Move to EXIT.\nEXPLORE: Check your surroundings.\nEXAMINE: Investigate area of interest.\nSPEAK: Talk to NPCs.\nHEAL: Use potion to restore HP.\nSTATS: View your current level and stats.\nITEMS: Check current inventory.\nEQUIPMENT: View equipment.\nMAP: Display current area.\nTYPE: Change text display settings.\nSAVE: Create save file.\nLOAD: Load a save file.\nQUIT: Exit the game.\Additional commands may be presented to you or hidden.\n',
        typingActive)



def equipment_check(p1, typingActive):
  while True:
      print_slow(f"\n**********{p1.name}'s Equipment**********\n", typingActive)
      print_slow(f"MAIN HAND: {p1.mainHand}\n", typingActive)
      print_slow(f"OFF HAND: {p1.offHand}\n", typingActive)
      print_slow(f"HEAD: {p1.head}\n", typingActive)
      print_slow(f"CHEST: {p1.chest}\n", typingActive)
      print_slow(f"LEGS: {p1.legs}\n", typingActive) 
      print_slow(f"ACCS1: {p1.accs1}\n", typingActive)
      print_slow(f"ACCS2: {p1.accs2}\n", typingActive)
      print_slow(f"Type the equipment slot you wish to change, or BACK to exit menu.\n", typingActive)
      selc = input().upper().strip()
      print('\n')
      if selc == 'MAIN HAND':
        s = set(world.mainHand_equipment)
        equipment = [x for x in p1.inventory if x in s]
        if p1.mainHand == None or p1.mainHand == 'EMPTY':
          print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
        elif p1.mainHand != None and p1.mainHand != 'EMPTY':
          print_slow(f'Equipped: {p1.mainHand}\nATK: {world.key_items[p1.mainHand]["ATK"]}\nDEF: {world.key_items[p1.mainHand]["DEF"]}%\nLVL: {world.key_items[p1.mainHand]["gear_level"]}\n"{world.key_items[p1.mainHand]["description2"]}"\n', typingActive)
        print_slow(f'Inventory: {equipment}\n',typingActive)
        change_gear = 1
        while change_gear == 1:
          print_slow(f"Type the item you wish to equip, or BACK to return to previous menu.\n", typingActive)
          selc = input().upper().strip()
          print('\n')
          if selc in equipment:
            if p1.job in world.key_items[selc]['classes']:
              if (p1.MaxHP + world.key_items[selc]['HP']) <= 0:
                print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.\n", typingActive)
              else:
                change_gear = 0
                previous_gear = p1.mainHand
                p1.mainHand = selc
                world.equip_stat_update(p1, selc, previous_gear)
            else:
              print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.\n', typingActive)
          elif selc == 'BACK':
            change_gear = 0
          else:
            print_slow('\nInvalid selection. Try again.\n', typingActive)
            
      elif selc == 'OFF HAND':
        s = set(world.offHand_equipment)
        equipment = [x for x in p1.inventory if x in s]
        if p1.offHand == None:
          print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
        if p1.offHand != None:
          print_slow(f'Equipped: {p1.offHand}\nATK: {world.key_items[p1.offHand]["ATK"]}\nDEF: {world.key_items[p1.offHand]["DEF"]}%\nLVL: N/A\n"{world.key_items[p1.offHand]["description2"]}"\n', typingActive)
        print_slow(f"\nInventory: {equipment}\n", typingActive)
        change_gear = 1
        while change_gear == 1:
          print_slow(f"Type the item you wish to equip, or BACK to return to previous menu.\n", typingActive)
          selc = input().upper().strip()
          print('\n')
          if selc in equipment:
            if p1.job in world.key_items[selc]['classes']:
              if (p1.MaxHP + world.key_items[selc]['HP']) <= 0:
                print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.\n", typingActive)
              else:
                change_gear = 0
                previous_gear = p1.offHand
                p1.offHand = selc
                world.equip_stat_update(p1, selc, previous_gear)
            else:
              print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.\n', typingActive)
          elif selc == 'BACK':
            change_gear = 0
          else:
            print_slow('\nInvalid selection. Try again.\n', typingActive)

      elif selc == 'HEAD':
        s = set(world.head_equipment)
        equipment = [x for x in p1.inventory if x in s]
        if p1.head == None:
          print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
        if p1.head != None:
          print_slow(f'Equipped: {p1.head}\nATK: {world.key_items[p1.head]["ATK"]}\nDEF: {world.key_items[p1.head]["DEF"]}%\nLVL: {world.key_items[p1.head]["gear_level"]}\n"{world.key_items[p1.head]["description2"]}"\n', typingActive)
        print_slow(f"\nInventory: {equipment}\n", typingActive)
        change_gear = 1
        while change_gear == 1:
          print_slow(f"Type the item you wish to equip, or BACK to return to previous menu.\n", typingActive)
          selc = input().upper().strip()
          print('\n')
          if selc in equipment:
            if p1.job in world.key_items[selc]['classes']:
              if (p1.MaxHP + world.key_items[selc]['HP']) <= 0:
                print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.\n", typingActive)
              else:
                change_gear = 0
                previous_gear = p1.head
                p1.head = selc
                world.equip_stat_update(p1, selc, previous_gear)
            else:
              print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.\n', typingActive)
          elif selc == 'BACK':
            change_gear = 0
          else:
            print_slow('\nInvalid selection. Try again.\n', typingActive)

      elif selc == 'CHEST':
        s = set(world.chest_equipment)
        equipment = [x for x in p1.inventory if x in s]
        if p1.chest == None:
          print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
        if p1.chest != None:
          print_slow(f'Equipped: {p1.chest}\nATK: {world.key_items[p1.chest]["ATK"]}\nDEF: {world.key_items[p1.chest]["DEF"]}%\nLVL: {world.key_items[p1.chest]["gear_level"]}\n"{world.key_items[p1.chest]["description2"]}"\n', typingActive)
        print_slow(f"\nInventory: {equipment}\n", typingActive)
        change_gear = 1
        while change_gear == 1:
          print_slow(f"Type the item you wish to equip, or BACK to return to previous menu.\n", typingActive)
          selc = input().upper().strip()
          print('\n')
          if selc in equipment:
            if p1.job in world.key_items[selc]['classes']:
              if (p1.MaxHP + world.key_items[selc]['HP']) <= 0:
                print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.\n", typingActive)
              else:
                change_gear = 0
                previous_gear = p1.chest
                p1.chest = selc
                world.equip_stat_update(p1, selc, previous_gear)
            else:
              print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.\n', typingActive)
          elif selc == 'BACK':
            change_gear = 0
          else:
            print_slow('\nInvalid selection. Try again.\n', typingActive)

      elif selc == 'LEGS':
        s = set(world.legs_equipment)
        equipment = [x for x in p1.inventory if x in s]
        if p1.legs == None:
          print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
        if p1.legs != None:
          print_slow(f'Equipped: {p1.legs}\nATK: {world.key_items[p1.legs]["ATK"]}\nDEF: {world.key_items[p1.legs]["DEF"]}%\nLVL: {world.key_items[p1.legs]["gear_level"]}\n"{world.key_items[p1.legs]["description2"]}"\n', typingActive)
        print_slow(f"\nInventory: {equipment}\n", typingActive)
        change_gear = 1
        while change_gear == 1:
          print_slow(f"Type the item you wish to equip, or BACK to return to previous menu.\n", typingActive)
          selc = input().upper().strip()
          print('\n')
          if selc in equipment:
            if p1.job in world.key_items[selc]['classes']:
              if (p1.MaxHP + world.key_items[selc]['HP']) <= 0:
                print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.\n", typingActive)
              else:
                change_gear = 0
                previous_gear = p1.legs
                p1.legs = selc
                world.equip_stat_update(p1, selc, previous_gear)
            else:
              print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.\n', typingActive)
          elif selc == 'BACK':
            change_gear = 0
          else:
            print_slow('\nInvalid selection. Try again.\n', typingActive)

      elif selc == 'ACCS1':
        s = set(world.accs_equipment)
        equipment = [x for x in p1.inventory if x in s]
        if p1.accs1 == None:
          print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
        if p1.accs1 != None:
          print_slow(f'Equipped: {p1.accs1}\nATK: {world.key_items[p1.accs1]["ATK"]}\nDEF: {world.key_items[p1.accs1]["DEF"]}%\nLVL: N/A\n"{world.key_items[p1.accs1]["description2"]}"\n', typingActive)
        print_slow(f"\nInventory: {equipment}\n", typingActive)
        change_gear = 1
        while change_gear == 1:
          print_slow(f"Type the item you wish to equip, or BACK to return to previous menu.\n", typingActive)
          selc = input().upper().strip()
          print('\n')
          if selc in equipment and selc != p1.accs2:
            if p1.job in world.key_items[selc]['classes']:
              if (p1.MaxHP + world.key_items[selc]['HP']) <= 0:
                print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.\n", typingActive)
              else:
                change_gear = 0
                previous_gear = p1.accs1
                p1.accs1 = selc
                world.equip_stat_update(p1, selc, previous_gear)
          elif selc in equipment and selc == p1.accs2:
            print_slow('\nThat item is equipped in another slot. Try another item.\n', typingActive)
          elif selc == 'BACK':
            change_gear = 0
          else:
            print_slow('\nInvalid selection. Try again.\n', typingActive)

      elif selc == 'ACCS2':
        s = set(world.accs_equipment)
        equipment = [x for x in p1.accs2 if x in s]
        if p1.accs2 == None:
          print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
        if p1.accs2 != None:
          print_slow(f'Equipped: {p1.accs2}\nATK: {world.key_items[p1.accs2]["ATK"]}\nDEF: {world.key_items[p1.accs2]["DEF"]}%\nLVL: N/A\n"{world.key_items[p1.accs2]["description2"]}"\n', typingActive)
        print_slow(f"\nInventory: {equipment}\n", typingActive)
        change_gear = 1
        while change_gear == 1:
          print_slow(f"Type the item you wish to equip, or BACK to return to previous menu.\n", typingActive)
          selc = input().upper().strip()
          print('\n')
          if selc in equipment and selc != p1.accs1:
            if p1.job in world.key_items[selc]['classes']:
              if (p1.MaxHP + world.key_items[selc]['HP']) <= 0:
                print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.\n", typingActive)
              else:
                change_gear = 0
                previous_gear = p1.accs2
                p1.accs2 = selc
              world.equip_stat_update(p1, selc, previous_gear)
          elif selc in equipment and selc == p1.accs1:
            print_slow('\nThat item is equipped in another slot. Try another item.\n', typingActive)
          elif selc == 'BACK':
            change_gear = 0
          else:
            print_slow('\nInvalid selection. Try again.\n', typingActive)
            
      elif selc == 'BACK':
        break
      else:
        print_slow('\nInvalid selection. Try again.\n', typingActive)



directions = ['NORTH', 'EAST', 'SOUTH', 'WEST', 'EXIT', 'CLIMB']
actions = [
    'EXPLORE', 'EXAMINE', 'SPEAK', 'HEAL', 'REST', 'PRAY', 'BUY', "TRADE", "UPGRADE",
    "CRAFT"
]

special_list = ['JUMP', 'FLY', 'SWIM', 'DIVE', 'DRINK', 'SEARCH', 'RIBBIT', 'RIBBITING', 'CROAK','CROAKING', 'KERO', 'KEROKERO', 'PLAY', 'WAIT', 'PICK', 'SAIL', 'THROW WEAPON', 'TANNINIM']

helper = [
    'HELP', 'STATS', 'ITEMS', 'LOCATION', 'MAP', 'TYPE', 'SAVE', 'LOAD',
    'PRINT', 'QUIT', 'EQUIPMENT'
]

current_room = 'Camp Site'
previous_room = ''

typingActive = "OFF"
gameSetup = 2
while True:
    while gameSetup == 2:
        intro_load()
    while gameSetup == 1:
        setup()
    while gameSetup == 0:
      print_slow(f"\n**********[ {world.rooms[current_room]['name']} ]**********\n",
                 typingActive)
      print_slow(world.rooms[current_room]['intro'], typingActive)
      player_choice = 0
      while player_choice == 0:
          print_slow('\nEnter command or type HELP:\n', typingActive)
          selc = input().upper().strip()
          print('\n')
          if selc in directions:
              move_rooms()
  
          elif selc in actions:
              take_actions()
  
          elif selc in special_list:
              special_actions()
  
          elif selc in helper:
              helper_actions()
          elif selc == 'TRASH':
            p1.inventory.remove('MAP')
            
          else:
              print_slow('\nInvalid selection. Try again.\n', typingActive)
