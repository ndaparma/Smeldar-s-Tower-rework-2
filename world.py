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

def merchant_death():
  enemy_spawn5.remove(p28)
  enemy_spawn9.remove(p28)
  enemy_spawn17.remove(p28)
def key_itemBought(p1, selc, typingActive):
  if selc == 'MAP':
    print_slow(f"{p1.name} purchases a MAP! Now {p1.name} can stop getting lost all the time! (Type MAP or LOCATION to view current area) {p1.GP}GP remaining.\n", typingActive)
  if selc == 'LANTERN':
    print_slow(f'{p1.name} purchases a LANTERN and straps it to their belt. {p1.name} can quit being so afraid of the dark! {p1.GP}GP remaining.\n', typingActive)
  if selc == 'CRAFTING POUCH':
    print_slow(f'{p1.name} purchases a CRAFTING POUCH and attaches it to their pack. {p1.name} can store all sorts of weird things now! {p1.GP}GP remaining.\n', typingActive)
  if selc == 'SPECIAL FEED':
    print_slow(f'{p1.name} purchases the SPECIAL FEED. Hopefully the Farmers pig is still doing fine... {p1.GP}GP remaining.\n', typingActive)
  if selc == 'EXTRA POUCH':
    print_slow(f'{p1.name} purchases the EXTRA POUCH. Now {p1.name} can now store an additional 5 each of POTIONS, ANTIDOTES, ETHERS, and SMOKE BOMBS. {p1.GP}GP remaining.\n', typingActive)
  if selc == 'DRAGON SCALE':
    print_slow(f'{p1.name} purchases the DRAGON SCALE. What a lucky find for such a deal! {p1.GP}GP remaining.\n', typingActive)
  if selc == 'GORGET':
    print_slow(f'{p1.name} purchases the GORGET. Not the most comfortable piece of armor to wear, but it may just save your life! {p1.name} has gained 10% DEF! {p1.GP}GP remaining.\n', typingActive)


def sales_mechanic(p1, rooms, current_room, typingActive):
  global shop_open
  global traveling_shop
  global merchant_alive
  sale = 0
  selc = (input().upper()).strip()
  print_slow("\n", typingActive)

  if (selc == "ATK" or selc == "ATTACK") and traveling_shop == 1:
    foe = p28
    print_slow(f"{p1.name} assaults the Traveling Merchant! The Merchant narrowly avoids the attack before drawing his own weapon!\n", typingActive)
    standard_battle(p1, foe, typingActive)
    print_slow(f"{p1.name} slays the Merchant in cold blood. The gnome's body lays motionless on the ground. {p1.name} rummages through the Merchants wares for anything valuable that is still intact. {p1.name} finds some POTIONS, ANTIDOTES, and ETHERS. {p1.name} takes whatever they can carry; it's not like the Merchant will be needing them anymore.\n", typingActive)
    p1.POTS = min(p1.POTS + 3, p1.MaxPOTS)
    p1.ANT = min(p1.ANT + 2, p1.MaxANT)
    p1.ETR = min(p1.ETR + 2, p1.MaxETR)
    merchant_death()
    p1.stat_check(typingActive)
    shop_open = 0
    traveling_shop = 0
    merchant_alive = 0
    return
  if selc in shop_items:
    
    if p1.GP < key_items[selc]['price']:
      print_slow(""""Sorry, it doesn't look like you have enough GP for that."\n""", typingActive)

    if p1.GP >= key_items[selc]['price']: 
      
      if selc == 'POTION':
        if p1.POTS < p1.MaxPOTS:
          p1.POTS += 1
          sale = 2
        else:
          sale = 1
      if selc == 'ANTIDOTE':
        if p1.ANT < p1.MaxANT:
          p1.ANT += 1
          sale = 2
        else:
          sale = 1
      if selc == 'ETHER':
        if p1.ETR < p1.MaxETR:
          p1.ETR += 1
          sale = 2
        else:
          sale = 1
      if selc == 'SMOKE BOMB':
        if p1.SMB < p1.MaxSMB:
          p1.SMB += 1
          sale = 2
        else:
          sale = 1
      if selc in shop_keyItems:
        if selc in p1.inventory:
          print_slow(f""""It looks like that isn't available, sorry about that!"\n""", typingActive)
          sale = 3
        elif traveling_shop == 1 and selc in travelingMerchant_items:
          p1.GP -= key_items[selc]['price']
          travelingMerchant_items.remove(selc)
          p1.inventory.append(selc)
          if selc == "GORGET":
            p1.DEF = max(p1.DEF - 10, 25)
          key_itemBought(p1, selc, typingActive)
        elif 'items' in rooms[current_room]:
          if selc in rooms[current_room]['items']:
            p1.GP -= key_items[selc]['price']
            rooms[current_room]['items'].remove(selc)
            if selc == 'EXTRA POUCH':
              p1.MaxPOTS += 5
              p1.MaxANT += 5
              p1.MaxETR += 5
              p1.MaxSMB += 5
            elif selc == 'DRAGON SCALE':
              p1.DragonP += 1
            elif selc == 'GORGET':
              p1.DEF = max(p1.DEF - 10, 25)
              p1.inventory.append(selc)
            else:  
              p1.inventory.append(selc)
            key_itemBought(p1, selc, typingActive)
        else:
          print_slow(f""""It looks like that isn't available, sorry about that!"\n""", typingActive)
          sale = 3

      if sale == 3:
        pass
      if sale == 2:
          p1.GP -= key_items[selc]['price']
          print_slow(f"{p1.name} purchases a {selc} for {key_items[selc]['price']} GP and adds it to their inventory. {p1.name} has {p1.GP} GP.\n", typingActive)
      if sale == 1:
          print_slow('"Looks like your inventory is full."\n', typingActive)   
        
  elif selc == "BACK":
        shop_open = 0
        traveling_shop = 0
  else:
     print_slow('\nInvalid selection. Try again.\n', typingActive)
    
def shrine_pray(p1, typingActive):
  if p1.GP >= 35:
    p1.MP = p1.MaxMP
    p1.GP -= 35
    print_slow(f"{p1.name} drops 35 GP into an ornate donation box and kneels between the lanterns at the alter. {p1.name} is filled with a surge of power. {p1.name}'s MP is fully restored.\n", typingActive)
  else:
    print_slow(f"{p1.name} is too poor to spend on charity.\n", typingActive)

def city_shop(p1, rooms, current_room, typingActive):
  global shop_open
  global traveling_shop
  shop_open = 1
  traveling_shop = 0
    
  if rooms['Shop']['event'] == 1 and p1.MonP >= 5:
    print_slow(""""I can tell you've got those MONSTER GUTS! Quick, pass them here before anyone else walks in!"\nThe Shop Keep frantically grabs the MONSTER GUTS and slips them into a jar tucked away under the counter.\n"Now I suppose I should hold up my end of the deal. I'll discount that SPECIAL FEED just for you." """, typingActive)
    p1.MonP -= 5
    rooms['Shop']['event'] = 2
    key_items['SPECIAL FEED']['price'] = key_items['SPECIAL FEED']['price']//2
    
  if rooms['Farm House']['speach'] == 3 and 'SPECIAL FEED' in rooms['Shop']['items'] and rooms['Shop']['event'] == 1:
      print_slow('If you can find me those 5 MONSTER GUTS I will give you a big discount on that SPECIAL FEED. Just be sure not to tell anyone I want them...', typingActive)
    
  if rooms['Farm House']['speach'] == 3 and 'SPECIAL FEED' in rooms['Shop']['items'] and rooms['Shop']['event'] == 0:
    print_slow(f"""\n"Hmm? Looking for SPECIAL FEED? We have some in the back. That will be [{key_items['SPECIAL FEED']['price']}GP]...Unless you are looking to barter? (Input selection: YES or NO)"\n""", typingActive)
    while True:
      selc = (input().upper()).strip()
      print_slow("\n", typingActive)
      if selc == 'YES':
        if 'CRAFTING POUCH' not in rooms['Shop']['items']:
          print_slow(""""I'll tell you what, if you can bring me 5 MONSTER GUTS I'll knock off half the price on that SPECIAL FEED. Don't worry what they're for... it's ah, for a project.\n" """, typingActive)
        else:
          print_slow(""""I'll tell you what, if you can bring me 5 MONSTER GUTS I'll knock off half the price on that SPECIAL FEED. I'll even give you a CRAFTING POUCH to store those MONSTER GUTS in. It should also fit other materials. Don't worry what they're for... it's ah, for a project.\n" """, typingActive)
          p1.inventory.append('CRAFTING POUCH')
          rooms['Shop']['items'].remove('CRAFTING POUCH')
          
        rooms['Shop']['event'] = 1
        break
      elif selc == 'NO':
        print_slow(""""Hmm... Alright, well let me know if you change your mind next time.\n """, typingActive)
        break
      else:
        print_slow('\nInvalid selection. Try YES or NO.\n', typingActive)
        

  while shop_open == 1:    
    print_slow(""""Well what will it be?"\n """, typingActive)
    print_slow(f"POTION:[{key_items['POTION']['price']} GP]\n", typingActive)
    print_slow(f"SMOKE BOMB:[{key_items['SMOKE BOMB']['price']} GP]\n", typingActive)
    print_slow(f"ANTIDOTE:[{key_items['ANTIDOTE']['price']} GP]\n", typingActive)
    print_slow(f"ETHER:[{key_items['ETHER']['price']} GP]\n", typingActive)
    if 'MAP' not in p1.inventory:
      print_slow(f"MAP:[{key_items['MAP']['price']} GP]\n", typingActive)
    if 'LANTERN' not in p1.inventory:
      print_slow(f"LANTERN:[{key_items['LANTERN']['price']} GP]\n", typingActive)
    if 'CRAFTING POUCH' not in p1.inventory:
      print_slow(f"CRAFTING POUCH:[{key_items['CRAFTING POUCH']['price']} GP]\n", typingActive)
    if rooms['Farm House']['speach'] == 3 and 'SPECIAL FEED' in rooms['Shop']['items']:
      print_slow(f"SPECIAL FEED:[{key_items['SPECIAL FEED']['price']}GP]\n", typingActive)
    print_slow(f"\n{p1.name}'s Wallet:[{p1.GP} GP]\n", typingActive)

    
    print_slow('\nType your selection or BACK to leave shopping window.\n', typingActive)    
    sales_mechanic(p1, rooms, current_room, typingActive)

def harbor_shop(p1, rooms, current_room, typingActive):
  global shop_open
  global traveling_shop
  shop_open = 1
  traveling_shop = 0

  while shop_open == 1:    
    print_slow(""""Anything catch your eye?"\n """, typingActive)
    print_slow(f"POTION:[{key_items['POTION']['price']} GP]\n", typingActive)
    print_slow(f"SMOKE BOMB:[{key_items['SMOKE BOMB']['price']} GP]\n", typingActive)
    print_slow(f"ANTIDOTE:[{key_items['ANTIDOTE']['price']} GP]\n", typingActive)
    print_slow(f"ETHER:[{key_items['ETHER']['price']} GP]\n", typingActive)
    if 'MAP' not in p1.inventory:
      print_slow(f"MAP:[{key_items['MAP']['price']} GP]\n", typingActive)
    if 'GORGET' not in p1.inventory:
      print_slow(f"GORGET:[{key_items['GORGET']['price']} GP]\n", typingActive)
    if 'CRAFTING POUCH' not in p1.inventory:
      print_slow(f"CRAFTING POUCH:[{key_items['CRAFTING POUCH']['price']} GP]\n", typingActive)
    if 'EXTRA POUCH' in rooms[current_room]['items']:
      print_slow(f"EXTRA POUCH:[{key_items['EXTRA POUCH']['price']}GP]\n", typingActive)
    if 'DRAGON SCALE' in rooms[current_room]['items']:
      print_slow(f"DRAGON SCALE:[{key_items['DRAGON SCALE']['price']}GP]\n", typingActive)
    print_slow(f"\n{p1.name}'s Wallet:[{p1.GP} GP]\n", typingActive)

    
    print_slow('\nType your selection or BACK to leave shopping window.\n', typingActive)    
    sales_mechanic(p1, rooms, current_room, typingActive)

def traveling_merchant(p1, foe, current_room, typingActive):
  global shop_open
  global traveling_shop
  global merchant_alive 
  shop_open = 1
  traveling_shop = 1
  merchant_alive = 1
  
  print_slow(line305, typingActive)
  while shop_open == 1:
    print_slow(""""Take a look!"\n""", typingActive)
    print_slow(f"POTION:[{key_items['POTION']['price']} GP]\n", typingActive)
    print_slow(f"SMOKE BOMB:[{key_items['SMOKE BOMB']['price']} GP]\n", typingActive)
    print_slow(f"ANTIDOTE:[{key_items['ANTIDOTE']['price']} GP]\n", typingActive)
    print_slow(f"ETHER:[{key_items['ETHER']['price']} GP]\n", typingActive)
    if 'MAP' not in p1.inventory:
      print_slow(f"MAP:[{key_items['MAP']['price']} GP]\n", typingActive)
    if 'LANTERN' not in p1.inventory:
      print_slow(f"LANTERN:[{key_items['LANTERN']['price']} GP]\n", typingActive)
    print_slow(f"\n{p1.name}'s Wallet:[{p1.GP} GP]\n", typingActive)
    print_slow('\nType your selection or BACK to leave merchant.\n', typingActive) 
    sales_mechanic(p1, rooms, current_room, typingActive)
      
    if shop_open == 0:
      if merchant_alive == 1:
        print_slow('You bid farewell to the merchant and continue on your way.\n',typingActive)
      break
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
def fairy_examine(p1, rooms, typingActive):
  while True:
    if p1.faeCount == 0:
      print_slow(line2905, typingActive)
      break
    elif p1.faeCount >= 1 and rooms['Fairy Circle']['speach'] == 0:
      print_slow(line2906, typingActive)
      rooms['Fairy Circle']['speach'] = 1
      rooms['Fairy Circle']['EXPLORE'] = line2903
      break
    elif "Dark Fairy Prince" in rooms['Fairy Circle']['boss'] and rooms['Fairy Circle']['speach'] == 1:
      print_slow(line2907, typingActive)
      break
    elif "Dark Fairy Prince" not in rooms['Fairy Circle']['boss']:
      print_slow(line2908, typingActive)
      break
def swamp4_examine(p1, rooms, typingActive):
  while True:
    if rooms['Rotten Swamp 4']['event'] == 0:
      print_slow(line2709, typingActive)
      selc = (input().upper()).strip()
      print_slow("", typingActive)
      if selc == 'LEFT':
        print_slow(line2713, typingActive)
        p1.POISON += 3
        foe = rooms['Rotten Swamp 4']['foe']
        standard_battle(p1, foe, typingActive)
        print_slow(line2714, typingActive)
        rooms['Rotten Swamp 4']['map'] = swamp4_map2
        rooms['Rotten Swamp 4']['event'] = 1
        break
      elif selc == 'RIGHT':
        print_slow(line2715, typingActive)
        p1.inventory.append('MOUTH-PIECE')
        rooms['Rotten Swamp 4']['map'] = swamp4_map3
        if ('MOUTH-PIECE' and 'BROKEN HORN') in p1.inventory:
          p1.inventory.append('COMPLETE HORN')
          p1.inventory.remove('MOUTH-PIECE')
          p1.inventory.remove('BROKEN HORN')
          rooms['Rotten Swamp 8']['EXPLORE'] = line2729
          print_slow(line2716, typingActive)
          rooms['Rotten Swamp 4']['event'] = 2
        break
      elif selc == 'BACK':
        print_slow('You decide to leave the chests be for now.\n', typingActive)
        break
      else:
        print_slow('\nInvalid selection. Try again.\n', typingActive)
        
    elif rooms['Rotten Swamp 4']['event'] == 1:
      print_slow(line2710, typingActive)
      selc = (input().upper()).strip()
      print_slow("", typingActive)
      if selc == 'RIGHT':
        print_slow(line2715, typingActive)
        p1.inventory.append('MOUTH-PIECE')
        rooms['Rotten Swamp 4']['map'] = swamp4_map4
        if ('MOUTH-PIECE' and 'BROKEN HORN') in p1.inventory:
          p1.inventory.append('COMPLETE HORN')
          p1.inventory.remove('MOUTH-PIECE')
          p1.inventory.remove('BROKEN HORN')
          print_slow(line2716, typingActive)
          rooms['Rotten Swamp 4']['event'] = 3
        break
      elif selc == 'BACK':
        print_slow('You decide to leave the chests be for now.\n', typingActive)
        break
      else:
        print_slow('\nInvalid selection. Try again.\n', typingActive)
        
    elif rooms['Rotten Swamp 4']['event'] == 2:  
      print_slow(line2711, typingActive)
      selc = (input().upper()).strip()
      print_slow("", typingActive)
      if selc == 'LEFT':
        print_slow(line2713, typingActive)
        p1.POISON = 3
        foe = rooms['Rotten Swamp 4']['foe']
        standard_battle(p1, foe, typingActive)
        print_slow(line2714, typingActive)
        rooms['Rotten Swamp 4']['map'] = swamp4_map4
        rooms['Rotten Swamp 4']['event'] = 3
        break
      elif selc == 'BACK':
        print_slow('You decide to leave the chests be for now.\n', typingActive)
        break
      else:
        print_slow('\nInvalid selection. Try again.\n', typingActive)
        
    elif rooms['Rotten Swamp 4']['event'] == 3:
      print_slow(line2712, typingActive)
      break

def shipwreck_examine(p1, rooms, typingActive):
  while True:
    if rooms['Shipwreck']['chest'] == 'OPEN':
      print_slow(line3309, typingActive)
      break
    elif rooms['Shipwreck']['chest'] == 'CLOSED':
      print_slow(line3304, typingActive)
      selc = input().upper().strip()
      print('\n')
      if selc == 'YES':
        print_slow(line3306, typingActive)
        hit = random.randrange(0,10) + rooms['Shipwreck']['event']
        if hit >= 9:
          print_slow(line3308, typingActive)
          p1.GP += 300
          p1.POTS = min(p1.POTS + 2, p1.MaxPOTS)
          print_slow(f"{p1.name} has {p1.GP} GP and {p1.POTS}/{p1.MaxPOTS} POTIONS.\n", typingActive)
          rooms['Shipwreck']['chest'] = 'OPEN'
          break
        elif hit < 9:
          print_slow(line3307, typingActive)
          foe = random.choice(rooms['Shipwreck']['enemy_spawn_set'])
          standard_battle(p1, foe, typingActive)
          rooms['Shipwreck']['event'] += 2
          break
      elif selc == 'NO':
        print_slow(line3305, typingActive)
        break
      else:
        print_slow('\nInvalid selection. Select YES or NO.', typingActive)
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
def waterfall_lock(p1, selc, rooms, typingActive):
  while True:
    if rooms['Waterfall Pool']['SOUTH'] == 'LOCKED':
      print_slow("\nYou can't go to the south.\n", typingActive)
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
      p1.MaxHP += 10
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
        print_slow(f'{p1.name} was given a BUCKLER! This sturdy steel shield should help block damage. {p1.name} has gained 10% DEF!\n', typingActive)
        p1.DEF = max(p1.DEF - 10, 25)
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
        rooms['Shop']['event'] = 1
        rooms['Shop']['items'].append('SPECIAL FEED')
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
def witch_speak(p1, rooms, typingActive):
  while True:
    if rooms["Witch's Cabin"]['speach'] == 0:
      print_slow(line2403,typingActive)
      rooms["Witch's Cabin"]['speach'] = 1
      rooms["Witch's Cabin"]['crafting'] = 'ACTIVE'
      break
    if rooms["Witch's Cabin"]['speach'] == 1:
      print_slow(line2404,typingActive)
      break
def fairy_speak(p1, rooms, typingActive):
  while True:
    if rooms['Fairy Circle']['speach'] == 0:
      print_slow('\nInvalid selection. Try again.', typingActive)
      break
    elif rooms['Fairy Circle']['speach'] == 1:
      if p1.faeCount < rooms['Fairy Circle']['fairy_reward']:
        print_slow(f""""Hello, thank you for returning. I appreciate all of your assistance. If you can return after defeating {rooms['Fairy Circle']['fairy_reward'] - p1.faeCount} more Dark Fae I should regain enough strength to reward you."\n """,typingActive)
        break
      elif p1.faeCount >= rooms['Fairy Circle']['fairy_reward']:
        if rooms['Fairy Circle']['fairy_reward'] == 5:      
          print_slow(line2909,typingActive)
          p1.GP += 100
          print_slow(f'{p1.name} is given 100 GP! {p1.name} has {p1.GP} GP in their wallet.',typingActive)
          rooms['Fairy Circle']['fairy_reward'] = 10
          break
        if rooms['Fairy Circle']['fairy_reward'] == 10:      
          print_slow(line2910,typingActive)
          p1.ETR = min(p1.ETR + 3, p1.MaxETR)
          print_slow(f'{p1.name} is given 3 ETHERS! {p1.name} has {p1.ETR}/{p1.MaxETR} ETHERS in their bag.',typingActive)
          rooms['Fairy Circle']['fairy_reward'] = 20
          break
        if rooms['Fairy Circle']['fairy_reward'] == 20:      
          print_slow(line2911,typingActive)
          foe = rooms['Fairy Circle']['foe'] 
          standard_battle(p1, foe, typingActive)
          print_slow(line2912,typingActive)
          p1.inventory.append('CRYSTAL NECKLACE')
          p1.MaxMP += 2
          p1.MP = p1.MaxMP
          print_slow(f"{p1.name} equips the CRYSTAL NECKLACE! {p1.name}'s max MP has increased.\n",typingActive)
          p1.stat_check(typingActive)
          rooms['Fairy Circle']['boss'].remove('Dark Fairy Prince') 
          rooms['Fairy Circle']['speach'] = 2
          rooms['Fairy Circle']['EXPLORE'] = line2904
          rooms['Fairy Circle']['map'] = fairy_map2
          break
    elif rooms['Fairy Circle']['speach'] == 2:
          print_slow('You try talking to the Dark Fairy Prince, but remember you killed him. Oh well. He was kind of a jerk.',typingActive)
          break
def marsh_speak(p1, rooms, typingActive):
  while True:
    if rooms["Frog Marsh"]['speach'] == 0:
      print_slow(line2803,typingActive)
      rooms["Frog Marsh"]['speach'] = 1
      p1.inventory.append('BROKEN HORN')
      if 'MOUTH-PIECE' in p1.inventory and 'BROKEN HORN' in p1.inventory:
          p1.inventory.append('COMPLETE HORN')
          p1.inventory.remove('MOUTH-PIECE')
          p1.inventory.remove('BROKEN HORN')
          rooms['Rotten Swamp 8']['EXPLORE'] = line2729
          print_slow(line2716, typingActive)
     
      break
    elif rooms["Frog Marsh"]['speach'] == 1:
      print_slow(line2806,typingActive)
      rooms["Frog Marsh"]['speach'] = 2
      break
    elif rooms["Frog Marsh"]['speach'] == 2:
      print_slow(line2804,typingActive)
      rooms["Frog Marsh"]['crafting'] = 'ACTIVE'
      rooms["Frog Marsh"]['speach'] = 3
      break
    elif rooms["Frog Marsh"]['speach'] == 3:
      print_slow(line2805,typingActive)
      break
def ship_speak(p1, rooms, typingActive):
  while True:
    if rooms['Docked Ship']['speach'] == 0:
      if rooms['Docked Ship']['event'] == 0:
        print_slow(line3503, typingActive)
      elif rooms['Docked Ship']['event'] == 1:
        print_slow(line3503b, typingActive)
      choice = 1
      while choice == 1:
        selc = input().upper().strip()
        print('\n')
        if selc == "YES":
          print_slow(line3504, typingActive)
          rooms['Docked Ship']['speach'] = 1
          rooms['Waterfall Pool']['SOUTH'] = 'Waterfall Cave'
          choice = 0
          break
        elif selc == "NO":
          print_slow(line3505, typingActive)
          rooms['Docked Ship']['event'] = 1
          choice = 0
          break
        else:
           print_slow('\nInvalid selection. Select YES or NO.\n', typingActive)
      rooms['Docked Ship']['intro'] = line3501b
      break
    elif rooms['Docked Ship']['speach'] == 1 and 'SERPENTS EYE' not in p1.inventory:
      print_slow(line3506, typingActive)
      break
    elif rooms['Docked Ship']['speach'] == 1 and 'SERPENTS EYE' in p1.inventory:
      print_slow(line3507, typingActive)
      p1.inventory.remove('SERPENTS EYE')
      p1.GP += 500
      print_slow(f"{p1.name} received a small treasure chest filled with gold coins worth 500 GP! {p1.name} has {p1.GP} GP in their wallet.", typingActive)
      rooms['Docked Ship']['speach'] = 2
      break
    elif rooms['Docked Ship']['speach'] == 2:
      print_slow(line3508, typingActive)
      break
def farm_crafting(p1, typingActive):
  while True:
    print_slow("Would you like to craft an ANTIDOTE using 5 PLANT PARTS? YES or NO.\n", typingActive)
    selc = (input().upper()).strip()
    if (selc == "YES" and p1.PlantP >= 5) and p1.ANT != p1.MaxANT:
      p1.PlantP -= 5
      p1.ANT = min(p1.ANT + 1, p1.MaxANT)
      print_slow(""""Here you go! One healing salve coming right up.\n" """, typingActive)
      print_slow(f'{p1.name} now has {p1.ANT} ANTIDOTES\n', typingActive)
    elif selc == "YES" and p1.ANT == p1.MaxANT:
      print_slow(f"Unable to craft more ANTIDOTES; {p1.name}'s inventory is full.\n", typingActive)
    elif selc == "YES" and p1.PlantP < 5:
      print_slow(f'{p1.name} does not have enough PLANT PARTS. {p1.name} only has {p1.PlantP} PLANT PARTS\n', typingActive)
    elif selc == "NO":
      break
    else:
      print_slow('\nInvalid selection. Try again. Please select YES or NO\n')
      
def witch_crafting(p1, typingActive):
  while True:
    print_slow("Would you like to craft an ETHER using 10 FAE DUST? YES or NO.\n", typingActive)
    selc = (input().upper()).strip()
    print_slow('\n', typingActive)
    if (selc == "YES" and p1.FaeP >= 10) and p1.ETR != p1.MaxETR:
      p1.FaeP -= 10
      p1.ETR = min(p1.ETR + 1, p1.MaxETR)
      print_slow(""""Hehehe! One freshly concocted ETHER for you.\n" """, typingActive)
      print_slow(f'{p1.name} now has {p1.ETR} ETHER\n', typingActive)
    elif selc == "YES" and p1.ETR == p1.MaxETR:
      print_slow(f"Unable to craft more ETHERS; {p1.name}'s inventory is full.\n", typingActive)
    elif selc == "YES" and p1.FaeP < 10:
      print_slow(f'{p1.name} does not have enough FAE DUST. {p1.name} only has {p1.FaeP} FAE DUST\n', typingActive)
    elif selc == "NO":
      break
    else:
      print_slow('\nInvalid selection. Try again. Please select YES or NO\n')
def marsh_crafting(p1, typingActive):
  while True:
    print_slow("Would you like to craft a SMOKE BOMB using 15 MONSTER PARTS? YES or NO.\n", typingActive)
    selc = (input().upper()).strip()
    print_slow('\n', typingActive)
    if (selc == "YES" and p1.MonP >= 15) and p1.SMB != p1.MaxSMB:
      p1.MonP -= 15
      p1.SMB = min(p1.SMB + 1, p1.MaxSMB)
      print_slow(""""Oh grandpappy would be proud of this one! Hope you get some good use out of this SMOKE BOMB.\n" """, typingActive)
      print_slow(f'{p1.name} now has {p1.ETR} SMOKE BOMBS\n', typingActive)
    elif selc == "YES" and p1.SMB == p1.MaxSMB:
      print_slow(f"Unable to craft more SMOKE BOMBS; {p1.name}'s inventory is full.\n", typingActive)
    elif selc == "YES" and p1.MonP < 15:
      print_slow(f'{p1.name} does not have enough MONSTER PARTS. {p1.name} only has {p1.MonP} MONSTER PARTS\n', typingActive)
    elif selc == "NO":
      break
    else:
      print_slow('\nInvalid selection. Try again. Please select YES or NO\n')

def cliff_special(p1, selc, typingActive): 
    print_slow(line610,typingActive)
    damage = 69
    p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
    player_death(p1, typingActive)
    if p1.HP > 0:
      rooms['Cliff Side']['secret_path'] = 1
      print_slow(line611,typingActive)
    return

def cave4_special(p1, selc, typingActive):
    print_slow(line946,typingActive)
    p1.HP = 0
    player_death(p1, typingActive)
    return
def berry_special(p1, selc, typingActive):
    if rooms['Berry Patch']['chest'] == "OPEN":
      if selc == 'WAIT':
        print_slow(f"{p1.name} waits for the REZZBERRIES to regrow. In that year SMELDAR's forces have conquered the kingdom. What do you think was going to happen?",typingActive)
        p1.HP = 0
        player_death(p1, typingActive)
      if selc == 'PICK':
        print_slow(line1006, typingActive)
        rooms['Berry Patch']['secret_path'] = 2 
    else:
      print_slow('\nInvalid selection. Try again.', typingActive)
      rooms['Berry Patch']['secret_path'] = 2 
    return
def river_special(p1, selc, typingActive):
    print_slow(line1207,typingActive)
    p1.HP = 0
    player_death(p1, typingActive)
    return
def lake_special(p1, selc, typingActive):
    print_slow(line1414,typingActive)
    p1.HP = 0
    player_death(p1, selc, typingActive)
    return
def swamp_special(p1, selc, typingActive):
    if selc == 'DRINK':
      print_slow(line2721,typingActive)
      p1.POISON += 3
      p1.HP -= 5
      if p1.HP <= 0:
        player_death(p1, typingActive)
      else:
        print_slow(f'{p1.name} takes 5 damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n',typingActive)
    elif selc == 'SWIM' or selc == 'DIVE':
      print_slow(line2722,typingActive)
      p1.HP = 0
      player_death(p1, typingActive)
    return
def swamp6_special(p1, selc, typingActive):
    swamp_special(p1, selc, typingActive)
    rooms['Rotten Swamp 6']['secret_path'] = 2   
    return
def swamp7_special(p1, selc, typingActive):
    if selc in song_term and rooms['Rotten Swamp 7']['event'] == 1:
      print_slow(line2726,typingActive)
    elif selc in song_term and rooms['Rotten Swamp 7']['event'] == 0:
      print_slow(line2725,typingActive)
      p1.GR += 1.5
      p1.inventory.append('GOLD RING')
      print_slow(f'{p1.name} recieved a GOLD RING! {p1.name} feels their fortune improving with the ring in hand.\n',typingActive)
      rooms['Rotten Swamp 7']['event'] = 1
    else:
      swamp_special(p1, selc, typingActive)
    rooms['Rotten Swamp 7']['secret_path'] = 2
    return
def swamp8_special(p1, selc, typingActive):
    if selc == 'PLAY' and rooms['Rotten Swamp 8']['event'] == 1:
      print_slow(line2737, typingActive)
    elif selc == 'PLAY' and rooms['Rotten Swamp 8']['event'] == 0:
      print_slow(line2731, typingActive)
      if 'WAFFLE' in p1.inventory:
        print_slow(line2733, typingActive)
        selc = (input().upper()).strip()
        print_slow('\n', typingActive)
        if selc == 'GIVE':
          print_slow(line2735, typingActive)
          p1.inventory.remove('WAFFLE')
          p1.inventory.append('GILDED DRAGON BONE KEY')
          rooms['Rotten Swamp 8']['event'] = 1
        if selc == 'KEEP':
          print_slow(line2736, typingActive)
          foe = rooms['Rotten Swamp 8']['foe']
          standard_battle(p1, foe, typingActive)
          p1.inventory.append('GILDED DRAGON BONE KEY')
          rooms['Rotten Swamp 8']['event'] = 1
          print_slow(line2738, typingActive)
        else: 
          print_slow('\nInvalid selection. Try again.', typingActive)
      elif 'WAFFLE' not in p1.inventory:
          print_slow(line2732, typingActive)
          foe = rooms['Rotten Swamp 8']['foe']
          standard_battle(p1, foe, typingActive)
          p1.inventory.append('GILDED DRAGON BONE KEY')
          rooms['Rotten Swamp 8']['event'] = 1
          print_slow(line2738, typingActive)
    else:
          swamp_special(p1, selc, typingActive)
          rooms['Rotten Swamp 8']['secret_path'] = 2
          return
  


rooms = {
    '' : {
        'name' : '',
        'intro' : None,
        'map' : None,
        'discovered' : [],
        'NORTH' : None,
        'EAST' : None,
        'SOUTH' : None,
        'WEST' : None,
        'EXPLORE' : None,
        'EXAMINE' : None,
        'SPEAK' : None,
        'REST' : None,
        'PRAY' : 'pray',
        'BUY' : "BUY",
        'CRAFT' : 'craft',
        'speach' : None,
        'crafting' : None,
        'secrets' : [],
        'secret_path' : 0,
        'spawn_rate' : 0,
        'enemy_spawn_set' : None,
        'boss' : [],
        'boss_ambush' : None,
        'items' : [],
        'foe' : None,
        'LOCK' : None,
        'chest' : None,
        'event' : None,
    },
    
    'TESTING GROUND' : {
        'name' : 'TESTING GROUND',
        'intro' : "How'd you end up here?",
        'map' : blank_map1,
        'discovered' : [],
        'NORTH' : 'Docked Ship',
        'EAST' : 'Camp Site',
        'SOUTH' : 'Camp Site',
        'WEST' : 'Camp Site',
        'EXPLORE' : 'Nothing to see here....',
       # 'EXAMINE' : None,
        #'SPEAK' : None,
        #'REST' : None,
        #'PRAY' : 'pray',
        #'BUY' : "BUY",
        #'CRAFT' : 'craft',
        #'speach' : None,
        #'crafting' : None,
        #'secrets' : [],
        #'secret_path' : 0,
        'spawn_rate' : 5,
        'enemy_spawn_set' : enemy_spawnT,
        #'boss' : [],
        #'boss_ambush' : None,
        #'foe' : None,
        #'LOCK' : None,
        #'chest' : None,
        #'event' : None,
    },
  
    'Camp Site' : {
        'name' : 'Camp Site',
        'intro' : line101,
        'map' : camp_map1,
        'discovered' : [],
        'NORTH' : 'Deep Forest',
        'EAST' : 'TESTING GROUND',
        'SOUTH' : 'Town Center',
        'WEST' : 'Cliff Side',
        'EXPLORE' : line103,
        'REST': camp_healing,
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
        'EXPLORE' : line602,
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
        'EXPLORE' : line202,
        'spawn_rate' : 0,
    },

  'Shop' : {
        'name' : 'Shop',
        'intro' : line301,
        'map' : shop_map1,
        'discovered' : [],
        'WEST' : 'Town Center',
        'EXIT' : 'Town Center',
        'EXPLORE' : line304,
        'BUY' : city_shop,
        'spawn_rate' : 0,
        'event' : 0,
        'items' : ['MAP', 'LANTERN', 'CRAFTING POUCH',],
    },

  'Inn' : {
        'name' : 'Inn',
        'intro' : line401,
        'map' : inn_map1,
        'discovered' : [],
        'EAST' : 'Town Center',
        'EXIT' : 'Town Center',
        'EXPLORE' : line404,
        'REST' : city_inn,
        'spawn_rate' : 0,
    },

  'Royal Castle' : {
        'name' : 'Royal Castle',
        'intro' : line501,
        'map' : castle_map1,
        'discovered' : [],
        'NORTH' : 'Town Center',
        'EXIT' : 'Town Center',
        'EXPLORE' : line502,
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
        'EXPLORE' : line702,
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
        'EAST' :'Misty Woods - Bend',
        'SOUTH' : 'Rocky Hill',
        'EXPLORE' : line1102,
        'SPEAK' : shrine_speak,
        'PRAY' : shrine_pray,
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
        'EXPLORE' : line906,
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
        'EXPLORE' : line917,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn8,
    },

  'Rocky Cave 2' : {
        'name' : 'Rocky Cave 2',
        'intro' : line922,
        'map' : cave2_map1,
        'discovered' : [],
        'SOUTH' : 'Rocky Cave 1',
        'EXPLORE' : line923,
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
        'EXPLORE' : line932a,
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
        'EXPLORE' : line950,
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
        'EXPLORE' : line1202,
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
        'SOUTH' : 'LOCKED',
        'EXPLORE' : line1302,
        'EXAMINE' : waterfall_examine,
        'secrets' : ['JUMP', 'SWIM', 'DIVE'],
        'special' : river_special,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn5,
        'chest' : 'CLOSED',
        'event' : 0,
    },
  'Waterfall Cave' : {
        'name' : 'Waterfall Cave',
        'intro' : None,
        'map' : None,
        'discovered' : [],
        'NORTH' : None,
        'EAST' : None,
        'SOUTH' : None,
        'WEST' : None,
        'EXPLORE' : None,
        'EXAMINE' : None,
        'SPEAK' : None,
        'REST' : None,
        'PRAY' : 'pray',
        'BUY' : "BUY",
        'CRAFT' : 'craft',
        'speach' : None,
        'crafting' : None,
        'secrets' : [],
        'secret_path' : 0,
        'spawn_rate' : 0,
        'enemy_spawn_set' : None,
        'boss' : [],
        'boss_ambush' : None,
        'items' : [],
        'foe' : None,
        'LOCK' : None,
        'chest' : None,
        'event' : None,
    },

  'Lake Beach' : {
        'name' : 'Lake Beach',
        'intro' : line1401,
        'map' : lake_map1,
        'discovered' : [],
        'NORTH' : 'Boat House',
        'EAST' : 'LOCKED',
        'SOUTH' : 'River Channel',
        'EXPLORE' : line1402,
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
        'EXPLORE' : line1502,
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
        'EXPLORE' : line1002,
        'EXAMINE' : berry_examine,
        'secrets' : ['WAIT', 'PICK'],
        'special' : berry_special,
        'secret_path' : 0,
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
        'NORTH' : "Witch's Cabin",
        'EAST' : 'Great Oak',
        'SOUTH' : 'Quiet Village',
        'WEST' : 'Berry Patch',
        'EXPLORE' : line1702,
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
        'EXPLORE' : line2402,
        'SPEAK' : witch_speak,
        'CRAFT' : witch_crafting,
        'speach' : 0,
        'crafting' : 'INACTIVE',
        'spawn_rate' : 0, 
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
        'EXPLORE' : line1802,
        'spawn_rate' : 0,
    },

  'Tavern & Inn' : {
        'name' : 'Tavern & Inn',
        'intro' : line401b,
        'map' : tavern_map1,
        'discovered' : [],
        'NORTH' : 'Quiet Village',
        'EXIT' : 'Quiet Village',
        'EXPLORE' : line404b,
        'REST' : city_inn,
        'spawn_rate' : 0,
    },

  "Smith's Workshop" : {
        'name' : "Smith's Workshop",
        'intro' : line1901,
        'map' : smith_map1,
        'discovered' : [],
        'EAST' : 'Quiet Village',
        'EXIT' : 'Quiet Village',
        'EXPLORE' : line1902,
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
        'EXPLORE' : line2202,
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
        'EXPLORE' : line2002,
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
        'EXPLORE' : line2105,
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
        'SOUTH' : 'Fairy Circle',
        'WEST' : 'Lake Beach',
        'EXPLORE' : line1602,
        'EXAMINE' : mushroom_examine,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn7,
        #'LOCK' : None,
        'chest' : "CLOSED",
        #'event' : None,
    },'secrets' : ['JUMP', 'FLY', 'DIVE'],

  'Fairy Circle' : {
        'name' : 'Fairy Circle',
        'intro' : line2901,
        'map' : fairy_map1,
        'discovered' : [],
        'NORTH' : 'Mushroom Grove',
        'EXPLORE' : line2902,
        'EXAMINE' : fairy_examine,
        'SPEAK' : fairy_speak,
        'speach' : 0,
        'spawn_rate' : 0,
        'boss': ["Dark Fairy Prince"],
        'foe' : p40,
        'fairy_reward' : 5,
        
    },
  
  'Rotting Woods' : {
        'name' : 'Rotting Woods',
        'intro' : line2601,
        'map' : rot_map1,
        'discovered' : [],
        'NORTH' : 'Frog Marsh',
        'SOUTH' : 'Mushroom Grove',
        'WEST' : 'Rotten Swamp 1',
        'EXPLORE' : line2602,
        'spawn_rate' : 2,
        'enemy_spawn_set' : enemy_spawn11,
    },

  #Ogre Dungeon start
  'Rotten Swamp 1' : {
        'name' : 'Rotten Swamp 1',
        'intro' : line2701,
        'map' : swamp1_map1,
        'discovered' : [],
        'EAST' : 'Rotting Woods',
        'WEST' : 'Rotten Swamp 2',
        'EXPLORE' : line2702,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn12,
    },
  'Rotten Swamp 2' : {
        'name' : 'Rotten Swamp 2',
        'intro' : line2703,
        'map' : swamp2_map1,
        'discovered' : [],
        'EAST' : 'Rotten Swamp 1',
        'SOUTH' : 'Rotten Swamp 6',
        'WEST' : 'Rotten Swamp 3',
        'EXPLORE' : line2704,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn13,
    },
  'Rotten Swamp 3' : {
        'name' : 'Rotten Swamp 3',
        'intro' : line2705,
        'map' : swamp3_map1,
        'discovered' : [],
        'NORTH' : 'Rotten Swamp 4',
        'EAST' : 'Rotten Swamp 2',
        'SOUTH' : 'Rotten Swamp 5',
        'EXPLORE' : line2706,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn13,
    },
  'Rotten Swamp 4' : {
        'name' : 'Rotten Swamp 4',
        'intro' : line2707,
        'map' : swamp4_map1,
        'discovered' : [],
        'SOUTH' : 'Rotten Swamp 3',
        'EXPLORE' : line2708,
        'EXAMINE' : swamp4_examine,
        'event' : 0,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn12,
        'foe' : p29b,
    },
  'Rotten Swamp 5' : {
        'name' : 'Rotten Swamp 5',
        'intro' : line2717,
        'map' : swamp5_map1,
        'discovered' : [],
        'NORTH' : 'Rotten Swamp 3',
        'EAST' : 'Rotten Swamp 6',
        'SOUTH' : 'Rotten Swamp 8',
        'WEST' : 'Rotten Swamp 7',
        'EXPLORE' : line2718,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn13,
    },
  'Rotten Swamp 6' : {
        'name' : 'Rotten Swamp 6',
        'intro' : line2719,
        'map' : swamp6_map1,
        'discovered' : [],
        'NORTH' : 'Rotten Swamp 2',
        'WEST' : 'Rotten Swamp 5',
        'EXPLORE' : line2720,
        'special' : swamp6_special,
        'secrets' : ['DRINK', 'SWIM', 'DIVE'],
        'secret_path' : 0,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn14,
    },
  'Rotten Swamp 7' : {
        'name' : 'Rotten Swamp 7',
        'intro' : line2723,
        'map' : swamp7_map1,
        'discovered' : [],
        'EAST' : 'Rotten Swamp 5',
        'EXPLORE' : line2724,
        'special' : swamp7_special,
        'secrets' : ['DRINK', 'SWIM', 'DIVE', 'RIBBIT', 'RIBBITING', 'CROAK','CROAKING', 'KERO', 'KEROKERO'],
        'secret_path' : 0,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn12,
        'event' : 0,
     },
  'Rotten Swamp 8' : {
        'name' : 'Rotten Swamp 8',
        'intro' : line2727,
        'map' : swamp8_map1,
        'discovered' : [],
        'NORTH' : 'Rotten Swamp 5',
        'EXPLORE' : line2728,
        'special' : swamp8_special,
        'secrets' : ['PLAY', 'DRINK', 'SWIM', 'DIVE'],
        'secret_path' : 0,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn13,
        'foe': p35,
        'event' : 0,
     },
  #Ogre Dungeon End

  'Frog Marsh' : {
        'name' : 'Frog Marsh',
        'intro' : line2801,
        'map' : marsh_map1,
        'discovered' : [],
        'EAST' : 'Grassy Plains',
        'SOUTH' : 'Rotting Woods',
        'EXPLORE' : line2802,
        'SPEAK' : marsh_speak,
        'CRAFT' : marsh_crafting,
        'speach' : 0,
        'crafting' : 'INACTIVE',
        #'secrets' : [],
        #'secret_path' : 0,
        'spawn_rate' : 0,
        'chest' : None,
        'event' : None,
    },
  'Grassy Plains' : {
        'name' : 'Grassy Plains',
        'intro' : line3001,
        'map' : plains_map1,
        'discovered' : [],
        'NORTH' : 'Northern Coast',
        'EAST' : 'Foot Hills',
        'WEST' : 'Frog Marsh',
        'EXPLORE' : line3002,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawnT,
    },
  'Foot Hills' : {
        'name' : 'Foot Hills',
        'intro' : line3101,
        'map' : foothills_map1,
        'discovered' : [],
        'NORTH' : 'Shipwreck',
        'WEST' : 'Grassy Plains',
        'EXPLORE' : line3102,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawnT,
    },
  'Northern Coast' : {
        'name' : 'Northern Coast',
        'intro' : line3201,
        'map' : coast_map1,
        'discovered' : [],
        'EAST' : 'Shipwreck',
        'SOUTH' : 'Grassy Plains',
        'WEST' : 'Harbor Town',
        'EXPLORE' : line3202,
        'spawn_rate' : 4,
        'enemy_spawn_set' : enemy_spawn16,
    },
  'Shipwreck' : {
        'name' : 'Shipwreck',
        'intro' : line3301,
        'map' : shipwreck_map1,
        'discovered' : [],        
        'SOUTH' : 'Foot Hills',
        'WEST' : 'Northern Coast',
        'EXPLORE' : line3302,
        'EXAMINE' : shipwreck_examine,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn16,
        'chest' : 'CLOSED',
        'event' : 0,
    },
  #Harbor Town Start
    'Harbor Town' : {
        'name' : 'Harbor Town',
        'intro' : line3401,
        'map' : harbor1_map1,
        'discovered' : [],
        'NORTH' : 'Harbor Markets',
        'EAST' : 'Northern Coast',
        'WEST' : 'Harbor Inn',
        'EXPLORE' : line3402,
        'spawn_rate' : 0,
    },
    'Harbor Inn' : {
        'name' : 'Harbor Inn',
        'intro' : line401c,
        'map' : harborinn_map1,
        'discovered' : [],
        'EAST' : 'Harbor Town',
        'EXIT' : 'Harbor Town',
        'EXPLORE' : line404c,
        'REST' : city_inn,
        'spawn_rate' : 0,
    },
    'Harbor Markets' : {
        'name' : 'Harbor Markets',
        'intro' : line302,
        'map' : harbormarket_map1,
        'discovered' : [],
        'SOUTH' : 'Harbor Town',
        'WEST' : 'Docked Ship',
        'EXPLORE' : line303,
        'BUY' : harbor_shop,
        'spawn_rate' : 0,
        'items' : ['MAP', 'CRAFTING POUCH', 'DRAGON SCALE', 'EXTRA POUCH', 'GORGET',],
    },
    'Docked Ship' : {
        'name' : 'Docked Ship',
        'intro' : line3501,
        'map' : harborship_map1,
        'discovered' : [],
        'EAST' : 'Harbor Markets',
        'EXPLORE' : line3502,
        'SPEAK' : ship_speak,
        'speach' : 0,
        'spawn_rate' : 0,
        'event' : 0,
    },
      
  'Misty Woods - Bend' : {
        'name' : 'Misty Woods - Bend',
        'intro' : line3801,
        'map' : woodsBend_map1,
        'discovered' : [],
        #'NORTH' : None,
        'WEST' : 'Mystic Shrine',
        'EXPLORE' : line3802,
        'spawn_rate' : 3,
        'enemy_spawn_set' : enemy_spawn15,
    },
  
}

song_term = ['RIBBIT', 'RIBBITING', 'CROAK','CROAKING', 'KERO', 'KEROKERO']

#define player key items

key_items = {
    '': {
        'name': '',
        'description': '',
    },

  'POTION': {
        'name': 'POTION',
        'description': None,
        'price' : 35,
    },
  'ANTIDOTE': {
        'name': 'ANTIDOTE',
        'description': None,
        'price' : 25,
    },
  'ETHER': {
        'name': 'ETHER',
        'description': None,
        'price' : 40,
    },
  'SMOKE BOMB': {
        'name': 'SMOKE BOMB',
        'description': None,
        'price' : 30,
    },
  'DRAGON SCALE': {
        'name': 'DRAGON SCALE',
        'description': None,
        'price' : 350
    },
  
    'MAP': {
        'name': 'MAP',
        'description': 'A map coated in magical ink. The ink reacts to your surroundings and changes depending on your location. (Type MAP or LOCATION to view current area)',
        'price' : 50,
    },
    'CRAFTING POUCH': {
        'name': 'CRAFTING POUCH',
        'description': "A special pouch in your pack for storing crafting materials. You're not sure how it can hold so much, but you're not about to question it either.",
        'price' : 300,
    },
    'LANTERN': {
        'name': 'LANTERN',
        'description': 'A lantern that attaches to a belt for hands free use. Allows travel through dark areas.',  
        'price' : 200,
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
    'GILDED DRAGON BONE KEY': {
        'name': 'GILDED DRAGON BONE KEY',
        'description': 'A key made of Dragon bone. Dragon Bone Keys are said to be used to secure magical seals. This one has been covered in a layer of thin gold.',
    },
    'ROYAL JELLY': {
        'name': 'ROYAL JELLY',
        'description':'A jar of Giant Bee Royal Jelly. This substance is capable of enhancing the healing properties of potions. Just a tiny bit mixed in will greatly increase the potancy.',
    },
    'SPECIAL FEED': {
        'name': 'SPECIAL FEED',
        'description': 'A medicated feed for pigs. Quite pricey; the Farmer better have the GP to cover the costs...',
        'price' : 500,
    },
    'MOUTH-PIECE': {
        'name': 'MOUTH-PIECE',
        'description': 'A mouth piece belonging to a musical horn. Not much use on its own, but it could be attached to the right instrument...',
    },
    'BROKEN HORN': {
        'name': 'BROKEN HORN',
        'description': 'A musical horn that is missing its mouth piece. The Frog-Man claims you will need this to seek an audience with the Ogre Chief. but it cant be played without the missing part.',
    },
    'COMPLETE HORN': {
        'name': 'COMPLETE HORN',
        'description': 'A complete musical horn. Made by combining the BROKEN HORN and the MOUTH PIECE. Can be played in the deepest part of the swamp to seak an audience with the Ogre Chief.',
    },
  'WAFFLE': {
        'name': 'WAFFLE',
        'description': 'A large, perfectly made breakfast waffle dropped by a donkey in the swamp. Probably not safe to eat, but maybe you will find some use for it?..',
    },
  'GOLD RING': {
        'name': 'GOLD RING',
        'description': 'A perfectly polished gold ring. Given to you by one of the Frog-Sirens of the swamp. You feel luckier holding this, like your wealth is about to grow.',
    },
  'CRYSTAL NECKLACE': {
        'name': 'CRYSTAL NECKLACE',
        'description': 'A necklace made from an unusual crystal. A faint warmth can be felt emanating from it. Wearing it fills you with magical energy.',
    },
  'EXTRA POUCH': {
        'name': 'EXTRA POUCH',
        'description': None,
        'price' : 500,
    },
  'MYTHRIL MAIL': {
        'name': 'MYTHRIL MAIL',
        'description': 'A shirt made with rings of pure mythril. This legendary metal is stronger and tougher than steel, yet weighs as much as silk. Even a king would be jealous of such a fine piece of armor.',
    },
  'GORGET': {
        'name': 'GORGET',
        'description': 'A collar of metal plates covered in leather. Offers additional protection against blows to the throat; an essential piece of armor by all accounts.',
        'price' : 1250,
    },
  'STRANGE GREASE': {
        'name': 'STRANGE GREASE',
        'description': 'A strange grease found in the Waterfall Cave after defeating the River Serpant. Perhaps you should ask a SMITH about it...',
    },
  'MAGIC GREASE': {
        'name': 'MAGIC GREASE',
        'description': 'A strange grease found in the Waterfall Cave after defeating the River Serpant. Blades coated in it seem to never rust and retain their edge indefinitely.',
    },
  'SERPANT EYE': {
        'name': 'SERPANT EYE',
        'description': 'An eye plucked from the River Serpent. This trophy was requested by the old Captain as retribution for his lost eye from many years ago. Hopefully it was worth the trouble to get this nasty thing.'
}


shop_items = ['POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 'MAP', 'LANTERN', 'CRAFTING POUCH', 'SPECIAL FEED', 'DRAGON SCALE', 'EXTRA POUCH', 'GORGET']


shop_keyItems = ['MAP', 'LANTERN', 'CRAFTING POUCH', 'SPECIAL FEED', 'DRAGON SCALE', 'EXTRA POUCH', 'GORGET']
travelingMerchant_items = ['MAP', 'LANTERN', 'GORGET']


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


