from script import *
from character import *
import random
#Contains room and item information

#define rooms/areas for game


def city_shop(p1): #City Shop mechanics
    potion = 25
    smoke_bomb = 35
    antd = 30
    ether = 40
    lantern_price = 200
    
    while True:
        print(
            "Purchase a POTION for [25GP], an ANTIDOTE for [30GP], an ETHER for [40GP], a SMOKE BOMB for [35GP], or a LANTERN for [200GP]. Type your selection or BACK to leave shopping window."
        )

        selc = (input().upper()).strip()
        print("")

        if (selc == 'POTION' and p1.GP >= potion) and p1.POTS < p1.MaxPOTS:
            p1.GP -= 25
            p1.POTS = min(p1.POTS + 1, p1.MaxPOTS)
            print(
                f'{p1.name} purchases a POTION and puts it in their bag. {p1.name} now has {p1.POTS} POTIONS and {p1.GP}GP.\n'
            )
          

        elif (selc == 'SMOKE BOMB'
              and p1.GP >= smoke_bomb) and p1.SMB < p1.MaxSMB:
            p1.GP -= 35
            p1.SMB = min(p1.SMB + 1, p1.MaxSMB)
            print(
                f'{p1.name} purchases a SMOKE BOMB and puts it in their bag. {p1.name} now has {p1.SMB} SMOKE BOMBS and {p1.GP}GP.\n'
            )

        elif (selc == 'ANTIDOTE' and p1.GP >= antd) and p1.ANT < p1.MaxANT:
            p1.GP -= 30
            p1.ANT = min(p1.ANT + 1, p1.MaxANT)
            print(
                f'{p1.name} purchases an ANTIDOTE and puts it in their bag. {p1.name} now has {p1.ANT} ANTIDOTES and {p1.GP}GP.\n'
            )

        elif (selc == 'ETHER' and p1.GP >= ether) and p1.ETR < p1.MaxETR:
            p1.GP -= 40
            p1.ETR = min(p1.ETR + 1, p1.MaxETR)
            print(
                f'{p1.name} purchases an ETHER and puts it in their bag. {p1.name} now has {p1.ETR} ETHERS and {p1.GP}GP.\n'
            )     

        elif (selc == 'LANTERN'
              and 'LANTERN' not in p1.inventory) and p1.GP >= lantern_price:
            p1.GP -= 200
            p1.inventory.append('LANTERN')
            print(
                f'{p1.name} purchases a LANTERN and straps it to their belt. {p1.name} can stop being afraid of the dark! {p1.GP}GP remaining.\n'
            )

        elif (selc == 'POTION' and p1.GP < potion) or (
                selc == 'SMOKE BOMB' and p1.GP < smoke_bomb) or (
                    selc == 'ANTIDOTE'
                    and p1.GP < antd) or (selc == 'ETHER' and p1.GP < ether) or ((selc == 'LANTERN'
              and 'Lantern' not in p1.inventory) and p1.GP < lantern_price):
            print(
                f'{p1.name} does not have enough GP to purchase this item.\n')

        elif ((selc == "POTION" and p1.POTS == p1.MaxPOTS) or
              (selc == "SMOKE BOMB" and p1.SMB == p1.MaxSMB) or
                  (selc == "ANTIDOTE" and p1.ANT == p1.MaxANT) or
                  (selc == "ETHER" and p1.ETR == p1.MaxETR) or (selc == 'LANTERN' and 'LANTERN' in p1.inventory)):
            print(
                f'\n"Hey, looks like your p1.inventory is full."\n\n{p1.name} is unable to purchase more of this item.\n'
            )

        elif selc == "BACK":
          break
        else:
           print('That command is invalid.\n')


def city_inn(p1):  #Inn Mechanics
    inn_room = 40
    
    while True:

        if p1.GP >= inn_room:
            p1.GP -= 40
            heal = random.randrange(50, 100)
            p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
            print(
                f'\n{p1.name} took a well earned rest and restored HP. {p1.name} has {p1.HP}/{p1.MaxHP}HP, and {p1.GP}GP.\n'
            )
            break

        elif p1.GP < inn_room:
            print(
                f'{p1.name} does not have enough GP in their wallet. {p1.name} has {p1.GP}GP.\n'
            )
            break
def village_smith(p1):
  while True:
    if p1.GrLvl < 5:
        print(f"Improve WEAPON or ARMOR for {rooms['Smith']['upgrade_cost']}GP or go BACK?")
        selc = (input().upper()).strip()
        print("")
        if selc == "WEAPON" and p1.GP >= rooms['Smith']['upgrade_cost']:
          p1.GrLvl += 1
          p1.ATK += 1
          p1.GP -= rooms['Smith']['upgrade_cost']
          rooms['Smith']['upgrade_cost'] = rooms['Smith']['upgrade_cost'] * 2
          print(f"The SMITH takes back {p1.name}'s WEAPON and begins making improvements. After a while he returns with your UPGRADED gear.")
          p1.stat_check()
        elif selc == "ARMOR" and p1.GP >= rooms['Smith']['upgrade_cost']:
          p1.GrLvl += 1
          p1.DEF = max(p1.DEF - .5, 3)
          p1.GP -= rooms['Smith']['upgrade_cost']
          rooms['Smith']['upgrade_cost'] = rooms['Smith']['upgrade_cost'] * 2
          print(f"The SMITH takes back {p1.name}'s ARMOR and begins making improvements. After a while he returns with your UPGRADED gear.")
          p1.stat_check()
        elif (selc == "WEAPON" or selc == "ARMOR") and p1.GP < rooms['Smith']['upgrade_cost']:
          print( f"{p1.name} does not have enough GP for an UPGRADE. {p1.name} only has {p1.GP} GP.\n")
        elif selc == "BACK":
          break
        else:
          print('Invalid command. Please select WEAPON or ARMOR, or BACK to leave.') 
    else:
        print(line1903)
        break
def potion_healing(p1):
  heal = 15 + p1.RJ
  p1.POTS -= 1
  p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
  print(
      f'{p1.name} drinks a POTION and heals {heal} HP. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n'
  )
def camp_healing(p1):
  while True:
    if rooms['Camp']['fire'] > 0:
      heal = random.randrange(10, 20)
      p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
      rooms['Camp']['fire'] -= 1
      print(f'\n{p1.name} has rested and restored {heal}HP. {p1.name} now has {p1.HP}/{p1.MaxHP}HP.\n')
      if rooms['Camp']['fire'] > 0:
        print(f"{p1.name} may rest {rooms['Camp']['fire']} times before the camp fire dies.")
        break
      else:
        rooms['Camp']['intro'] = line102
        print(
                f'The fire has finally died and {p1.name} is unable to rest here.'
            )
        break
    else:
      print(
              f'The fire has finally died and {p1.name} is unable to rest here.'
          )
      break

def shrine_pray(p1):
  if p1.GP >= 35:
    p1.MP = p1.MaxMP
    p1.GP -= 35
    print(f"{p1.name} drops 35 GP into an ornate donation box and kneels between the lanterns at the alter. {p1.name} is filled with a surge of power. {p1.name}'s MP is fully restored.")
  else:
    print(f"{p1.name} is too poor to spend on charity.")

def cliff_examine(p1):
  while True:
    if rooms['Cliff']['chest'] == "CLOSED" and 'AXE' not in p1.inventory:
      print(line604)
      break
    elif rooms['Cliff']['chest'] == "CLOSED" and 'AXE' in p1.inventory:
      print(line605)
      selc = (input().upper()).strip()
      print("")
      if selc == "CUT":
          print(line605b)
          rooms['Cliff']['chest'] = "OPEN"
          p1.inventory.append('PENDANT')
          rooms['Cliff']['EXPLORE'] = line603
          break

      elif selc == "BACK" or selc == "BACK OUT":
          print(line605c)
          break
      else:
          print('That command is invalid.\n')
    else:
      print(line605d)
      break

def hill_examine(p1):
  while True:
    if rooms['Hill']['SOUTH'] == 'LOCKED':
      if 'AXE' not in p1.inventory:
        print(line805)
        break
      elif 'AXE' in p1.inventory:
        print(line805b)
        selc = (input().upper()).strip()
        print("")
        if selc == 'CUT':
          print(line806)
          rooms['Hill']['SOUTH'] = 'Berry'
          rooms['Hill']['EXPLORE'] = line804
          break
        elif selc == 'LEAVE':
          print(line806b)
          break
        else:
          print('That command is invalid.\n')
    else:
      print(line811)
      break
def waterfall_examine(p1):
  while True:
    if rooms['Waterfall']['chest'] == 'CLOSED':
      print(line1302b)
      selc = (input().upper()).strip()
      print("")
      if selc == "TAKE":
          print(line1303)
          p1.inventory.append('SALMON')
          rooms['Waterfall']['chest'] = 'OPEN'
          break
      elif selc == "SAVE":
          print(line1304)
          rooms['Waterfall']['chest'] = 'OPEN'
          rooms['Waterfall']['event'] = 1
          break
      elif selc == "LEAVE":
          print(line1305)
          break
      else:
          print('That command is invalid.\n')
    elif rooms['Waterfall']['chest'] == 'OPEN':
      if rooms['Waterfall']['event'] == 1:
        print(line1307)
        p1.GP += 100
        rooms['Waterfall']['event'] = 2
        print(f'\n{p1.name} has {p1.GP}GP.\n')
        break
      else:
        print(line1308)
        break 
          
def lake_examine(p1):
  while True:
    if rooms['Lake']['EAST'] == 'LOCKED':
      if 'AXE' not in p1.inventory:
        print(line1404)
        break
      elif 'AXE' in p1.inventory:
        print(line1405)
        selc = (input().upper()).strip()
        print("")
        if selc == 'CUT':
          print(line1406)
          boss_initiaiton()
          print(line1408)
          rooms['Lake']['EAST'] = 'Mushroom'
          rooms['Lake']['EXPLORE'] = line1403
          break
        elif selc == 'LEAVE':
          print(line1407)
          break
        else:
          print('That command is invalid.\n')
    else:
      print(line1408)
      break
  
def cave_examine(p1):
  while True:
    if 'Bear' in rooms['Cave']['boss']:
      if 'SALMON' not in p1.inventory:
        print(f'\n{line903}')
      else:
        print(f'\n{line904}')
      selc = (input().upper()).strip()
      print("")
      if selc == "POKE":
          print(line911)
          boss_initiaiton()
          rooms['Cave']['boss'].remove('Bear')
          p1.inventory.append('AXE')
          rooms['Cave']['intro'] = line902
          rooms['Cave']['EXPLORE'] = line906b
          print(line912)
          break

      elif selc == "FEED" and 'SALMON' in p1.inventory:
          p1.inventory.remove('SALMON')
          rooms['Cave']['boss'].remove('Bear')
          p1.inventory.append('AXE')
          rooms['Cave']['intro'] = line902
          rooms['Cave']['EXPLORE'] = line906b
          print(line913)
          break
      elif selc == "BACK" or selc == "BACK OUT":
          print(line907)
          break
      else:
          print('That command is invalid.\n')
    else:
      print(line912b)
      break
    

def cave2_examine(p1):
  while True:
    if rooms['Cave2']['chest'] == "CLOSED":
      print(line925)
      selc = (input().upper()).strip()
      print("")
      if selc == "OPEN":
          print(line926)
          boss_initiaiton()
          rooms['Cave2']['chest'] = "OPEN"
          p1.inventory.append('IRON KEY')
          rooms['Cave2']['EXPLORE'] = line924
          print(line927)
          break

      elif selc == "BACK" or selc == "BACK OUT":
          print(line928)
          break
      else:
          print('That command is invalid.\n')
    else:
      print(line928b)
      break
    

def cave4_examine(p1):

  while True:
     if rooms['Cave4']['EAST'] == 'LOCKED':
      if 'IRON KEY' not in p1.inventory:
        print(f'\n{line940}')
        break
      else:
        print(f'\n{line940b}')
        selc = (input().upper()).strip()
        print("")
        if selc == "OPEN":
            print(line941)
            rooms['Cave4']['EAST'] = 'Cave5'
            rooms['Cave4']['EXPLORE'] = line939
            break
        elif selc == "BACK" or selc == "BACK OUT":
            print(line941b)
            break
        else:
            print('That command is invalid.\n')
  


def berry_examine(p1):
  while True:
    if rooms['Berry']['chest'] == 'CLOSED':
      print(line1002b)
      selc = (input().upper()).strip()
      print("")
      if selc == "PICK":
        print(line1003)
        boss_initiaiton()
        print(line1004)
        berriesPicked = random.randrange(2, 6)
        p1.POTS = min(p1.POTS + berriesPicked, p1.MaxPOTS)
        rooms['Berry']['chest'] = "OPEN"
        rooms['Berry']['EXPLORE'] = line1005
        print(f'{p1.name} has made {berriesPicked} POTIONS. {p1.name} has {p1.POTS} POTS.')
        break
      elif selc == "LEAVE":
        print(line1002c)
        break
      else:
            print('That command is invalid.\n')
    else:
      print(line1006)
      break

def oak_examine(p1):
  global current_room
  while True:
    print(line2003)
    selc = (input().upper()).strip()
    print("")
    if selc == "CLIMB":
      print(line2004)
      current_room = 'Hive'
      rooms[current_room]['boss_ambush']()
      print(f"\n**********[ {rooms[current_room]['name']} ]**********\n")
      print(rooms[current_room]['intro'])
      break
    elif selc == "BACK":
      print(line2005)
      break
    else:
      print('That command is invalid.\n')

def hive_examine(p1):
  global current_room
  while True:
    if rooms['Hive']['chest'] == "CLOSED":
      print(line2105b)
      p1.POTS = min(p1.POTS + 3, p1.MaxPOTS)
      rooms['Hive']['EXPLORE'] = line2106
      rooms['Hive']['chest'] = "OPEN"
      break
    else:
      print(line2106b)
      break

def mushroom_examine(p1):
  while True:
    if p1.gCount >= 10 and rooms['Mushroom']['chest'] == 'CLOSED':
      print(line1604)
      p1.inventory.append('HEROS MEDAL')
      rooms['Mushroom']['chest'] = 'OPEN'
      break
    elif p1.gCount >= 10 and rooms['Mushroom']['chest'] == 'OPEN':
      print(line1604b)
      break
    else:
      print(line1603)
      break
def hill_lock(p1):
  while True:
    if rooms['Hill']['SOUTH'] == 'LOCKED':
      print(line811)
      break
    else:
      continue
def lake_lock(p1):
  while True:
    if rooms['Lake']['EAST'] == 'LOCKED':
      print(line1410)
      break
    else:
      continue
def cave_lock(p1):
  while True:
    if 'Bear' in rooms['Cave']['boss']:
      print(line914)
      break
    elif (selc == 'EAST' and rooms['Cave']['EAST'] == 'LOCKED') and "LANTERN" not in p1.inventory:
      print(line909)
      break
    elif (selc == 'EAST' and rooms['Cave']['EAST'] == 'LOCKED') and "LANTERN" in p1.inventory:
      print(line915)
      rooms['Cave']['EAST'] = 'Cave1'
      break
    else:
      continue
      
      
def cave4_lock(p1):
  while True:
    if rooms['Cave4']['EAST'] == 'LOCKED':
      print(line943)
      break
    else:
      continue

      
def cave4_boss_ambush(p1): 
  while True:
    if 'Hobgoblin Gang' in rooms['Cave4']['boss']:
      print(line935)
      boss_initiaiton()
      rooms['Cave4']['boss'].remove('Hobgoblin Gang')
      rooms['Cave4']['spawn_rate'] = 4
      print(line936)
    else:
      break
def cave5_boss_ambush(p1):
  while True:
    if 'Goblin Queen' in rooms['Cave5']['boss']:
      print(line947)
      boss_initiaiton()
      rooms['Cave5']['boss'].remove('Goblin Queen')
      p1.inventory.append('DRAGON BONE KEY')
      print(line949)
    else:
      break
def hive_boss_ambush(p1):
  global enemy_spawn3
  global enemy_spawn9 
  while True:
    if 'Giant Bee Queen' in rooms['Hive']['boss']:
      print(line2101)
      encounter_initiaiton()
      print(line2101b)
      encounter_initiaiton()
      print(line2101b)
      encounter_initiaiton()
      print(line2102)
      boss_initiaiton()
      rooms['Hive']['boss'].remove('Giant Bee Queen')
      rooms['Hive']['spawn_rate'] = 0
      p1.inventory.append('ROYAL JELLY')
      enemy_spawn3.remove(p14)
      enemy_spawn9.remove(p14)
      enemy_spawn3.append(p25)
      enemy_spawn9.append(p25)
      p1.RJ += 5
      print(line2103)
      current_room = 'Oak'
     # print(f"\n**********[ {rooms[current_room]['name']} ]**********\n")
    else:
      break
def castle_speak(p1):
  while True:
    if rooms['Castle']['speach'] == 0:
      print(line505)
      print(line506)
      rooms['Castle']['speach'] += 1
      break
    elif 'HEROS MEDAL' in p1.inventory and rooms['Castle']['event'] == 0:
      print(line505)
      print(line508)
      p1.MaxHP += 25
      p1.HP = p1.MaxHP
      p1.stat_check()
      rooms['Castle']['event'] = 1
      key_items['HEROS MEDAL']['description'] = 'A gold medal found on a corpse covered in mushrooms. Engraved with the royal crest on the front; the back reads "For Jeremy the Goblin-Slayer". You can feel the medal filling you with vigor ever since the princess unlocked its magic.'
      break
    elif rooms['Castle']['speach'] == 1:
      print(line505)
      print(line507)
      break
def boat_speak(p1):
  while True:
    if rooms['Boat']['speach'] == 0:
      print(line1504)
      rooms['Boat']['speach'] = 1
      break
    elif rooms['Boat']['speach'] == 1 and 'SALMON' in p1.inventory:
      print(line1506) 
      selc = (input().upper()).strip()
      print("")
      if selc == "GIVE":
        print(line1508)
        print(f'{p1.name} was given a BUCKLER! This sturdy steel shield should help block damage. {p1.name} has gained 5% DEF!')
        p1.DEF = max(p1.DEF - 1.5, 3)
        rooms['Boat']['speach'] = 2
        rooms['Boat']['EXPLORE'] = line1503
        p1.inventory.remove('SALMON')
        p1.inventory.append('BUCKLER')
        p1.stat_check()
        break
      elif selc == "KEEP":
        print(line1507)
        break
      else:
        print('That command is invalid.\n')
    elif rooms['Boat']['speach'] == 1 and 'SALMON' not in p1.inventory:
      print(line1510)
      break
    else:
      print(line1509)
      break


def shrine_speak(p1):
  while True:
    if rooms['Shrine']['speach'] == 0:
      print(line1105)
      print(line1106)
      rooms['Shrine']['speach'] = 1
      break
    elif rooms['Shrine']['speach'] == 1 and 'PENDANT' in p1.inventory:
      print(line1108) 
      print(line1109) 
      print(f"{p1.name} is given the FRIAR's MESSER. This single edge sword is finely crafted. Much better than the rusty old blade you found in the trash before you started adventuring... {p1.name} gained 5 ATK")
      p1.inventory.remove('PENDANT')
      p1.inventory.append('MESSER')
      p1.ATK += 5
      p1.stat_check()
      break
    elif rooms['Shrine']['speach'] == 1:
      print(line1107)
      break



rooms = {
    '' : {
        'name' : '',
        'intro' : '',
        'NORTH' : None,
        'EAST' : None,
        'SOUTH' : None,
        'WEST' : None,
        'EXPLORE': '',
        'EXAMINE' : None,
        'SPEAK' : None,
        'REST' : 'rest',
        'PRAY' : 'pray',
        'BUY' : "BUY",
        'speach' : None,
        'spawn_rate' : 0,
        'enemy_spawn_set' : None,
        'boss' : [],
        'boss_ambush' : None,
        'foe' : None,
        'LOCK' : None,
        'chest' : None,
        'event' : None,
    },

    'Camp' : {
        'name' : 'Camp Site',
        'intro' : line101,
        'NORTH' : 'Forest',
        'SOUTH' : 'Town',
        'WEST' : 'Cliff',
        'EXPLORE': line103,
        'REST': 'rest',
        'fire' : 3,
        'spawn_rate' : 0,
    },

    'Cliff' : {
        'name' : 'Cliff Side',
        'intro' : line601,
        'EAST' : 'Camp',
        'EXPLORE': line602,
        'EXAMINE' : cliff_examine,
        'spawn_rate' : 2,
        'enemy_spawn_set' : enemy_spawn0,
        'chest' : 'CLOSED',
    },
#Town start
  'Town' : {
        'name' : 'Town Center',
        'intro' : line201,
        'NORTH' : 'Camp',
        'EAST' : 'Shop',
        'SOUTH' : 'Castle',
        'WEST' : 'Inn',
        'EXPLORE': line202,
        'spawn_rate' : 0,
    },

  'Shop' : {
        'name' : 'Shop',
        'intro' : line301,
        'WEST' : 'Town',
        'EXIT' : 'Town',
        'EXPLORE': line304,
        'BUY' : "BUY",
        'spawn_rate' : 0,
    },

  'Inn' : {
        'name' : 'Inn',
        'intro' : line401,
        'EAST' : 'Town',
        'EXIT' : 'Town',
        'EXPLORE': line404,
        'REST' : 'rest',
        'spawn_rate' : 0,
    },

  'Castle' : {
        'name' : 'Royal Castle',
        'intro' : line501,
        'NORTH' : 'Town',
        'EXIT' : 'Town',
        'EXPLORE': line502,
        'spawn_rate' : 0,
        'SPEAK' : castle_speak,
        'speach' : 0,
        'event' : 0,
    }, #Town end

  'Forest' : {
        'name' : 'Deep Forest',
        'intro' : line701,
        #'NORTH' : 'Thicket',
        'EAST' : 'Hill',
        'SOUTH' : 'Camp',
        'WEST' : 'River',
        'EXPLORE': line702,
        'spawn_rate' : 2,
        'enemy_spawn_set' : enemy_spawn1,
    },

  'Hill' : {
        'name' : 'Rocky Hill',
        'intro' : line801,
        'NORTH' : 'Shrine',
        'EAST' : 'Cave',
        'SOUTH' : 'LOCKED',
        'WEST' : 'Forest',
        'EXPLORE' : line802,
        'EXAMINE' : hill_examine, 
        'spawn_rate': 3,
        'enemy_spawn_set' : enemy_spawn6,
        'LOCK' : hill_lock,
    },
  
  'Shrine' : {
        'name' : 'Mystic Shrine',
        'intro' : line1101,
        'SOUTH' : 'Hill',
        'EXPLORE': line1102,
        'SPEAK' : shrine_speak,
        'PRAY' : 'PRAY',
        'speach' : 0,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn4,
    },
#Dungeon 1 start
  'Cave' : {
        'name' : 'Bear Cave',
        'intro' : line901,
        'WEST' : 'Hill',
        'EAST' : 'LOCKED',
        'EXPLORE': line906,
        'EXAMINE' : cave_examine,
        'spawn_rate' : 0,
        'boss' : ['Bear'],
        'foe' : p12,
        'LOCK' : cave_lock,
    },

  'Cave1' : {
        'name' : 'Rocky Cave',
        'intro' : line916,
        'NORTH' : 'Cave2',
        'SOUTH' : 'Cave3',
        'WEST' : 'Cave',
        'EXPLORE': line917,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn8,
    },

  'Cave2' : {
        'name' : 'Rocky Cave',
        'intro' : line922,
        'SOUTH' : 'Cave1',
        'EXPLORE': line923,
        'EXAMINE' : cave2_examine,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn8,
        'chest' : 'CLOSED',
    },
  'Cave3' : {
        'name' : 'Rocky Cave',
        'intro' : line931,
        'NORTH' : 'Cave1',
        'SOUTH' : 'Cave4',
        'EXPLORE': line932a,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn8,
    },
  'Cave4' : {
        'name' : 'Rocky Cave',
        'intro' : line937,
        'NORTH' : 'Cave3',
        'EAST' : 'LOCKED',
        'EXPLORE' : line938,
        'EXAMINE' : cave4_examine,
        'spawn_rate' : 0,
        'enemy_spawn_set' : enemy_spawn8,
        'boss' : ['Hobgoblin Gang'],
        'boss_ambush' : cave4_boss_ambush,
        'foe' :  p23,
        'LOCK' : cave4_lock,
    },
  'Cave5' : {
        'name' : "Queen's Chamber",
        'intro' : line948,
        'WEST' : 'Cave4',
        'EXPLORE': line950,
        'spawn_rate' : 0,
        'boss' : ['Goblin Queen'],
        'boss_ambush' : cave5_boss_ambush,
        'foe' : p22,
    }, #Dungeon 1 end

  'River' : {
        'name' : 'River Channel',
        'intro' : line1201,
        'NORTH' : 'Lake',
        'EAST' : 'Forest',
        'SOUTH' : 'Waterfall',
        'EXPLORE': line1202,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn5,
    },

  'Waterfall' : {
        'name' : 'Waterfall Pool',
        'intro' : line1301,
        'NORTH' : 'River',
        'EXPLORE': line1302,
        'EXAMINE' : waterfall_examine,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn5,
        'chest' : 'CLOSED',
        'event' : 0,
    },

  'Lake' : {
        'name' : 'Lake Beach',
        'intro' : line1401,
        'NORTH' : 'Boat',
        'EAST' : 'LOCKED',
        'SOUTH' : 'River',
        'EXPLORE': line1402,
        'EXAMINE': lake_examine,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn5,
        'foe' : p16,
        "LOCK" : lake_lock,
    },

  'Boat' : {
        'name' : 'Boat House',
        'intro' : line1501,
        'SOUTH' : 'Lake',
        'EXPLORE': line1502,
        'SPEAK' : boat_speak,
        'speach' : 0,
        'spawn_rate' : 0,
    },

  'Berry' : {
        'name' : 'Berry Patch',
        'intro' : line1001,
        'NORTH' : 'Hill',
        'EAST' : 'Meadow',
        'EXPLORE': line1002,
        'EXAMINE' : berry_examine,
        'spawn_rate' : 2,
        'enemy_spawn_set' : enemy_spawn3,
       # 'foe' : p15,
        'chest' : 'CLOSED',
    },

  'Meadow' : {
        'name' : 'Flower Meadow',
        'intro' : line1701,
        #'NORTH' : 'Witch',
        'EAST' : 'Oak',
        'SOUTH' : 'Village',
        'WEST' : 'Berry',
        'EXPLORE': line1702,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn9,
        'foe' : None,
        'chest' : None,
        'event' : None,
    },
#Quite Village start
  'Village' : {
        'name' : 'Quiet Village',
        'intro' : line1801,
        'NORTH' : 'Meadow',
        #'EAST' : 'Farm',
        'SOUTH' : 'Tavern',
        'WEST' : 'Smith',
        'EXPLORE': line1802,
        'spawn_rate' : 0,
    },

  'Tavern' : {
        'name' : 'Tavern & Inn',
        'intro' : line401b,
        'NORTH' : 'Village',
        'EXIT' : 'Village',
        'EXPLORE': line404b,
        'REST' : 'rest',
        'spawn_rate' : 0,
    },

  'Smith' : {
        'name' : "Smith's Workshop",
        'intro' : line1901,
        'EAST' : 'Village',
        'EXIT' : 'Village',
        'EXPLORE': line1902,
        'UPGRADE' : village_smith,
        'upgrade_cost' : 75,
        'spawn_rate' : 0,
    },

#Quite Village end
  'Oak' : {
        'name' : 'Great Oak',
        'intro' : line2001,
        'WEST' : 'Meadow',
        'EXPLORE': line2002,
        'EXAMINE' : oak_examine,
        'spawn_rate' : 0,
 
    },

  'Hive' : {
        'name' : 'Bee Hive',
        'intro' : line2104,
        'EXIT' : 'Oak',
        'EXPLORE': line2105,
        'EXAMINE' : hive_examine,
        'spawn_rate' : 7,
        'enemy_spawn_set' : enemy_spawn10,
        'boss' : ['Giant Bee Queen'],
        'boss_ambush' : hive_boss_ambush,
        'foe' : p24,
        'chest' : "CLOSED",
    },
  'Mushroom' : {
        'name' : 'Mushroom Grove',
        'intro' : line1601,
        #'NORTH' : 'Swamp',
        #'SOUTH' : 'Fairy',
        'WEST' : 'Lake',
        'EXPLORE': line1602,
        'EXAMINE' : mushroom_examine,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn7,
        #'LOCK' : None,
        'chest' : "CLOSED",
        #'event' : None,
    },
}


#define player key items

key_items = {
    '': {
        'name': '',
        'description': '',
    },
    'LANTERN': {
        'name': 'LANTERN',
        'description': 'A lantern that attaches to a belt for hands free use. Allows travel through dark areas.',   
    },
    'AXE': {
        'name': 'AXE',
        'description': 'An axe made for chopping wood. Not sure what a bear was doing with this...',
    },
    'PENDANT': {
        'name': 'PENDANT',
        'description': 'A round silver PENDANT with the words "for my love" engraved on the back. Found stuck in an olive tree burl. Who knows how many years it has been there?',
    },
  
    'SALMON': {
        'name': 'SALMON',
        'description': 'A not so lucky fish found at the Waterfall. Could make for a tasty meal.',
    },
    'BUCKLER': {
        'name': 'BUCKLER',
        'description': 'A small center-grip shield made of hardened steel. Looks like its been a little neglected over the years.',
    },
    'MESSER': {
        'name': 'Messer',
        'description': 'A long single edged sword with a knife like construction. It doesnt show signs of use, but the Friar kept it well maintained.'
    },
    'HEROS MEDAL': {
        'name': 'HEROS MEDAL',
        'description': 'A gold medal found on a corpse covered in mushrooms. Engraved with the royal crest on the front; the back reads "For Jeremy the Goblin-Slayer". Seems to have some significance to the royal family.',
    },
    'IRON KEY': {
        'name': 'IRON KEY',
        'description': 'A small key made of iron. Dropped from a pesky Hobgoblin.',
    },
    'DRAGON BONE KEY': {
        'name': 'DRAGON BONE KEY',
        'description': 'A key made of Dragon bone. Dragon Bone Keys are said to be used to secure magical seals.',
    },
    'ROYAL JELLY': {
        'name': 'ROYAL JELLY',
        'description':'A jar of Giant Bee Royal Jelly. This substance is capable of enhancing the healing properties of potions. Just a tiny bit mixed in will greatly increase the potancy.',
    },
}
