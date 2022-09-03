import random
import os
import sys
from slowprint import *
goblin_mobs = ["Goblin", "Hobgoblin", "Goblin Gang", "Goblin Queen", "Zomblin", "Moldy Zomblin"]
fae_mobs = ['Gnome', 'Traveling Merchant', 'Imp', 'Pixie', 'Fairy', 'Nymph', 'Dark Fairy Prince' ]

rounds = 0
player_special = None
foe_special = None
def standard_battle(p1, foe, typingActive):   
      global battle
      global turn_count
      global player_turn
      global enemy_turn
      global player_wait
      global foe_wait
      global focus
      global focus_turns
      global command
      global haste
      haste = 0
      focus_turns = 0
      turn_count = 1
      player_wait = 0
      foe_wait = 0
      damage = 0
      focus = 1
      enemy_turn = 0
    
      print_slow("\n**********COMBAT START**********", typingActive)
      print_slow(f"\nYou encounter a {foe.name}!\n", typingActive)
      p1.stat_sCheck(typingActive)
      foe.stat_check(typingActive)
  
      battle = 'ACTIVE'
      while battle == 'ACTIVE':
        print_slow(f"********** Turn[{turn_count}] **********\n", typingActive)
        #Posion effects and player death
        if focus_turns > 0:
          focus_turns -= 1
          print_slow(f'{p1.name} is powered up for {focus_turns} more turns.\n',typingActive)
        if focus_turns < 0:
          focus_turns += 1
          print_slow(f'{p1.name} is weakend for {focus_turns} more turns.\n',typingActive)
        if focus_turns == 0:
          focus = 1
        player_turn = 1
        poison_effect(p1, foe, typingActive)
        player_death(p1, typingActive)       
        #Start of player turn
        while player_turn == 1:       
          if player_wait == 0:
            print_slow("Type battle command or type HELP for command list:\n", typingActive) 
            command = (input().upper())
            print_slow("", typingActive)
          #Attack command
            if command == "ATK":
                dam = random.randrange((p1.ATK // 4), p1.ATK)
                damage = max(
                    round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * focus),
                    0)
                foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
                print_slow(
                    f'{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive
                )
                turn_update(p1, foe, typingActive)
                break
            #Use item command
            elif command == "ITEM":
                use_item(p1, foe, typingActive)
                turn_update(p1, foe, typingActive)
                break
    
            #DEF Command
            elif command == "DEF":
                block = max(min(p1.DEF * 1.2, 85), 50)
                p1.TDEF -= block 
                print_slow(f'{p1.name} is defending!\n', typingActive)
                turn_update(p1, foe, typingActive)
                break
    
            #Flee Command
            elif command == "FLEE" and foe.boss == 0:
                if p1.SMB > 0:
                  p1.SMB -= 1
                  print_slow(f'{p1.name} threw a SMOKE BOMB and escaped from combat! \n', typingActive)
                  battle = 'INACTIVE'
                  break
                elif p1.SMB <= 0:
                  print_slow(f'{p1.name} is out of SMOKE BOMBS and is unable to escape at this time \n', typingActive)
    
            elif command == "FLEE" and foe.boss == 1:
                print_slow(f'{p1.name} is unable to escape from the boss!\n', typingActive)
    
            #Player skills commands
            elif command in p1.skills and p1.MP > 0:
                if command == "HARDEN":
                    warrior_harden(p1, foe, typingActive)
                elif command == "STRIKE":
                    warrior_wildstrikes(p1, foe, typingActive)
                elif command == "BERSERK":
                    warrior_berserk(p1, foe, typingActive)
                elif command == "BLOOD":
                    warrior_bloodlust(p1, foe, typingActive)
                elif command == "BOLT":
                    wizard_spell(p1, foe, typingActive)
                elif command == "FOCUS":
                    wizard_focus(p1, foe, typingActive)
                elif command == "STORM":
                    wizard_storm(p1, foe, typingActive)
                elif command == "BLAST":
                    wizard_blast(p1, foe, typingActive)
                elif command == "STEAL":
                    thief_steal(p1, foe, typingActive)
                elif command == "THROW":
                    thief_poisondagger(p1, foe, typingActive)
                elif command == "MUG":
                    thief_mug(p1, foe, typingActive)
                elif command == "HASTE":
                    thief_haste(p1, foe, typingActive)
                turn_update(p1, foe, typingActive)
                break
            #Out of MP for skill
            elif command in p1.skills and p1.MP == 0:
                print_slow(f'{p1.name} is out of MP and unable to use their SKILL \n', typingActive)
            #Player needs help
            elif command == "STATS":
                p1.stat_check(typingActive)
                foe.stat_check(typingActive)
            elif command == "HELP":
                combat_menu(p1, typingActive)
            else:
                print_slow('That command is invalid.\n', typingActive)
              
          elif player_wait == 1:
            player_special(p1, foe, typingActive)
            turn_update(p1, foe, typingActive)
            break
        #Start of enemy turn      
        enemy_death(p1, foe, command, damage, typingActive)
        while enemy_turn == 1:
          command2 = random.randrange(0, 7)
          
          #Enemy Commands [1]
          #ATTACK
          if foe_wait == 0:
            if command2 <= 2:  
                dam = random.randrange(foe.ATK // 3, foe.ATK)
                damage = max(round(dam * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
                p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
                print_slow(f'The enemy {foe.name} ATTACKS.\n', typingActive)
                print_slow(
                    f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
                )
                p1.TDEF = 100
                enemy_turn = 0
                break
            #DEFEND
            elif command2 == 3 or command2 == 4:  
                foe.TDEF = max(min(foe.DEF * 1.2, 85), 50)
                print_slow(f'The enemy {foe.name} DEFENDS\n', typingActive)
                print_slow(f'{foe.name} has raised its defenses! \n', typingActive)
                p1.TDEF = 100
                enemy_turn = 0
                break
            #HEAL
            elif (command2 == 5 and foe.POTS > 0) and foe.HP < foe.MaxHP:  
                print_slow(f'The enemy {foe.name} HEALS\n', typingActive)
                heal = random.randrange(5, 10)
                foe.HP = min(max(foe.HP + heal, 0), foe.MaxHP)
                foe.POTS -= 1
                print_slow(
                    f'{foe.name} has healed {heal} HP. {foe.name} has {foe.HP}/{foe.MaxHP} HP\n', typingActive
                )
                p1.TDEF = 100
                enemy_turn = 0
                break
            #SKILL
            elif command2 == 6 and foe.MP > 0:  
                enemy_skills(p1, foe, typingActive)
                enemy_turn = 0
                break
            else:
                pass
          if foe_wait == 1:
            foe_special(p1, foe, typingActive)
            enemy_turn = 0
            break
            
def turn_update(p1, foe, typingActive):
  global turn_count
  global player_turn
  global enemy_turn
  global haste
  global command

  if haste > 0 and command == 'HASTE':
    pass
  if haste > 0 and command != 'HASTE':
    haste -= 1
    if haste != 0:
      print_slow(f'{p1.name} has {haste} more action(s) this turn.\n',typingActive)
  if haste == 0:
    foe.TDEF = 100
    turn_count += 1
    player_turn = 0
    enemy_turn = 1
  
#Poison effect    
def poison_effect(p1, foe, typingActive):
  command = None
  if p1.POISON > 0:
      damage = p1.MaxHP // 25
      p1.HP = p1.HP - damage
      p1.POISON = max(p1.POISON - 1, 0)
      print_slow(
          f"{p1.name} is suffering from the effects of poison! {p1.name} takes {damage} poison damage. {p1.name} has {p1.HP}/{p1.MaxHP}HP\n", typingActive
      )
      player_death(p1, typingActive)
  if foe.POISON > 0:
      damage = foe.MaxHP // 25
      foe.HP = foe.HP - damage
      foe.POISON = max(foe.POISON - 1, 0)
      print_slow(
          f"{foe.name} is suffering from the effects of poison! {foe.name} takes {damage} poison damage. {foe.name} has {foe.HP}/{foe.MaxHP}HP\n", typingActive
      )
      enemy_death(p1, foe, command, damage, typingActive)
    
#Player death
def player_death(p1, typingActive):
  if p1.HP <= 0:
    p1.alive = "dead"
    print_slow(f'\n{p1.name} is DEAD\n', typingActive)
    print_slow('\n Do you wish to retry? YES or NO\n', typingActive)
    while p1.alive == "dead":
        restart = (input().upper())
        if restart == 'YES':
            sys.stdout.flush()
            os.execv(sys.executable, ['python'] + sys.argv)
        elif restart == 'NO':
            quit()
        else:
            print_slow('Please select YES or NO.\n', typingActive)

#Enemy Death
def enemy_death(p1, foe, command, damage, typingActive):
  global battle
  global enemy_turn
  global player_turn
  if foe.HP <= 0:
      enemy_turn = 0
      player_turn = 0
      GPE = round(random.randrange(foe.MinGP, foe.MaxGP) * p1.GR)
      p1.GP = p1.GP + GPE
      p1.xp = p1.xp + foe.exp
      if foe.name in goblin_mobs:
          p1.gobCount += 1
      if foe.name in fae_mobs:
          p1.faeCount += 1
      if command == "BOLT":
          print_slow(f'{p1.name} vaporized the enemy!\n', typingActive)
      elif damage >= foe.MaxHP // 2:
          print_slow(f'{p1.name} obliterated the enemy!\n', typingActive)
      elif command == "STRIKE":
          print_slow(f'{p1.name} pulverised the enemy!\n', typingActive)
      else:
          print_slow(f'{p1.name} defeated the enemy.\n', typingActive)
      print_slow(
          f'{p1.name} gained {GPE}GP and {foe.exp}EXP. {p1.name} has {p1.GP}GP\n', typingActive
      )
      mug = 1
      item_drop(p1, foe, mug, typingActive)
      p1.level_up(typingActive)
      print_slow("********** VICTORY!!! **********\n", typingActive)
      foe.HP = foe.MaxHP
      foe.POTS = foe.MaxPOTS
      foe.MP = foe.MaxMP
      foe.POISON = 0
      p1.POISON = 0
      battle = 'INACTIVE'

def item_drop(p1, foe, mug, typingActive):
      inv = "CLOSED"
      itemDrop = random.randrange(1,100)
      if itemDrop > foe.drop // mug:
        if 'CRAFTING POUCH' in p1.inventory:
          inv = "OPEN"
          if foe.item == 1:
            p1.PlantP += 1
            spoils = "PLANT PART"
          if foe.item == 2:
            p1.MonP += 1
            spoils = "MONSTER PART"
          if foe.item == 3:
            p1.RareP += 1
            spoils = "RARE MONSTER PART"
          if foe.item == 4:
            p1.FaeP += 1
            spoils = "FAE DUST"
          if foe.item == 5:
            p1.DragonP += 1
            spoils = "DRAGON SCALE"
        if foe.item == 6:
          if p1.POTS < p1.MaxPOTS:
            p1.POTS = min(p1.POTS + 1, p1.MaxPOTS)
            spoils = "POTION"
          else:
            inv = "FULL"
        if foe.item == 7:
          spoils = "ANTIDOTE"
          if p1.ANT < p1.MaxANT:
            p1.ANT = min(p1.ANT + 1, p1.MaxANT)
            inv = "OPEN"
          else:
            inv = "FULL"
        if foe.item == 8:
          spoils = "ETHER"
          if p1.ETR < p1.MaxETR:
            p1.ETR = min(p1.ETR + 1, p1.MaxETR)
            inv = "OPEN"
          else:
            inv = "FULL"
        if foe.item == 9:
          spoils = "SMOKE BOMB"
          if p1.SMB < p1.MaxSMB:
            p1.SMB = min(p1.SMB + 1, p1.MaxSMB)
            inv = "OPEN"
          else:
            inv = "FULL"
        if foe.item == 10:
          spoils = "WAFFLE"
          if mug == 1 and 'WAFFLE' not in p1.inventory:
            inv = "OPEN"
            p1.inventory.append('WAFFLE')
          else:
            inv = "FULL"
        
        if inv == "OPEN":
          if mug == 1:
            print_slow(f'The enemy {foe.name} dropped a {spoils}.\n', typingActive)
            print_slow(f'{p1.name} has added the {spoils} to their inventory.\n', typingActive)
          if mug == 2:
            print_slow(f'{p1.name} stole a {spoils} from the enemy {foe.name}!\n', typingActive)
            print_slow(f'{p1.name} has added the {spoils} to their inventory.\n', typingActive)
      if inv == "CLOSED" and mug == 2:
        print_slow(f'{p1.name} failed to steal anything.\n', typingActive)  
      if inv == "FULL":
        print_slow(f"{foe.name} dropped a {spoils}, however {p1.name}'s inventory is full.\n", typingActive)  
#Use item menu
def use_item(p1, foe, typingActive): 
  items_list = "ON"
  while items_list == "ON":
      print_slow(
          f"Select item to use or BACK to return to battle commands:\nPOTION: {p1.POTS}\nANTIDOTE: {p1.ANT}\nETHER: {p1.ETR}\n", typingActive
      )
      command = (input().upper())
      if command == "POTION" and p1.POTS > 0:
          heal = random.randrange(5, 16) + p1.RJ
          p1.POTS -= 1
          p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
          items_list = "OFF"
          print_slow(f'{p1.name} drinks a POTION and heals {heal} HP. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
      elif command == "ANTIDOTE" and p1.ANT > 0:
          p1.ANT -= 1
          p1.POISON = 0
          items_list = "OFF"
          print_slow(f"{p1.name} drinks an ANTIDOTE and is relieved of POISON!\n", typingActive)
      elif command == "ETHER" and p1.ETR > 0:
          heal = random.randrange(3, 6)
          p1.ETR -= 1
          p1.MP = min(max(p1.MP + heal, 0), p1.MaxMP)
          items_list = "OFF"
          print_slow(f"{p1.name} drinks an ETHER and restores {heal} MP. {p1.name} has {p1.MP}/{p1.MaxMP} MP. \n", typingActive)
      elif command == "POTION" and p1.POTS == 0:
          print_slow('Unable to use a POTION at this time.\n', typingActive)
      elif command == "ANTIDOTE" and p1.ANT == 0:
          print_slow('Unable to use an ANTIDOTE at this time.\n', typingActive)
      elif command == "ETHER" and p1.ETR == 0:
          print_slow('Unable to use an ETHER at this time.\n', typingActive)
      elif command == "BACK":
          items_list = "OFF"
      else:
          print_slow('That command is invalid.\n', typingActive)

#Warrior skill effects
def warrior_harden(p1, foe, typingActive):
    heal = random.randrange(p1.MaxHP // 10, p1.MaxHP // 3)
    p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
    p1.TDEF = max(p1.DEF, 3) 
    p1.MP -= 1
    print_slow(
        f'{p1.name} has bolstered their constitution. {p1.name} healed {heal} HP and shielded themself this turn. {p1.name} has {p1.HP}/{p1.MaxHP} HP \n', typingActive
    )

def warrior_wildstrikes(p1, foe, typingActive):
    print_slow(f'{p1.name} strikes at the enemy {foe.name} with a mighty blow!\n', typingActive)
    hit = random.randrange(0, 4)
    if hit >= 1:
        dam = random.randrange(p1.ATK // 3, p1.ATK)
        damage1 = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01)) * 2, 0)
        print_slow(f'{p1.name} strikes for {damage1} damage!\n', typingActive)
    else:
      print_slow(f'{p1.name} swings and misses completely!', typingActive)


def warrior_berserk(p1, foe, typingActive):
    global player_special
    global player_wait
    global rounds
    
    if player_wait == 1:
      if rounds >= 1:
        dam = random.randrange((p1.ATK // 2), round(p1.ATK * 1.8))
        damage = max(
            round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01)), 0)
        foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
        print_slow(f'{p1.name} attacks madly!\n',typingActive)
        print_slow(
            f'{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive
        )
        rounds -= 1
      if rounds == 0:
        player_wait = 0
      return
    if player_wait == 0:
      rounds = random.randrange(2, 4)
      player_wait = 1
      player_special = warrior_berserk
      p1.MP -= 1
      print_slow(f'{p1.name} is fueled by rage. {p1.name} has gone BERSERK for {rounds} turns!\n', typingActive)
      
#Wizard skill effects
def warrior_bloodlust(p1, foe, typingActive):
        dam = random.randrange((p1.ATK // 3), round(p1.ATK * 1.3))
        damage = max(
            round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01)), 0)
        foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
        p1.HP = min(p1.HP + (damage // 2), p1.MaxHP)
        print_slow(f'{p1.name} is filled with a bloodlust!',typingActive)
        print_slow(
            f"{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n{p1.name} has abosrbed the enemy {foe.name}'s life force! {p1.name} gains {damage // 2} HP. {p1.name} has {p1.HP}/{p1.MaxHP}\n", typingActive
        )
        p1.MP -= 2

#Wizard skill effects
def wizard_spell(p1, foe, typingActive):
    global focus
    dam = random.randrange(p1.ATK, round(p1.ATK * 1.5))
    damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * focus), 0)
    foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
    p1.MP -= 1
    print_slow(
        f'{p1.name} casts a magical bolt at the enemy {foe.name}.\n{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive
    )

def wizard_focus(p1, foe, typingActive):
    global focus
    global focus_turns
    focus = 1.5
    focus_turns = random.randrange(2, 6)
    p1.MP -= 1
    print_slow(f'{p1.name} focuses their power. {p1.name} is powered up for {focus_turns - 1} turns!\n', typingActive)
        
def wizard_storm(p1, foe, typingActive):
    global focus
    print_slow(f'{p1.name} conjuers a fierce lightning storm!\n', typingActive)
    storm_hits = 0
    tl_damage = 0
    while storm_hits < 3:
      hit = random.randrange(0, 4)
      if hit >= 1:
          dam = random.randrange(p1.ATK // 2.5, p1.ATK)
          damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * focus, 0))
          tl_damage = tl_damage + damage
          storm_hits += 1
          print_slow(f'Lighting strikes for {damage} damage!\n', typingActive)
      else:
          print_slow('lightning strikes and misses!\n', typingActive)
    foe.HP = min(max(foe.HP - tl_damage, 0), foe.MaxHP)
    p1.MP -= 1
    print_slow(
        f'{foe.name} has taken {tl_damage} total damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive
    )
def wizard_blast(p1, foe, typingActive):
    print_slow(f'{p1.name} concentrates their magic!\n', typingActive)
    hit = random.randrange(0, 6)
    if hit >= 4:
        damage = foe.HP // 4
        foe.HP -= damage
        print_slow(f'{p1.name} blasts the enemy {foe.name} away for {damage} damage!\n', typingActive)
    else:
        print_slow(f'{p1.name} magical energy fizzles out...\n', typingActive)
    p1.MP -= 2
  
#Thief skill effects
def thief_steal(p1, foe, typingActive):
    mug = random.randrange(0, 5)
    if mug >= 2:
        GPE = round(random.randrange(foe.MinGP, round(foe.MaxGP * 0.8)) * p1.GR)
        p1.GP = p1.GP + GPE
        p1.MP -= 1
        print_slow(
            f'{p1.name} manages to steal {GPE}GP from the enemy {foe.name}. {p1.name} now has {p1.GP}GP.\n', typingActive
        )
    elif mug == 1:
        p1.MP -= 1
        print_slow(f'{p1.name} failed to steal anything!\n', typingActive)
    elif mug == 0:
        p1.MP -= 1
        bribe = foe.MinGP // 3
        p1.GP = p1.GP - bribe
        print_slow(f'{p1.name} failed to steal anything and dropped {bribe}! \n', typingActive)

def thief_poisondagger(p1, foe, typingActive):
    dagger = 0
    print_slow(f'{p1.name} throws a handful of poison daggers!\n', typingActive)
    hit = random.randrange(0, 3)
    if hit >= 1:
        foe.POISON += 2
        dagger += 1
        damage1 = round(p1.ATK // 8)
    else:
        damage1 = 0
    hit = random.randrange(0, 3)
    if hit >= 1:
        foe.POISON += 2
        dagger += 1
        damage2 = round(p1.ATK // 8)
    else:
        damage2 = 0
    hit = random.randrange(0, 3)
    if hit >= 1:
        foe.POISON += 2
        dagger += 1
        damage3 = round(p1.ATK // 8)
    else:
        damage3 = 0
    tl_damage = damage1 + damage2 + damage3
    foe.HP = min(max(foe.HP - tl_damage, 0), foe.MaxHP)
    p1.MP -= 1
    print_slow(
        f'{p1.name} hit the enemy {foe.name} with {dagger} poison dagger(s)! The enemy {foe.name} has taken {tl_damage} total damage and is poisoned for {foe.POISON} turns. {foe.name} has {foe.HP}/{foe.MaxHP} HP\n', typingActive
    )

def thief_mug(p1, foe, typingActive):
    print_slow(f'{p1.name} mugs the enemy {foe.name}!', typingActive)
    dam = random.randrange((p1.ATK // 3.5), p1.ATK)
    damage = max(
        round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * focus),
        0)
    foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
    print_slow(f'{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
    p1.MP -= 1
    mug = 2
    item_drop(p1, foe, mug, typingActive)
#Enemy skills
def thief_haste(p1, foe, typingActive):
  global haste
  if haste == 0:
    print_slow(f"{p1.name}'s adrenalin is pumping! {p1.name} gains additional actions this turn.\n", typingActive)
    haste = 2
    p1.MP -= 2
    print_slow(f'{p1.name} has {haste} more action(s) this turn.\n',typingActive)
  else:
    print_slow('Unable to use skill twice in a row.', typingActive)
    print_slow(f'{p1.name} has {haste} more action(s) this turn.\n',typingActive)


#def summoner_
def enemy_skills(p1, foe, typingActive):
    global battle
    global foe_special
    global foe_wait
    global focus
    global focus_turns
  
    if foe.skill == 1:  #FLee
        escape = random.randrange(0, 4)
        if escape >= 2:
            battle = 'INACTIVE'
            print_slow(
                f'The enemy {foe.name} scuttles away! You earn nothing. Sucks to suck.\n', typingActive
            )
            print_slow("**********Enemy Escape!**********\n", typingActive)
            foe.HP = foe.MaxHP
            foe.MP = foe.MaxMP
            foe.POTS = foe.MaxPOTS
            foe.POISON = 0
            p1.POISON = 0
        else:
            print_slow(
                f'Enemy {foe.name} attempted to escape but stumbled and failed!\n', typingActive
            )
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 2:  #Cleave
        dam = random.randrange(round(foe.ATK // 1.5), foe.ATK)
        damage = max(round(dam * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        print_slow(f'The enemy {foe.name} strikes with a cleaving blow!\n', typingActive)
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 3:  #Maul
        dam = random.randrange(foe.ATK // 2, foe.ATK)
        damage = damage = max(round(dam + 3 * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        print_slow(f'The enemy {foe.name} charges wildly and mauls {p1.name}!\n', typingActive)
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 4:  #Magic Bolt
        dam = random.randrange(foe.ATK, round(foe.ATK * 1.3))
        damage = max(round(dam * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        print_slow(
            f'The enemy {foe.name} concentrates their power into a magic bolt and hurls it at {p1.name}!\n', typingActive
        )
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 5:  #Steal
        pilfer = random.randrange(0, 3)
        if pilfer >= 2:
            GPL = random.randrange(foe.MinGP, round(foe.MaxGP // 1.5))
            p1.GP = p1.GP + GPL
            print_slow(
                f'The enemy {foe.name} manages to steal {GPL}GP from {p1.name}. {p1.name} now has {p1.GP}GP.\n', typingActive
            )
        elif pilfer < 2:
            print_slow(
                f'{foe.name} attempted to steal but failed to grab anything!\n', typingActive
            )
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 6:  #Fire Breath
      while True:
        if foe_wait == 1:
          dam = random.randrange(foe.ATK, round(foe.ATK * 1.2))
          damage = max(round(dam + 6 * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
          p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
          
          print_slow(
              f"Fire bellows from the enemy {foe.name}'s mouth, scorching '{p1.name}!\n", typingActive
          )
          print_slow(
              f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP remaining. \n', typingActive
          )
          foe_wait = 0
          p1.TDEF = 100
          break
        if foe_wait == 0:
          
          foe_special = enemy_skills
          print_slow(f'Smoke begins raising from {foe.name} mouth...\n', typingActive)
          foe_wait = 1
          p1.TDEF = 100
          foe.MP -= 1
          break

    elif foe.skill == 7:  #Sting
        dam = random.randrange(foe.ATK // 2 + 4, foe.ATK + 4)
        damage = max(round(dam * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
        pdamage = random.randrange(1, 3)
        p1.POISON += pdamage
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        damage2 = 5
        foe.HP = min(max(foe.HP - damage2, 0), foe.MaxHP)

        print_slow(f'The enemy {foe.name} rushes at {p1.name} with their stinger!\n', typingActive)
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )
        print_slow(
            f'{foe.name} has taken {damage2} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP. \n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1
        if foe.HP <= 0:
            print_slow(f'{foe.name} killed themself.\n', typingActive)
            command = None
            enemy_death(p1, foe, command, damage, typingActive)
          
    elif foe.skill == 8:  #Poison Mist
        pdamage = random.randrange(1, 4)
        p1.POISON += pdamage
        print_slow(
            f'{foe.name} spews a poison mist at {p1.name}! {p1.name} is poisoned for {pdamage} turns.\n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 9:  #Quake
        damage = max(
            random.randrange(round(foe.ATK // 2), round(foe.ATK * 0.8)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        print_slow(
            f'The enemy {foe.name} strikes with the ground causing a mighty quake!\n', typingActive
        )
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 10:  #Summon Swarm
        print_slow(
            f'{foe.name} summons a swarm of smaller BEES to attack {foe.name}.\n', typingActive
        )
        bee_hits = 0
        tl_damage = 0
        while bee_hits < 3:
          hit = random.randrange(0, 4)
          if hit >= 1:
              dam = random.randrange(foe.ATK // 2, foe.ATK // 1.5)
              damage = max(round(dam * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
              tl_damage = tl_damage + damage
              p1.POISON += 1
              bee_hits += 1
              print_slow(f'{p1.name} is stung for {damage} damage and is poisoned!\n', typingActive)
          else:
              print_slow(f'{p1.name} swats a BEE away!\n', typingActive)
        p1.HP = min(max(p1.HP - tl_damage, 0), p1.MaxHP)    
        print_slow(
            f'{p1.name} has taken {tl_damage} total damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n{p1.name} is poisoned for the next {p1.POISON} turns.', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 11:  #Roar
        print_slow(
            f"{foe.name} lets out a ferocious roar reducing {p1.name}'s defenses temporarily!\n", typingActive
        )
        p1.TDEF = 150
        foe.MP -= 1

    elif foe.skill == 12:  #Kancho
        print_slow(
            f"{foe.name} grabs {p1.name} from behind!\n", typingActive
        )
        hit = random.randrange(0, 4)
        if hit >= 2:
            dam = random.randrange(foe.ATK // 3, foe.ATK // 1.5)
            damage = max(round(dam * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
            foe.HP = min(max(foe.HP + damage // 2, 0), foe.MaxHP)
            print_slow(f'{p1.name} has their life force ripped from their body and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n{foe.name} consumes the life force and gains {damage//2} HP! {foe.name} has {foe.HP}/{foe.MaxHP}.\n', typingActive)
        else:
            print_slow(f"{p1.name} escapes the {foe.name}'s hold!\n", typingActive)      
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 13:  #Poison Bite
        dam = random.randrange(foe.ATK // 2.5, foe.ATK)
        damage = max(round(dam * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        pdamage = random.randrange(1, 4)
        p1.POISON += pdamage
        print_slow(
            f'{foe.name} bites down on {p1.name} with their toxic fangs! {p1.name} is poisoned for {pdamage} turns and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif foe.skill == 14:  #dales pocket sand
        focus = .7
        focus_turns = -4
        print_slow(f"{foe.name} throws a blue powder in {p1.name}'s face! {p1.name} has their power lowered for {(focus_turns * -1) + 1} turns!\n", typingActive)
        p1.TDEF = 100
        foe.MP -= 1
      
    elif foe.skill == 15:  #Skewer
        print_slow(f'The enemy {foe.name} charges forward with their weapon and skewers {p1.name}!\n', typingActive)
        hit = random.randrange(0, 4)
        dam = random.randrange(round(foe.ATK // 2), foe.ATK)
        damage = max(round(dam * (p1.DEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        if hit >= 2:
          print_slow(f"The enemy {foe.name} manages to break through {p1.name}'s armor'! {p1.name}'s defenses are temporarily lowered.\n", typingActive)
          p1.TDEF += 5
        elif hit < 2:
          print_slow(f"{p1.name}'s armor saved them from being impaled!\n", typingActive)
          p1.TDEF = 100
        print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
        foe.MP -= 1

#Help menu for combat
def combat_menu(p1, typingActive):
  if p1.job == "WARRIOR":
      warrior_menu = "Battle commands:\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\nHARDEN: Restore some HP, temp. increase def for 1 turn.\n"
      if p1.lvl >= 2:
        warrior_menu += 'STRIKE: Wildy strike foe for high damage. Chance to miss.\n'
      if p1.lvl >= 5:
        warrior_menu += 'BERSERK: Become blinded by range for several turns. Can only attack while berserk, but damage is increased.\n'
      print_slow(warrior_menu, typingActive)
      if p1.lvl >= 10:
        warrior_menu += 'BLOOD: Become filled with a lust for blood. Absorb 50% of damage dealt as HP.\n'
      print_slow(warrior_menu, typingActive)
  
  elif p1.job == "WIZARD" or p1.job == "WITCH":
      wizard_menu = "Battle commands:\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\nFOCUS: Concentrates to increase damage of follow up attacks for several turns."
      if p1.lvl >= 2:
        wizard_menu += "\nBOLT: Cast magical bolt dealing high damage.\n"
      if p1.lvl >= 5:
        wizard_menu += "\nSTORM: Cast magical storm, hitting the enemy multiple times. Chance to miss.\n"
      print_slow(wizard_menu, typingActive)
      if p1.lvl >= 10:
        wizard_menu += "\nBLAST: Send a concentrated magical blast at the enemy. Damaged based on enemy HP; high chance to miss.\n"
      print_slow(wizard_menu, typingActive)

  elif p1.job == "THIEF":
      thief_menu = "Battle commands:\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\n\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\nSTEAL: Steal GP from enemy. Chance to fail.\n"
      if p1.lvl >= 2:
        thief_menu =+ 'THROW: Throw up to 3 poison daggers at the enemy. Deals damage and poisons.\n'
      if p1.lvl >= 5:
        thief_menu =+ 'MUG: Attack enemy and steal item from enemy. Chance stealing may fail.\n'
      if p1.lvl >= 10:
        thief_menu =+ 'HASTE: Spend 2 MP to use 2 actions in the same turn. Does not stack.\n'
      print_slow(thief_menu, typingActive)