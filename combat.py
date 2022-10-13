import random
import os
import sys
from slowprint import *
goblin_mobs = ["Goblin", "Hobgoblin", "Goblin Gang", "Goblin Queen", "Zomblin", "Moldy Zomblin"]
fae_mobs = ['Gnome', 'Traveling Merchant', 'Imp', 'Pixie', 'Fairy', 'Nymph', 'Dark Fairy Prince' ]

combat_skills = {
  'HARDEN' : {'MP' : 1,}, 
  'STRIKE': {'MP' : 1,},
  'BERSERK': {'MP' : 1,}, 
  'BLOOD': {'MP' : 2,}, 
  'BATTLECRY': {'MP' : 2,}, 
  'BOLT': {'MP' : 1,}, 
  'FOCUS': {'MP' : 1,}, 
  'STORM': {'MP' : 1,}, 
  'BLAST': {'MP' : 2,}, 
  'SHOCK': {'MP' : 3,}, 
  'STEAL': {'MP' : 1,}, 
  'THROW': {'MP' : 1,}, 
  'MUG': {'MP' : 1,}, 
  'HASTE': {'MP' : 2,}, 
  '$TOSS': {'MP' : 1,}, }
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
      global cDEF
      global foe_powerdebuff
      global playerDefault_ATK
      global playerDefault_DEF
      global enemyDefault_ATK
  
      foe_powerdebuff = 0
      haste = 0
      focus_turns = 0
      turn_count = 1
      player_wait = 0
      foe_wait = 0
      wait_skill = 0
      damage = 0
      focus = 1
      enemy_turn = 0
  
      cDEF = max(p1.DEF - p1.GDEF, 25)
      playerDefault_ATK = p1.ATK
      playerDefault_DEF = p1.DEF
      enemyDefault_ATK = foe.ATK
      

    
      print_slow("\n**********COMBAT START**********", typingActive)
      print_slow(f"\nYou encounter a {foe.name}!\n", typingActive)
      p1.stat_sCheck(typingActive)
      foe.stat_check(typingActive)
  
      battle = 'ACTIVE'
      while battle == 'ACTIVE':
        print_slow(f"********** Turn[{turn_count}] **********\n", typingActive)
        #Satus effects and player death
        if focus_turns > 0:
          focus_turns -= 1
          if focus > 1:
            print_slow(f'{p1.name} is powered up for {focus_turns} more turns.\n',typingActive)
          if focus < 1:
            print_slow(f'{p1.name} is weakend for {focus_turns} more turns.\n',typingActive)
          if focus_turns == 0:
            if focus < 1:
              print_slow(f'{p1.name} has recovered!\n',typingActive)
            focus = 1
        if foe_powerdebuff > 0:
          foe_powerdebuff -= 1
          if foe_powerdebuff == 0:
            print_slow(f'The enemy {foe.name} is back to full strength!\n',typingActive)
            foe.ATK = enemyDefault_ATK
        player_turn = 1
        equipment_augments(p1, foe, typingActive)
        poison_effect(p1, foe, typingActive)
        player_death(p1, typingActive)
        blind_effect(p1, foe, typingActive)
        #Start of player turn
        while player_turn == 1:       
          if player_wait == 0:
            print_slow("Type battle command or type HELP for command list:\n", typingActive) 
            command = (input().upper())
            print_slow("", typingActive)
          #Attack command
            if command == "ATK":
                hit = random.randrange(0, 101)
                if hit <= p1.ACC:
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
                elif hit > p1.ACC:
                  print_slow(
                      f'{p1.name} misses their attack!\n', typingActive
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
                block = max(min(cDEF * 1.2, 85), 50)
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
            elif command in p1.skills and p1.MP >= combat_skills[command]['MP']:
                if command == "HARDEN":
                    warrior_harden(p1, foe, typingActive)
                elif command == "STRIKE":
                    warrior_wildstrikes(p1, foe, typingActive)
                elif command == "BERSERK":
                    warrior_berserk(p1, foe, typingActive)
                elif command == "BLOOD":
                    warrior_bloodlust(p1, foe, typingActive)
                elif command == "BATTLECRY":
                    warrior_battlecry(p1, foe, typingActive)
                elif command == "BOLT":
                    wizard_bolt(p1, foe, typingActive)
                elif command == "FOCUS":
                    wizard_focus(p1, foe, typingActive)
                elif command == "STORM":
                    wizard_storm(p1, foe, typingActive)
                elif command == "BLAST":
                    wizard_blast(p1, foe, typingActive)
                elif command == "SHOCK":
                    wizard_shock(p1, foe, typingActive)
                elif command == "STEAL":
                    thief_steal(p1, foe, typingActive)
                elif command == "THROW":
                    thief_poisondagger(p1, foe, typingActive)
                elif command == "MUG":
                    thief_mug(p1, foe, typingActive)
                elif command == "HASTE":
                    thief_haste(p1, foe, typingActive)
                elif command == "COIN THROW":
                    thief_cointhrow(p1, foe, typingActive)
                turn_update(p1, foe, typingActive)
                break
            #Out of MP for skill
            elif command in p1.skills and p1.MP < combat_skills[command]['MP']:
                print_slow(f'{p1.name} does not have enough MP and is unable to use {command} \n', typingActive)
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
                hit = random.randrange(0, 101)
                if hit <= foe.ACC:
                  dam = random.randrange(foe.ATK // 3, foe.ATK)
                  damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
                  p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
                  print_slow(f'The enemy {foe.name} ATTACKS.\n', typingActive)
                  print_slow(
                      f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
                  )
                  p1.TDEF = 100
                  enemy_turn = 0
                  break
                elif hit > foe.ACC:
                  print_slow(
                      f'{foe.name} misses their attack!\n', typingActive
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
          if foe_wait >= 1:
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
def equipment_augments(p1, foe, typingActive):
  global playerDefault_ATK
  global playerDefault_DEF
  global enemyDefault_ATK
  global skill_boost
  skill_boost = 1
  foe.ACC = foe.MACC
  
  if p1.mainHand == 'AETHON':
    p1.ATK = playerDefault_ATK
    if p1.HP == p1.MaxHP:
      p1.ATK += 0
    elif (p1.MaxHP * .8) < p1.HP < p1.MaxHP:
      p1.ATK += 2
    elif (p1.MaxHP * .6) < p1.HP < (p1.MaxHP * .8):
      p1.ATK += 4
    elif (p1.MaxHP * .4) < p1.HP < (p1.MaxHP * .6):
      p1.ATK += 6
    elif (p1.MaxHP * .2) < p1.HP < (p1.MaxHP * .4):
      p1.ATK += 8
    elif 1 < p1.HP < (p1.MaxHP * .2):
      p1.ATK += 12
  if p1.mainHand == 'FULGUR':
    skill_boost += .5
  if p1.mainHand == 'MIDAS':
    p1.ATK = playerDefault_ATK
    if p1.GP <= 100:
      p1.ATK -= 8
    elif 100 < p1.GP < 250:
      p1.ATK -= 3
    elif 250 < p1.GP < 500:
      p1.ATK += 0
    elif 500 < p1.GP < 750:
      p1.ATK += 3
    elif 750 < p1.GP < 1000:
      p1.ATK += 6
    elif p1.GP >= 1000:
      p1.ATK += 8
  if p1.offHand == 'STAFF':
    skill_boost += .25
  if p1.offHand == 'CLOAK':
    foe.ACC -= 10
  if p1.accs1 == 'CRYSTAL RING' or p1.accs2 == 'CRYSTAL RING':
    skill_boost += .25
    
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
    
def blind_effect(p1, foe, typingActive):
  command = None
  if p1.BLIND > 0:
      p1.ACC = 50
      p1.BLIND = max(p1.BLIND - 1, 0)
      if p1.BLIND > 0:
        print_slow(
            f"{p1.name} is temporarily blinded! {p1.name}'s accuracy is reduced for {p1.BLIND} more turns.\n", typingActive
        )
      if p1.BLIND == 0:
        print_slow(f"{p1.name}'s vision has cleared!",typingActive)
        p1.ACC = 99
  if foe.BLIND > 0:
      foe.ACC = foe.MACC // 2
      foe.BLIND = max(foe.BLIND - 1, 0)
      if foe_special.BLIND > 0:
        print_slow(
            f"{foe.name} is temporarily blinded! {foe.name}'s accuracy is reduced for {foe.BLIND} more turns.\n", typingActive
        )
      if foe.BLIND == 0:
        print_slow(f"{foe.name}'s vision has cleared!",typingActive)
        foe.ACC = foe.MACC
 
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

def enemy_death(p1, foe, command, damage, typingActive):
  global battle
  global enemy_turn
  global player_turn
  global skill_boost
  global playerDefault_ATK
  global playerDefault_DEF
  global enemyDefault_ATK
  
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
      elif command == "STRIKE":
          print_slow(f'{p1.name} pulverised the enemy!\n', typingActive)
      elif command == "SEPPUKU":
          print_slow(f'{foe.name} defeated themself!\n', typingActive)
      elif damage >= foe.MaxHP // 2:
          print_slow(f'{p1.name} obliterated the enemy!\n', typingActive)
      else:
          print_slow(f'{p1.name} defeated the enemy.\n', typingActive)
      print_slow(
          f'{p1.name} gained {GPE}GP and {foe.exp}EXP. {p1.name} has {p1.GP}GP\n', typingActive
      )
      mug = 1
      item_drop(p1, foe, mug, typingActive)
      p1.level_up(typingActive)
      print_slow("********** VICTORY!!! **********\n", typingActive)
      combat_end_reset(p1, foe)
    
def combat_end_reset(p1, foe):
  global battle
  global enemy_turn
  global player_turn
  global skill_boost
  global playerDefault_ATK
  global playerDefault_DEF
  global enemyDefault_ATK
  foe.HP = foe.MaxHP
  foe.POTS = foe.MaxPOTS
  foe.MP = foe.MaxMP
  foe.ATK = enemyDefault_ATK
  foe.POISON = 0
  p1.ATK = playerDefault_ATK 
  p1.DEF = playerDefault_DEF
  p1.POISON = 0
  skill_boost = 1
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
          spoils = "POTION"
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
          heal = random.randrange(4, 9)
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
    p1.TDEF = max(cDEF, 3) 
    p1.MP -= 1
    print_slow(
        f'{p1.name} has bolstered their constitution. {p1.name} healed {heal} HP and shielded themself this turn. {p1.name} has {p1.HP}/{p1.MaxHP} HP \n', typingActive
    )

def warrior_wildstrikes(p1, foe, typingActive):
    print_slow(f'{p1.name} strikes at the enemy {foe.name} with a mighty blow!\n', typingActive)
    hit = random.randrange(0, 101)
    if hit <= p1.ACC - 30:
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
def warrior_battlecry(p1, foe, typingActive):
        print_slow(f"{foe.name} looks to the sky and unleashes a mighty BATTLECRY!", typingActive)
        hit = random.randrange(2,5)
        hit2 = random.randrange(1,4)
        foe_powerdebuff += hit
        if hit2 == 1:
          foe.ATK *= .9
          print_slow(f"{p1.name}'s BATTLECRY confuses the enemy {foe.name}. The enemy {foe.name}'s attack is reduced for {foe_powerdebuff - 1} turns.\n", typingActive)
        elif hit2 == 2:
          foe.ATK *= .75
          print_slow(f"{p1.name}'s BATTLECRY intimidates the enemy {foe.name}! The enemy {foe.name}'s attack is reduced for {foe_powerdebuff - 1} turns.\n", typingActive)
        elif hit2 == 3:
          foe.ATK *= .5
          print_slow(f"{p1.name}'s BATTLECRY strikes fear into the heart of the enemy {foe.name}! The enemy {foe.name}'s attack is reduced for {foe_powerdebuff - 1} turns.\n", typingActive)
        p1.MP -= 2

#Wizard skill effects
def wizard_focus(p1, foe, typingActive):
    global focus
    global focus_turns
    global skill_boost
    focus = 1.5 * skill_boost
    focus_turns = random.randrange(2, 6)
    p1.MP -= 1
    print_slow(f'{p1.name} focuses their power. {p1.name} is powered up for {focus_turns - 1} turns!\n', typingActive)

def wizard_bolt(p1, foe, typingActive):
    global focus
    global skill_boost
    dam = random.randrange(p1.ATK, round(p1.ATK * 1.5)) * skill_boost
    damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * focus), 0)
    foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
    p1.MP -= 1
    print_slow(
        f'{p1.name} casts a magical bolt at the enemy {foe.name}.\n{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive
    )

def wizard_storm(p1, foe, typingActive):
    global focus
    global skill_boost
    print_slow(f'{p1.name} conjuers a fierce lightning storm!\n', typingActive)
    storm_hits = 0
    tl_damage = 0
    while storm_hits < 3:
      hit = random.randrange(0, 4)
      if hit >= 1:
          dam = random.randrange(p1.ATK // 2.5, p1.ATK) * skill_boost
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
    global skill_boost
    print_slow(f'{p1.name} concentrates their magic!\n', typingActive)
    hit = random.randrange(0, 6) * skill_boost
    if hit >= 4:
        damage = foe.HP // 4
        foe.HP -= damage
        print_slow(f'{p1.name} blasts the enemy {foe.name} away for {damage} damage! {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
    else:
        print_slow(f'{p1.name} magical energy fizzles out...\n', typingActive)
    p1.MP -= 2
def wizard_shock(p1, foe, typingActive):
  global focus
  global skill_boost
  global haste
  print_slow(f'{p1.name} conjures a ball of magical lightning!\n', typingActive)
  hit = random.randrange(0,101)
  dam = random.randrange(p1.ATK * 1.5, round(p1.ATK * 2)) * skill_boost
  damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * focus), 0)
  foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
  if hit <= 10:
    p1.TDEF += 100
    p1.HP = min(max(p1.HP - (dam // 4), 0), p1.MaxHP)
    print_slow(f"{p1.name}'s lightning ball errupts across the battlefield too soon, shocking everything in the area!\n", typingActive)
    print_slow(f"The enemy {foe.name} is shocked for {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n{p1.name} is shocked for {dam // 4} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. {p1.name}'s DEF is temporarily reduced!'\n", typingActive)
    
  if 10 < hit <= 65:
    print_slow(f"{p1.name}'s lightning ball explodes just ahead of the enemy {foe.name}!\n", typingActive)
    print_slow(f"The enemy {foe.name} is shocked for {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n", typingActive)
    
  if 65 < hit <= 100:
    haste += random.randrange(2, 4)
    print_slow(f"{p1.name}'s lightning ball discharges directly into the the enemy {foe.name}!\n", typingActive)
    print_slow(f"The enemy {foe.name} is shocked for {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\nThe enemy {foe.name} is paralyzed! {p1.name} has {haste - 1} more actions this turn.\n", typingActive)
  p1.MP -= 3
#Thief skill effects
def thief_steal(p1, foe, typingActive):
    mug = random.randrange(0, 6)
    if mug == 5:
        GPE = round(random.randrange(foe.MinGP, round(foe.MaxGP * 0.8)) * p1.GR)
        p1.GP = p1.GP + GPE
        print_slow(
            f'{p1.name} manages to steal {GPE} GP from the enemy {foe.name}. {p1.name} now has {p1.GP}GP.\n', typingActive
        )
    elif 0 < mug < 5:
        GPE = round(random.randrange(foe.MinGP * 0.5 , round(foe.MaxGP * 0.5)) * p1.GR)
        p1.GP = p1.GP + GPE
        print_slow(f'{p1.name} manages to steal {GPE} GP from the enemy {foe.name}. {p1.name} now has {p1.GP}GP.\n', typingActive)
    elif mug == 0:
        print_slow(f'{p1.name} failed to steal anything! \n', typingActive)
    p1.MP -= 1

def thief_poisondagger(p1, foe, typingActive):
    dagger = 0
    print_slow(f'{p1.name} throws a handful of poison daggers!\n', typingActive)
    hit = random.randrange(0, 101)
    if hit <= p1.ACC - 25:
        foe.POISON += 2
        dagger += 1
        damage1 = round(p1.ATK // 8)
    else:
        damage1 = 0
    hit = random.randrange(0, 3)
    if hit <= p1.ACC - 25:
        foe.POISON += 2
        dagger += 1
        damage2 = round(p1.ATK // 8)
    else:
        damage2 = 0
    hit = random.randrange(0, 3)
    if hit <= p1.ACC - 25:
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



def thief_cointhrow(p1, foe, typingActive):
  while True:
    print_slow(f"Input amount of GP you would like to throw (0-{p1.GP})\n", typingActive)
    toss = input()   
    if toss.isdigit():
      toss = int(toss)
      if 0 <= toss <= p1.GP:
        if toss == 0:
          dam = 0
        elif 0 < toss <= 50:
          dam = random.randrange(1, 6)
          foe.HP -= dam
        elif 50 < toss <= 100:
          dam = random.randrange(5, 11)
          foe.HP -= dam
        elif 100 < toss <= 250:
          dam = random.randrange(10, 21)
          foe.HP -= dam
        elif 250 < toss <= 500:
          dam = random.randrange(20, 36)
          foe.HP -= dam
        elif 500 < toss:
          dam = random.randrange(35, 51)
          foe.HP -= dam
        print_slow(f"{p1.name} tosses {toss} GP at the enemy {foe.name}! The enemy {foe.name} takes {dam} damage!\n", typingActive)
        p1.MP -= 1
        break
      else:
        print_slow(f"Invalid selection. Please select an amount between (0-{p1.GP}\n", typingActive)
    else:
        print_slow(f"Invalid selection. Please select an amount between (0-{p1.GP}\n", typingActive)
      
      


#def summoner_
def enemy_skills(p1, foe, typingActive):
    global battle
    global foe_special
    global foe_wait
    global focus
    global focus_turns
    global wait_skill
    global cDEF

    # 1.  Flee
    # 2.  Cleave
    # 3.  Maul
    # 4.  Magic Bolt
    # 5.  Steal
    # 6.  Fire Breath
    # 7.  Sting
    # 8.  Poison Mist
    # 9.  Quake
    # 10. Summon Swarm
    # 11. Roar
    # 12. Kancho
    # 13. Poison Bite
    # 14. Dales Pocket-sand
    # 15. Skewer
    # 16. Gunk Shot
    # 17. Cripple
    # 18. Assualt
    # 19. Root
    # 20. Vampire Bite
    # 21. Spirit Drain
    # 22. Vanish
    # 23. Self-Destruct
    # 24. Whirlwind
    # 25. Peck

    if foe_wait == 0:
      f_Skill = random.choice(foe.skill)
    if foe_wait >= 1:
      f_Skill = wait_skill
    
    if f_Skill == 1:  #Flee
        escape = random.randrange(0, 4)
        if escape >= 2:
            battle = 'INACTIVE'
            print_slow(
                f'The enemy {foe.name} scuttles away! You earn nothing. Sucks to suck.\n', typingActive
            )
            print_slow("**********Enemy Escape!**********\n", typingActive)
            combat_end_reset(p1, foe)
        else:
            print_slow(
                f'Enemy {foe.name} attempted to escape but stumbled and failed!\n', typingActive
            )
        p1.TDEF = 100
        foe.MP -= 1

    elif f_Skill == 2:  #Cleave
        dam = random.randrange(round(foe.ATK // 1.5), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        print_slow(f'The enemy {foe.name} strikes with a cleaving blow!\n', typingActive)
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif f_Skill == 3:  #Maul
        dam = random.randrange(foe.ATK // 2, foe.ATK)
        damage = damage = max(round(dam + 3 * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        print_slow(f'The enemy {foe.name} charges wildly and mauls {p1.name}!\n', typingActive)
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif f_Skill == 4:  #Magic Bolt
        dam = random.randrange(foe.ATK, round(foe.ATK * 1.3))
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        print_slow(
            f'The enemy {foe.name} concentrates their power into a magic bolt and hurls it at {p1.name}!\n', typingActive
        )
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif f_Skill == 5:  #Steal
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

    elif f_Skill == 6:  #Fire Breath
      while True:
        if foe_wait == 1:
          dam = random.randrange(foe.ATK, round(foe.ATK * 1.2))
          damage = max(round(dam + 6 * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
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
          print_slow(f'Smoke begins raising from {foe.name} mouth...\n', typingActive)
          foe_special = enemy_skills
          foe_wait = 1
          wait_skill = 6
          p1.TDEF = 100
          foe.MP -= 1
          break

    elif f_Skill == 7:  #Sting
        dam = random.randrange(foe.ATK // 2 + 4, foe.ATK + 4)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
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
            command = "SEPPUKU"
            enemy_death(p1, foe, command, damage, typingActive)
          
    elif f_Skill == 8:  #Poison Mist
        pdamage = random.randrange(1, 4)
        p1.POISON += pdamage
        print_slow(
            f'{foe.name} sprays a poison mist at {p1.name}! {p1.name} is poisoned for {pdamage} turns.\n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif f_Skill == 9:  #Quake
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

    elif f_Skill == 10:  #Summon Swarm
        print_slow(
            f'{foe.name} summons a swarm of smaller BEES to attack {foe.name}.\n', typingActive
        )
        bee_hits = 0
        tl_damage = 0
        while bee_hits < 3:
          hit = random.randrange(0, 4)
          if hit >= 1:
              dam = random.randrange(foe.ATK // 2, foe.ATK // 1.5)
              damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
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

    elif f_Skill == 11:  #Roar
        if foe.name == "Dire Wolf":
          print_slow(
              f"{foe.name} lets out a tremendous howl reducing {p1.name}'s defenses temporarily!\n", typingActive
          )
          p1.TDEF = 125
        elif foe.name == "Dragon King, Tanninim":
          print_slow(
              f"{foe.name} lets out an ear shattering shriek reducing {p1.name}'s defenses temporarily!\n", typingActive
          )
          p1.TDEF = 200
        else:
          print_slow(
              f"{foe.name} lets out a ferocious roar reducing {p1.name}'s defenses temporarily!\n", typingActive
          )
          p1.TDEF = 150
        foe.MP -= 1

    elif f_Skill == 12:  #Kancho
        print_slow(
            f"{foe.name} grabs {p1.name} from behind!\n", typingActive
        )
        hit = random.randrange(0, 4)
        if hit >= 2:
            dam = random.randrange(foe.ATK // 3, foe.ATK // 1.5)
            damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
            foe.HP = min(max(foe.HP + damage // 2, 0), foe.MaxHP)
            print_slow(f'{p1.name} has their life force ripped from their body and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n{foe.name} consumes the life force and gains {damage//2} HP! {foe.name} has {foe.HP}/{foe.MaxHP}.\n', typingActive)
        else:
            print_slow(f"{p1.name} escapes the {foe.name}'s hold!\n", typingActive)      
        p1.TDEF = 100
        foe.MP -= 1

    elif f_Skill == 13:  #Poison Bite
        dam = random.randrange(foe.ATK // 2.5, foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)        
        if foe.name == 'Harpy':
          pdamage = random.randrange(2, 6)
          p1.POISON += pdamage
          print_slow(
            f'The {foe.name} claws at {p1.name} with their toxic talons! {p1.name} is poisoned for {pdamage} turns and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive
        )
        else:
          pdamage = random.randrange(1, 4)
          p1.POISON += pdamage
          print_slow(
            f'The {foe.name} bites down on {p1.name} with their toxic fangs! {p1.name} is poisoned for {pdamage} turns and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1

    elif f_Skill == 14:  #Dales Pocket-sand
        focus = .7
        focus_turns += 4
        print_slow(f"{foe.name} throws a blue powder in {p1.name}'s face! {p1.name} has their power lowered for {focus_turns - 1} turns!\n", typingActive)
        p1.TDEF = 100
        foe.MP -= 1
      
    elif f_Skill == 15:  #Skewer
        if foe.name == 'Unicorn':
          print_slow(f'The enemy {foe.name} charges forward with their horn and skewers {p1.name}!\n', typingActive)
        else:
          print_slow(f'The enemy {foe.name} charges forward with their weapon and skewers {p1.name}!\n', typingActive)
        hit = random.randrange(0, 4)
        dam = random.randrange(round(foe.ATK // 2), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        if hit >= 2:
          print_slow(f"The enemy {foe.name} manages to break through {p1.name}'s armor'! {p1.name}'s defenses are temporarily lowered.\n", typingActive)
          p1.TDEF += 50
        elif hit < 2:
          print_slow(f"{p1.name}'s armor saved them from being impaled!\n", typingActive)
          p1.TDEF = 100
        print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
        foe.MP -= 1

    elif f_Skill == 16:  #Gunk Shot
        print_slow(f"The enemy {foe.name} spews a tar-like gunk at {p1.name}'s face!\n", typingActive)
        hit = random.randrange(0, 4)
        if hit >= 1:
          p1.BLIND += 3
          print_slow(f"The enemy {foe.name} has temporarily blinded {p1.name}! {p1.name} is blinded for {p1.BLIND - 1} turns.\n", typingActive)
        elif hit < 1:
          print_slow(f"{p1.name} manages to avoid the gunk!\n", typingActive)
        p1.TDEF = 100
        foe.MP -= 1

    elif f_Skill == 17:  #Cripple
      dam = random.randrange(round(foe.ATK // 2), foe.ATK)
      damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
      p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
      hit = random.randrange(0, 101)
      if foe.name == "Tiger":
        print_slow(f'The enemy {foe.name} bites down with crippling force!\n', typingActive)
      else:
        print_slow(f'The enemy {foe.name} strikes with a crippling blow!\n', typingActive)
      print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
      if hit <= 65:
        focus = .5
        focus_turns += random.randrange(2, 4)
        print_slow(f"{p1.name}'s damage dealt has been reduced for {focus_turns - 1} turns.\n", typingActive)
      p1.TDEF = 100
      foe.MP -= 1

    elif f_Skill == 18: #Assualt
      print_slow(f'The enemy {foe.name} launches a coordinated strike!',typingActive)
      hit = random.randrange(0, 101)
      hit2 = random.randrange(0, 101)
      hit3 = random.randrange(0, 101)
      if hit <= 50:
        dam = random.randrange(round(foe.ATK // 2), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        focus = .5
        focus_turns += 2
        print_slow(f"The first Rouge strikes {p1.name} and flings a blue powder in their face! {p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n {p1.name}'s damage dealt has been reduced for {focus_turns - 1} turns.\n", typingActive)
      if hit > 50:
        print_slow(f'{p1.name} dodges the first attack!',typingActive)
      if hit2 <= 50:
        dam = random.randrange(round(foe.ATK // 2), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        pdamage = random.randrange(1, 4)
        p1.POISON += pdamage
        print_slow(f'The second Rouge stabs {p1.name} with a poison dagger! {p1.name} is poisoned for {pdamage} turns and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)
      if hit2 > 50:
        print_slow(f'{p1.name} dodges the second attack!\n',typingActive)
      if hit3 <= 50:
        dam = random.randrange(round(foe.ATK // 2), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.BLIND += 3
        print_slow(f"The third Rouge throws a TAR BOMB at {p1.name}! {p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n{p1.name} is blinded for {p1.BLIND - 1} turns.\n", typingActive) 
      if hit3 > 50:
        print_slow(f'{p1.name} dodges the final attack!\n',typingActive)
      p1.TDEF = 100
      foe.MP -= 1

    elif f_Skill == 19: # Root
      heal = foe.MaxHP // 100 * 15
      foe.HP = min(foe.HP + heal, foe.MaxHP)
      foe.TDEF -= 30
      print_slow(f'{foe.name} takes root and restores {heal} HP! {foe.name} has {foe.HP}/{foe.MaxHP}. {foe.name} is braced for the next attack.\n',typingActive)
      p1.TDEF = 100
      foe.MP -= 1

    elif f_Skill == 20: # Vampire Bite
      hit = random.randrange(0, 3)
      dam = random.randrange(foe.ATK // 2, foe.ATK )
      damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
      p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
      if hit == 0:
        heal = round(damage * .25)
      elif hit == 1:
        heal = round(damage * .50)
      elif hit == 2:
        heal = round(damage * .75)
      foe.HP = min(max(foe.HP + heal, 0), foe.MaxHP)
      if foe.name == 'Crescent Pond Naga':
        pdamage = random.randrange(1, 4)
        p1.POISON += pdamage
        print_slow(f'The {foe.name} injects {p1.name} with venom and drains their blood!\n{p1.name} takes {damage} damage and is poisoned for {pdamage} turns! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n{foe.name} has gained {heal} HP! {foe.name} has {foe.HP}/{foe.MaxHP}.\n{p1.name} ', typingActive) 
      else:
        print_slow(f'The {foe.name} bites {p1.name}, sucking their blood!\n{p1.name} has their blood drained and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n{foe.name} has gained {heal} HP! {foe.name} has {foe.HP}/{foe.MaxHP}.\n', typingActive) 
      p1.TDEF = 100
      foe.MP -= 1

    elif f_Skill == 21: # Spirit drain
      hit = random.randrange(0, 6)    
      if 0 <= hit <= 2:
        drain = round(p1.MaxMP * .75)
      elif 3 <= hit <= 4:
        drain = round(p1.MaxMP * .50)
      elif hit == 5:
        drain = round(p1.MaxMP * .25)
      p1.MP = min(max(p1.MP - drain, 0), p1.MaxMP)
      print_slow(f"{foe.name} drains {p1.name}'s spirit! {p1.name} losses {drain} MP. {p1.name} has {p1.MP}/{p1.MaxMP} MP remaining.\n", typingActive)
      p1.TDEF = 100
      foe.MP -= 1

    elif f_Skill == 22: # Vanish
      if foe.MP >= 2:
        foe.TDEF = 0
        print_slow(f"{foe.name} becomes incorporeal! {foe.name} cannot be damaged next turn!\n", typingActive)
        foe.MP -= 2
      else:
        foe.TDEF = 30
        print_slow(f"{foe.name} becomes partially incorporeal! {foe.name} will take reduced damaged next turn!\n", typingActive)
        foe.MP -= 1
      p1.TDEF = 100

    elif f_Skill == 23: # Self-Destruct
      while True:
        if foe_wait >= 1:
          foe_wait -= 1 
          print_slow(f'"...S E L F...D E S T R U C T...I N... {foe_wait}..."\n', typingActive) 
          if foe_wait == 0:
            damage = random.randrange(round(foe.ATK * 1.5), foe.ATK * 3)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
            foe.HP = 0
            command = 'SEPPUKU'
            print_slow(f'The enemy {foe.name} errupts into an explosion of shrapnel!\n\n',typingActive)
            print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP remaining. \n', typingActive)
            player_death(p1, typingActive)
            enemy_death(p1, foe, command, damage, typingActive)
          p1.TDEF = 100
          break
        elif foe_wait == 0:
          foe_special = enemy_skills
          wait_skill = 23
          foe_wait = 3
          print_slow('"...S E L F...D E S T R U C T...I N I T I A T E D..."\n', typingActive)
          print_slow(f'"...S E L F...D E S T R U C T...I N... {foe_wait}..."\n', typingActive)
          p1.TDEF = 100
          foe.MP -= 1
          break
          
    if f_Skill == 24:  #Whirlwind
        print_slow(
                f'The enemy {foe.name} flaps their wings and creates a massive gust of wind!\n', typingActive
            )
        while True:
          if foe.name == 'Roc':
            escape = random.randrange(0, 7)
            break
          else:
            escape = random.randrange(0, 4)
            break
        if escape >= 3:
            damage = max(round(foe.ATK * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP) 
            battle = 'INACTIVE'
            print_slow(
                f'The enemy {foe.name} blows {p1.name} away! {p1.name} takes {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. You earn nothing. Sucks to suck.\n', typingActive
            )
            player_death(p1, typingActive)
            print_slow("**********Enemy Escape!**********\n", typingActive)
            combat_end_reset(p1, foe)
        else:
            damage = max(round(foe.ATK // 2 * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP) 
            print_slow(
                f'The enemy {foe.name} blows {p1.name} back! {p1.name} takes {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. ', typingActive
            )
        p1.TDEF = 100
        foe.MP -= 1
      
    if f_Skill == 25:  #Peck
        print_slow(
                f'The enemy {foe.name} swoops in from above and begins pecking wildly!\n', typingActive
            )
        peck_hits = 0
        tl_damage = 0
        while peck_hits < 5:
          hit = random.randrange(0, 5)
          if hit >= 2:
              dam = random.randrange(foe.ATK // 2, foe.ATK // 1.5)
              damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
              tl_damage = tl_damage + damage
              peck_hits += 1
              if peck_hits == 1:
                print_slow(f'{p1.name} is pecked for {damage} damage!\n', typingActive)
              else:
                print_slow(f'{p1.name} is pecked again for {damage} damage!\n', typingActive)
          else:
              print_slow(f'The {foe.name} misses their attack and flys back!\n', typingActive)
              peck_hits = 5
        p1.HP = min(max(p1.HP - tl_damage, 0), p1.MaxHP)    
        print_slow(
            f'{p1.name} has taken {tl_damage} total damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive
        )
        p1.TDEF = 100
        foe.MP -= 1


      
#Help menu for combat
def combat_menu(p1, typingActive):
  if p1.job == "WARRIOR":
      warrior_menu = "Battle commands:\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\nHARDEN: Restore some HP, temp. increase def for 1 turn.\n"
      if p1.lvl >= 2:
        warrior_menu += 'STRIKE: Wildy strike foe for high damage. Chance to miss.\n'
      if p1.lvl >= 5:
        warrior_menu += 'BERSERK: Become blinded by range for several turns. Can only attack while berserk, but damage is increased.\n'
      if p1.lvl >= 10:
        warrior_menu += 'BLOOD: Become filled with a lust for blood. Absorb 50% of damage dealt as HP.\n'
      if p1.mainHand == 'AETON':
        warrior_menu =+ 'BATTLECRY: Spend 2 MP to unleash a mighty BATTLECRY to temporarily reduce enemy attack.\n'
      print_slow(warrior_menu, typingActive)
  
  elif p1.job == "WIZARD" or p1.job == "WITCH":
      wizard_menu = "Battle commands:\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\nFOCUS: Concentrates to increase damage of follow up attacks for several turns."
      if p1.lvl >= 2:
        wizard_menu += "\nBOLT: Cast magical bolt dealing high damage.\n"
      if p1.lvl >= 5:
        wizard_menu += "\nSTORM: Cast magical storm, hitting the enemy multiple times. Chance to miss.\n"
      if p1.lvl >= 10:
        wizard_menu += "\nBLAST: Send a concentrated magical blast at the enemy. Damaged based on enemy HP; high chance to miss.\n"
      if p1.mainHand == 'FULGUR':
        wizard_menu =+ 'SHOCK: Spend 3 MP to conjure a massive ball of lightning to shock the enemy for high damamge. Chance to paralyze enemy. Low chance to backfire.\n'
      print_slow(wizard_menu, typingActive)

  elif p1.job == "THIEF":
      thief_menu = "Battle commands:\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\nSTEAL: Steal GP from enemy. Chance to fail.\n"
      if p1.lvl >= 2:
        thief_menu =+ 'THROW: Throw up to 3 poison daggers at the enemy. Deals damage and poisons.\n'
      if p1.lvl >= 5:
        thief_menu =+ 'MUG: Attack enemy and steal item from enemy. Chance stealing may fail.\n'
      if p1.lvl >= 10:
        thief_menu =+ 'HASTE: Spend 2 MP to use 2 actions in the same turn. Does not stack.\n'
      if p1.mainHand == 'MIDAS':
        thief_menu =+ '$TOSS: Throw GP at the enemy for direct damage.\n'
      print_slow(thief_menu, typingActive)
      