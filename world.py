from script import *
from character import *
from combat import *
from slowprint import *
from map import *
import random
import pickle



def save_rooms2(savefile3):
  global rooms
  with open(f'saved_rooms/{savefile3}', 'wb') as f:
    pickle.dump(rooms, f)
def load_rooms2(savefile3):
  global rooms
  with open(f'saved_rooms/{savefile3}', 'rb') as f:
      rooms = pickle.load(f)
      

    
#define room mechanics/events  
def potion_healing(p1, typingActive):
  heal = 15 + p1.RJ
  p1.POTS -= 1
  p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
  print_slow(
      f'{p1.name} drinks a POTION and heals {heal} HP. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
  )
def camp_healing(p1, typingActive):
  while True:
    if rooms['Camp Site']['fire'] > 0:
      heal = random.randrange(10, 20)
      p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
      rooms['Camp Site']['fire'] -= 1
      print_slow(f'\n{p1.name} has rested and restored {heal}HP. {p1.name} now has {p1.HP}/{p1.MaxHP}HP.\n', typingActive)
      if rooms['Camp Site']['fire'] > 0:
        print_slow(f"{p1.name} may rest {rooms['Camp Site']['fire']} times before the camp fire dies.\n", typingActive)
        break
      else:
        rooms['Camp Site']['intro'] = line102
        rooms['Camp Site']['map'] = camp_map2
        print_slow(
                f'The fire has finally died and {p1.name} is unable to rest here.\n', typingActive
            )
        break
    else:
      print_slow(
              f'The fire has finally died and {p1.name} is unable to rest here.\n', typingActive
          )
      break

def shrine_pray(p1, typingActive):
  if p1.GP >= 35:
    p1.MP = p1.MaxMP
    p1.GP -= 35
    print_slow(f"{p1.name} drops 35 GP into an ornate donation box and kneels between the lanterns at the alter. {p1.name} is filled with a surge of power. {p1.name}'s MP is fully restored.\n", typingActive)
  else:
    print_slow(f"{p1.name} is too poor to spend on charity.\n", typingActive)

def city_shop(p1, rooms, typingActive): #City Shop mechanics   
    potion_price = 35
    smoke_bomb_price = 30
    antd_price = 25
    ether_price = 40
    map_price = 50
    lantern_price = 200
    craftingp_price = 300
    feed_price = 500 
    while True:
      
        if rooms['Farm House']['speach'] == 3 and 'SPECIAL FEED' in rooms['Shop']['items'] and rooms['Shop']['event'] == 0:
          print_slow(f'\n"Hmm? Looking for SPECIAL FEED? We have some in the back. That will be [{feed_price}GP]...Unless you are looking to BARTER."\n', typingActive)
        if rooms['Farm House']['speach'] == 3 and 'SPECIAL FEED' in rooms['Shop']['items'] and rooms['Shop']['event'] == 1:
          print_slow('If you can find me those 5 MONSTER GUTS I will give you a big discount on that SPECIAL FEED. Just be sure not to tell anyone I want them...', typingActive)
        if rooms['Shop']['event'] == 1 and p1.MonP >= 5:
          print_slow(""""I can tell you've got those MONSTER GUTS! Quick, pass them here before anyone else walks in!"\nThe Shop Keep frantically grabs the MONSTER GUTS and slips them into a jar tucked away under the counter.\n"Now I suppose I should hold up my end of the deal. I'll discount that SPECIAL FEED just for you." """, typingActive)
          p1.MonP -= 5
          rooms['Shop']['event'] = 2
          feed_price = feed_price//2

          
        print_slow(""""Well what will it be?"\n """, typingActive)
        print_slow(f"POTION:[{potion_price}GP]\n", typingActive)
        print_slow(f"SMOKE BOMB:[{smoke_bomb_price}GP]\n", typingActive)
        print_slow(f"ANTIDOTE:[{antd_price}GP]\n", typingActive)
        print_slow(f"ETHER:[{ether_price}GP]\n", typingActive)
        if 'MAP' in rooms['Shop']['items']:
          print_slow(f"MAP:[{map_price}GP]\n", typingActive)
        if 'LANTERN' in rooms['Shop']['items']:
          print_slow(f"LANTERN:[{lantern_price}GP]\n", typingActive)
        if 'CRAFTING POUCH' in rooms['Shop']['items']:
          print_slow(f"CRAFTING POUCH:[{craftingp_price}GP]\n", typingActive)
        if rooms['Farm House']['speach'] == 3 and 'SPECIAL FEED' in rooms['Shop']['items']:
          print_slow(f"SPECIAL FEED:[{feed_price}GP]\n", typingActive)
        print_slow(f"\n{p1.name}'s Wallet:[{p1.GP}GP]\n", typingActive)
        print_slow('\nType your selection or BACK to leave shopping window.\n', typingActive)
        selc = (input().upper()).strip()
        print_slow("\n", typingActive)

      
        if (selc == 'POTION' and p1.GP >= potion_price) and p1.POTS < p1.MaxPOTS:
            p1.GP -= potion_price
            p1.POTS = min(p1.POTS + 1, p1.MaxPOTS)
            print_slow(
                f'{p1.name} purchases a POTION and puts it in their bag. {p1.name} now has {p1.POTS} POTIONS and {p1.GP}GP.\n', typingActive
            )          

        elif (selc == 'SMOKE BOMB'
              and p1.GP >= smoke_bomb_price) and p1.SMB < p1.MaxSMB:
            p1.GP -= smoke_bomb_price
            p1.SMB = min(p1.SMB + 1, p1.MaxSMB)
            print_slow(
                f'{p1.name} purchases a SMOKE BOMB and puts it in their bag. {p1.name} now has {p1.SMB} SMOKE BOMBS and {p1.GP}GP.\n', typingActive
            )

        elif (selc == 'ANTIDOTE' and p1.GP >= antd_price) and p1.ANT < p1.MaxANT:
            p1.GP -= antd_price
            p1.ANT = min(p1.ANT + 1, p1.MaxANT)
            print_slow(
                f'{p1.name} purchases an ANTIDOTE and puts it in their bag. {p1.name} now has {p1.ANT} ANTIDOTES and {p1.GP}GP.\n', typingActive
            )

        elif (selc == 'ETHER' and p1.GP >= ether_price) and p1.ETR < p1.MaxETR:
            p1.GP -= ether_price
            p1.ETR = min(p1.ETR + 1, p1.MaxETR)
            print_slow(
                f'{p1.name} purchases an ETHER and puts it in their bag. {p1.name} now has {p1.ETR} ETHERS and {p1.GP}GP.\n', typingActive
            )     

        elif (selc == 'CRAFTING POUCH'
              and 'CRAFTING POUCH' in rooms['Shop']['items']) and p1.GP >= craftingp_price:
            p1.GP -= craftingp_price
            p1.inventory.append('CRAFTING POUCH')
            rooms['Shop']['items'].remove('CRAFTING POUCH')
            print_slow(
                f'{p1.name} purchases a CRAFTING POUCH and attaches it to their pack. {p1.name} can store all sorts of weird things now! {p1.GP}GP remaining.\n', typingActive
            )

      
        elif (selc == 'LANTERN'
              and 'LANTERN' in rooms['Shop']['items']) and p1.GP >= lantern_price:
            p1.GP -= lantern_price
            p1.inventory.append('LANTERN')
            rooms['Shop']['items'].remove('LANTERN')
            print_slow(
                f'{p1.name} purchases a LANTERN and straps it to their belt. {p1.name} can quit being so afraid of the dark! {p1.GP}GP remaining.\n', typingActive
            )

        elif (selc == 'MAP'
              and 'MAP' in rooms['Shop']['items']) and p1.GP >= map_price:
            p1.GP -= map_price
            p1.inventory.append('MAP')
            rooms['Shop']['items'].remove('MAP')
            print_slow(
                f"{p1.name} purchases a MAP! Now {p1.name} can stop getting lost all the time! {p1.GP}GP remaining.\n", typingActive
            )

        elif selc == 'SPECIAL FEED' and rooms['Farm House']['speach'] == 3 and 'SPECIAL FEED' in rooms['Shop']['items'] and p1.GP >= feed_price:
            p1.GP -= feed_price
            p1.inventory.append('SPECIAL FEED')
            rooms['Shop']['items'].remove('SPECIAL FEED')
            print_slow(
                f'{p1.name} purchases the SPECIAL FEED. Hopefully the Farmers pig is still doing fine... {p1.GP}GP remaining.\n', typingActive)
            if 'CRAFTING POUCH' not in p1.inventory:
              p1.inventory.append('CRAFTING POUCH')
              rooms['Shop']['items'].remove('CRAFTING POUCH')
              print_slow(""""Since you have been such a great customer I'll throw in this CRAFTING POUCH too. Should help you store any materials you find in your travels." """, typingActive)

        elif selc == 'BARTER' and rooms['Farm House']['speach'] == 3 and rooms['Shop']['event'] == 0:
            if 'CRAFTING POUCH' in rooms['Shop']['items']:
              print_slow(""""I'll tell you what, if you can bring me 5 MONSTER GUTS I'll knock off half the price on that SPECIAL FEED. I'll even give you a CRAFTING POUCH to store those MONSTER GUTS in. It should also fit other materials. Don't worry what they're for... it's ah, for a project.\n" """, typingActive)
              p1.inventory.append('CRAFTING POUCH')
              rooms['Shop']['items'].remove('CRAFTING POUCH')
            else:
              print_slow(""""I'll tell you what, if you can bring me 5 MONSTER GUTS I'll knock off half the price on that SPECIAL FEED. Don't worry what they're for... it's ah, for a project.\n" """, typingActive)
            rooms['Shop']['event'] = 1
      
        elif (selc == 'POTION' and p1.GP < potion_price) or (selc == 'SMOKE BOMB' and p1.GP < smoke_bomb_price) or (selc == 'ANTIDOTE' and p1.GP < antd_price) or (selc == 'ETHER' and p1.GP < ether_price) or ((selc == 'LANTERN' and 'Lantern' in rooms['Shop']['items']) and p1.GP < lantern_price) or ((selc == 'SPECIAL FEED'  and 'SPECIAL FEED' in rooms['Shop']['items']) and p1.GP < feed_price) or ((selc == 'MAP' and 'MAP' in rooms['Shop']['items']) and p1.GP < map_price) or ((selc == 'CRAFTING POUCH' and 'CRAFTING POUCH' in rooms['Shop']['items']) and p1.GP < craftingp_price):
            print_slow(
                f'{p1.name} does not have enough GP to purchase this item.\n', typingActive)

        elif (selc == "POTION" and p1.POTS == p1.MaxPOTS) or (selc == "SMOKE BOMB" and p1.SMB == p1.MaxSMB) or (selc == "ANTIDOTE" and p1.ANT == p1.MaxANT) or (selc == "ETHER" and p1.ETR == p1.MaxETR) or (selc == 'LANTERN' and 'LANTERN' in p1.inventory) or (selc == 'MAP' and 'MAP' in p1.inventory) or (selc == 'CRAFTING POUCH' and 'CRAFTING POUCH' in p1.inventory):
            print_slow(
                f'\n"Hey, looks like your inventory is full."\n\n{p1.name} is unable to purchase more of this item.\n', typingActive
            )
        elif selc == "BACK":
          break
        else:
           print_slow('\nInvalid selection. Try again.\n', typingActive)

def city_inn(p1, typingActive):  #Inn Mechanics
    inn_room = 40
    
    while True:

        if p1.GP >= inn_room:
            p1.GP -= 40
            heal = random.randrange(50, 100)
            p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
            print_slow(
                f'\n{p1.name} took a well earned rest and restored HP. {p1.name} has {p1.HP}/{p1.MaxHP}HP, and {p1.GP}GP.\n', typingActive
            )
            break

        elif p1.GP < inn_room:
            print_slow(
                f'{p1.name} does not have enough GP in their wallet. {p1.name} has {p1.GP}GP.\n', typingActive
            )
            break
def village_smith(p1, typingActive):
  while True:
    if p1.GrLvl < 5:
        print_slow(f""""Improve WEAPON or ARMOR for {rooms["Smith's Workshop"]['upgrade_cost']}GP or go BACK?\n" """, typingActive)
        selc = (input().upper()).strip()
        print_slow("\n", typingActive)
        if selc == "WEAPON" and p1.GP >= rooms["Smith's Workshop"]['upgrade_cost']:
          p1.GrLvl += 1
          p1.ATK += 1
          p1.GP -= rooms["Smith's Workshop"]['upgrade_cost']
          rooms["Smith's Workshop"]['upgrade_cost'] = rooms["Smith's Workshop"]['upgrade_cost'] * 2
          print_slow(f"The SMITH takes back {p1.name}'s WEAPON and begins making improvements. After a while he returns with your UPGRADED gear.\n", typingActive)
          p1.stat_check(typingActive)
        elif selc == "ARMOR" and p1.GP >= rooms["Smith's Workshop"]['upgrade_cost']:
          p1.GrLvl += 1
          p1.DEF = max(p1.DEF - .5, 3)
          p1.GP -= rooms["Smith's Workshop"]['upgrade_cost']
          rooms["Smith's Workshop"]['upgrade_cost'] = rooms["Smith's Workshop"]['upgrade_cost'] * 2
          print_slow(f"The SMITH takes back {p1.name}'s ARMOR and begins making improvements. After a while he returns with your UPGRADED gear.\n", typingActive)
          p1.stat_check(typingActive)
        elif (selc == "WEAPON" or selc == "ARMOR") and p1.GP < rooms["Smith's Workshop"]['upgrade_cost']:
          print_slow( f"{p1.name} does not have enough GP for an UPGRADE. {p1.name} only has {p1.GP} GP.\n", typingActive)
        elif selc == "BACK":
          break
        else:
          print_slow('Invalid command. Please select WEAPON or ARMOR, or BACK to leave.\n', typingActive) 
    else:
        print_slow(line1903, typingActive)
        break
def cliff_examine(p1, rooms, typingActive):
  while True:
    if rooms['Cliff Side']['chest'] == "CLOSED" and 'AXE' not in p1.inventory:
      print_slow(line604, typingActive)
      break
    elif rooms['Cliff Side']['chest'] == "CLOSED" and 'AXE' in p1.inventory:
      print_slow(line605, typingActive)
      selc = (input().upper()).strip()
      print_slow("\n", typingActive)
      if selc == "CUT":
          print_slow(line605b, typingActive)
          rooms['Cliff Side']['chest'] = "OPEN"
          p1.inventory.append('PENDANT')
          rooms['Cliff Side']['EXPLORE'] = line603
          rooms['Cliff Side']['map'] = cliff_map2
          break

      elif selc == "BACK" or selc == "BACK OUT":
          print_slow(line605c, typingActive)
          break
      else:
          print_slow('\nInvalid selection. Try again.\n', typingActive)
    else:
      print_slow(line605d, typingActive)
      break

def hill_examine(p1, rooms, typingActive):
  while True:
    if rooms['Rocky Hill']['SOUTH'] == 'LOCKED':
      if 'AXE' not in p1.inventory:
        print_slow(line805, typingActive)
        break
      elif 'AXE' in p1.inventory:
        print_slow(line805b, typingActive)
        selc = (input().upper()).strip()
        print_slow("\n", typingActive)
        if selc == 'CUT':
          print_slow(line806, typingActive)
          rooms['Rocky Hill']['SOUTH'] = 'Berry Patch'
          rooms['Rocky Hill']['EXPLORE'] = line804 
          rooms['Rocky Hill']['map'] = hill_map2
          break
        elif selc == 'LEAVE':
          print_slow(line806b, typingActive)
          break
        else:
          print_slow('\nInvalid selection. Try again.\n', typingActive)
    else:
      print_slow(line811, typingActive)
      break
def waterfall_examine(p1, rooms, typingActive):
  while True:
    if rooms['Waterfall Pool']['chest'] == 'CLOSED':
      print_slow(line1302b, typingActive)
      selc = (input().upper()).strip()
      print_slow("\n", typingActive)
      if selc == "TAKE":
          print_slow(line1303, typingActive)
          p1.inventory.append('SALMON')
          rooms['Waterfall Pool']['chest'] = 'OPEN'
          break
      elif selc == "SAVE":
          print_slow(line1304, typingActive)
          rooms['Waterfall Pool']['chest'] = 'OPEN'
          rooms['Waterfall Pool']['event'] = 1
          break
      elif selc == "LEAVE":
          print_slow(line1305, typingActive)
          break
      else:
          print_slow('\nInvalid selection. Try again.\n')
    elif rooms['Waterfall Pool']['chest'] == 'OPEN':
      if rooms['Waterfall Pool']['event'] == 1:
        print_slow(line1307, typingActive)
        p1.GP += 100
        rooms['Waterfall Pool']['event'] = 2
        print_slow(f'\n{p1.name} has {p1.GP}GP.\n', typingActive)
        break
      else:
        print_slow(line1308, typingActive)
        break 
          
def lake_examine(p1, rooms, typingActive):
  while True:
    if rooms['Lake Beach']['EAST'] == 'LOCKED':
      if 'AXE' not in p1.inventory:
        print_slow(line1404, typingActive)
        break
      elif 'AXE' in p1.inventory:
        print_slow(line1405, typingActive)
        selc = (input().upper()).strip()
        print_slow("\n", typingActive)
        if selc == 'CUT':
          print_slow(line1406, typingActive)
          foe = rooms['Lake Beach']['foe']
          standard_battle(p1, foe, typingActive)
          print_slow(line1408, typingActive)
          rooms['Lake Beach']['EAST'] = 'Mushroom Grove'
          rooms['Lake Beach']['EXPLORE'] = line1403
          rooms['Lake Beach']['map'] = lake_map2
          break
        elif selc == 'LEAVE':
          print_slow(line1407, typingActive)
          break
        else:
          print_slow('\nInvalid selection. Try again.\n', typingActive)
    else:
      print_slow(line1408, typingActive)
      break
  
def cave_examine(p1, rooms, typingActive):
  while True:
    if 'Bear' in rooms['Bear Cave']['boss']:
      if 'SALMON' not in p1.inventory:
        print_slow(f'\n{line903}\n', typingActive)
      else:
        print_slow(f'\n{line904}\n', typingActive)
      selc = (input().upper()).strip()
      print_slow("\n", typingActive)
      if selc == "POKE":
          print_slow(line911, typingActive)
          foe = rooms['Bear Cave']['foe']
          standard_battle(p1, foe, typingActive)
          rooms['Bear Cave']['boss'].remove('Bear')
          p1.inventory.append('AXE')
          rooms['Bear Cave']['intro'] = line902
          rooms['Bear Cave']['EXPLORE'] = line906b
          rooms['Bear Cave']['map'] = cave_map2
          print_slow(line912, typingActive)
          break

      elif selc == "FEED" and 'SALMON' in p1.inventory:
          p1.inventory.remove('SALMON')
          rooms['Bear Cave']['boss'].remove('Bear')
          p1.inventory.append('AXE')
          rooms['Bear Cave']['intro'] = line902
          rooms['Bear Cave']['EXPLORE'] = line906b
          rooms['Bear Cave']['map'] = cave_map2
          print_slow(line913, typingActive)
          break
      elif selc == "BACK" or selc == "BACK OUT":
          print_slow(line907, typingActive)
          break
      else:
          print_slow('\nInvalid selection. Try again.\n', typingActive)
    else:
      print_slow(line912b, typingActive)
      break
    

def cave2_examine(p1, rooms, typingActive):
  while True:
    if rooms['Rocky Cave 2']['chest'] == "CLOSED":
      print_slow(line925, typingActive)
      selc = (input().upper()).strip()
      print_slow("", typingActive)
      if selc == "OPEN":
          print_slow(line926, typingActive)
          foe = rooms['Rocky Cave 2']['foe']
          standard_battle(p1, foe, typingActive)
          rooms['Rocky Cave 2']['chest'] = "OPEN"
          p1.inventory.append('IRON KEY')
          rooms['Rocky Cave 2']['EXPLORE'] = line924
          rooms['Rocky Cave 2']['map'] = cave2_map2
          print_slow(line927, typingActive)
          break

      elif selc == "BACK" or selc == "BACK OUT":
          print_slow(line928, typingActive)
          break
      else:
          print_slow('\nInvalid selection. Try again.\n')
    else:
      print_slow(line928b, typingActive)
      break
    

def cave4_examine(p1, rooms, typingActive):
  while True:
     if rooms['Rocky Cave 4']['EAST'] == 'LOCKED':
      if 'IRON KEY' not in p1.inventory:
        print_slow(f'\n{line940}', typingActive)
        break
      else:
        print_slow(f'\n{line940b}', typingActive)
        selc = (input().upper()).strip()
        print_slow("", typingActive)
        if selc == "OPEN":
            print_slow(line941, typingActive)
            rooms['Rocky Cave 4']['EAST'] = "Queen's Chamber"
            rooms['Rocky Cave 4']['EXPLORE'] = line939
            break
        elif selc == "BACK" or selc == "BACK OUT":
            print_slow(line941b, typingActive)
            break
        else:
            print_slow('\nInvalid selection. Try again.\n', typingActive)
  


def berry_examine(p1, rooms, typingActive):
  while True:
    if rooms['Berry Patch']['chest'] == 'CLOSED':
      print_slow(line1002b, typingActive)
      selc = (input().upper()).strip()
      print_slow("", typingActive)
      if selc == "PICK":
        print_slow(line1003, typingActive)
        foe = rooms['Berry Patch']['foe']
        standard_battle(p1, foe, typingActive)
        print_slow(line1004, typingActive)
        berriesPicked = random.randrange(2, 6)
        p1.POTS = min(p1.POTS + berriesPicked, p1.MaxPOTS)
        rooms['Berry Patch']['chest'] = "OPEN"
        rooms['Berry Patch']['EXPLORE'] = line1005
        print_slow(f'{p1.name} has made {berriesPicked} POTIONS. {p1.name} has {p1.POTS} POTS.\n', typingActive)
        break
      elif selc == "LEAVE":
        print_slow(line1002c, typingActive)
        break
      else:
            print_slow('\nInvalid selection. Try again.\n', typingActive)
    else:
      print_slow(line1006, typingActive)
      break

def oak_examine(p1, rooms, typingActive):
    print_slow(line2003, typingActive)
    
def hive_examine(p1, rooms, typingActive):
  global current_room
  while True:
    if rooms['Bee Hive']['chest'] == "CLOSED":
      print_slow(line2105b, typingActive)
      p1.POTS = min(p1.POTS + 3, p1.MaxPOTS)
      print_slow(f'\n{p1.name} gains 3 potions.\n', typingActive)
      rooms['Bee Hive']['EXPLORE'] = line2106
      rooms['Bee Hive']['chest'] = "OPEN"
      rooms['Bee Hive']['map'] = hive_map2
      break
    else:
      print_slow(line2106b, typingActive)
      break

def mushroom_examine(p1, rooms, typingActive):
  while True:
    if p1.gobCount >= 10 and rooms['Mushroom Grove']['chest'] == 'CLOSED':
      print_slow(line1604, typingActive)
      p1.inventory.append('HEROS MEDAL')
      rooms['Mushroom Grove']['chest'] = 'OPEN'
      break
    elif p1.gobCount >= 10 and rooms['Mushroom Grove']['chest'] == 'OPEN':
      print_slow(line1604b, typingActive)
      break
    else:
      print_slow(line1603, typingActive)
      break
def hill_lock(p1, selc, rooms, typingActive):
 while True:
    if rooms['Rocky Hill']['SOUTH'] == 'LOCKED':
      print_slow(line812, typingActive)
      break
    else:
      continue
def lake_lock(p1, selc, rooms, typingActive):
  while True:
    if rooms['Lake Beach']['EAST'] == 'LOCKED':
      print_slow(line1410, typingActive)
      break
    else:
      continue
def cave_lock(p1, selc, rooms, typingActive):
  while True:
    if 'Bear' in rooms['Bear Cave']['boss']:
      print_slow(line914, typingActive)
      break
    elif (selc == 'EAST' and rooms['Bear Cave']['EAST'] == 'LOCKED') and "LANTERN" not in p1.inventory:
      print_slow(line909, typingActive)
      break
    elif (selc == 'EAST' and rooms['Bear Cave']['EAST'] == 'LOCKED') and "LANTERN" in p1.inventory:
      print_slow(line915, typingActive)
      rooms['Bear Cave']['EAST'] = 'Rocky Cave 1'
      rooms['Bear Cave']['map'] = cave_map3
      break
    else:
      continue
      
      
def cave4_lock(p1, selc, rooms, typingActive):
  while True:
    if rooms['Rocky Cave 4']['EAST'] == 'LOCKED':
      print_slow(line943, typingActive)
      break
    else:
      continue

def cave4_boss_ambush(p1, typingActive): 
  while True:
    if 'Hobgoblin Gang' in rooms['Rocky Cave 4']['boss']:
      print_slow(line935, typingActive)
      foe = rooms['Rocky Cave 4']['foe']
      standard_battle(p1, foe, typingActive)
      rooms['Rocky Cave 4']['boss'].remove('Hobgoblin Gang')
      rooms['Rocky Cave 4']['spawn_rate'] = 4
      print_slow(line936, typingActive)
    else:
      break
def cave5_boss_ambush(p1, typingActive):
  while True:
    if 'Goblin Queen' in rooms["Queen's Chamber"]['boss']:
      print_slow(line947, typingActive)
      foe = rooms["Queen's Chamber"]['foe']
      standard_battle(p1, foe, typingActive)
      rooms["Queen's Chamber"]['boss'].remove('Goblin Queen')
      p1.inventory.append('DRAGON BONE KEY')
      print_slow(line949, typingActive)
    else:
      break
def hive_boss_ambush(p1, typingActive):
  global enemy_spawn3
  global enemy_spawn9 
  while True:
    rooms['Great Oak']['map'] = oak_map2
    if 'Giant Bee Queen' in rooms['Bee Hive']['boss']:
      print_slow(line2101, typingActive)
      foe = random.choice(rooms['Bee Hive']['enemy_spawn_set'])
      standard_battle(p1, foe, typingActive)
      print_slow(line2101b, typingActive)
      foe = random.choice(rooms['Bee Hive']['enemy_spawn_set'])
      standard_battle(p1, foe, typingActive)
      print_slow(line2101b, typingActive)
      foe = random.choice(rooms['Bee Hive']['enemy_spawn_set'])
      standard_battle(p1, foe, typingActive)
      print_slow(line2102, typingActive)
      foe = rooms['Bee Hive']['foe']
      standard_battle(p1, foe, typingActive)
      rooms['Bee Hive']['boss'].remove('Giant Bee Queen')
      rooms['Bee Hive']['spawn_rate'] = 0
      p1.inventory.append('ROYAL JELLY')
      enemy_spawn3.remove(p14)
      enemy_spawn9.remove(p14)
      enemy_spawn3.append(p25)
      enemy_spawn9.append(p25)
      p1.RJ += 5
      print_slow(line2103, typingActive)
      current_room = 'Great Oak'
     # print_slow(f"\n**********[ {rooms[current_room]['name']} ]**********\n", typingActive)
    else:
      break
def castle_speak(p1, rooms, typingActive):
  while True:
    if rooms['Royal Castle']['speach'] == 0:
      print_slow(line505, typingActive)
      print_slow(line506, typingActive)
      rooms['Royal Castle']['speach'] += 1
      break
    elif 'HEROS MEDAL' in p1.inventory and rooms['Royal Castle']['event'] == 0:
      print_slow(line505, typingActive)
      print_slow(line508, typingActive)
      p1.MaxHP += 25
      p1.HP = p1.MaxHP
      p1.stat_check(typingActive)
      rooms['Royal Castle']['event'] = 1
      key_items['HEROS MEDAL']['description'] = 'A gold medal found on a corpse covered in mushrooms. Engraved with the royal crest on the front; the back reads "For Jeremy the Goblin-Slayer". You can feel the medal filling you with vigor ever since the princess unlocked its magic.\n'
      break
    elif rooms['Royal Castle']['speach'] == 1:
      print_slow(line505, typingActive)
      print_slow(line507, typingActive)
      break
def boat_speak(p1, rooms, typingActive):
  while True:
    if rooms['Boat House']['speach'] == 0:
      print_slow(line1504, typingActive)
      rooms['Boat House']['speach'] = 1
      break
    elif rooms['Boat House']['speach'] == 1 and 'SALMON' in p1.inventory:
      print_slow(line1506, typingActive) 
      selc = (input().upper()).strip()
      print_slow("\n", typingActive)
      if selc == "GIVE":
        print_slow(line1508, typingActive)
        print_slow(f'{p1.name} was given a BUCKLER! This sturdy steel shield should help block damage. {p1.name} has gained 5% DEF!\n', typingActive)
        p1.DEF = max(p1.DEF - 1.5, 3)
        rooms['Boat House']['speach'] = 2
        rooms['Boat House']['EXPLORE'] = line1503
        p1.inventory.remove('SALMON')
        p1.inventory.append('BUCKLER')
        p1.stat_check(typingActive)
        break
      elif selc == "KEEP":
        print_slow(line1507, typingActive)
        break
      else:
        print_slow('\nInvalid selection. Try again.\n')
    elif rooms['Boat House']['speach'] == 1 and 'SALMON' not in p1.inventory:
      print_slow(line1510, typingActive)
      break
    else:
      print_slow(line1509, typingActive)
      break


def shrine_speak(p1, rooms, typingActive):
  while True:
    if rooms['Mystic Shrine']['speach'] == 0:
      print_slow(line1105, typingActive)
      print_slow(line1106, typingActive)
      rooms['Mystic Shrine']['speach'] = 1
      rooms['Mystic Shrine']['EXPLORE'] = line1103
      break
    elif rooms['Mystic Shrine']['speach'] == 1 and 'PENDANT' in p1.inventory:
      print_slow(line1108, typingActive) 
      print_slow(line1109, typingActive) 
      print_slow(f"{p1.name} is given the FRIAR's MESSER. This single edge sword is finely crafted. Much better than the rusty old blade you found in the trash before you started adventuring... {p1.name} gained 5 ATK\n", typingActive)
      rooms['Mystic Shrine']['EXPLORE'] = line1104
      p1.inventory.remove('PENDANT')
      p1.inventory.append('MESSER')
      p1.ATK += 5
      p1.stat_check(typingActive)
      break
    elif rooms['Mystic Shrine']['speach'] == 1:
      print_slow(line1107, typingActive)
      break
def farm_speak(p1, rooms, typingActive):
  while True:
    if rooms['Farm House']['speach'] == 0:
      print_slow(line2203, typingActive)
      rooms['Farm House']['speach'] = 1
    if rooms['Farm House']['speach'] == 1:
      print_slow("\n", typingActive)
      selc = (input().upper()).strip()
      if selc == "YES":
        print_slow(line2205, typingActive)
        print_slow(f'{p1.name} was given a 100GP. The Farmer expects you to use his money to buy his pig some special feed from the City\n', typingActive)
        p1.GP += 100
        rooms['Farm House']['speach'] = 3
        rooms['Shop']['Event'] = 1
        break
      elif selc == "NO":
        print_slow(line2204, typingActive)
        rooms['Farm House']['speach'] = 2
        break
      else:
        print_slow('\nInvalid selection. Try again. Please select YES or NO\n', typingActive)
    if rooms['Farm House']['speach'] == 2:
      print_slow(line2204b, typingActive)
      rooms['Farm House']['speach'] = 1
    if rooms['Farm House']['speach'] == 3:
      if 'SPECIAL FEED' in p1.inventory:
        p1.inventory.remove('SPECIAL FEED')
        p1.GP += 150
        p1.ETR += min(p1.ETR + 2, p1.MaxETR)
        rooms['Farm House']['speach'] = 4
        rooms['Farm House']['crafting'] = "ACTIVE" 
        print_slow(line2206,typingActive)
        break
      else:
        print_slow(line2207,typingActive)
        break
    elif rooms['Farm House']['speach'] == 4:
      print_slow(line2208, typingActive)
      break


#define rooms/areas for game
def farm_crafting(p1, typingActive):
  while True:
    print_slow("Would you like to craft a ANTIDOTE using 5 PLANT PARTS? YES or NO.\n", typingActive)
    selc = (input().upper()).strip()
    if (selc == "YES" and p1.PlantP >= 5) and p1.ANT != p1.MaxANT:
      p1.PlantP -= 5
      p1.ANT = min(p1.ANT + 1, p1.MaxANT)
      print_slow(""" "Here you go! One healing salve coming right up.\n" """, typingActive)
      print_slow(f'{p1.name} now has {p1.ANT} ANTIDOTES\n', typingActive)
    elif selc == "YES" and p1.ANT == p1.MaxANT:
      print_slow(f"Unable to craft more ANTIDOTES; {p1.name}'s inventory is full.\n", typingActive)
    elif selc == "YES" and p1.PlantP < 5:
      print_slow(f'{p1.name} does not have enough PLANT PARTS. {p1.name} only has {p1.PlantP} PLANT PARTS\n', typingActive)
    elif selc == "NO":
      break
    else:
      print_slow('\nInvalid selection. Try again. Please select YES or NO\n')


def cliff_special(p1, typingActive): 
    print_slow(line610,typingActive)
    damage = 69
    p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
    player_death(p1, typingActive)
    if p1.HP > 0:
      rooms['Cliff Side']['secret_path'] = 1
      print_slow(line611,typingActive)
    return

def cave4_special(p1, typingActive):
    print_slow(line946,typingActive)
    p1.HP = 0
    player_death(p1, typingActive)
    return
def river_special(p1, typingActive):
    print_slow(line1207,typingActive)
    p1.HP = 0
    player_death(p1, typingActive)
    return
def lake_special(p1, typingActive):
    print_slow(line1414,typingActive)
    p1.HP = 0
    player_death(p1, typingActive)
    return

def traveling_merchant(p1, foe, typingActive):
  potion_price = 30
  smoke_bomb_price = 25
  antd_price = 20
  ether_price = 35
  map_price = 50
  print_slow(line305, typingActive)
  while True:
    print_slow(""""Take a look!"\n """, typingActive)
    print_slow(f"POTION:[{potion_price}GP]\n", typingActive)
    print_slow(f"SMOKE BOMB:[{smoke_bomb_price}GP]\n", typingActive)
    print_slow(f"ANTIDOTE:[{antd_price}GP]\n", typingActive)
    print_slow(f"ETHER:[{ether_price}GP]\n", typingActive)
    if 'MAP' in rooms['Shop']['items']:
      print_slow(f"MAP:[{map_price}GP]\n", typingActive)
    print_slow('\nEnter command or type EXIT to leave the Traveling Merchant:\n', typingActive)
    selc = (input().upper()).strip()
    print_slow("\n", typingActive)
  
    if (selc == 'POTION' and p1.GP >= potion_price) and p1.POTS < p1.MaxPOTS:
              p1.GP -= potion_price
              p1.POTS = min(p1.POTS + 1, p1.MaxPOTS)
              print_slow(
                  f'{p1.name} purchases a POTION and puts it in their bag. {p1.name} now has {p1.POTS} POTIONS and {p1.GP}GP.\n', typingActive
              )          
  
    elif (selc == 'SMOKE BOMB'
          and p1.GP >= smoke_bomb_price) and p1.SMB < p1.MaxSMB:
        p1.GP -= smoke_bomb_price
        p1.SMB = min(p1.SMB + 1, p1.MaxSMB)
        print_slow(
            f'{p1.name} purchases a SMOKE BOMB and puts it in their bag. {p1.name} now has {p1.SMB} SMOKE BOMBS and {p1.GP}GP.\n', typingActive
        )
  
    elif (selc == 'ANTIDOTE' and p1.GP >= antd_price) and p1.ANT < p1.MaxANT:
        p1.GP -= antd_price
        p1.ANT = min(p1.ANT + 1, p1.MaxANT)
        print_slow(
            f'{p1.name} purchases an ANTIDOTE and puts it in their bag. {p1.name} now has {p1.ANT} ANTIDOTES and {p1.GP}GP.\n', typingActive
        )
  
    elif (selc == 'ETHER' and p1.GP >= ether_price) and p1.ETR < p1.MaxETR:
        p1.GP -= ether_price
        p1.ETR = min(p1.ETR + 1, p1.MaxETR)
        print_slow(
            f'{p1.name} purchases an ETHER and puts it in their bag. {p1.name} now has {p1.ETR} ETHERS and {p1.GP}GP.\n', typingActive
        )
  
    elif (selc == 'MAP'
                and 'MAP' in rooms['Shop']['items']) and p1.GP >= map_price:
              p1.GP -= map_price
              p1.inventory.append('MAP')
              rooms['Shop']['items'].remove('MAP')
              print_slow(
                  f"{p1.name} purchases a MAP! Now {p1.name} can stop getting lost all the time! {p1.GP}GP remaining.\n", typingActive
              )
    elif (selc == 'POTION' and p1.GP < potion_price) or (selc == 'SMOKE BOMB' and p1.GP < smoke_bomb_price) or (selc == 'ANTIDOTE' and p1.GP < antd_price) or (selc == 'ETHER' and p1.GP < ether_price) or ((selc == 'MAP' and 'MAP' in rooms['Shop']['items']) and p1.GP < map_price):
              print_slow(
                  f'{p1.name} does not have enough GP to purchase this item.\n', typingActive)
    
    elif (selc == "POTION" and p1.POTS == p1.MaxPOTS) or (selc == "SMOKE BOMB" and p1.SMB == p1.MaxSMB) or (selc == "ANTIDOTE" and p1.ANT == p1.MaxANT) or (selc == "ETHER" and p1.ETR == p1.MaxETR) or (selc == 'MAP' and 'MAP' in p1.inventory):
              print_slow(
                  f'\n"Hey, looks like your inventory is full."\n\n{p1.name} is unable to purchase more of this item.\n', typingActive
              )
      
    elif selc == "EXIT" or selc == "BACK":
      print_slow('You bid farewell to the merchant and continue on your way.\n',typingActive)
      break
    else:
       print_slow('\nInvalid selection. Try again.\n', typingActive)
  
rooms = {
    '' : {
        'name' : '',
        'intro' : '',
        'map' : None,
        'discovered' : [],
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
        'CRAFT' : 'craft',
        'speach' : None,
        'crafting' : None,
        'spawn_rate' : 0,
        'enemy_spawn_set' : None,
        'boss' : [],
        'boss_ambush' : None,
        'foe' : None,
        'LOCK' : None,
        'chest' : None,
        'event' : None,
    },

    'Camp Site' : {
        'name' : 'Camp Site',
        'intro' : line101,
        'map' : camp_map1,
        'discovered' : [],
        'NORTH' : 'Deep Forest',
        'SOUTH' : 'Town Center',
        'WEST' : 'Cliff Side',
        'EXPLORE': line103,
        'REST': 'rest',
        'fire' : 3,
        'spawn_rate' : 0,
    },

    'Cliff Side' : {
        'name' : 'Cliff Side',
        'intro' : line601,
        'map' : cliff_map1,
        'discovered' : [],
        'EAST' : 'Camp Site',
        'SECRET_ROUTE' : 'Waterfall Pool',
        'EXPLORE': line602,
        'EXAMINE' : cliff_examine,
        'secrets' : ['JUMP', 'FLY', 'DIVE'],
        'secret_path' : 0,
        'special' : cliff_special,
        'spawn_rate' : 2,
        'enemy_spawn_set' : enemy_spawn0,
        'chest' : 'CLOSED',
    },
#Town start
  'Town Center' : {
        'name' : 'Town Center',
        'intro' : line201,
        'map' : town_map1,
        'discovered' : [],
        'NORTH' : 'Camp Site',
        'EAST' : 'Shop',
        'SOUTH' : 'Royal Castle',
        'WEST' : 'Inn',
        'EXPLORE': line202,
        'spawn_rate' : 0,
    },

  'Shop' : {
        'name' : 'Shop',
        'intro' : line301,
        'map' : shop_map1,
        'discovered' : [],
        'WEST' : 'Town Center',
        'EXIT' : 'Town Center',
        'EXPLORE': line304,
        'BUY' : "BUY",
        'spawn_rate' : 0,
        'event' : 0,
        'items' : ['MAP', 'LANTERN', 'CRAFTING POUCH', 'SPECIAL FEED'],
    },

  'Inn' : {
        'name' : 'Inn',
        'intro' : line401,
        'map' : inn_map1,
        'discovered' : [],
        'EAST' : 'Town Center',
        'EXIT' : 'Town Center',
        'EXPLORE': line404,
        'REST' : 'rest',
        'spawn_rate' : 0,
    },

  'Royal Castle' : {
        'name' : 'Royal Castle',
        'intro' : line501,
        'map' : castle_map1,
        'discovered' : [],
        'NORTH' : 'Town Center',
        'EXIT' : 'Town Center',
        'EXPLORE': line502,
        'spawn_rate' : 0,
        'SPEAK' : castle_speak,
        'speach' : 0,
        'event' : 0,
    }, #Town end

  'Deep Forest' : {
        'name' : 'Deep Forest',
        'intro' : line701,
        'map' : forest_map1,
        'discovered' : [],
        #'NORTH' : 'Thicket',
        'EAST' : 'Rocky Hill',
        'SOUTH' : 'Camp Site',
        'WEST' : 'River Channel',
        'EXPLORE': line702,
        'spawn_rate' : 2,
        'enemy_spawn_set' : enemy_spawn1,
    },

  'Rocky Hill' : {
        'name' : 'Rocky Hill',
        'intro' : line801,
        'map' : hill_map1,
        'discovered' : [],
        'NORTH' : 'Mystic Shrine',
        'EAST' : 'Bear Cave',
        'SOUTH' : 'LOCKED',
        'WEST' : 'Deep Forest',
        'EXPLORE' : line802,
        'EXAMINE' : hill_examine, 
        'spawn_rate': 3,
        'enemy_spawn_set' : enemy_spawn6,
        'LOCK' : hill_lock,
    },
  
  'Mystic Shrine' : {
        'name' : 'Mystic Shrine',
        'intro' : line1101,
        'map' : shrine_map1,
        'discovered' : [],
        'SOUTH' : 'Rocky Hill',
        'EXPLORE': line1102,
        'SPEAK' : shrine_speak,
        'PRAY' : 'PRAY',
        'speach' : 0,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn4,
    },
#Dungeon 1 start
  'Bear Cave' : {
        'name' : 'Bear Cave',
        'intro' : line901,
        'map' : cave_map1,
        'discovered' : [],
        'WEST' : 'Rocky Hill',
        'EAST' : 'LOCKED',
        'EXPLORE': line906,
        'EXAMINE' : cave_examine,
        'spawn_rate' : 0,
        'boss' : ['Bear'],
        'foe' : p12,
        'LOCK' : cave_lock,
    },

  'Rocky Cave 1' : {
        'name' : 'Rocky Cave 1',
        'intro' : line916,
        'map' : cave1_map1,
        'discovered' : [],
        'NORTH' : 'Rocky Cave 2',
        'SOUTH' : 'Rocky Cave 3',
        'WEST' : 'Bear Cave',
        'EXPLORE': line917,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn8,
    },

  'Rocky Cave 2' : {
        'name' : 'Rocky Cave 2',
        'intro' : line922,
        'map' : cave2_map1,
        'discovered' : [],
        'SOUTH' : 'Rocky Cave 1',
        'EXPLORE': line923,
        'EXAMINE' : cave2_examine,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn8,
        'foe' : p3b,
        'chest' : 'CLOSED',
    },
  'Rocky Cave 3' : {
        'name' : 'Rocky Cave 3',
        'intro' : line931,
        'map' : cave3_map1,
        'discovered' : [],
        'NORTH' : 'Rocky Cave 1',
        'SOUTH' : 'Rocky Cave 4',
        'EXPLORE': line932a,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn8,
    },
  'Rocky Cave 4' : {
        'name' : 'Rocky Cave 4',
        'intro' : line937,
        'map' : cave4_map1,
        'discovered' : [],
        'NORTH' : 'Rocky Cave 3',
        'EAST' : 'LOCKED',
        'EXPLORE' : line938,
        'EXAMINE' : cave4_examine,
        'secrets' : ['JUMP', 'FLY', 'DIVE'],
        'special' : cave4_special,
        'spawn_rate' : 0,
        'enemy_spawn_set' : enemy_spawn8,
        'boss' : ['Hobgoblin Gang'],
        'boss_ambush' : cave4_boss_ambush,
        'foe' :  p22b,
        'LOCK' : cave4_lock,
    },
  "Queen's Chamber" : {
        'name' : "Queen's Chamber",
        'intro' : line948,
        'map' : cave5_map1,
        'discovered' : [],
        'WEST' : 'Rocky Cave 4',
        'EXPLORE': line950,
        'spawn_rate' : 0,
        'boss' : ['Goblin Queen'],
        'boss_ambush' : cave5_boss_ambush,
        'foe' : p23,
    }, #Dungeon 1 end

  'River Channel' : {
        'name' : 'River Channel',
        'intro' : line1201,
        'map' : river_map1,
        'discovered' : [],
        'NORTH' : 'Lake Beach',
        'EAST' : 'Deep Forest',
        'SOUTH' : 'Waterfall Pool',
        'EXPLORE': line1202,
        'secrets' : ['JUMP', 'SWIM', 'DIVE'],
        'special' : river_special,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn5,
    },

  'Waterfall Pool' : {
        'name' : 'Waterfall Pool',
        'intro' : line1301,
        'map' : waterfall_map1,
        'discovered' : [],
        'NORTH' : 'River Channel',
        'EXPLORE': line1302,
        'EXAMINE' : waterfall_examine,
        'secrets' : ['JUMP', 'SWIM', 'DIVE'],
        'special' : river_special,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn5,
        'chest' : 'CLOSED',
        'event' : 0,
    },

  'Lake Beach' : {
        'name' : 'Lake Beach',
        'intro' : line1401,
        'map' : lake_map1,
        'discovered' : [],
        'NORTH' : 'Boat House',
        'EAST' : 'LOCKED',
        'SOUTH' : 'River Channel',
        'EXPLORE': line1402,
        'EXAMINE': lake_examine,
        'secrets' : ['JUMP', 'SWIM', 'DIVE'],
        'special' : lake_special,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn5,
        'foe' : p16,
        "LOCK" : lake_lock,
    },

  'Boat House' : {
        'name' : 'Boat House',
        'intro' : line1501,
        'map' : boat_map1,
        'discovered' : [],
        'SOUTH' : 'Lake Beach',
        'EXPLORE': line1502,
        'SPEAK' : boat_speak,
        'speach' : 0,
        'spawn_rate' : 0,
    },

  'Berry Patch' : {
        'name' : 'Berry Patch',
        'intro' : line1001,
        'map' : berry_map1,
        'discovered' : [],
        'NORTH' : 'Rocky Hill',
        'EAST' : 'Flower Meadow',
        'EXPLORE': line1002,
        'EXAMINE' : berry_examine,
        'spawn_rate' : 2,
        'enemy_spawn_set' : enemy_spawn3,
        'foe' : p15b,
        'chest' : 'CLOSED',
    },

  'Flower Meadow' : {
        'name' : 'Flower Meadow',
        'intro' : line1701,
        'map' : meadow_map1,
        'discovered' : [],
        #'NORTH' : "Witch's Cabin",
        'EAST' : 'Great Oak',
        'SOUTH' : 'Quiet Village',
        'WEST' : 'Berry Patch',
        'EXPLORE': line1702,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn9,
        'foe' : None,
        'chest' : None,
        'event' : None,
    },
  "Witch's Cabin" : {
        'name' : "Witch's Cabin",
        'intro' : line2401,
        'map' : witch_map1,
        'discovered' : [],
        'SOUTH' : 'Flower Meadow',
        'EXPLORE': line2402,
        'EXAMINE' : None,
        'SPEAK' : None,
        'speach' : None,
        'spawn_rate' : 0,
        'enemy_spawn_set' : None,
        'chest' : None,
        'event' : None,
    },
#Quite Village start
  'Quiet Village' : {
        'name' : 'Quiet Village',
        'intro' : line1801,
        'map' : village_map1,
        'discovered' : [],
        'NORTH' : 'Flower Meadow',
        'EAST' : 'Farm House',
        'SOUTH' : 'Tavern & Inn',
        'WEST' : "Smith's Workshop",
        'EXPLORE': line1802,
        'spawn_rate' : 0,
    },

  'Tavern & Inn' : {
        'name' : 'Tavern & Inn',
        'intro' : line401b,
        'map' : tavern_map1,
        'discovered' : [],
        'NORTH' : 'Quiet Village',
        'EXIT' : 'Quiet Village',
        'EXPLORE': line404b,
        'REST' : 'rest',
        'spawn_rate' : 0,
    },

  "Smith's Workshop" : {
        'name' : "Smith's Workshop",
        'intro' : line1901,
        'map' : smith_map1,
        'discovered' : [],
        'EAST' : 'Quiet Village',
        'EXIT' : 'Quiet Village',
        'EXPLORE': line1902,
        'UPGRADE' : village_smith,
        'upgrade_cost' : 75,
        'spawn_rate' : 0,
    },

  'Farm House' : {
        'name' : 'Farm House',
        'intro' : line2201,
        'map' : farm_map1,
        'discovered' : [],
        'WEST' : 'Quiet Village',
        'EXPLORE': line2202,
        'SPEAK' : farm_speak,
        'CRAFT' : farm_crafting,
        'crafting' : 'INACTIVE',
        'speach' : 0,
        'spawn_rate' : 0,
    },

#Quite Village end
  'Great Oak' : {
        'name' : 'Great Oak',
        'intro' : line2001,
        'map' : oak_map1,
        'discovered' : [],
        'WEST' : 'Flower Meadow',
        'CLIMB': 'Bee Hive',
        'EXPLORE': line2002,
        'EXAMINE' : oak_examine,
        'spawn_rate' : 0,
 
    },

  'Bee Hive' : {
        'name' : 'Bee Hive',
        'intro' : line2104,
        'map' : hive_map1,
        'discovered' : [],
        'EXIT' : 'Great Oak',
        'CLIMB' : 'Great Oak',
        'EXPLORE': line2105,
        'EXAMINE' : hive_examine,
        'spawn_rate' : 0,
        'enemy_spawn_set' : enemy_spawn10,
        'boss' : ['Giant Bee Queen'],
        'boss_ambush' : hive_boss_ambush,
        'foe' : p24,
        'chest' : "CLOSED",
    },
  
  'Mushroom Grove' : {
        'name' : 'Mushroom Grove',
        'intro' : line1601,
        'map' : mushroom_map1,
        'discovered' : [],
        'NORTH' : 'Rotting Woods',
        #'SOUTH' : 'Fairy',
        'WEST' : 'Lake Beach',
        'EXPLORE': line1602,
        'EXAMINE' : mushroom_examine,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn7,
        #'LOCK' : None,
        'chest' : "CLOSED",
        #'event' : None,
    },'secrets' : ['JUMP', 'FLY', 'DIVE'],

  'Rotting Woods' : {
        'name' : 'Rotting Woods',
        'intro' : line2601,
        'map' : rot_map1,
        'discovered' : [],
        #'NORTH' : 'Marsh',
        'SOUTH' : 'Mushroom Grove',
        #'WEST' : 'Swamp',
        'EXPLORE': line2602,
        'spawn_rate' : 2,
        'enemy_spawn_set' : enemy_spawn11,
    },
}

#define player key items


key_items = {
    '': {
        'name': '',
        'description': '',
    },
    'MAP': {
        'name': 'MAP',
        'description': 'A map coated in magical ink. The ink reacts to your surroundings and changes depending on your location.',
    },
    'CRAFTING POUCH': {
        'name': 'CRAFTING POUCH',
        'description': "A special pouch in your pack for storing crafting materials. You're not sure how it can hold so much, but you're not about to question it either.",
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
    'SPECIAL FEED': {
        'name': 'SPECIAL FEED',
        'description': 'A medicated feed for pigs. Quite pricey; the Farmer better have the GP to cover the costs...',
    },
}


crafting_items = {
      '': {
          'name': '',
          'description': '',
      },
    'PLANT PARTS': {
          'name': 'PLANT PARTS',
          'description': 'Various parts of magical plants. Commonly harvested from plant type enemies.',
      },
    'MONSTER GUTS': {
          'name': 'MONSTER GUTS',
          'description': 'A mix of different monster organs and body parts. Really weird that you just carry this stuff with you.',
      },
    'RARE MONSTER PARTS': {
          'name': 'RARE MONSTER PARTS',
          'description': "These uncommon monster parts are highly prized. Still weird that you're carring them with you.",
      },
    'FAE DUST': {
          'name': 'FAE DUST',
          'description': 'A glistening powder found on creatures of the fae like Fairies and Pixies. A common source of magical energy.',
      },
    'DRAGON SCALES': {
          'name': 'DRAGON SCALES',
          'description': "The scales of Dragons are incredibly hard to come by. Prying one off a dragon, live or dead, is nearly impossible before they're already loose, and these are rarely shed. The inner surface is a beautiful shifting rainbow.",
      },
  }


