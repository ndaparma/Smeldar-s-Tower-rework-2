from script import *
from character import *
from combat import *
from slowprint import *
from map import *
import random



def equip_stat_update(p1, selc, previous_gear):
  if previous_gear != None and previous_gear != 'EMPTY':
    p1.ATK += key_items[previous_gear]['ATK'] * -1
    p1.GDEF += (key_items[previous_gear]['DEF'] * -1)
    p1.MaxHP += key_items[previous_gear]['HP'] * -1 
    p1.MaxMP += key_items[previous_gear]['MP'] * -1 
    if previous_gear == 'AETHON':
      p1.skills.remove('BATTLECRY')
    if previous_gear == 'FULGUR':
      p1.skills.remove('SHOCK')
    if previous_gear == 'MIDAS':
      p1.skills.remove('$TOSS')
  p1.ATK += key_items[selc]['ATK']
  p1.GDEF += key_items[selc]['DEF']
  p1.MaxHP += key_items[selc]['HP'] 
  p1.MaxMP += key_items[selc]['MP']
  if p1.HP > p1.MaxHP:
    p1.HP = p1.MaxHP
  if p1.MP > p1.MaxMP:
    p1.MP = p1.MaxMP
  if selc == 'AETHON':
    p1.skills.append('BATTLECRY')
  if selc == 'FULGUR':
    p1.skills.append('SHOCK')
  if selc == 'MIDAS':
    p1.skills.append('$TOSS')


def potion_healing(p1, typingActive):
    heal = 15 + p1.RJ
    p1.POTS -= 1
    p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
    print_slow(
        f'{p1.name} drinks a POTION and heals {heal} HP. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n',
        typingActive)


def camp_healing(p1, current_room, typingActive):
    if rooms[current_room]['fire'] > 0:
        heal = random.randrange(10, 26) + (p1.MaxHP // 2)
        p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
        rooms[current_room]['fire'] -= 1
        print_slow(
            f'\n{p1.name} has rested and restored {heal}HP. {p1.name} now has {p1.HP}/{p1.MaxHP}HP.\n',
            typingActive)
        if rooms[current_room]['fire'] > 0:
            print_slow(
                f"{p1.name} may rest {rooms[current_room]['fire']} times before the tinder runs out.\n",
                typingActive)
        else:
            print_slow(
                f'The tinder has been used up and {p1.name} is unable to rest here.\n',
                typingActive)
    else:
        print_slow(
            f'The tinder has been used up and {p1.name} is unable to rest here.\n',
            typingActive)


def camp_rest(p1, current_room, typingActive):
    camp_healing(p1, current_room, typingActive)
    if rooms['Camp Site']['fire'] == 0:
        rooms['Camp Site']['intro'] = line102
        rooms['Camp Site']['EXPLORE'] = line104
        rooms['Camp Site']['map'] = camp_map2


def faecamp_rest(p1, current_room, typingActive):
    camp_healing(p1, current_room, typingActive)
    if rooms['Fae Woods - Camp']['fire'] == 0:
        rooms['Fae Woods - Camp']['intro'] = line4002
        rooms['Fae Woods - Camp']['EXPLORE'] = line4004
        rooms['Fae Woods - Camp']['map'] = faecamp_map2


def shrine_pray(p1, typingActive):
    if p1.GP >= 35:
        p1.MP = p1.MaxMP
        p1.GP -= 35
        print_slow(
            f"{p1.name} drops 35 GP into an ornate donation box and kneels between the lanterns at the alter. {p1.name} is filled with a surge of power. {p1.name}'s MP is fully restored.\n",
            typingActive)
    else:
        print_slow(f"{p1.name} is too poor to spend on charity.\n",
                   typingActive)


def merchant_death():
    enemy_spawn5.remove(p28)
    enemy_spawn9.remove(p28)
    enemy_spawn17.remove(p28)
    enemy_spawnT.remove(p28)

def key_itemBought(p1, selc, typingActive):
    if selc == 'MAP':
        print_slow(
            f"{p1.name} purchases a MAP! Now {p1.name} can stop getting lost all the time! (Type MAP or LOCATION to view current area) {p1.GP}GP remaining.\n",
            typingActive)
    if selc == 'LANTERN':
        print_slow(
            f'{p1.name} purchases a LANTERN and straps it to their belt. {p1.name} can quit being so afraid of the dark! {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'CRAFTING POUCH':
        print_slow(
            f'{p1.name} purchases a CRAFTING POUCH and attaches it to their pack. {p1.name} can store all sorts of weird things now! {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'SPECIAL FEED':
        print_slow(
            f'{p1.name} purchases the SPECIAL FEED. Hopefully the Farmers pig is still doing fine... {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'EXTRA POUCH':
        print_slow(
            f'{p1.name} purchases the EXTRA POUCH. Now {p1.name} can now store an additional 5 each of POTIONS, ANTIDOTES, ETHERS, and SMOKE BOMBS. {p1.GP}GP remaining.\n',
            typingActive)
        p1.MaxPOTS += 5
        p1.MaxANT += 5
        p1.MaxETR += 5
        p1.MaxSMB += 5
    if selc == 'DRAGON SCALE':
        print_slow(
            f'{p1.name} purchases the DRAGON SCALE. What a lucky find for such a deal! {p1.GP}GP remaining.\n',
            typingActive)
        p1.DragonP += 1


    if selc == 'MACE':
        print_slow(
            f'{p1.name} purchases the MACE. A sturdy blunt weapon perfect for smashing and bashing. {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'OBSIDIAN DAGGER':
        print_slow(
            f'{p1.name} purchases the OBSIDIAN DAGGER. A most unusual dagger made from volcanic glass. Must have been traded from a far off land... {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'ARMING SWORD':
        print_slow(
            f'{p1.name} purchases the ARMING SWORD. A common sword of a basic, but effective design. {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'BROAD SWORD':
        print_slow(
            f'{p1.name} purchases the BROAD SWORD. A finely crafted blade with superior hand protection. {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'SIDE SWORD':
        print_slow(
            f'{p1.name} purchases the SIDE SWORD. A finely crafted sword equal in strength and beauty. {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'HANGER':
        print_slow(
            f'{p1.name} purchases the HANGER. A simple navel sword, but the fine craftsmanship is obvious upon inspection. {p1.GP}GP remaining.\n',
            typingActive)

    if selc == 'LEATHER CAP':
        print_slow(
            f"{p1.name} purchases the LEATHER CAP. It might help protect your head from the sun at least?.. {p1.GP}GP remaining.\n",
            typingActive)
    if selc == 'SALLET':
        print_slow(
            f'{p1.name} purchases the SALLET. This fancy helmet has a hinged visor to make breathing and looking around the battlefield easier! {p1.GP}GP remaining.\n',
            typingActive)
            
    
    if selc == 'GAMBESON':
        print_slow(
            f"{p1.name} purchases the GAMBESON. Just because this armor is made from cloth doesn't mean you should underestimate its protection! {p1.GP}GP remaining.\n",
            typingActive)
    if selc == 'ORICHALCUM BRIGANDINE':
        print_slow(
            f'{p1.name} purchases the ORICHALCUM BRIGANDINE. Masterfully crafted from the legendary dwarven alloy!  {p1.GP}GP remaining.\n',
            typingActive)

    if selc == 'LEATHER BOOTS':
        print_slow(
            f'{p1.name} purchases the LEATHER BOOTS. Keeps your feet safe from rough terrain and stubbed toes at least. {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'VELVET SLIPPERS':
        print_slow(
            f'{p1.name} purchases the VELVET SLIPPERS. These fancy shoes are light as a feather and fashionable to boot! {p1.GP}GP remaining.\n',
            typingActive)
    if selc == 'CUISSES':
        print_slow(
            f'{p1.name} purchases the CUISSES. Wearing these cusioned pieces of plate armor make you feel like a Golem. {p1.GP}GP remaining.\n',
            typingActive)
      
    if selc == 'GORGET':
        print_slow(
            f'{p1.name} purchases the GORGET. Not the most comfortable piece of armor to wear, but it may just save your life! {p1.GP}GP remaining.\n',
            typingActive)


def sales_mechanic(p1, rooms, current_room, typingActive):
    global shop_open
    global traveling_shop
    global merchant_alive

    sale = 0
    selc = (input().upper()).strip()
    print_slow("\n", typingActive)

    if (selc == "ATK" or selc == "ATTACK") and traveling_shop == 1:
      foe = p28
      print_slow(
          f"{p1.name} assaults the Traveling Merchant! The Merchant narrowly avoids the attack before drawing his own weapon!\n",
          typingActive)
      standard_battle(p1, foe, typingActive)
      print_slow(
          f"{p1.name} slays the Merchant in cold blood. The gnome's body lays motionless on the ground. {p1.name} rummages through the Merchants wares for anything valuable that is still intact. {p1.name} finds some POTIONS, ANTIDOTES, and ETHERS. {p1.name} takes whatever they can carry; it's not like the Merchant will be needing them anymore.\n",
          typingActive)
      p1.POTS = min(p1.POTS + 3, p1.MaxPOTS)
      p1.ANT = min(p1.ANT + 2, p1.MaxANT)
      p1.ETR = min(p1.ETR + 2, p1.MaxETR)
      merchant_death()
      p1.stat_check(typingActive)
      shop_open = 0
      traveling_shop = 0
      merchant_alive = 0
      return

    if selc in shop_items or selc in shop_keyItems:

        if p1.GP < key_items[selc]['price']:
            print_slow(
                f"""{p1.name} does not have enough GP.\n""",
                typingActive)

        if p1.GP >= key_items[selc]['price']:

            if selc in shop_items:
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
                if traveling_shop == 1:
                    if selc in travelingMerchant_items:
                        sale = 5
                    else:
                        print_slow("""That item is unavailable!\n""", typingActive)
                        sale = 3
                else:
                    if selc in rooms[current_room]['items']:
                        sale = 5
                    else:
                        print_slow(f""""That item is unavailable!"\n""", typingActive)
                        sale = 3
                
                  

            if sale == 5:
                if selc in p1.inventory:
                    print_slow( 
                        f"""{p1.name} already has one in their inventory and cannot carry another!\n""", typingActive)
                    sale = 3
                else:
                    if 'classes' in key_items[selc]:
                        if p1.job in key_items[selc]['classes']:
                            sale = 4
                        else:
                            print_slow( f"""{p1.name} is unable to purchase this. (Cannot be used by {p1.job}'s.)\n""", typingActive)
                            sale = 3               
                    else:
                        sale = 4
            if sale == 4:
              if traveling_shop == 1:
                      p1.GP -= key_items[selc]['price']
                      p1.inventory.append(selc)
                      travelingMerchant_items.remove(selc)
                      key_itemBought(p1, selc, typingActive)
              else:
                  if selc == 'DRAGON SCALE' and 'CRAFTING POUCH' not in p1.inventory:
                    print_slow(f""""You'll need a CRAFTING POUCH in order to carry this item!"\n""", typingActive)
                  else:
                      p1.inventory.append(selc)
                      rooms[current_room]['items'].remove(selc)
                      p1.GP -= key_items[selc]['price']
                      key_itemBought(p1, selc, typingActive)
            if sale == 3:
                pass
            if sale == 2:
                p1.GP -= key_items[selc]['price']
                print_slow(
                    f"{p1.name} purchases a {selc}. {p1.name} has {p1.GP} GP.\n",
                    typingActive)
            if sale == 1:
                print_slow(f"""{p1.name} is unable to cary any more {selc}S. {p1.name}'s inventory is full!""",
                           typingActive)

    elif selc == "BACK":
        shop_open = 0
        traveling_shop = 0
    else:
        print_slow('\nInvalid selection. Try again.\n', typingActive)


def dwarf_sales(p1, rooms, current_room, typingActive):
  global shop_open
  selc = (input().upper()).strip()
  print_slow("\n", typingActive)
  if selc in rooms[current_room]['items']:
    if p1.GP < key_items[selc]['price']:
      print_slow(""""Stoap wasting mah time 'n' come back whin ye hae th' coin!"\n""",typingActive)
    else:
        if p1.job in key_items[selc]['classes']:
            p1.inventory.append(selc)
            p1.GP -= key_items[selc]['price']
            rooms[current_room]['items'].remove(selc)
            key_itemBought(p1, selc, typingActive)
        else:
            print_slow('\nAh kin tell ye that wont dae ye ony guid...\n', typingActive)
  elif selc == "BACK":
        shop_open = 0
  else:
      print_slow('\nInvalid selection. Try again.\n', typingActive)


def dwarf_shop(p1, rooms, current_room, typingActive):
  global shop_open
  
  shop_open = 1
  while shop_open == 1:
    print_slow(""""The finest weapons and armor in the realm!"\n """, typingActive)
    for k in rooms[current_room]['items']:
        item = k
        print_slow(f'{key_items[item]["name"]}: [{key_items[item]["price"]} GP]\n', typingActive)      
    print_slow(f"\n{p1.name}'s Wallet:[{p1.GP} GP]\n", typingActive)
    print_slow('\nType your selection or BACK to leave shopping window.\n', typingActive)
    dwarf_sales(p1, rooms, current_room, typingActive)


def dwarf_trade(p1, rooms, current_room, typingActive):
  global line4506
  while True:
    if rooms["Dwarf's Workshop"]['event2'] == 1:
      print_slow(""""Ah appreciate th' offer bit a've git plenty tae wirk wi' fur th' time bein', 'n' nothn' else tae trade wi' ye.  "\n """, typingActive)
      break
    elif rooms["Dwarf's Workshop"]['event2'] == 0:
      print_slow(""""If ye trade me 5 dragon scales ah wull gift ye yin o' mah greatest weapons. Whit dae ye say?"\n """, typingActive)
      selc = (input().upper()).strip()
      print_slow("\n", typingActive)
      if selc == 'YES':
        if p1.DragonP >= 5:
          p1.DragonP -= 5
          if p1.job == "WARRIOR":
            p1.inventory.append('AETHON')
            ultimateweapon = 'AETHON'
          if p1.job == "WIZARD" or p1.job == "WITCH":
            p1.inventory.append('FULGUR')
          if p1.job == "THIEF":
            ultimateweapon = 'FULGUR'
            p1.inventory.append('MIDAS')
            ultimateweapon = 'MIDAS'
          if p1.job == "GOD":
            p1.inventory.append('AETHON')
            p1.inventory.append('FULGUR')
            p1.inventory.append('MIDAS')
            ultimateweapon = 'ULTIMATE WEAPONS'
          rooms["Dwarf's Workshop"]['event2'] = 1
          line4506 = line4506b
          print_slow(""""Ye'v made a wise choice mukker. As promised, yin o' mah greatest wirks. Tak' stoatin care wi' it, wull ye?"\n """, typingActive)
          print_slow(f"{p1.name} receives the {ultimateweapon} from the DWARF! This weapon is of legendary quality, crafted from the greatest smith in all the realm.\n", typingActive)
          break
        if p1.DragonP < 5:
          print_slow(""""Dinnae shite mah time! Come back whin ye actually hae th' materials a'm needin'!"\n """, typingActive)
          break
      elif selc == 'NO':
        print_slow(""""Bah! Then be gaen wi' ye!"\n """, typingActive)
        break
      else:
        print_slow('\nInvalid selection. Select YES or NO.\n', typingActive)


def city_shop(p1, rooms, current_room, typingActive):
    global shop_open
    global traveling_shop
    shop_open = 1
    traveling_shop = 0

    if rooms['Shop']['event'] == 1 and p1.MonP >= 5:
        print_slow(
            """"I can tell you've got those MONSTER GUTS! Quick, pass them here before anyone else walks in!"\nThe Shop Keep frantically grabs the MONSTER GUTS and slips them into a jar tucked away under the counter.\n"Now I suppose I should hold up my end of the deal. I'll discount that SPECIAL FEED just for you." """,
            typingActive)
        p1.MonP -= 5
        rooms['Shop']['event'] = 2
        key_items['SPECIAL FEED'][
            'price'] = key_items['SPECIAL FEED']['price'] // 2

    if rooms['Farm House']['speach'] == 3 and 'SPECIAL FEED' in rooms['Shop'][
            'items'] and rooms['Shop']['event'] == 1:
        print_slow(
            'If you can find me those 5 MONSTER GUTS I will give you a big discount on that SPECIAL FEED. Just be sure not to tell anyone I want them...',
            typingActive)

    if rooms['Farm House']['speach'] == 3 and 'SPECIAL FEED' in rooms['Shop'][
            'items'] and rooms['Shop']['event'] == 0:
        print_slow(
            f"""\n"Hmm? Looking for SPECIAL FEED? We have some in the back. That will be [{key_items['SPECIAL FEED']['price']}GP]...Unless you are looking to barter? (Input selection: YES or NO)"\n""",
            typingActive)
        while True:
            selc = (input().upper()).strip()
            print_slow("\n", typingActive)
            if selc == 'YES':
                if 'CRAFTING POUCH' not in rooms['Shop']['items']:
                    print_slow(
                        """"I'll tell you what, if you can bring me 5 MONSTER GUTS I'll knock off half the price on that SPECIAL FEED. Don't worry what they're for... it's ah, for a project.\n" """,
                        typingActive)
                else:
                    print_slow(
                        """"I'll tell you what, if you can bring me 5 MONSTER GUTS I'll knock off half the price on that SPECIAL FEED. I'll even give you a CRAFTING POUCH to store those MONSTER GUTS in. It should also fit other materials. Don't worry what they're for... it's ah, for a project.\n" """,
                        typingActive)
                    p1.inventory.append('CRAFTING POUCH')
                    rooms['Shop']['items'].remove('CRAFTING POUCH')

                rooms['Shop']['event'] = 1
                break
            elif selc == 'NO':
                print_slow(
                    """"Hmm... Alright, well let me know if you change your mind next time.\n """,
                    typingActive)
                break
            else:
                print_slow('\nInvalid selection. Try YES or NO.\n',
                           typingActive)

    while shop_open == 1:
        print_slow(""""Well what will it be?"\n """, typingActive)
        for k in rooms[current_room]['items']:
            item = k
            print_slow(f'{key_items[item]["name"]}: [{key_items[item]["price"]} GP]\n', typingActive)      
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
        for k in rooms[current_room]['items']:
            item = k
            print_slow(f'{key_items[item]["name"]}: [{key_items[item]["price"]} GP]\n', typingActive)      
        print_slow(f"\n{p1.name}'s Wallet:[{p1.GP} GP]\n", typingActive)
        print_slow('\nType your selection or BACK to leave shopping window.\n', typingActive)
        sales_mechanic(p1, rooms, current_room, typingActive)


def kobold_shop(p1, rooms, current_room, typingActive):
    global shop_open
    global traveling_shop
    shop_open = 1
    traveling_shop = 0
  
    while shop_open == 1:
        print_slow(""""Many helpful things for other friend!"\n """, typingActive)
        for k in rooms[current_room]['items']:
            item = k
            print_slow(f'{key_items[item]["name"]}: [{key_items[item]["price"]} GP]\n', typingActive)      
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
        for k in travelingMerchant_items:
            item = k
            print_slow(f'{key_items[item]["name"]}: [{key_items[item]["price"]} GP]\n', typingActive)      
        print_slow(f"\n{p1.name}'s Wallet:[{p1.GP} GP]\n", typingActive)
        print_slow('\nType your selection or BACK to leave shopping window.\n', typingActive)
        sales_mechanic(p1, rooms, current_room, typingActive)

        if shop_open == 0:
            if merchant_alive == 1:
                print_slow(
                    'You bid farewell to the merchant and continue on your way.\n',
                    typingActive)
            break


def city_inn(p1, current_room, typingActive):#general inn mechanics  
    inn_room = 40

    while True:

        if p1.GP >= inn_room:
            p1.GP -= 40
            heal = random.randrange(50, 100)
            p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
            print_slow(
                f'\n{p1.name} took a well earned rest and restored HP. {p1.name} has {p1.HP}/{p1.MaxHP}HP, and {p1.GP}GP.\n',
                typingActive)
            break

        elif p1.GP < inn_room:
            print_slow(
                f'{p1.name} does not have enough GP in their wallet. {p1.name} has {p1.GP}GP.\n',
                typingActive)
            break


def smithing_upgrade(p1, current_room, typingActive):
    while True:
        s = set(mainHand_equipment)
        weapons = [x for x in p1.inventory if x in s]
        z = set(armor_equipment)
        armor = [x for x in p1.inventory if x in z]
        print_slow(
            f"""Select the weapon or armor piece you would like to UPGRADE, or type BACK to exit menu.\n""",
            typingActive)
        print_slow(f"""Weapons: {weapons}\n""", typingActive)
        print_slow(f"""Armor: {armor}\n""", typingActive)
        selc = (input().upper()).strip()
        print_slow("\n", typingActive)
        if selc in weapons:
            smithing_check(p1, selc, current_room, typingActive)
        elif selc in armor:
            smithing_check(p1, selc, current_room, typingActive)
        elif selc == "BACK":
            break
        else:
            print_slow(
                'Invalid command. Please select a weapon or armor from the lists, or type BACK to exit menu.\n',
                typingActive)


def smithing_check(p1, selc, current_room, typingActive):
    if key_items[selc]['quality'] == 'POOR':
        if key_items[selc]['gear_level'] < 3:
            smithing_increase(p1, selc, current_room, typingActive)
        else:
            print_slow(
                """"Aye, it looks lik' a've dane everything ah kin fur ye 'n' yer equipment.\n" """,
                typingActive)
    elif key_items[selc]['quality'] == 'GOOD':
        if key_items[selc]['gear_level'] < 5:
            smithing_increase(p1, selc, current_room, typingActive)
        else:
            print_slow(
                """"Aye, it looks lik' a've dane everything ah kin fur ye 'n' yer equipment.\n """,
                typingActive)
    elif key_items[selc]['quality'] == 'LEGENDARY':
        if current_room == "Smith's Workshop":
            print_slow(
                """"This is sic an incredible piece... A'm feart a'd dae it na justice. If ye kin tak' it tae mah auld master oot WAST he kin be able tae hulp. He's a streenge jimmy, bit na finer smith ye'll fin'."\n """,
                typingActive)
        elif current_room == "Dwarf's Workshop":
            if key_items[selc]['gear_level'] < 7:
                smithing_increase(p1, selc, current_room, typingActive)
            else:
                print_slow(
                    """"Aye, it looks lik' a've dane everything ah kin fur ye 'n' yer equipment.\n" """,
                    typingActive)


def smithing_increase(p1, selc, current_room, typingActive):
    while True:
        print_slow(
            f""""So you'd like to upgrade your {selc} for {key_items[selc]['upgrade']} GP?" (YES or NO.)\n""",
            typingActive)
        print_slow(f"""{p1.name}'s Wallet': {p1.GP} GP\n""", typingActive)
        selc2 = (input().upper()).strip()
        print_slow("\n", typingActive)
        if selc2 == 'YES' and p1.GP >= key_items[selc]['upgrade']:
            p1.GP -= key_items[selc]['upgrade']
            key_items[selc]['upgrade'] *= 2
            key_items[selc]['gear_level'] += 1
            if selc in mainHand_equipment:
                if selc == p1.mainHand or selc == p1.offHand:
                    p1.ATK += 1
                key_items[selc]['ATK'] += 1
            elif selc in armor_equipment:
                if selc == p1.head or selc == p1.chest or selc == p1.legs or selc == p1.offHand:
                    p1.GDEF += 1
                key_items[selc]['DEF'] += .5
            print_slow(
                f"The Smith takes back {p1.name}'s equipment and begins making improvements. After a while he returns with your improved gear.\n",
                typingActive)
            break
        elif selc2 == 'YES' and p1.GP < key_items[selc]['upgrade']:
            print_slow(
                f""""Why don't you come back when you have enough GP for that..."\n\n{p1.name} only has {p1.GP} GP in their wallet.\n""",
                typingActive)
            break
        elif selc2 == 'NO':
            break
        else:
            print_slow('Invalid command. Please select YES or NO.\n',
                       typingActive)


def cliff_examine(p1, rooms, typingActive):
    while True:
        if rooms['Cliff Side'][
                'chest'] == "CLOSED" and ('AXE' not in p1.inventory and 'SHARP AXE' not in p1.inventory):
            print_slow(line604, typingActive)
            break
        elif rooms['Cliff Side']['chest'] == "CLOSED" and ('AXE' in p1.inventory or 'SHARP AXE' in p1.inventory):
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
                    print_slow('\nInvalid selection. Try again.\n',
                               typingActive)
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
                print_slow('\nInvalid selection. Try again.\n', typingActive)
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


def waterfallcave2_examine(p1, rooms, typingActive):
    while True:
        if rooms['Waterfall Cave 2']['SOUTH'] == 'LOCKED':
            print_slow(line1316, typingActive)
            selc = input().upper().strip()
            print('\n')
            if selc == 'WEST':
                print_slow(line1317, typingActive)
                rooms['Waterfall Cave 2']['SOUTH'] = 'Waterfall Cave 3'
                rooms['Waterfall Cave 2']['map'] = waterfallcave2_map2
                rooms['Waterfall Cave 2']['EXPLORE'] = line1315b
                break
            elif selc == 'EAST':
                print_slow(line1318, typingActive)
                p1.HP = max(p1.HP - 20, 0)
                print_slow(
                    f'{p1.name} takes 20 damage from the fall. {p1.name} has {p1.HP}/{p1.MaxHP} HP.',
                    typingActive)
                player_death(p1, typingActive)
                rooms['Waterfall Cave 2']['SOUTH'] = 'Waterfall Cave 3'
                rooms['Waterfall Cave 2']['map'] = waterfallcave2_map2
                rooms['Waterfall Cave 2']['secret_path'] = 1
                rooms['Waterfall Cave 2']['EXPLORE'] = line1315b
                break
            elif selc == 'BACK':
                print_slow(line1320, typingActive)
                break
            else:
                print_slow('\nInvalid selection. Try again.\n', typingActive)
        elif rooms['Waterfall Cave 2']['SOUTH'] != 'LOCKED':
            print_slow(line1316, typingActive)
            break


def waterfallcave3_examine(p1, rooms, typingActive):
    while True:
        if 'River Serpent' in rooms['Waterfall Cave 3']['boss']:
            if 'LANTERN' not in p1.inventory:
                print_slow(line1327, typingActive)
                p1.ACC = 60
                foe = p51
                standard_battle(p1, foe, typingActive)
                rooms['Waterfall Cave 3']['boss'].remove('River Serpent')
                rooms['Waterfall Cave 3']['EXPLORE'] = line1325
                p1.ACC = 95
                p1.inventory.append('SERPENTS EYE')
                p1.inventory.append('STRANGE GREASE')
                print_slow(line1328, typingActive)
                break
            elif 'LANTERN' in p1.inventory:
                print_slow(line1327a, typingActive)
                rooms['Waterfall Cave 3']['EXPLORE'] = line1324
                rooms['Waterfall Cave 3']['event'] = 1
                #player_choice = 0
                while True:  #player_choice == 0:
                    selc = input().upper().strip()
                    print('\n')
                    if selc == 'ATTACK':
                        print_slow(line1327b, typingActive)
                        foe = p51
                        standard_battle(p1, foe, typingActive)
                        rooms['Waterfall Cave 3']['boss'].remove(
                            'River Serpent')
                        rooms['Waterfall Cave 3']['EXPLORE'] = line1326
                        p1.inventory.append('SERPENTS EYE')
                        p1.inventory.append('STRANGE GREASE')
                        print_slow(line1328, typingActive)
                        player_choice = 1
                        break
                    elif selc == 'BACK':
                        print_slow(line1327c, typingActive)
                        player_choice = 1
                        break
                    else:
                        print_slow(
                            '\nInvalid selection. Select ATTACK or BACK.\n',
                            typingActive)
        elif 'River Serpent' not in rooms['Waterfall Cave 3']['boss']:
            if 'LANTERN' not in p1.inventory:
                print_slow(line1328a, typingActive)
                break
            elif 'LANTERN' in p1.inventory:
                if rooms['Waterfall Cave 3']['event'] == 0:
                    rooms['Waterfall Cave 3']['event'] = 1
                    rooms['Waterfall Cave 3']['EXPLORE'] = line1326
                    print_slow(line1328b, typingActive)
                    print_slow(line1328c, typingActive)
                    break
                elif rooms['Waterfall Cave 3']['event'] == 1:
                    print_slow(line1328c, typingActive)
                    break
        break


def lake_examine(p1, rooms, typingActive):
    while True:
        if rooms['Echobo Lake']['EAST'] == 'LOCKED':
            if 'AXE' not in p1.inventory and 'SHARP AXE' not in p1.inventory:
                print_slow(line1404, typingActive)
                break
            elif 'AXE' in p1.inventory:
                print_slow(line1405, typingActive)
                selc = (input().upper()).strip()
                print_slow("\n", typingActive)
                if selc == 'CUT':
                    print_slow(line1409, typingActive)
                    break
                elif selc == 'LEAVE':
                    print_slow(line1407, typingActive)
                    break
                else:
                    print_slow('\nInvalid selection. Try again.\n',
                               typingActive)
            elif 'SHARP AXE' in p1.inventory:
                print_slow(line1405, typingActive)
                selc = (input().upper()).strip()
                print_slow("\n", typingActive)
                if selc == 'CUT':
                    print_slow(line1406, typingActive)
                    foe = rooms['Echobo Lake']['foe']
                    standard_battle(p1, foe, typingActive)
                    print_slow(line1408, typingActive)
                    rooms['Echobo Lake']['EAST'] = 'Mushroom Grove'
                    rooms['Echobo Lake']['EXPLORE'] = line1403
                    rooms['Echobo Lake']['map'] = lake_map2
                    p1.inventory.append('THORN BRACERS')
                    break
                elif selc == 'LEAVE':
                    print_slow(line1407, typingActive)
                    break
                else:
                    print_slow('\nInvalid selection. Try again.\n',
                               typingActive)
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
                    print_slow('\nInvalid selection. Try again.\n',
                               typingActive)


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
                print_slow(
                    f'{p1.name} has made {berriesPicked} POTIONS. {p1.name} has {p1.POTS} POTS.\n',
                    typingActive)
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


def mushroom_examine(p1, rreeseesooms, typingActive):
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
        elif "Dark Fairy Prince" in rooms['Fairy Circle']['boss'] and rooms[
                'Fairy Circle']['speach'] == 1:
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
                print_slow('You decide to leave the chests be for now.\n',
                           typingActive)
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
                print_slow('You decide to leave the chests be for now.\n',
                           typingActive)
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
                print_slow('You decide to leave the chests be for now.\n',
                           typingActive)
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
                hit = random.randrange(0, 10) + rooms['Shipwreck']['event']
                if hit >= 9:
                    print_slow(line3308, typingActive)
                    p1.GP += 300
                    p1.POTS = min(p1.POTS + 2, p1.MaxPOTS)
                    print_slow(
                        f"{p1.name} has {p1.GP} GP and {p1.POTS}/{p1.MaxPOTS} POTIONS.\n",
                        typingActive)
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
                print_slow('\nInvalid selection. Select YES or NO.',
                           typingActive)


def riverwest_examine(p1, rooms, typingActive):
    if rooms['River - West Bank']['event'] == 0:
        print_slow(line3805, typingActive)
        while True:
            selc = input().upper().strip()
            print('\n')
            if selc == 'PUSH':
                print_slow(line3806, typingActive)
                rooms['River - West Bank']['map'] = westriver_map2
                rooms['Serpent River']['map'] = river_map2
                rooms['River - West Bank']['secrets'].append('SAIL')
                rooms['Serpent River']['secrets'].append('SAIL')
                rooms['River - West Bank']['event'] = 1
                rooms['Serpent River']['EXPLORE'] = line1203
                rooms['River - West Bank']['EXPLORE'] = line3803
                break
            elif selc == 'LEAVE':
                break
            else:
                print_slow('\nInvalid selection. Select PUSH or LEAVE.\n',
                           typingActive)
    elif rooms['River - West Bank']['event'] == 1:
        print_slow(line3807, typingActive)
    elif rooms['River - West Bank']['event'] == 2:
        print_slow(line3808, typingActive)


def deepwoodsfork_examine(p1, rooms, typingActive):
    if rooms['Deep Woods - Fork']['EAST'] == 'LOCKED':
      if 'AXE' not in p1.inventory and 'SHARP AXE' not in p1.inventory:
        print_slow(line4708, typingActive)
      elif 'AXE' in p1.inventory:
        print_slow(line4709, typingActive)
        while True:
          selc = input().upper().strip()
          print('\n')
          if selc == 'CUT':
            print_slow(line4711, typingActive)
            break
          elif selc == 'LEAVE':
            print_slow(line4711d, typingActive)
            break
          else:
            print_slow('\nInvalid selection. Select CUT or LEAVE.\n', typingActive)
      elif 'SHARP AXE' in p1.inventory:
        print_slow(line4709, typingActive)
        while True:
          selc = input().upper().strip()
          print('\n')
          if selc == 'CUT':
            print_slow(line4710, typingActive)
            rooms['Deep Woods - Fork']['EAST'] = 'Deep Woods - EAST'
            rooms['Deep Woods - Fork']['map'] = deepwoodsfork_map2
            rooms['Deep Woods - Fork']['EXPLORE'] = line4707
            break
          elif selc == 'LEAVE':
            print_slow(line4711d, typingActive)
            break
          else:
            print_slow('\nInvalid selection. Select CUT or LEAVE.\n', typingActive)
    else:
        print_slow(line4711c, typingActive)


def deepwoodswest_examine(p1, rooms, typingActive):
  if rooms['Deep Woods - WEST']['NORTH'] == 'LOCKED':
      if 'AXE' not in p1.inventory and 'SHARP AXE' not in p1.inventory:
        print_slow(line4715, typingActive)
      elif 'AXE' in p1.inventory:
        print_slow(line4716, typingActive)
        while True:
          selc = input().upper().strip()
          print('\n')
          if selc == 'CUT':
            print_slow(line4717, typingActive)
            break
          elif selc == 'LEAVE':
            print_slow(line4719, typingActive)
            break
          else:
            print_slow('\nInvalid selection. Select CUT or LEAVE.\n', typingActive)
      elif 'SHARP AXE' in p1.inventory:
        print_slow(line4716, typingActive)
        while True:
          selc = input().upper().strip()
          print('\n')
          if selc == 'CUT':
            print_slow(line4718, typingActive)
            rooms['Deep Woods - WEST']['NORTH'] = 'Deep Woods - Fallen Hive'
            rooms['Deep Woods - WEST']['map'] = deepwoodswest_map2
            rooms['Deep Woods - WEST']['EXPLORE'] = line4714
            break
          elif selc == 'LEAVE':
            print_slow(line4719, typingActive)
            break
          else:
            print_slow('\nInvalid selection. Select CUT or LEAVE.\n', typingActive)
  else:
      print_slow(line4718c, typingActive)
      

def tatteredhive_examine(p1, rooms, typingActive):
    if rooms['Tattered Hive']['event'] == 0:
      print_slow(line4805, typingActive)
      foe = p74
      standard_battle(p1, foe, typingActive)
      print_slow(line4806, typingActive)
      foe = p75
      standard_battle(p1, foe, typingActive)
      print_slow(line4807, typingActive)
      p1.HP += round(p1.MaxHP // 2)
      p1.stat_check(typingActive)
      rooms['Tattered Hive']['event'] = 1
      rooms['Tattered Hive']['EXPLORE'] = line4803
      rooms['Tattered Hive']['map'] = hive2_map2
    elif rooms['Tattered Hive']['event'] == 1:
      print_slow(line4808, typingActive)
      p1.inventory.append('STRANGE JELLY')
      p1.RJ += 20
      rooms['Tattered Hive']['EXPLORE'] = line4804
      rooms['Tattered Hive']['map'] = hive2_map3
    else:
      print_slow(line4809, typingActive)


def hill_lock(p1, selc, rooms, typingActive):
    while True:
        if rooms['Rocky Hill']['SOUTH'] == 'LOCKED':
            print_slow(line812, typingActive)
            break
        else:
            continue


def lake_lock(p1, selc, rooms, typingActive):
    while True:
        if rooms['Echobo Lake']['EAST'] == 'LOCKED':
            print_slow(line1410, typingActive)
            break
        else:
            continue


def cave_lock(p1, selc, rooms, typingActive):
    while True:
        if 'Bear' in rooms['Bear Cave']['boss']:
            print_slow(line914, typingActive)
            break
        elif (selc == 'EAST' and rooms['Bear Cave']['EAST']
              == 'LOCKED') and "LANTERN" not in p1.inventory:
            print_slow(line909, typingActive)
            break
        elif (selc == 'EAST' and rooms['Bear Cave']['EAST']
              == 'LOCKED') and "LANTERN" in p1.inventory:
            print_slow(line915, typingActive)
            rooms['Bear Cave']['EAST'] = 'Rocky Cave 1'
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


def waterfallcave2_lock(p1, selc, rooms, typingActive):
    while True:
        if rooms['Waterfall Cave 2']['SOUTH'] == 'LOCKED':
            print_slow(line1319, typingActive)
            break
        else:
            continue


def deepwoodsfork_lock(p1, selc, rooms, typingActive):
    while True:
      if rooms['Deep Woods - Fork']['EAST'] == 'LOCKED':
          print_slow(line4711b, typingActive)
          break
      else:
          continue
        

def deepwoodswest_lock(p1, selc, rooms, typingActive):
    while True:
      if rooms['Deep Woods - WEST']['NORTH'] == 'LOCKED':
          print_slow(line4718b, typingActive)
          break
      else:
          continue


def cave4_boss_ambush(p1, typingActive):
    if 'Hobgoblin Gang' in rooms['Rocky Cave 4']['boss']:
        print_slow(line935, typingActive)
        foe = rooms['Rocky Cave 4']['foe']
        standard_battle(p1, foe, typingActive)
        p1.inventory.append('GOBLIN CHOPPER')
        rooms['Rocky Cave 4']['boss'].remove('Hobgoblin Gang')
        rooms['Rocky Cave 4']['spawn_rate'] = 4
        print_slow(line936, typingActive)


def cave5_boss_ambush(p1, typingActive):
    if 'Goblin Queen' in rooms["Queen's Chamber"]['boss']:
        print_slow(line947, typingActive)
        foe = rooms["Queen's Chamber"]['foe']
        standard_battle(p1, foe, typingActive)
        rooms["Queen's Chamber"]['boss'].remove('Goblin Queen')
        rooms['Pinerift Forest - EAST']['event'] = 1
        p1.inventory.append('DRAGON BONE KEY')
        print_slow(line949, typingActive)
        if rooms["Smith's Workshop"]['event'] == 1:
          p1.inventory.append('GOBLIN FINGER')
          print_slow(line951, typingActive)


def foresteast_ambush(p1, typingActive):
    if rooms['Pinerift Forest - EAST']['event'] == 1:
        ambush = random.randrange(0, 10)
        if ambush >= 7:
            foe = p67
            print_slow(line707, typingActive)
            standard_battle(p1, foe, typingActive)
            print_slow(line708, typingActive)
            rooms['Pinerift Forest - EAST']['event'] = 2
            rooms['Pinerift Forest - EAST']['EXPLORE'] = line706
            rooms['Pinerift Forest']['EXPLORE'] = line703


def hive_boss_ambush(p1, typingActive):
    global enemy_spawn3
    global enemy_spawn9
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
        p1.RJ += 10
        print_slow(line2103, typingActive)


def faeeast_ambush(p1, typingActive):
    global stolen_gp

    if 'Rouge Gang' in rooms['Fae Woods - EAST']['boss']:
        print_slow(line3903, typingActive)
        while True:
            selc = input().upper().strip()
            print('\n')
            if selc == "FIGHT":
                print_slow(line3905, typingActive)
                foe = p52
                standard_battle(p1, foe, typingActive)
                rooms['Fae Woods - EAST']['boss'].remove('Rouge Gang')
                rooms['Fae Woods - Camp']['boss'].remove('Rouge Gang')
                p1.GP += 250
                print_slow(line3906, typingActive)
                print_slow(
                    f'{p1.name} adds the 250 GP to their wallet. {p1.name} has {p1.GP} GP.\n',
                    typingActive)
                break
            elif selc == "GIVE":
                print_slow(line3904, typingActive)
                rooms['Fae Woods - EAST']['boss'].remove('Rouge Gang')
                stolen_gp = p1.GP
                p1.GP -= p1.GP
                print_slow(
                    f'{p1.name} gives up all their gold. {p1.name} has {p1.GP} GP.',
                    typingActive)
                break
            else:
                print_slow('\nInvalid selection. Select GIVE or FIGHT.\n',
                           typingActive)


def faecamp_ambush(p1, typingActive):
    global stolen_gp

    if 'Rouge Gang' in rooms['Fae Woods - Camp']['boss']:
        print_slow(line4005, typingActive)
        foe = p52
        standard_battle(p1, foe, typingActive)
        rooms['Fae Woods - Camp']['boss'].remove('Rouge Gang')
        p1.GP += stolen_gp
        print_slow(line4006, typingActive)
        print_slow(
            f'{p1.name} adds their GP back to their wallet. {p1.name} has {p1.GP} GP.\n',
            typingActive)


def dragon_ambush(p1, typingActive):
  if "Dragon King, Tanninim" in rooms['Drake Mountains Summit']['boss']:
      print_slow(line4615, typingActive)
      foe = p73
      standard_battle(p1, foe, typingActive)
      rooms['Drake Mountains Summit']['boss'].remove("Dragon King, Tanninim")
      rooms['Drake Mountains Summit']['intro'] = line4613
      rooms['Drake Mountains 3']['EXPLORE'] = line4607b
      p1.inventory.append('DRAGON HEART')
      print_slow(line4616, typingActive)
      print_slow(
          f'{p1.name} adds the DRAGON HEART to their inventory!\n',
          typingActive)


def castle_speak(p1, rooms, typingActive):
    while True:
        if rooms['Royal Castle']['speach'] == 0:
            print_slow(line505, typingActive)
            print_slow(line506, typingActive)
            rooms['Royal Castle']['speach'] += 1
            break
        elif 'HEROS MEDAL' in p1.inventory and rooms['Royal Castle'][
                'event'] == 0:
            print_slow(line505, typingActive)
            print_slow(line508, typingActive)
            p1.MaxHP += 10
            p1.HP = p1.MaxHP
            p1.stat_check(typingActive)
            rooms['Royal Castle']['event'] = 1
            key_items['HEROS MEDAL'][
                'description'] = 'A gold medal found on a corpse covered in mushrooms. Engraved with the royal crest on the front; the back reads "For Jeremy the Goblin-Slayer". The Princess graciously unlocked its magic potential for you!.\n'
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
                print_slow(
                    f'{p1.name} was given a BUCKLER! This sturdy steel shield should help block damage.\n',
                    typingActive)
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
        elif rooms['Boat House'][
                'speach'] == 1 and 'SALMON' not in p1.inventory:
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
        elif rooms['Mystic Shrine'][
                'speach'] == 1 and 'PENDANT' in p1.inventory:
            print_slow(line1108, typingActive)
            print_slow(line1109, typingActive)
            print_slow(
                f"{p1.name} is given the FRIAR's MESSER. This single edge sword is finely crafted. Much better than the rusty old blade you found in the trash before you started adventuring... {p1.name} gained 5 ATK\n",
                typingActive)
            rooms['Mystic Shrine']['EXPLORE'] = line1104
            p1.inventory.remove('PENDANT')
            p1.inventory.append('MESSER')
            p1.stat_check(typingActive)
            break
        elif rooms['Mystic Shrine']['speach'] == 1:
            print_slow(line1107, typingActive)
            break


def smith_speak(p1, rooms, typingActive):
    if 'AXE' in p1.inventory and rooms["Smith's Workshop"]['event'] == 0:
      print_slow(line1906, typingActive)
      rooms["Smith's Workshop"]['event'] = 1
      if 'Goblin Queen' not in rooms["Queen's Chamber"]['boss']:
        print_slow(line1907b, typingActive)
        rooms["Smith's Workshop"]['event'] = 2
        p1.inventory.remove('AXE')
        p1.inventory.append('SHARP AXE')
    elif 'GOBLIN FINGER' not in p1.inventory and rooms["Smith's Workshop"]['event'] == 1:
      print_slow(line1906b, typingActive)
    elif 'GOBLIN FINGER' in p1.inventory and rooms["Smith's Workshop"]['event'] == 1:
      print_slow(line1907, typingActive)
      rooms["Smith's Workshop"]['event'] = 2
      p1.inventory.remove('GOBLIN FINGER')
      p1.inventory.remove('AXE')
      p1.inventory.append('SHARP AXE')
    elif 'STRANGE GREASE' in p1.inventory:
        print_slow(line1905, typingActive)
    else:
        print_slow(line1904, typingActive)


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
                print_slow(
                    f'{p1.name} was given a 100GP. The Farmer expects you to use his money to buy his pig some special feed from the City\n',
                    typingActive)
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
                print_slow(
                    '\nInvalid selection. Try again. Please select YES or NO\n',
                    typingActive)
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
                print_slow(line2206, typingActive)
                break
            else:
                print_slow(line2207, typingActive)
                break
        elif rooms['Farm House']['speach'] == 4:
            print_slow(line2208, typingActive)
            break


def witch_speak(p1, rooms, typingActive):
    while True:
        if rooms["Witch's Cabin"]['speach'] == 0:
            print_slow(line2403, typingActive)
            rooms["Witch's Cabin"]['speach'] = 1
            rooms["Witch's Cabin"]['crafting'] = 'ACTIVE'
            break
        if rooms["Witch's Cabin"]['speach'] == 1:
            print_slow(line2404, typingActive)
            break


def fairy_speak(p1, rooms, typingActive):
    while True:
        if rooms['Fairy Circle']['speach'] == 0:
            print_slow('\nInvalid selection. Try again.', typingActive)
            break
        elif rooms['Fairy Circle']['speach'] == 1:
            if p1.faeCount < rooms['Fairy Circle']['fairy_reward']:
                print_slow(
                    f""""Hello, thank you for returning. I appreciate all of your assistance. If you can return after defeating {rooms['Fairy Circle']['fairy_reward'] - p1.faeCount} more Dark Fae I should regain enough strength to reward you."\n """,
                    typingActive)
                break
            elif p1.faeCount >= rooms['Fairy Circle']['fairy_reward']:
                if rooms['Fairy Circle']['fairy_reward'] == 5:
                    print_slow(line2909, typingActive)
                    p1.GP += 100
                    print_slow(
                        f'{p1.name} is given 100 GP! {p1.name} has {p1.GP} GP in their wallet.',
                        typingActive)
                    rooms['Fairy Circle']['fairy_reward'] = 10
                    break
                if rooms['Fairy Circle']['fairy_reward'] == 10:
                    print_slow(line2910, typingActive)
                    p1.ETR = min(p1.ETR + 3, p1.MaxETR)
                    print_slow(
                        f'{p1.name} is given 3 ETHERS! {p1.name} has {p1.ETR}/{p1.MaxETR} ETHERS in their bag.',
                        typingActive)
                    rooms['Fairy Circle']['fairy_reward'] = 20
                    break
                if rooms['Fairy Circle']['fairy_reward'] == 20:
                    print_slow(line2911, typingActive)
                    foe = rooms['Fairy Circle']['foe']
                    standard_battle(p1, foe, typingActive)
                    print_slow(line2912, typingActive)
                    p1.inventory.append('CRYSTAL NECKLACE')
                    p1.MP = p1.MaxMP
                    rooms['Fairy Circle']['boss'].remove('Dark Fairy Prince')
                    rooms['Fairy Circle']['speach'] = 2
                    rooms['Fairy Circle']['EXPLORE'] = line2904
                    rooms['Fairy Circle']['map'] = fairy_map2
                    break
        elif rooms['Fairy Circle']['speach'] == 2:
            print_slow(
                'You try talking to the Dark Fairy Prince, but remember you killed him. Oh well. He was kind of a jerk.',
                typingActive)
            break


def marsh_speak(p1, rooms, typingActive):
    while True:
        if rooms["Frog Marsh"]['speach'] == 0:
            print_slow(line2803, typingActive)
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
            print_slow(line2806, typingActive)
            rooms["Frog Marsh"]['speach'] = 2
            break
        elif rooms["Frog Marsh"]['speach'] == 2:
            print_slow(line2804, typingActive)
            rooms["Frog Marsh"]['crafting'] = 'ACTIVE'
            rooms["Frog Marsh"]['speach'] = 3
            break
        elif rooms["Frog Marsh"]['speach'] == 3:
            print_slow(line2805, typingActive)
            break


def alchemist_speak(p1, rooms, typingActive):
    while True:
        if rooms["Alchemist Shop"]['speach'] == 0:
            print_slow(line3603, typingActive)
            rooms["Alchemist Shop"]['crafting'] = 'ACTIVE'
            rooms["Alchemist Shop"]['speach'] = 1
            break
        elif rooms["Alchemist Shop"]['speach'] == 1:
            print_slow(line3604, typingActive)
            break


def harbortemple_speak(p1, rooms, typingActive):
  if rooms['Harbor Temple']['speach'] == 0:
    print_slow(line3405, typingActive)
    rooms['Harbor Temple']['speach'] = 1
  elif rooms['Harbor Temple']['speach'] == 1:
    print_slow(line3406, typingActive)
    rooms['Harbor Temple']['speach'] = 2
  elif rooms['Harbor Temple']['speach'] == 2:
    print_slow(line3407, typingActive)
    

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
                    rooms['Waterfall Pool']['SOUTH'] = 'Waterfall Cave 1'
                    rooms['Waterfall Pool']['map'] = waterfall_map2
                    choice = 0
                    break
                elif selc == "NO":
                    print_slow(line3505, typingActive)
                    rooms['Docked Ship']['event'] = 1
                    choice = 0
                    break
                else:
                    print_slow('\nInvalid selection. Select YES or NO.\n',
                               typingActive)
            rooms['Docked Ship']['intro'] = line3501b
            break
        elif rooms['Docked Ship'][
                'speach'] == 1 and 'SERPENTS EYE' not in p1.inventory:
            print_slow(line3506, typingActive)
            break
        elif rooms['Docked Ship'][
                'speach'] == 1 and 'SERPENTS EYE' in p1.inventory:
            print_slow(line3507, typingActive)
            p1.inventory.remove('SERPENTS EYE')
            p1.GP += 500
            print_slow(
                f"{p1.name} received a small treasure chest filled with gold coins worth 500 GP! {p1.name} has {p1.GP} GP in their wallet.",
                typingActive)
            rooms['Docked Ship']['speach'] = 2
            break
        elif rooms['Docked Ship']['speach'] == 2:
            print_slow(line3508, typingActive)
            break


def dwarf_speak(p1, rooms, typingActive):
    global line4506
  
    if rooms["Dwarf's Workshop"]['speach'] == 0:
        print_slow(line4505, typingActive)
        rooms["Dwarf's Workshop"]['intro'] = line4502
        rooms["Dwarf's Workshop"]['EXPLORE'] = line4504
        rooms["Dwarf's Workshop"]['UPGRADE'] = smithing_upgrade
        rooms["Dwarf's Workshop"]['BUY'] = dwarf_shop
        rooms["Dwarf's Workshop"]['TRADE'] = dwarf_trade
        rooms["Dwarf's Workshop"]['speach'] = 1
    elif rooms["Dwarf's Workshop"]['event'] == 1:
        print_slow(line4510, typingActive)
        while True:
            selc = input().upper().strip()
            print('\n')
            if selc == 'YES':
                print_slow(line4508, typingActive)
                p1.inventory.append('MAGIC CIRCLET')
                print_slow(f'{p1.name} gave some of the extra MAGIC GREASE to the Dwarf and added the MAGIC CIRCLET to their inventory.', typingActive)
                break
            elif selc == 'NO':
                print_slow(line4509, typingActive)
                rooms["Dwarf's Workshop"]['event'] = 1
                break
            else:
                print_slow('\nInvalid command. Type YES or NO.\n',
                           typingActive)
    elif rooms["Dwarf's Workshop"][
            'speach'] == 1 and 'STRANGE GREASE' not in p1.inventory:
        print_slow(line4506, typingActive)
    elif rooms["Dwarf's Workshop"][
            'speach'] == 1 and 'STRANGE GREASE' in p1.inventory:
        print_slow(line4507, typingActive)
        p1.inventory.remove('STRANGE GREASE')
        p1.inventory.append('MAGIC GREASE')
        while True:
            selc = input().upper().strip()
            print('\n')
            if selc == 'YES':
                print_slow(line4508, typingActive)
                p1.inventory.append('MAGIC CIRCLET')
                print_slow(f'{p1.name} gave some of the extra MAGIC GREASE to the Dwarf and added the MAGIC CIRCLET to their inventory.', typingActive)
                break
            elif selc == 'NO':
                print_slow(line4509, typingActive)
                rooms["Dwarf's Workshop"]['event'] = 1
                break
            else:
                print_slow('\nInvalid command. Type YES or NO.\n',
                           typingActive)


def kobold_speak(p1, rooms, typingActive):
    if rooms['Deep Woods - Forest Hut']['speach'] == 0:
        print_slow(line4728, typingActive)
        rooms['Deep Woods - Forest Hut']['speach'] = 1
    elif rooms['Deep Woods - Forest Hut']['speach'] == 1:
        print_slow(line4729, typingActive)
        rooms['Deep Woods - Forest Hut']['speach'] = 2
    elif rooms['Deep Woods - Forest Hut']['speach'] == 2:
        print_slow(line4730, typingActive)
        rooms['Deep Woods - Forest Hut']['intro'] = line4723
        rooms['Deep Woods - Forest Hut']['EXPLORE'] = line4726
        rooms['Deep Woods - Forest Hut']['speach'] = 3
        rooms['Deep Woods - Forest Hut']['secrets'].append('SEARCH')
        rooms['Deep Woods - Forest Hut']['event'] = 1
    elif rooms['Deep Woods - Forest Hut']['speach'] == 3 and 'PAINTED SNAIL' in p1.inventory:
        print_slow(line4733, typingActive)
        p1.inventory.remove("PAINTED SNAIL")
        if "SLEEPY SQUIRELL" in p1.inventory:
            p1.inventory.remove("SLEEPY SQUIRELL")
        if "WET TOAD" in p1.inventory:
            p1.inventory.remove("WET TOAD")
        rooms['Deep Woods - Forest Hut']['intro'] = line4724
        rooms['Deep Woods - Forest Hut']['EXPLORE'] = line4727
        rooms['Deep Woods - Forest Hut']['BUY'] = kobold_shop
        rooms['Deep Woods - Forest Hut']['speach'] = 4
        rooms['Deep Woods - Forest Hut']['event'] = 2
    elif rooms['Deep Woods - Forest Hut']['speach'] == 3 and ("WET TOAD" or "SLEEPY SQUIRELL") in p1.inventory:
        print_slow(line4732, typingActive)
        while True:
            if "SLEEPY SQUIRELL" in p1.inventory:
                p1.inventory.remove("SLEEPY SQUIRELL")
                break
            elif "WET TOAD" in p1.inventory:
                p1.inventory.remove("WET TOAD")
                break
    elif rooms['Deep Woods - Forest Hut']['speach'] == 3 and any(x in rooms['Deep Woods - Forest Hut']['items2'] for x in p1.inventory) == False:
        print_slow(line4731, typingActive)
    elif rooms['Deep Woods - Forest Hut']['speach'] == 4:
        print_slow(line4734, typingActive)
        


def farm_crafting(p1, typingActive):
    while True:
        print_slow(
            "Would you like to craft an ANTIDOTE using 5 PLANT PARTS? YES or NO.\n",
            typingActive)
        selc = (input().upper()).strip()
        if (selc == "YES" and p1.PlantP >= 5) and p1.ANT != p1.MaxANT:
            p1.PlantP -= 5
            p1.ANT = min(p1.ANT + 1, p1.MaxANT)
            print_slow(
                """"Here you go! One healing salve coming right up.\n" """,
                typingActive)
            print_slow(f'{p1.name} now has {p1.ANT} ANTIDOTES\n', typingActive)
        elif selc == "YES" and p1.ANT == p1.MaxANT:
            print_slow(
                f"Unable to craft more ANTIDOTES; {p1.name}'s inventory is full.\n",
                typingActive)
        elif selc == "YES" and p1.PlantP < 5:
            print_slow(
                f'{p1.name} does not have enough PLANT PARTS. {p1.name} only has {p1.PlantP} PLANT PARTS\n',
                typingActive)
        elif selc == "NO":
            break
        else:
            print_slow(
                '\nInvalid selection. Try again. Please select YES or NO\n')


def witch_crafting(p1, typingActive):
    while True:
        print_slow(
            "Would you like to craft an ETHER using 10 FAE DUST? YES or NO.\n",
            typingActive)
        selc = (input().upper()).strip()
        print_slow('\n', typingActive)
        if (selc == "YES" and p1.FaeP >= 10) and p1.ETR != p1.MaxETR:
            p1.FaeP -= 10
            p1.ETR = min(p1.ETR + 1, p1.MaxETR)
            print_slow(""""Hehehe! One freshly concocted ETHER for you.\n" """,
                       typingActive)
            print_slow(f'{p1.name} now has {p1.ETR} ETHER\n', typingActive)
        elif selc == "YES" and p1.ETR == p1.MaxETR:
            print_slow(
                f"Unable to craft more ETHERS; {p1.name}'s inventory is full.\n",
                typingActive)
        elif selc == "YES" and p1.FaeP < 10:
            print_slow(
                f'{p1.name} does not have enough FAE DUST. {p1.name} only has {p1.FaeP} FAE DUST\n',
                typingActive)
        elif selc == "NO":
            break
        else:
            print_slow(
                '\nInvalid selection. Try again. Please select YES or NO\n')


def marsh_crafting(p1, typingActive):
    while True:
        print_slow(
            "Would you like to craft a SMOKE BOMB using 15 MONSTER PARTS? YES or NO.\n",
            typingActive)
        selc = (input().upper()).strip()
        print_slow('\n', typingActive)
        if (selc == "YES" and p1.MonP >= 15) and p1.SMB != p1.MaxSMB:
            p1.MonP -= 15
            p1.SMB = min(p1.SMB + 1, p1.MaxSMB)
            print_slow(
                """"Oh grandpappy would be proud of this one! Hope you get some good use out of this SMOKE BOMB.\n" """,
                typingActive)
            print_slow(f'{p1.name} now has {p1.ETR} SMOKE BOMBS\n',
                       typingActive)
        elif selc == "YES" and p1.SMB == p1.MaxSMB:
            print_slow(
                f"Unable to craft more SMOKE BOMBS; {p1.name}'s inventory is full.\n",
                typingActive)
        elif selc == "YES" and p1.MonP < 15:
            print_slow(
                f'{p1.name} does not have enough MONSTER PARTS. {p1.name} only has {p1.MonP} MONSTER PARTS\n',
                typingActive)
        elif selc == "NO":
            break
        else:
            print_slow(
                '\nInvalid selection. Try again. Please select YES or NO\n')


def alchemist_crafting(p1, typingActive):
    while True:
        print_slow(line3605, typingActive)
        selc = input().upper().strip()
        print('\n')
        if selc == 'SMOKE BOMB':
            if p1.MonP >= 10 and p1.SMB < p1.MaxSMB:
                p1.MonP -= 10
                p1.SMB += 1
                print_slow(line3606, typingActive)
                print_slow(
                    f"{p1.name} has received a SMOKE BOMB from the Alchemist! {p1.name} has {p1.SMB}/{p1.MaxSMB} SMOKE BOMBS and {p1.MonP} MONSTER PARTS remaining.\n",
                    typingActive)
            elif p1.MonP < 10:
                print_slow(
                    f"{p1.name} does not have enough MONSTER PARTS. {p1.name} only has and {p1.MonP}/10 MONSTER PARTS required\n",
                    typingActive)
            elif p1.SMB == p1.MaxSMB:
                print_slow(
                    f"Unable to craft more SMOKE BOMBS; {p1.name}'s inventory is full.\n",
                    typingActive)
        elif selc == 'POTION':
            if p1.RareP >= 5 and p1.POTS < p1.MaxPOTS:
                p1.RareP -= 5
                p1.POTS += 1
                print_slow(line3606, typingActive)
                print_slow(
                    f"{p1.name} has received a POTION from the Alchemist! {p1.name} has {p1.POTS}/{p1.MaxPOTS} POTIONS and {p1.RareP} RARE MONSTER PARTS remaining.\n",
                    typingActive)
            elif p1.RareP < 5:
                print_slow(
                    f"{p1.name} does not have enough RARE MONSTER PARTS. {p1.name} only has and {p1.RareP}/5 RARE MONSTER PARTS required\n",
                    typingActive)
            elif p1.POTS == p1.MaxPOTS:
                print_slow(
                    f"Unable to craft more POTIONS; {p1.name}'s inventory is full.\n",
                    typingActive)
        elif selc == 'BACK':
            print_slow(""""Come back with more ingredients soon!"\n """,
                       typingActive)
            break
        else:
            print_slow(
                '\nInvalid selection. Select SMOKE BOMB, POTION, or BACK.\n',
                typingActive)


def cliff_special(p1, selc, typingActive):
    print_slow(line610, typingActive)
    damage = 69
    p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
    player_death(p1, typingActive)
    if p1.HP > 0:
        rooms['Cliff Side']['secret_path'] = 1
        print_slow(line611, typingActive)
    return


def cave4_special(p1, selc, typingActive):
    print_slow(line946, typingActive)
    p1.HP = 0
    player_death(p1, typingActive)
    return


def berry_special(p1, selc, typingActive):
    if rooms['Berry Patch']['chest'] == "OPEN":
        if selc == 'WAIT':
            print_slow(
                f"{p1.name} waits for the REZZBERRIES to regrow. In that year SMELDAR's forces have conquered the kingdom. What do you think was going to happen?",
                typingActive)
            p1.HP = 0
            player_death(p1, typingActive)
        if selc == 'PICK':
            print_slow(line1006, typingActive)
    else:
        print_slow('\nInvalid selection. Try again.', typingActive)
    return


def river_special(p1, selc, typingActive):
    if selc != 'SAIL':
        print_slow(line1207, typingActive)
        p1.HP = 0
        player_death(p1, typingActive)
        return
    elif selc == 'SAIL':
        if rooms['Serpent River']['event'] == 1:
            rooms['River - West Bank']['map'] = westriver_map2
            rooms['River - West Bank']['event'] = 1
            rooms['River - West Bank']['EXPLORE'] = line3803
            rooms['Serpent River']['map'] = river_map2
            rooms['Serpent River']['secret_path'] = 1
            rooms['Serpent River']['event'] = 2
            rooms['Serpent River']['EXPLORE'] = line1203
            print_slow(
                f'{p1.name} hops on the raft and begins sailing across the river!\n',
                typingActive)
        elif rooms['Serpent River']['event'] == 2:
            print_slow(
                f'{p1.name} is unable to SAIL across - the raft is on the wrong side of the river for that.\n',
                typingActive)


def lake_special(p1, selc, typingActive):
    print_slow(line1414, typingActive)
    p1.HP = 0
    player_death(p1, selc, typingActive)
    return


def swamp_special(p1, selc, typingActive):
    if selc == 'DRINK':
        print_slow(line2721, typingActive)
        p1.POISON += 3
        p1.HP -= 5
        if p1.HP <= 0:
            player_death(p1, typingActive)
        else:
            print_slow(
                f'{p1.name} takes 5 damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n',
                typingActive)
    elif selc == 'SWIM' or selc == 'DIVE':
        print_slow(line2722, typingActive)
        p1.HP = 0
        player_death(p1, typingActive)


def swamp7_special(p1, selc, typingActive):
    if selc in song_term and rooms['Rotten Swamp 7']['event'] == 1:
        print_slow(line2726, typingActive)
    elif selc in song_term and rooms['Rotten Swamp 7']['event'] == 0:
        print_slow(line2725, typingActive)
        p1.inventory.append('GOLD RING')
        print_slow(
            f'{p1.name} recieved a GOLD RING! {p1.name} feels their fortune improving with the ring in hand.\n',
            typingActive)
        rooms['Rotten Swamp 7']['event'] = 1
    else:
        swamp_special(p1, selc, typingActive)


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
                rooms['Rotten Swamp 8']['EAST'] = 'Western Lake'
                rooms['Rotten Swamp 8']['map'] = swamp8_map2
            if selc == 'KEEP':
                print_slow(line2736, typingActive)
                foe = rooms['Rotten Swamp 8']['foe']
                standard_battle(p1, foe, typingActive)
                p1.inventory.append('GILDED DRAGON BONE KEY')
                rooms['Rotten Swamp 8']['event'] = 1
                rooms['Rotten Swamp 8']['EAST'] = 'Western Lake'
                rooms['Rotten Swamp 8']['map'] = swamp8_map2
                print_slow(line2738, typingActive)
            else:
                print_slow('\nInvalid selection. Try again.', typingActive)
        elif 'WAFFLE' not in p1.inventory:
            print_slow(line2732, typingActive)
            foe = rooms['Rotten Swamp 8']['foe']
            standard_battle(p1, foe, typingActive)
            p1.inventory.append('GILDED DRAGON BONE KEY')
            rooms['Rotten Swamp 8']['event'] = 1
            rooms['Rotten Swamp 8']['EAST'] = 'Western Lake'
            rooms['Rotten Swamp 8']['map'] = swamp8_map2
            print_slow(line2738, typingActive)
    else:
        swamp_special(p1, selc, typingActive)


def riverwest_special(p1, selc, typingActive):
    if rooms['River - West Bank']['event'] == 1:
        rooms['River - West Bank']['map'] = westriver_map3
        rooms['River - West Bank']['secret_path'] = 1
        rooms['River - West Bank']['event'] = 2
        rooms['River - West Bank']['EXPLORE'] = line3804
        rooms['Serpent River']['map'] = river_map3
        rooms['Serpent River']['event'] = 1
        rooms['Serpent River']['EXPLORE'] = line1204
        print_slow(
            f'{p1.name} hops on the raft and begins sailing across the river\n',
            typingActive)
    elif rooms['River - West Bank']['event'] == 2:
        print_slow(
            f'{p1.name} is unable to SAIL across - the raft is on the wrong side of the river for that.\n',
            typingActive)


def crescent_special(p1, selc, typingActive):
    if 'Naga' in rooms['Crescent Pond']['boss']:
        print_slow(f"""You take your {p1.mainHand} and throw it into the pool. The water begins to foam and a women clad in flowing white robes raises from the depths of the pond. In her hands she holds a blade of pure silver\n\n"Hello dear traveler. It seems you may have lost something in the waters... I have retreived it for you. This is your SILVER SWORD, correct?\n" """, typingActive)
        previous_gear = p1.mainHand
        p1.mainHand = 'EMPTY'
        selc = 'EMPTY'
        equip_stat_update(p1, selc, previous_gear)
        while True:
            selc = input().upper().strip()
            print('\n')
            if selc == "YES":
                print_slow(line4106, typingActive)
                foe = p53
                standard_battle(p1, foe, typingActive)
                print_slow(f"""The defeated Naga writhes in agony on the ground before its gut burst open, the {p1.mainHand} falling to the ground. You wipe off the Naga's innards from the {p1.mainHand} and notice that it seems more polished than before.""", typingActive)
                rooms['Crescent Pond']['EXPLORE'] = line4104
                rooms['Crescent Pond']['boss'].remove('Naga')
                key_items[previous_gear]['ATK'] += 3
                p1.mainHand = previous_gear 
                previous_gear = 'EMPTY'
                selc = 'EMPTY'
                equip_stat_update(p1, selc, previous_gear)
                p1.stat_check(typingActive)
                break
            elif selc == "NO":
                print_slow(line4107, typingActive)
                while True:
                    selc = input().upper().strip()
                    print('\n')
                    if selc == "YES":
                        print_slow(line4106, typingActive)
                        foe = p53
                        standard_battle(p1, foe, typingActive)
                        print_slow(f"""The defeated Naga writhes in agony on the ground before its gut burst open, the {p1.mainHand} falling to the ground. You wipe off the Naga's innards from the {p1.mainHand} and notice that it seems more polished than before.""", typingActive)
                        rooms['Crescent Pond']['EXPLORE'] = line4104
                        rooms['Crescent Pond']['boss'].remove('Naga')
                        key_items[previous_gear]['ATK'] += 3
                        p1.stat_check(typingActive)
                        break
                    elif selc == "NO":
                        print_slow(f"""The women submerges herself in the pond once more this time pulling out the {p1.mainHand} you threw into the water.\n\n"This must be your weapon then. It does not befit one as noble as you though. I will take this from you and in exchange I will grant you the ADAMANTITE SWORD. No blade is sharper or more durable. May it serve you well..."\n\n The woman pulls the ADAMANTITE SWORD from her robes and places the blade at your feet. You draw your new weapon and admire its immaculate craftsmanship before returning it to its scabbard. When you look back up the woman is already gone...\n """, typingActive)
                        rooms['Crescent Pond']['EXPLORE'] = line4103
                        rooms['Crescent Pond']['boss'].remove('Naga')
                        p1.inventory.remove(previous_gear)
                        p1.inventory.append('ADAMANTITE SWORD')
                        previous_gear = p1.mainHand
                        p1.mainHand = 'ADAMANTITE SWORD'
                        selc = 'ADAMANTITE SWORD'
                        equip_stat_update(p1, selc, previous_gear)
                        p1.stat_check(typingActive)
                        break
                    else:
                        print_slow('\nInvalid selection. Select YES or NO.\n',
                                   typingActive)
                break
            else:
                print_slow('\nInvalid selection. Select YES or NO.\n',
                           typingActive)
    else:
        print_slow('\nInvalid selection. Try again.\n', typingActive)


def drake_special(p1, selc, typingActive):
  if rooms['Drake Mountains 3']['event'] == 0:
    rooms['Drake Mountains 3']['SOUTH'] = 'Drake Mountains Summit'
    rooms['Drake Mountains 3']['EXPLORE'] = line4607
    rooms['Drake Mountains 3']['event'] = 1
    print_slow(line4607c, typingActive)
  else: 
    print_slow('You speak the name "TANNINIM" once more, but nothing else seems to happen...', typingActive)


def kobold_special(p1, selc, typingActive):
    if rooms['Deep Woods - Forest Hut']['event'] == 1:
        hit = random.randrange(0,11)
        investigate = rooms['Deep Woods - Forest Hut']['event2'] + hit
        if investigate >=7:
            if bool(rooms['Deep Woods - Forest Hut']['items2']):
              friend = random.choice(rooms['Deep Woods - Forest Hut']['items2'])
              if friend == "PAINTED SNAIL":
                  p1.inventory.append("PAINTED SNAIL")
                  rooms['Deep Woods - Forest Hut']['items2'].remove("PAINTED SNAIL")
                  print_slow(line4735, typingActive)
              if friend == "SLEEPY SQUIRELL":
                  p1.inventory.append("SLEEPY SQUIRELL")
                  rooms['Deep Woods - Forest Hut']['items2'].remove("SLEEPY SQUIRELL")
                  print_slow(line4736, typingActive)
              if friend == "WET TOAD":
                  p1.inventory.append("WET TOAD")
                  rooms['Deep Woods - Forest Hut']['items2'].remove("WET TOAD")
                  print_slow(line4737, typingActive)
              print_slow(f"{p1.name} picks up the {friend} and carefully places it in their bag.\n", typingActive)
            else:
              print_slow(f"You search around the area, but turn up nothing.\n", typingActive)
        if 2 < investigate < 7:
          foe = random.choice(enemy_spawn26)
          print_slow(f"You search around the area, and soon hear a rustling come from the woods. Suddenly a {foe.name} rushes to attack you! You draw your weapon and defend yourself against the ambush!\n", typingActive)
          standard_battle(p1, foe, typingActive)
          rooms['Deep Woods - Forest Hut']['event2'] += 1
        if investigate <= 2:
          foe = random.choice(enemy_spawn27)
          print_slow(f"You search around the area, and soon hear crashing come from the woods. Suddenly a {foe.name} emerges and sets its sights on you! You draw your weapon and defend yourself against the ambush!\n", typingActive)
          standard_battle(p1, foe, typingActive)
          rooms['Deep Woods - Forest Hut']['event2'] += 2
    if rooms['Deep Woods - Forest Hut']['event'] == 2:
        print_slow(line4738, typingActive)
            
            

rooms = {
    '': {
        'name': '',
        'intro': None,
        'map': None,
        'discovered': [],
        'NORTH': None,
        'EAST': None,
        'SOUTH': None,
        'WEST': None,
        'SECRET_ROUTE': None,
        'EXPLORE': None,
        'EXAMINE': None,
        'SPEAK': None,
        'REST': None,
        'PRAY': 'pray',
        'BUY': "BUY",
        'CRAFT': 'craft',
        'speach': None,
        'crafting': None,
        'secrets': [],
        'secret_path': 0,
        'special': None,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'boss': [],
        'boss_ambush': None,
        'items': [],
        'foe': None,
        'LOCK': None,
        'chest': None,
        'event': None,
    },
    'TESTING GROUND': {
        'name': 'TESTING GROUND',
        'intro': "How'd you end up here?",
        'map': blank_map1,
        'discovered': [],
        'NORTH': 'Harbor Markets',
        'EAST': 'River - West Bank',
        'SOUTH': 'Berry Patch',
        'WEST': 'Camp Site',
        'EXPLORE': 'Nothing to see here....',
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
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawnT,
        #'boss' : [],
        #'boss_ambush' : None,
        #'foe' : None,
        #'LOCK' : None,
        #'chest' : None,
        #'event' : None,
    },
    'Camp Site': {
        'name': 'Camp Site',
        'intro': line101,
        'map': camp_map1,
        'discovered': [],
        'NORTH': 'Pinerift Forest',
        'EAST': 'TESTING GROUND',
        'SOUTH': 'Royal Capital',
        'WEST': 'Cliff Side',
        'EXPLORE': line103,
        'REST': camp_rest,
        'fire': 3,
        'spawn_rate': 0,
    },
    'Cliff Side': {
        'name': 'Cliff Side',
        'intro': line601,
        'map': cliff_map1,
        'discovered': [],
        'EAST': 'Camp Site',
        'SECRET_ROUTE': 'Waterfall Pool',
        'EXPLORE': line602,
        'EXAMINE': cliff_examine,
        'secrets': ['JUMP', 'FLY', 'DIVE'],
        'secret_path': 0,
        'special': cliff_special,
        'spawn_rate': 2,
        'enemy_spawn_set': enemy_spawn0,
        'chest': 'CLOSED',
    },
    #Town start
    'Royal Capital': {
        'name': 'Royal Capital',
        'intro': line201,
        'map': town_map1,
        'discovered': [],
        'NORTH': 'Camp Site',
        'EAST': 'Shop',
        'SOUTH': 'Royal Castle',
        'WEST': 'Inn',
        'EXPLORE': line202,
        'spawn_rate': 0,
    },
    'Shop': {
        'name': 'Shop',
        'intro': line301,
        'map': shop_map1,
        'discovered': [],
        'WEST': 'Royal Capital',
        'EXIT': 'Royal Capital',
        'EXPLORE': line304,
        'BUY': city_shop,
        'spawn_rate': 0,
        'event': 0,
        'items': ['POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 'MAP','LANTERN','CRAFTING POUCH', 'MACE', 'GAMBESON', 'LEATHER BOOTS', 'LEATHER CAP'],
    },
    'Inn': {
        'name': 'Inn',
        'intro': line401,
        'map': inn_map1,
        'discovered': [],
        'EAST': 'Royal Capital',
        'EXIT': 'Royal Capital',
        'EXPLORE': line404,
        'REST': city_inn,
        'spawn_rate': 0,
    },
    'Royal Castle': {
        'name': 'Royal Castle',
        'intro': line501,
        'map': castle_map1,
        'discovered': [],
        'NORTH': 'Royal Capital',
        'EXIT': 'Royal Capital',
        'EXPLORE': line502,
        'spawn_rate': 0,
        'SPEAK': castle_speak,
        'speach': 0,
        'event': 0,
    },  #Town end
    'Pinerift Forest': {
        'name': 'Pinerift Forest',
        'intro': line701,
        'map': forest_map1,
        'discovered': [],
        #'NORTH' : 'Thicket',
        'EAST': 'Pinerift Forest - EAST',
        'SOUTH': 'Camp Site',
        'WEST': 'Pinerift Forest - WEST',
        'EXPLORE': line702,
        'spawn_rate': 2,
        'enemy_spawn_set': enemy_spawn1,
    },
    'Pinerift Forest - EAST': {
        'name': 'Pinerift Forest - EAST',
        'intro': line704,
        'map': foresteast_map1,
        'discovered': [],
        'EAST': 'Rocky Hill',
        'WEST': 'Pinerift Forest',
        'EXPLORE': line705,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn1,
        'boss_ambush': foresteast_ambush,
        'event': 0,
    },
    'Pinerift Forest - WEST': {
        'name': 'Pinerift Forest - WEST',
        'intro': line709,
        'map': forestwest_map1,
        'discovered': [],
        'EAST': 'Pinerift Forest',
        'WEST': 'Serpent River',
        'EXPLORE': line710,
        'spawn_rate': 2,
        'enemy_spawn_set': enemy_spawn1,
    },
    'Rocky Hill': {
        'name': 'Rocky Hill',
        'intro': line801,
        'map': hill_map1,
        'discovered': [],
        'NORTH': 'Mystic Shrine',
        'EAST': 'Bear Cave',
        'SOUTH': 'LOCKED',
        'WEST': 'Pinerift Forest - EAST',
        'EXPLORE': line802,
        'EXAMINE': hill_examine,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn6,
        'LOCK': hill_lock,
    },
    'Mystic Shrine': {
        'name': 'Mystic Shrine',
        'intro': line1101,
        'map': shrine_map1,
        'discovered': [],
        'EAST': 'Deep Woods - Entrance',
        'SOUTH': 'Rocky Hill',
        'EXPLORE': line1102,
        'SPEAK': shrine_speak,
        'PRAY': shrine_pray,
        'speach': 0,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn4,
    },
    #Dungeon 1 start
    'Bear Cave': {
        'name': 'Bear Cave',
        'intro': line901,
        'map': cave_map1,
        'discovered': [],
        'WEST': 'Rocky Hill',
        'EAST': 'LOCKED',
        'EXPLORE': line906,
        'EXAMINE': cave_examine,
        'spawn_rate': 0,
        'boss': ['Bear'],
        'foe': p12,
        'LOCK': cave_lock,
    },
    'Rocky Cave 1': {
        'name': 'Rocky Cave 1',
        'intro': line916,
        'map': cave1_map1,
        'discovered': [],
        'NORTH': 'Rocky Cave 2',
        'SOUTH': 'Rocky Cave 3',
        'WEST': 'Bear Cave',
        'EXPLORE': line917,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn8,
    },
    'Rocky Cave 2': {
        'name': 'Rocky Cave 2',
        'intro': line922,
        'map': cave2_map1,
        'discovered': [],
        'SOUTH': 'Rocky Cave 1',
        'EXPLORE': line923,
        'EXAMINE': cave2_examine,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn8,
        'foe': p3b,
        'chest': 'CLOSED',
    },
    'Rocky Cave 3': {
        'name': 'Rocky Cave 3',
        'intro': line931,
        'map': cave3_map1,
        'discovered': [],
        'NORTH': 'Rocky Cave 1',
        'SOUTH': 'Rocky Cave 4',
        'EXPLORE': line932a,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn8,
    },
    'Rocky Cave 4': {
        'name': 'Rocky Cave 4',
        'intro': line937,
        'map': cave4_map1,
        'discovered': [],
        'NORTH': 'Rocky Cave 3',
        'EAST': 'LOCKED',
        'EXPLORE': line938,
        'EXAMINE': cave4_examine,
        'secrets': ['JUMP', 'FLY', 'DIVE'],
        'special': cave4_special,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn8,
        'boss': ['Hobgoblin Gang'],
        'boss_ambush': cave4_boss_ambush,
        'foe': p22b,
        'LOCK': cave4_lock,
    },
    "Queen's Chamber": {
        'name': "Queen's Chamber",
        'intro': line948,
        'map': cave5_map1,
        'discovered': [],
        'WEST': 'Rocky Cave 4',
        'EXPLORE': line950,
        'spawn_rate': 0,
        'boss': ['Goblin Queen'],
        'boss_ambush': cave5_boss_ambush,
        'foe': p23,
    },  #Dungeon 1 end
    'Serpent River': {
        'name': 'Serpent River',
        'intro': line1201,
        'map': river_map1,
        'discovered': [],
        'NORTH': 'Echobo Lake',
        'EAST': 'Pinerift Forest - WEST',
        'SOUTH': 'Waterfall Pool',
        'SECRET_ROUTE': 'River - West Bank',
        'EXPLORE': line1202,
        'secrets': ['JUMP', 'SWIM', 'DIVE'],
        'secret_path': 0,
        'special': river_special,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn5,
        'event': 0,
    },

    #Waterfall start
    'Waterfall Pool': {
        'name': 'Waterfall Pool',
        'intro': line1301,
        'map': waterfall_map1,
        'discovered': [],
        'NORTH': 'Serpent River',
        'EXPLORE': line1302,
        'EXAMINE': waterfall_examine,
        'secrets': ['JUMP', 'SWIM', 'DIVE'],
        'special': river_special,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn5,
        'chest': 'CLOSED',
        'event': 0,
    },
    'Waterfall Cave 1': {
        'name': 'Waterfall Cave 1',
        'intro': line1312,
        'map': waterfallcave1_map1,
        'discovered': [],
        'NORTH': 'Waterfall Pool',
        'SOUTH': 'Waterfall Cave 2',
        'WEST': 'Waterfall Cave 4',
        'EXPLORE': line1313,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn23,
    },
    'Waterfall Cave 2': {
        'name': 'Waterfall Cave 2',
        'intro': line1314,
        'map': waterfallcave2_map1,
        'discovered': [],
        'NORTH': 'Waterfall Cave 1',
        'SOUTH': 'LOCKED',
        'SECRET_ROUTE': 'Waterfall Cave 4',
        'EXPLORE': line1315,
        'EXAMINE': waterfallcave2_examine,
        'secrets': [],
        'secret_path': 0,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn23,
        'LOCK': waterfallcave2_lock,
        'event': 0,
    },
    'Waterfall Cave 3': {
        'name': 'Waterfall Cave 3',
        'intro': line1322,
        'map': waterfallcave3_map1,
        'discovered': [],
        'NORTH': 'Waterfall Cave 2',
        'EXPLORE': line1323,
        'EXAMINE': waterfallcave3_examine,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn23,
        'boss': ['River Serpent'],
        'event': 0,
    },
    'Waterfall Cave 4': {
        'name': 'Waterfall Cave 4',
        'intro': line1329,
        'map': waterfallcave4_map1,
        'discovered': [],
        'EAST': 'Waterfall Cave 1',
        'EXPLORE': line1330,
        'secrets': [],
        'secret_path': 0,
        'spawn_rate': 0,
    },
    #Waterfall end
    'Echobo Lake': {
        'name': 'Echobo Lake',
        'intro': line1401,
        'map': lake_map1,
        'discovered': [],
        'NORTH': 'Boat House',
        'EAST': 'LOCKED',
        'SOUTH': 'Serpent River',
        'EXPLORE': line1402,
        'EXAMINE': lake_examine,
        'secrets': ['JUMP', 'SWIM', 'DIVE'],
        'special': lake_special,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn5,
        'foe': p16,
        "LOCK": lake_lock,
    },
    'Boat House': {
        'name': 'Boat House',
        'intro': line1501,
        'map': boat_map1,
        'discovered': [],
        'SOUTH': 'Echobo Lake',
        'EXPLORE': line1502,
        'SPEAK': boat_speak,
        'speach': 0,
        'spawn_rate': 0,
    },
    'Berry Patch': {
        'name': 'Berry Patch',
        'intro': line1001,
        'map': berry_map1,
        'discovered': [],
        'NORTH': 'Rocky Hill',
        'EAST': 'Flower Meadow',
        'EXPLORE': line1002,
        'EXAMINE': berry_examine,
        'secrets': ['WAIT', 'PICK'],
        'special': berry_special,
        'secret_path': 0,
        'spawn_rate': 2,
        'enemy_spawn_set': enemy_spawn3,
        'foe': p15b,
        'chest': 'CLOSED',
    },
    'Flower Meadow': {
        'name': 'Flower Meadow',
        'intro': line1701,
        'map': meadow_map1,
        'discovered': [],
        'NORTH': "Witch's Cabin",
        'EAST': 'Great Oak',
        'SOUTH': 'Quiet Village',
        'WEST': 'Berry Patch',
        'EXPLORE': line1702,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn9,
        'foe': None,
        'chest': None,
        'event': None,
    },
    "Witch's Cabin": {
        'name': "Witch's Cabin",
        'intro': line2401,
        'map': witch_map1,
        'discovered': [],
        'SOUTH': 'Flower Meadow',
        'EXPLORE': line2402,
        'SPEAK': witch_speak,
        'CRAFT': witch_crafting,
        'speach': 0,
        'crafting': 'INACTIVE',
        'spawn_rate': 0,
    },

    #Quite Village start
    'Quiet Village': {
        'name': 'Quiet Village',
        'intro': line1801,
        'map': village_map1,
        'discovered': [],
        'NORTH': 'Flower Meadow',
        'EAST': 'Farm House',
        'SOUTH': 'Tavern & Inn',
        'WEST': "Smith's Workshop",
        'EXPLORE': line1802,
        'spawn_rate': 0,
    },
    'Tavern & Inn': {
        'name': 'Tavern & Inn',
        'intro': line401b,
        'map': tavern_map1,
        'discovered': [],
        'NORTH': 'Quiet Village',
        'EXIT': 'Quiet Village',
        'EXPLORE': line404b,
        'REST': city_inn,
        'spawn_rate': 0,
    },
    "Smith's Workshop": {
        'name': "Smith's Workshop",
        'intro': line1901,
        'map': smith_map1,
        'discovered': [],
        'EAST': 'Quiet Village',
        'EXIT': 'Quiet Village',
        'EXPLORE': line1902,
        'SPEAK': smith_speak,
        'UPGRADE': smithing_upgrade,
        'speach' : 0,
        'upgrade_cost': 75,
        'spawn_rate': 0,
        'event': 0,
    },
    'Farm House': {
        'name': 'Farm House',
        'intro': line2201,
        'map': farm_map1,
        'discovered': [],
        'WEST': 'Quiet Village',
        'EXPLORE': line2202,
        'SPEAK': farm_speak,
        'CRAFT': farm_crafting,
        'crafting': 'INACTIVE',
        'speach': 0,
        'spawn_rate': 0,
    },
    #Quite Village end
    'Great Oak': {
        'name': 'Great Oak',
        'intro': line2001,
        'map': oak_map1,
        'discovered': [],
        'WEST': 'Flower Meadow',
        'CLIMB': 'Bee Hive',
        'EXPLORE': line2002,
        'EXAMINE': oak_examine,
        'spawn_rate': 0,
    },
    'Bee Hive': {
        'name': 'Bee Hive',
        'intro': line2104,
        'map': hive_map1,
        'discovered': [],
        'EXIT': 'Great Oak',
        'CLIMB': 'Great Oak',
        'EXPLORE': line2105,
        'EXAMINE': hive_examine,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn10,
        'boss': ['Giant Bee Queen'],
        'boss_ambush': hive_boss_ambush,
        'foe': p24,
        'chest': "CLOSED",
    },
    'Mushroom Grove': {
        'name': 'Mushroom Grove',
        'intro': line1601,
        'map': mushroom_map1,
        'discovered': [],
        'NORTH': 'Rotting Woods',
        'SOUTH': 'Fairy Circle',
        'WEST': 'Echobo Lake',
        'EXPLORE': line1602,
        'EXAMINE': mushroom_examine,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn7,
        #'LOCK' : None,
        'chest': "CLOSED",
        #'event' : None,
    },
    
    'Fairy Circle': {
        'name': 'Fairy Circle',
        'intro': line2901,
        'map': fairy_map1,
        'discovered': [],
        'NORTH': 'Mushroom Grove',
        'EXPLORE': line2902,
        'EXAMINE': fairy_examine,
        'SPEAK': fairy_speak,
        'speach': 0,
        'spawn_rate': 0,
        'boss': ["Dark Fairy Prince"],
        'foe': p40,
        'fairy_reward': 5,
    },
    'Rotting Woods': {
        'name': 'Rotting Woods',
        'intro': line2601,
        'map': rot_map1,
        'discovered': [],
        'NORTH': 'Frog Marsh',
        'SOUTH': 'Mushroom Grove',
        'WEST': 'Rotten Swamp 1',
        'EXPLORE': line2602,
        'spawn_rate': 2,
        'enemy_spawn_set': enemy_spawn11,
    },

    #Ogre Dungeon start
    'Rotten Swamp 1': {
        'name': 'Rotten Swamp 1',
        'intro': line2701,
        'map': swamp1_map1,
        'discovered': [],
        'EAST': 'Rotting Woods',
        'WEST': 'Rotten Swamp 2',
        'EXPLORE': line2702,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn12,
    },
    'Rotten Swamp 2': {
        'name': 'Rotten Swamp 2',
        'intro': line2703,
        'map': swamp2_map1,
        'discovered': [],
        'EAST': 'Rotten Swamp 1',
        'SOUTH': 'Rotten Swamp 6',
        'WEST': 'Rotten Swamp 3',
        'EXPLORE': line2704,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn13,
    },
    'Rotten Swamp 3': {
        'name': 'Rotten Swamp 3',
        'intro': line2705,
        'map': swamp3_map1,
        'discovered': [],
        'NORTH': 'Rotten Swamp 4',
        'EAST': 'Rotten Swamp 2',
        'SOUTH': 'Rotten Swamp 5',
        'EXPLORE': line2706,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn13,
    },
    'Rotten Swamp 4': {
        'name': 'Rotten Swamp 4',
        'intro': line2707,
        'map': swamp4_map1,
        'discovered': [],
        'SOUTH': 'Rotten Swamp 3',
        'EXPLORE': line2708,
        'EXAMINE': swamp4_examine,
        'event': 0,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn12,
        'foe': p29b,
    },
    'Rotten Swamp 5': {
        'name': 'Rotten Swamp 5',
        'intro': line2717,
        'map': swamp5_map1,
        'discovered': [],
        'NORTH': 'Rotten Swamp 3',
        'EAST': 'Rotten Swamp 6',
        'SOUTH': 'Rotten Swamp 8',
        'WEST': 'Rotten Swamp 7',
        'EXPLORE': line2718,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn13,
    },
    'Rotten Swamp 6': {
        'name': 'Rotten Swamp 6',
        'intro': line2719,
        'map': swamp6_map1,
        'discovered': [],
        'NORTH': 'Rotten Swamp 2',
        'WEST': 'Rotten Swamp 5',
        'EXPLORE': line2720,
        'special': swamp_special,
        'secrets': ['DRINK', 'SWIM', 'DIVE'],
        'secret_path': 0,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn14,
    },
    'Rotten Swamp 7': {
        'name': 'Rotten Swamp 7',
        'intro': line2723,
        'map': swamp7_map1,
        'discovered': [],
        'EAST': 'Rotten Swamp 5',
        'EXPLORE': line2724,
        'special': swamp7_special,
        'secrets': [ 'DRINK', 'SWIM', 'DIVE', 'RIBBIT', 'RIBBITING', 'CROAK','CROAKING', 'KERO', 'KEROKERO'],
        'secret_path': 0,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn12,
        'event': 0,
    },
    'Rotten Swamp 8': {
        'name': 'Rotten Swamp 8',
        'intro': line2727,
        'map': swamp8_map1,
        'discovered': [],
        'NORTH': 'Rotten Swamp 5',
        'EXPLORE': line2728,
        'special': swamp8_special,
        'secrets': ['PLAY', 'DRINK', 'SWIM', 'DIVE'],
        'secret_path': 0,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn13,
        'foe': p35,
        'event': 0,
    },
    #Ogre Dungeon End
    'Frog Marsh': {
        'name': 'Frog Marsh',
        'intro': line2801,
        'map': marsh_map1,
        'discovered': [],
        'EAST': 'Grassy Plains',
        'SOUTH': 'Rotting Woods',
        'EXPLORE': line2802,
        'SPEAK': marsh_speak,
        'CRAFT': marsh_crafting,
        'speach': 0,
        'crafting': 'INACTIVE',
        'spawn_rate': 0,
    },
    'Grassy Plains': {
        'name': 'Grassy Plains',
        'intro': line3001,
        'map': plains_map1,
        'discovered': [],
        'NORTH': 'Northern Coast',
        'EAST': 'Foot Hills',
        'WEST': 'Frog Marsh',
        'EXPLORE': line3002,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn17,
    },
    'Foot Hills': {
        'name': 'Foot Hills',
        'intro': line3101,
        'map': foothills_map1,
        'discovered': [],
        'NORTH': 'Shipwreck',
        'WEST': 'Grassy Plains',
        'EXPLORE': line3102,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn18,
    },
    'Northern Coast': {
        'name': 'Northern Coast',
        'intro': line3201,
        'map': coast_map1,
        'discovered': [],
        'EAST': 'Shipwreck',
        'SOUTH': 'Grassy Plains',
        'WEST': 'Harbor Town',
        'EXPLORE': line3202,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn16,
    },
    'Shipwreck': {
        'name': 'Shipwreck',
        'intro': line3301,
        'map': shipwreck_map1,
        'discovered': [],
        'SOUTH': 'Foot Hills',
        'WEST': 'Northern Coast',
        'EXPLORE': line3302,
        'EXAMINE': shipwreck_examine,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn16,
        'chest': 'CLOSED',
        'event': 0,
    },
    #Harbor Town Start
    'Harbor Town': {
        'name': 'Harbor Town',
        'intro': line3401,
        'map': harbor1_map1,
        'discovered': [],
        'NORTH': 'Harbor Markets',
        'EAST': 'Northern Coast',
        'WEST': 'Harbor Inn',
        'EXPLORE': line3402,
        'spawn_rate': 0,
    },
    'Harbor Inn': {
        'name': 'Harbor Inn',
        'intro': line401c,
        'map': harborinn_map1,
        'discovered': [],
        'EAST': 'Harbor Town',
        'EXIT': 'Harbor Town',
        'EXPLORE': line404c,
        'REST': city_inn,
        'spawn_rate': 0,
    },
    'Harbor Markets': {
        'name': 'Harbor Markets',
        'intro': line302,
        'map': harbormarket_map1,
        'discovered': [],
        'EAST': 'Harbor Temple',
        'SOUTH': 'Harbor Town',
        'WEST': 'Docked Ship',
        'EXPLORE': line303,
        'BUY':harbor_shop,
        'spawn_rate': 0,
        'items': ['POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 'MAP','CRAFTING POUCH','DRAGON SCALE','EXTRA POUCH','ARMING SWORD', 'PARMA', 'BASCINET', 'BRIGANDINE', 'OLD CUIRASS', 'GREAVES', 'GORGET',],
    },
    'Docked Ship': {
        'name': 'Docked Ship',
        'intro': line3501,
        'map': harborship_map1,
        'discovered': [],
        'EAST': 'Harbor Markets',
        'EXPLORE': line3502,
        'SPEAK': ship_speak,
        'speach': 0,
        'spawn_rate': 0,
        'event': 0,
    },
    'Alchemist Shop': {
        'name': 'Alchemist Shop',
        'intro': line3601,
        'map': alchemist_map1,
        'discovered': [],
        'NORTH': 'Harbor Town',
        'EXPLORE': line3602,
        'SPEAK': alchemist_speak,
        'CRAFT': alchemist_crafting,
        'speach': 0,
        'crafting': 'INACTIVE',
        'secrets': [],
        'secret_path': 0,
        'spawn_rate': 0,
    },
    'Harbor Temple': {
        'name': 'Harbor Temple',
        'intro': line3403,
        'map': harborshrine_map1,
        'discovered': [],
        'WEST': 'Harbor Markets',
        'EXPLORE': line3404,
        'SPEAK': harbortemple_speak,
        'PRAY': shrine_pray,
        'speach': 0,
        'spawn_rate': 0,
    },
    #Harbor town end
    'Western Lake': {
        'name': 'Western Lake',
        'intro': line3701,
        'map': westlake_map1,
        'discovered': [],
        'WEST': 'Rotten Swamp 8',
        'SOUTH': 'River - West Bank',
        'EXPLORE': line3702,
        'secrets': [],
        'secret_path': 0,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn19,
    },
    'River - West Bank': {
        'name': 'River - West Bank',
        'intro': line3801,
        'map': westriver_map1,
        'discovered': [],
        'NORTH': 'Western Lake',
        'SOUTH': 'Fae Woods - EAST',
        'SECRET_ROUTE': 'Serpent River',
        'EXPLORE': line3802,
        'EXAMINE': riverwest_examine,
        'secrets': [],
        'secret_path': 0,
        'special': riverwest_special,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn20,
        'event': 0,
    },
    'Fae Woods - EAST': {
        'name': 'Fae Woods - EAST',
        'intro': line3901,
        'map': faeeast_map1,
        'discovered': [],
        'NORTH': 'River - West Bank',
        'WEST': 'Fae Woods - Camp',
        'EXPLORE': line3902,
        'spawn_rate': 2,
        'enemy_spawn_set': enemy_spawn21,
        'boss': ['Rouge Gang'],
        'boss_ambush': faeeast_ambush,
    },
    'Fae Woods - Camp': {
        'name': 'Fae Woods - Camp',
        'intro': line4001,
        'map': faecamp_map1,
        'discovered': [],
        'NORTH': 'Crescent Pond',
        'EAST': 'Fae Woods - EAST',
        'WEST': 'Fae Woods - WEST',
        'EXPLORE': line4003,
        'REST': faecamp_rest,
        'spawn_rate': 0,
        'boss': ['Rouge Gang'],
        'boss_ambush': faecamp_ambush,
        'fire': 3,
    },
    'Crescent Pond': {
        'name': 'Crescent Pond',
        'intro': line4101,
        'map': crescentlake_map1,
        'discovered': [],
        'SOUTH': 'Fae Woods - Camp',
        'EXPLORE': line4102,
        'secrets': ['THROW WEAPON'],
        'special': crescent_special,
        'spawn_rate': 1,
        'enemy_spawn_set': enemy_spawn21,
        'boss': ['Naga'],
        'event': None,
    },
    'Fae Woods - WEST': {
        'name': 'Fae Woods - WEST',
        'intro': line4201,
        'map': faewest_map1,
        'discovered': [],
        'EAST': 'Fae Woods - Camp',
        'SOUTH': 'Fae Woods - SOUTH',
        'EXPLORE': line4202,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn22,
    },
    'Fae Woods - SOUTH': {
        'name': 'Fae Woods - SOUTH',
        'intro': line4301,
        'map': faesouth_map1,
        'discovered': [],
        'NORTH': 'Fae Woods - WEST',
        'SOUTH': 'Mountain Pass',
        'EXPLORE': line4302,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn21,
    },
    'Mountain Pass': {
        'name': 'Mountain Pass',
        'intro': line4401,
        'map': mountainpass_map1,
        'discovered': [],
        'NORTH': 'Fae Woods - SOUTH',
        'EAST': "Dwarf's Workshop",
        'SOUTH': 'Drake Mountains 1',
        'EXPLORE': line4402,
        'secrets': [],
        'special': None,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
    },
    "Dwarf's Workshop": {
        'name': "Dwarf's Workshop",
        'intro': line4501,
        'map': dwarf_map1,
        'discovered': [],
        'WEST': 'Mountain Pass',
        'EXPLORE': line4503,
        'SPEAK': dwarf_speak,
        'speach': 0,
        'secrets': [],
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'items': ['BROAD SWORD', 'SIDE SWORD', 'HANGER', 'SALLET', 'CUISSES', 'ORICHALCUM BRIGANDINE'],
        'event': 0,
        'event2' : 0,
    },
    #Drake Mountain Dungeon start
    'Drake Mountains 1': {
        'name': 'Drake Mountains 1',
        'intro': line4601,
        'map': drake1_map1,
        'discovered': [],
        'NORTH': 'Mountain Pass',
        'SOUTH': 'Drake Mountains 2',
        'EXPLORE': line4602,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn25,
    },
    'Drake Mountains 2': {
        'name': 'Drake Mountains 2',
        'intro': line4603,
        'map': drake2_map1,
        'discovered': [],
        'NORTH': 'Drake Mountains 1',
        'EAST': 'Drake Mountains 3',
        'EXPLORE': line4604,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn25,
    },
    'Drake Mountains 3': {
        'name': 'Drake Mountains 3',
        'intro': line4605,
        'map': drake3_map1,
        'discovered': [],
        'EAST': 'Drake Mountains 4',
        'WEST': 'Drake Mountains 2',
        'SECRET_ROUTE': None,
        'EXPLORE': line4606,
        'secrets': ['TANNINIM'],
        'special': drake_special,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn25,
        'event': 0,
    },
    'Drake Mountains 4': {
        'name': 'Drake Mountains 4',
        'intro': line4608,
        'map': drake4_map1,
        'discovered': [],
        'NORTH': 'Drake Mountains 5',
        'WEST': 'Drake Mountains 3',
        'EXPLORE': line4609,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn25,
    },
    'Drake Mountains 5': {
        'name': 'Drake Mountains 5',
        'intro': line4610,
        'map': drake5_map1,
        'discovered': [],
        'SOUTH': 'Drake Mountains 4',
        'EXPLORE': line4611,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn25,
    },
    'Drake Mountains Summit': {
        'name': 'Drake Mountains Summit',
        'intro': line4612,
        'map': drake6_map1,
        'discovered': [],
        'NORTH': 'Drake Mountains 3',
        'EXPLORE': line4614,
        'secrets': [],
        'secret_path': 0,
        'special': None,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'boss': ["Dragon King, Tanninim"],
        'boss_ambush': dragon_ambush,
        'foe': None,
        'event': None,
    },
    #Drake Mountain Dungeon end
  
    'Deep Woods - Entrance': {
        'name': 'Deep Woods - Entrance',
        'intro': line4701,
        'map': deepwoodsentrance_map1,
        'discovered': [],
        'NORTH' : 'Deep Woods - SOUTH',
        'WEST': 'Mystic Shrine',
        'EXPLORE': line4702,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn15,
    },
    'Deep Woods - SOUTH': {
        'name': 'Deep Woods - SOUTH',
        'intro': line4703,
        'map': deepwoodssouth_map1,
        'discovered': [],
        'NORTH' : 'Deep Woods - Fork',
        'SOUTH': 'Deep Woods - Entrance',
        'EXPLORE': line4704,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn15,
    },
    'Deep Woods - Fork': {
        'name': 'Deep Woods - Fork',
        'intro': line4705,
        'map': deepwoodsfork_map1,
        'discovered': [],
        'EAST' : 'LOCKED',
        'SOUTH': 'Deep Woods - SOUTH',
        'WEST': 'Deep Woods - WEST',
        'EXPLORE': line4706,
        'EXAMINE' : deepwoodsfork_examine,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn15,
        'LOCK': deepwoodsfork_lock,
    },
    'Deep Woods - WEST': {
        'name': 'Deep Woods - WEST',
        'intro': line4712,
        'map': deepwoodswest_map1,
        'discovered': [],
        'NORTH' : 'LOCKED',
        'EAST': 'Deep Woods - Fork',
        'SOUTH': 'Deep Woods - Forest Hut',
        'EXPLORE': line4713,
        'EXAMINE' : deepwoodswest_examine,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn15,
        'LOCK': deepwoodswest_lock,
    },
    'Deep Woods - Forest Hut': {
        'name': 'Deep Woods - Forest Hut',
        'intro': line4722,
        'map': None,
        'discovered': [],
        'NORTH': 'Deep Woods - WEST',
        'EXPLORE': line4725,
        'SPEAK': kobold_speak,
        'speach': 0,
        'secrets': [],
        'special': kobold_special,
        'spawn_rate': 0,
        'items': ['POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 'MAP', 'LANTERN', 'GORGET', 'OBSIDIAN DAGGER', 'VELVET SLIPPERS' ],
        'items2': ['PAINTED SNAIL', 'SLEEPY SQUIRELL', 'WET TOAD'],
        'event': 0,
        'event2': 0,
    },
    'Deep Woods - Fallen Hive': {
        'name': 'Deep Woods - Fallen Hive',
        'intro': 'place holder txt',
        'map': deepwoodshive_map1,
        'discovered': [],
        'NORTH': 'Tattered Hive',
        'SOUTH': 'Deep Woods - WEST',
        'EXPLORE': 'place holder txt',
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn15,
    },
    'Tattered Hive': {
        'name': 'Tattered Hive',
        'intro': line4801,
        'map': hive2_map1,
        'discovered': [],
        'SOUTH': 'Deep Woods - Fallen Hive',
        'EXPLORE': line4802,
        'EXAMINE': tatteredhive_examine,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn15,
        'event': 0,
    },
    
}

song_term = ['RIBBIT', 'RIBBITING', 'CROAK', 'CROAKING', 'KERO', 'KEROKERO']

#define player key items
key_items = {
    '': {
        'name': '',
        'description': '',
    },
    'POTION': {
        'name': 'POTION',
        'description': None,
        'price': 35,
    },
    'ANTIDOTE': {
        'name': 'ANTIDOTE',
        'description': None,
        'price': 25,
    },
    'ETHER': {
        'name': 'ETHER',
        'description': None,
        'price': 40,
    },
    'SMOKE BOMB': {
        'name': 'SMOKE BOMB',
        'description': None,
        'price': 30,
    },
    'DRAGON SCALE': {
        'name': 'DRAGON SCALE',
        'description': None,
        'price': 350
    },

  
    'EMPTY': {
        'name': 'blank',
        'description': 'nothing.',
        'ATK': 0,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': None,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'RUSTY DAGGER': {
        'name': 'RUSTY DAGGER',
        'description': 'A simple quillon dagger with a dull edge and rusty blade. An awful weapon, but better than nothing... probably.',
        'ATK': 1,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'A basic dagger. Usable by any class.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 25,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'MESSER': {
        'name': 'MESSER',
        'description': 'A long single edged sword with a knife like construction. It doesnt show signs of use, but the Friar kept it well maintained.',
        'ATK': 5,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'A well made, single edge sword. Usable by any class.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 75,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'MACE': {
        'name': 'MACE',
        'description': 'A flanged mace with a strudy, full metal construction. The extra heaft adds to its power, but the weapon offers no defensive capabilities.',
        'ATK': 8,
        'DEF': -3,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'A sturdy, flanged mace. Usable by any class.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 75,
        'price': 100,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'GOBLIN CHOPPER': {
        'name': 'GOBLIN CHOPPER',
        'description': 'A brutish chopping weapon used by Goblins. Comfort was not a thought when crafting this weapon; sharp edges dig into your hand while holding it. The thick construction does make it a durable and powerful weapon however...',
        'ATK': 11,
        'DEF': 0,
        'HP': -20,
        'MP': 0,
        'GR': 0,
        'description2':
        'A basic, single edge chopping blade. Usable by any class.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'OBSIDIAN DAGGER': {
        'name': 'OBSIDIAN DAGGER',
        'description': 'A dagger crafted from obsidian. Not particularly durable, but has a razor sharp edge. ',
        'ATK': 12,
        'DEF': -5,
        'HP': 0,
        'MP': 1,
        'GR': 0,
        'description2':
        'A fragile, razor sharp obsidian dagger. Usable by any class.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'price': 250,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'ARMING SWORD': {
        'name': 'ARMING SWORD',
        'description': 'A typical arming sword. Not a fancy weapon by any means, but well crafted and reliable.',
        'ATK': 9,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'A quality, arming sword. Usable by any class.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 50,
        'price': 300,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'BROAD SWORD': {
        'name': 'BROAD SWORD',
        'description': 'A broad sword with a basket hilt lined with a soft velvet. An elegant, and highly protective blade. The basket hilt does make wielding a little trickier, however.',
        'ATK': 11,
        'DEF': 8,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'A protective, double edge sword. Usable by WARRIORS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'price': 500,
        'classes': ['GOD','WARRIOR',],
    },
    'SIDE SWORD': {
        'name': 'SIDE SWORD',
        'description': 'An exquisite double edge sword with finger rings on the hilt. Capable of delivering devestating cuts and thrusts.',
        'ATK': 16,
        'DEF': 0,
        'HP': 0,
        'MP': 1,
        'GR': 0,
        'description2': 'An exquisite, double edge sword. Usable by WIZARDS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'price': 500,
        'classes': ['GOD', 'WIZARD', 'WITCH',],
    },
    'HANGER': {
        'name': 'HANGER',
        'description':
        'A robust single edge blade with a simple knuckle guard. A favorite among sea faring folk as the are great for close quarters combat on ships. You feel extra lucky wielding this sword.',
        'ATK': 13,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 1,
        'description2': 'A fine, single edge sword. Increases GP earned from combat. Usable by THIEVES.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'price': 500,
        'classes': ['GOD', 'THIEF'],
    },
    'AETHON': {
        'name': 'AETHON',
        'description': "A falchion crafted from steel sourced from a fallen star. The blade draws energy from the wielder, but will grow mightier to defend them as their health diminishes. The complex hilt is atypical for this type of sword, but does improve it's defensive capabilities.",
        'ATK': 18,
        'DEF': 4,
        'HP': 0,
        'MP': -3,
        'GR': 0,
        'description2': 'A mighty falchion of legendary quality. Bonus ATK the lower your HP, reduces max MP. Unlocks skill: BATTLECRY. Usable by WARRIORS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD','WARRIOR',],
    },
    'FULGUR': {
        'name': 'FULGUR',
        'description': 'An arming sword crafted from pure mythril. Embued with powerful magic, this blade gets its name from the way energy surges through the wielders body like lightning. Such power comes at the cost of ones own life...',
        'ATK': 25,
        'DEF': 0,
        'HP': -50,
        'MP': 2,
        'GR': 0,
        'description2': 'A magic arming sword of legendary quality. Increases MP and skill power at the cost of HP. Unlocks skill: SHOCK. Usable by WIZARDS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD','WIZARD','WITCH',],
    },
    'MIDAS': {
        'name': 'MIDAS',
        'description': 'A xiphos crafted from the legendary Dwarven alloy, orichalcum. As ones wealth grows, so too does the strength of this blade. If one were so unfortunate as to lose all their riches however, this sword would just as quickly sap the users power...',
        'ATK': 20,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'description2':
        'A nimble xiphos of legendary quality. Bonus ATK the more GP in wallet, damage penalty for low GP. Unlocks skill: $TOSS. Usable by THEIVES.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD','THIEF',],
    },
    'ADAMANTITE SWORD': {
        'name': 'ADAMANTITE SWORD',
        'description':'A hand and a half sword made from the mythical metal adamantite. Legend states the metal is harvested off the shells of World Tortoise and is said to be stronger and tougher than any other metal. Few weapons can match this blades quality.',
        'ATK': 30,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'A sword of legendary quality. Usable by any class.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },

  
    'BUCKLER': {
        'name': 'BUCKLER',
        'description':
        'A small center-grip shield made of hardened steel. Looks like its been a little neglected over the years.',
        'ATK': 0,
        'DEF': 10,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Small shield that improves defenses for all classes',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'PARMA': {
        'name': 'PARMA',
        'description':
        'A large center-grip shield made of wood and reinforced with a steel rim. The large size offers amazing protection, but at the cost of attack power and stamina.',
        'ATK': -4,
        'DEF': 10,
        'HP': -25,
        'MP': 0,
        'GR': 0,
        'description2': 'Large shield that improves defenses for all classes. Reduces ATK and HP.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'STAFF': {
        'name': 'STAFF',
        'description': 'A staff carved from white oak. It is said that staves made from the wood of the white oak have a special connection to magic, and are prizedby mages everywhere.',
        'ATK' : 7,
        'DEF' : 0,
        'HP' : 0,
        'MP' : 1,
        'GR' : 0,
        'description2': 'A white oak staff. Enhances ATK and magic abilities, increases MP +1. Usable by WIZARDS.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'CLOAK': {
        'name': 'CLOAK',
        'description': 'A dark cloak useful for defending and concealing attacks. While not as defensive as a shield, foes would be wise not to underestimate its usefulness in combat...',
        'ATK': 2,
        'DEF': 3,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Offers small increase in protection and power. Causes enemies to miss more frequently. Usable by THIEVES.',
        'price': 0,
        'classes': ['GOD', 'THIEF'],
    },
    'BATTLE AXE': {
        'name': 'BATTLE AXE',
        'description': 'An single handed axe with a specialized head for combat. A devestating off-hand weapon used by WARRIORS seeking to cast aside extra protection for raw power.',
        'ATK': 10,
        'DEF': -6,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Increases ATK, reduces DEF. Usable by WARRIORS.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR'],
    },

  
    'POINTED HAT': {
        'name': 'POINTED HAT',
        'description': 'A pointed hat with a wide brim. A common piece of fashion among magic users. Some say that the hat acts as a conduit for magical power.',
        'ATK': 0,
        'DEF': 2,
        'HP': 0,
        'MP': 2,
        'GR': 0,
        'description2':
        'Light armor for WIZARDS. Boosts MP, but offers little defense',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 100,
        'price': 0,
        'classes': ['GOD', 'WIZARD', 'WITCH'],
    },
    'COWL': {
        'name': 'COWL',
        'description':
        'A large, loose hood often used by thieves to conceal their identity. Offers modest protection.',
        'ATK': 0,
        'DEF': 4,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'description2': 'Light armor for THIEVES. Boosts GP earned.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 100,
        'price': 0,
        'classes': ['GOD', 'THIEF'],
    },
    'LEATHER CAP': {
        'name': 'LEATHER CAP',
        'description':
        'A leather cap with a feather, commonly worn by travelers. Offers a very modest amount of protection, but is certainly better than nothing!',
        'ATK': 0,
        'DEF': 3,
        'HP': 5,
        'MP': 0,
        'GR': 0,
        'description2': 'Light armor for for all classes.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'BASCINET': {
        'name': 'BASCINET',
        'description':
        'A full face helmet that offers good protection. The pointed visor may look a little silly, but it very well may save your life!',
        'ATK': 0,
        'DEF': 5,
        'HP': 10,
        'MP': 0,
        'GR': 0,
        'description2': 'Medium armor for for all classes.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'price': 150,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'SALLET': {
        'name': 'SALLET',
        'description': 'A hardened steel helmet with a movable visor. The craftsmanship of this helm is impeccable',
        'ATK': 0,
        'DEF': 7,
        'HP': 25,
        'MP': 0,
        'GR': 0,
        'description2': 'Medium armor for for all classes.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 150,
        'price': 350,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },

  
    'MAGIC ROBE': {
        'name': 'MAGIC ROBE',
        'description': 'A flowing blue robe made with gold and silver thread weaved through. Amplifies magical energy when worn.',
        'ATK': 5,
        'DEF': 2,
        'HP': 0,
        'MP': 1,
        'GR': 0,
        'description2':
        'Light armor for WIZARDS. Boosts power, but offers little defense',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'price': 0,
        'classes': ['GOD', 'WIZARD', 'WITCH'],
    },
    'GAMBESON': {
        'name': 'GAMBESON',
        'description':
        'A padded jacket that is easy to repair and maintain. While not as protective as metal, it still offers a fair bit of extra defense.',
        'ATK': 0,
        'DEF': 4,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Light armor for all classes.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,  
        'price': 75,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'STEEL MAIL': {
        'name': 'STEEL MAIL',
        'description':
        'A surprisingly bulky set of armor made from hardened steel rings. Offers a good deal of protection and mobility.',
        'ATK': 0,
        'DEF': 7,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Average quality medium armor for all classes.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'price': 150,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'BRIGANDINE': {
        'name': 'BRIGANDINE',
        'description':
        'Armor made from overlapping plates of steel. Offers excellent levels of protection without compromising too much on mobility.',
        'ATK': 0,
        'DEF': 10,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'High quality, medium armor for WARRIORS and THIEVES',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'price': 250,
        'classes': ['GOD', 'WARRIOR', 'THIEF'],
    },
    'OLD CUIRASS': {
        'name': 'OLD CUIRASS',
        'description':
        'A cuirass with spots of rust and signs of battle damage. This previously used armor is heavy and poorly fitted, but the thick plate offers tremendous protection.',
        'ATK': 0,
        'DEF': 13,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'High quality, heavy armor for WARRIORS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'price': 350,
        'classes': ['GOD', 'WARRIOR'],
    },
    'MYTHRIL MAIL': {
        'name': 'MYTHRIL MAIL',
        'description':
        'A shirt made with rings of pure mythril. This legendary metal is stronger and tougher than steel, yet weighs as much as silk. Even a king would be jealous of such a fine piece of armor.',
        'ATK': 0,
        'DEF': 15,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'legendary quality, light armor for all classes.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 200,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'ORICHALCUM BRIGANDINE': {
        'name': 'ORICHALCUM BRIGANDINE',
        'description':
        'Made from overlapping plates of the orichalcum. This legendary alloy invented by the Dwarfs never tarnishes and causes blows to glance off like oil repells water.',
        'ATK': 0,
        'DEF': 18,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2':
        'legendary quality, medium armor for WARRIORS and THIEVES',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'price': 500,
        'upgrade': 200,
        'classes': ['GOD', 'WARRIOR', 'THIEF'],
    },
    'ADAMANTITE CUIRASS': {
        'name': 'ADAMANTITE CUIRASS',
        'description':
        'A cuirass with a deep emerald hue, made of plates of adamantite. No other metal matches the quality of this legendary material. Offers increadible protection',
        'ATK': 0,
        'DEF': 20,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'High quality, heavy armor for WARRIORS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 200,
        'price': 0,
        'classes': ['GOD', 'WARRIOR'],
    },

  
    'LEATHER BOOTS': {
        'name': 'LEATHER BOOTS',
        'description':
        'Simple leather boots with a nice thick soul. Offers little protection in combat, but may still come in handy.',
        'ATK': 0,
        'DEF': 1.5,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Basic light boots for all classes.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'VELVET SLIPPERS': {
        'name': 'VELVET SLIPPERS',
        'description':
        'Slippers crafted from a soft velvet. These light shoes are a favorite among thieves as they mute footsteps without affecting mobility.',
        'ATK': 0,
        'DEF': 1,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'description2':
        'Soft, light slippers for THIEVES. Increases GP earned.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 125,
        'price': 0,
        'classes': ['GOD', 'THIEF'],
    },
    'CUISSES': {
        'name': 'CUISSES',
        'description':
        'Plate metal leg coverings that fully encapsulate the thighs. Offers incredible protection against all kinds of strikes.',
        'ATK': 0,
        'DEF': 5,
        'HP': 35,
        'MP': 0,
        'GR': 0,
        'description2': 'High quality, heavy armor for WARRIORS.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 125,
        'price': 275,
        'classes': ['GOD', 'WARRIOR',],
    },
    'CHAUSSES': {
        'name': 'CHAUSSES',
        'description':
        'Full mail leg coverings made from hardened steel rings. Highly effective against cuts and slashes, but lacks cushioning against blunt strikes.',
        'ATK': 0,
        'DEF': 3,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Average quality, medium armor for all classes.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 75,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'GREAVES': {
        'name': 'GREAVES',
        'description':
        'Metal leg coverings that protect the full front of the shin. Offers great protection from frontal attacks, but leaves the back of the leg vulnerable',
        'ATK': 0,
        'DEF': 6,
        'HP': -25,
        'MP': 0,
        'GR': 0,
        'description2': 'Average quality, medium armor for all classes.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },

  
    'GORGET': {
        'name': 'GORGET',
        'description':
        'A collar of metal plates covered in leather. Offers additional protection against blows to the throat; an essential piece of armor by all accounts.',
        'ATK': 0,
        'DEF': 5,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Offers additional protection',
        'price': 300,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'HEROS MEDAL': {
        'name': 'HEROS MEDAL',
        'description':
        'A gold medal found on a corpse covered in mushrooms. The name "Jeremy The Goblin-Slayer" is engraved on the front. What an unfitting end for such a valiant hero.',
        'ATK': 0,
        'DEF': 0,
        'HP': 50,
        'MP': 0,
        'GR': 0,
        'description2': 'Increases max HP by +50.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'GOLD RING': {
        'name': 'GOLD RING',
        'description':
        'A perfectly polished gold ring. Given to you by one of the Frog-Sirens of the swamp. You feel luckier holding this, like your wealth is about to grow.',
        'ATK': 0,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'description2': 'Increases GP earned from combat.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'CRYSTAL NECKLACE': {
        'name': 'CRYSTAL NECKLACE',
        'description':
        'A necklace made from an unusual crystal. A faint warmth can be felt emanating from it. Wearing it fills you with magical energy.',
        'ATK': 0,
        'DEF': 0,
        'HP': 0,
        'MP': 2,
        'GR': 0,
        'description2': 'Increases MP by +2.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF'],
    },
    'THORN BRACERS': {
        'name': 'THORN BRACERS',
        'description':
        'Bracers made from dried thorns. Surprisingly durable, the sharp thorns are as much a threat to the wearer as their foes.',
        'ATK': 7,
        'DEF': -3,
        'HP': -15,
        'MP': 0,
        'GR': 0,
        'description2': 'Increases ATK, reduces DEF and HP.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF']
    },
    'WOLF FANG': {
        'name': 'WOLF FANG',
        'description': "A fang broken off a Dire Wolf. Wearing this around your neck gives you some of the wolf's strength.",
        'ATK': 3,
        'DEF': 0,
        'HP': 35,
        'MP': 0,
        'GR': 0,
        'description2': 'Enhances ATK and HP. Usable by WARRIORS',
        'price': 0,
        'classes': ['GOD', 'WARRIOR'],
    },
    'CRYSTAL RING': {
        'name': 'CRYSTAL RING',
        'description': 'A ring carved from an unusual crystal. The crystal glows faintly in dim light. Wearing it fills you with magical energy.',
        'ATK': 3,
        'DEF': 0,
        'HP': 0,
        'MP': 1,
        'GR': 0,
        'description2': 'Enhances ATK and magic abilities, increases MP +1. Usable by WIZARDS',
        'price': 0,
        'classes': ['GOD', 'WIZARD', 'WITCH',],
    },
    'GOLD HAIRPIN': {
        'name': 'GOLD HAIRPIN',
        'description': 'A glistening hairpin made of pure gold. Often worn for luck; the GOLD HAIRPIN is a symbol of wealth.',
        'ATK': 0,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'description2': 'Increases GP earned from combat. Usable by THIEVES',
        'price': 0,
        'classes': ['GOD', 'THIEF'],
    },
    'MAGIC CIRCLET': {
        'name': 'MAGIC CIRCLET',
        'description': 'A magically enhanced circlet crafted with secret dwarven smithing techniques from an orichalcum ingot. Confers several boons to the wearer.',
        'ATK': 0,
        'DEF': 0,
        'HP': 35,
        'MP': 1,
        'GR': .5,
        'description2': 'Increases HP, MP, and GP earned.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF']
    },
    'DRAGON HEART': {
        'name': 'DRAGON HEART',
        'description': 'A crimson gem created after killing an ancient and powerful dragon. This gem holds incredible power, but using it comes at a steep price...',
        'ATK': 20,
        'DEF': 0,
        'HP': -75,
        'MP': 4,
        'GR': 0,
        'description2': 'Greatly increases ATK and MP, greatly reduces HP',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF']
    },
  
    'MAP': {
        'name': 'MAP',
        'description': 'A map coated in magical ink. The ink reacts to your surroundings and changes depending on your location. (Type MAP or LOCATION outside item menu to view current area.)',
        'price': 50,
    },
    'CRAFTING POUCH': {
        'name': 'CRAFTING POUCH',
        'description':"A special pouch in your pack for storing crafting materials. You're not sure how it can hold so much, but you're not about to question it either.",
        'price': 300,
    },
    'LANTERN': {
        'name': 'LANTERN',
        'description': 'A lantern that attaches to a belt for hands free use. Allows travel through dark areas.',
        'price': 200,
    },
    'EXTRA POUCH': {
        'name': 'EXTRA POUCH',
        'description': 'Increases consumable item inventory',
        'price': 500,
    },
    'SPECIAL FEED': {
        'name': 'SPECIAL FEED',
        'description': 'A medicated feed for pigs. Quite pricey; the Farmer better have the GP to cover the costs...',
        'price': 500,
    },
    'AXE': {
        'name':'AXE',
        'description': 'An axe made for chopping wood. Covered in rust and in need of some serious maintenance. Not sure what a bear was doing with this in the first place though...',
    },
    'SHARP AXE': {
        'name':'SHARP AXE',
        'description': 'An axe made for chopping wood. Freshly sharpened by the Village Smith. Should have no trouble cutting through any tree or plant now.',
    },
    'PENDANT': {
        'name': 'PENDANT',
        'description': 'A round silver PENDANT with the words "for my love" engraved on the back. Found stuck in an olive tree burl. Who knows how many years it has been there?',
    },
    'SALMON': {
        'name':'SALMON',
        'description':'A not so lucky fish found at the Waterfall. Could make for a tasty meal.',
    },
    'GOBLIN FINGER': {
        'name':'GOBLIN FINGER',
        'description': 'A finger procured from the Goblin Queen as evidence to the Village Smith of her demise... Really nasty that you just have this loose in your bag, you know.',
    },
    'IRON KEY': {
        'name': 'IRON KEY',
        'description':'A small key made of iron. Dropped from a pesky Hobgoblin.',
    },
    'DRAGON BONE KEY': {
        'name':'DRAGON BONE KEY',
        'description':'A key made of Dragon bone. Dragon Bone Keys are said to be used to secure magical seals.',
    },
    'GILDED DRAGON BONE KEY': {
        'name':'GILDED DRAGON BONE KEY',
        'description': 'A key made of Dragon bone. Dragon Bone Keys are said to be used to secure magical seals. This one has been covered in a layer of thin gold.',
    },
    'ROYAL JELLY': {
        'name': 'ROYAL JELLY',
        'description':'A jar of Giant Bee Royal Jelly. This substance is capable of enhancing the healing properties of potions. Just a tiny bit mixed in will greatly increase the potancy.',
    },
    'STRANGE JELLY': {
        'name': 'STRANGE JELLY',
        'description':'A jar of Giant Bee Royal Jelly. This substance is capable of enhancing the healing properties of potions. This jelly has an unusually vibrant red colouring.',
    },
    'MOUTH-PIECE': {
        'name':'MOUTH-PIECE',
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
    'STRANGE GREASE': {
        'name':'STRANGE GREASE',
        'description':'A strange grease found in the Waterfall Cave after defeating the River Serpent. Perhaps you should ask a SMITH about it...',
    },
    'MAGIC GREASE': {
        'name':'MAGIC GREASE',
        'description': 'A strange grease found in the Waterfall Cave after defeating the River Serpent. Blades coated in it seem to never rust and retain their edge indefinitely.',
    },
    'SERPENTS EYE': {
        'name':'SERPENTS EYE',
        'description':'An eye plucked from the River Serpent. This trophy was requested by the old Captain as retribution for his lost eye from many years ago. Hopefully it was worth the trouble to get this nasty thing.',
    },
}

shop_items = [
    'POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 
]
shop_keyItems = [
    'MAP', 'LANTERN', 'CRAFTING POUCH', 'SPECIAL FEED', 'DRAGON SCALE',
    'EXTRA POUCH', 
  
  'MACE', 'OBSIDIAN DAGGER', 'ARMING SWORD', 'BROAD SWORD', 'SIDE SWORD', 'HANGER', 

  'PARMA', 'BATTLE AXE', 'STAFF', 'CLOAK',
  
  'POINTED HAT', 'COWL', 'LEATHER CAP', 'BASCINET', 'SALLET', 
  
  'MAGIC ROBE', 'GAMBESON', 'STEEL MAIL', 'BRIGANDINE', 'OLD CUIRASS',
  
    'MYTHRIL MAIL', 'ORICHALCUM BRIGANDINE', 'ADAMANTITE CUIRASS', 
  
  'LEATHER BOOTS', 'VELVET SLIPPERS', 'CUISSES', 'CHAUSSES', 'GREAVES',
  
  'GORGET',
]

travelingMerchant_items = ['POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 'MAP', 'LANTERN', 'GORGET', 'OBSIDIAN DAGGER', 'VELVET SLIPPERS' ]


mainHand_equipment = [
    'RUSTY DAGGER', 'MESSER', 'MACE', 'GOBLIN CHOPPER',
    'OBSIDIAN DAGGER', 'ARMING SWORD', 'BROAD SWORD', 'SIDE SWORD', 'HANGER', 'AETHON', 'FULGUR', 'MIDAS', 'ADAMANTITE SWORD'
]

offHand_equipment = [
    'BUCKLER', 'PARMA', 'BATTLE AXE', 'STAFF', 'CLOAK'
]

head_equipment = [
    'POINTED HAT', 'COWL', 'LEATHER CAP', 'BASCINET', 'SALLET',
]

chest_equipment = [
    'MAGIC ROBE', 'GAMBESON', 'STEEL MAIL', 'BRIGANDINE', 'OLD CUIRASS',
    'MYTHRIL MAIL', 'ORICHALCUM BRIGANDINE', 'ADAMANTITE CUIRASS'
]

legs_equipment = [
  'LEATHER BOOTS', 'VELVET SLIPPERS', 'CUISSES', 'CHAUSSES', 'GREAVES',
]

armor_equipment = [
    'POINTED HAT', 'COWL', 'LEATHER CAP', 'BASCINET', 'SALLET', 'MAGIC ROBE', 'GAMBESON', 'STEEL MAIL', 'BRIGANDINE', 'OLD CUIRASS',
    'MYTHRIL MAIL', 'ORICHALCUM BRIGANDINE', 'ADAMANTITE CUIRASS',  'LEATHER BOOTS', 'VELVET SLIPPERS', 'CUISSES', 'CHAUSSES', 'GREAVES'
]

accs_equipment = [
  'GORGET', 'HEROS MEDAL', 'GOLD RING', 'CRYSTAL NECKLACE', 'THORN BRACERS', 'WOLF FANG', 'CRYSTAL RING', 'GOLD HAIRPIN', 'MAGIC CIRCLET', 'DRAGON HEART'
]



crafting_items = {
    '': {
        'name': '',
        'description': '',
    },
    'PLANT PARTS': {
        'name':
        'PLANT PARTS',
        'description':
        'Various parts of magical plants. Commonly harvested from plant type enemies.',
    },
    'MONSTER GUTS': {
        'name':
        'MONSTER GUTS',
        'description':
        'A mix of different monster organs and body parts. Really weird that you just carry this stuff with you.',
    },
    'RARE MONSTER PARTS': {
        'name':
        'RARE MONSTER PARTS',
        'description':
        "These uncommon monster parts are highly prized. Still weird that you're carring them with you.",
    },
    'FAE DUST': {
        'name':
        'FAE DUST',
        'description':
        'A glistening powder found on creatures of the fae like Fairies and Pixies. A common source of magical energy.',
    },
    'DRAGON SCALES': {
        'name':

        'DRAGON SCALES',
        'description':
        "The scales of Dragons are incredibly hard to come by. Prying one off a dragon, live or dead, is nearly impossible before they're already loose, and these are rarely shed. The inner surface is a beautiful shifting rainbow.",
    },
}
