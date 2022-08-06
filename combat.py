import random
import os
import sys
from slowprint import *
goblin_mobs = ["Goblin", "Hobgoblin", "Goblin Gang", "Goblin Queen", "Zomblin", "Moldy Zomblin"]


def standard_battle(p1, foe, typingActive):   
      global battle
      global enemy_turn
      global player_turn
      global focus
      turn_count = 1
      damage = 0
      focus = 1  
      skill_command = ["HARDEN", "STRIKE", "BOLT", "FOCUS", "STEAL", "THROW"]
      
      print_slow("\n**********COMBAT START**********", typingActive)
      print_slow(f"\nYou encounter a {foe.name}!\n", typingActive)
      p1.stat_check(typingActive)
      foe.stat_check(typingActive)
  
      battle = 'ACTIVE'
      while battle == 'ACTIVE':
        print_slow(f"********** Turn[{turn_count}] **********\n", typingActive)
        #Posion effects and player death
        player_turn = 1
        poison_effect(p1, foe, typingActive)
        player_death(p1, typingActive)       
        #Start of player turn
        while player_turn == 1:
          print_slow("Type battle command or type HELP for command list:\n", typingActive)
          if p1.HP >= 1: 
              p1.TDEF = 0
              command = (input().upper())
              print_slow("", typingActive)
              #Attack command
              if command == "ATK":
                  dam = random.randrange((p1.ATK // 4), p1.ATK)
                  damage = max(
                      round(dam * (foe.DEF * 0.1 * foe.TDEF * 0.1) * focus),
                      0)
                  foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
                  foe.TDEF = 10
                  focus = 1
                  if foe.HP < 0:
                      foe.HP = 0
                  print_slow(
                      f'{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive
                  )
                  turn_count += 1
                  player_turn = 0
                  enemy_turn = 1
              #Use item command
              elif command == "ITEM":
                  use_item(p1, foe, typingActive)
                  turn_count += 1
                  player_turn = 0
                  enemy_turn = 1
                  break
  
              #DEF Command
              elif command == "DEF":
                  p1.TDEF = p1.DEF // 2
                  print_slow(f'{p1.name} is defending!\n', typingActive)
                  foe.TDEF = 10
                  turn_count += 1
                  player_turn = 0
                  enemy_turn = 1
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
              elif command in skill_command and p1.MP > 0:
                  if command == "HARDEN" and p1.job == "WARRIOR":
                      warrior_skill(p1, foe, typingActive)
                      turn_count += 1
                      player_turn = 0
                      enemy_turn = 1
                      break
                  elif command == "STRIKE" and p1.job == "WARRIOR":
                      warrior_wildstrikes(p1, foe, typingActive)
                      turn_count += 1
                      player_turn = 0
                      enemy_turn = 1
                      break
                  elif command == "BOLT" and p1.job == "WIZARD":
                      wizard_spell(p1, foe, typingActive)
                      turn_count += 1
                      player_turn = 0
                      enemy_turn = 1
                      break
                  elif command == "FOCUS" and p1.job == "WIZARD":
                      wizard_focus(p1, foe, typingActive)
                      turn_count += 1
                      player_turn = 0
                      enemy_turn = 1
                      break
                  elif command == "STEAL" and p1.job == "THIEF":
                      thief_steal(p1, foe, typingActive)
                      turn_count += 1
                      player_turn = 0
                      enemy_turn = 1
                      break
                  elif command == "THROW" and p1.job == "THIEF":
                      thief_poisondagger(p1, foe, typingActive)
                      turn_count += 1
                      player_turn = 0
                      enemy_turn = 1
                      break
                  else:
                      print_slow('That command is invalid.\n', typingActive)
              #Out of MP for skill
              elif (
                  ((command == "STRIKE" or command == "HARDEN") or
                   (command == "BOLT" or command == "FOCUS")) or
                  (command == "STEAL" or command == "THROW")) and p1.MP == 0:
                  print_slow(f'{p1.name} is out of MP and unable to use their SKILL \n', typingActive)
              #Player needs help
              elif command == "STATS":
                  p1.stat_check(typingActive)
              elif command == "HELP":
                  combat_menu(p1, typingActive)
              else:
                  print_slow('That command is invalid.\n', typingActive)
                
        #Start of enemy turn      
        enemy_death(p1, foe, command, damage, typingActive)
        while enemy_turn == 1:
          command2 = random.randrange(0, 7)
          
          #Enemy Commands [1]
          #ATTACK
          if command2 <= 2:  
              dam = random.randrange(foe.ATK // 3, foe.ATK)
              damage = max(round(dam - (p1.DEF * 0.1 - p1.TDEF * 0.1)), 0)
              p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
              
              enemy_turn = 0
              print_slow(f'The enemy {foe.name} ATTACKS.\n', typingActive)
              print_slow(
                  f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
              )
          #DEFEND
          elif command2 == 3 or command2 == 4:  
              foe.TDEF = foe.DEF // 2
              enemy_turn = 0
              print_slow(f'The enemy {foe.name} DEFENDS\n', typingActive)
              print_slow(f'{foe.name} has raised its defenses! \n', typingActive)
          #HEAL
          elif (command2 == 5 and foe.POTS > 0) and foe.HP < foe.MaxHP:  
              print_slow(f'The enemy {foe.name} HEALS\n', typingActive)
              enemy_turn = 0
              heal = random.randrange(5, 10)
              foe.HP = min(max(foe.HP + heal, 0), foe.MaxHP)
              foe.POTS -= 1
              print_slow(
                  f'{foe.name} has healed {heal} HP. {foe.name} has {foe.HP}/{foe.MaxHP} HP\n', typingActive
              )
          #SKILL
          elif command2 == 6 and foe.MP > 0:  
              enemy_skills(p1, foe, typingActive)
              enemy_turn = 0
          else:
              pass
            
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
      GPE = random.randrange(foe.MinGP, foe.MaxGP)
      p1.GP = p1.GP + GPE
      p1.xp = p1.xp + foe.exp
      if foe.name in goblin_mobs:
          p1.gobCount += 1
      if command == "BOLT" and p1.job == "WIZARD":
          print_slow(f'{p1.name} vaporized the enemy!\n', typingActive)
      elif damage >= foe.MaxHP // 2:
          print_slow(f'{p1.name} obliterated the enemy!\n', typingActive)
      elif command == "STRIKE" and p1.job == "WARRIOR":
          print_slow(f'{p1.name} pulverised the enemy!\n', typingActive)
      else:
          print_slow(f'{p1.name} killed the enemy.\n', typingActive)
      print_slow(
          f'{p1.name} gained {GPE}GP and {foe.exp}EXP. {p1.name} has {p1.GP}GP\n', typingActive
      )
      p1.level_up(typingActive)
      print_slow("********** VICTORY!!! **********\n", typingActive)
      foe.HP = foe.MaxHP
      foe.POTS = foe.MaxPOTS
      foe.MP = foe.MaxMP
      foe.POISON = 0
      p1.POISON = 0
      battle = 'INACTIVE'

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
          foe.TDEF = 10
          items_list = "OFF"
          print_slow(f'{p1.name} drinks a POTION and heals {heal} HP. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
      elif command == "ANTIDOTE" and p1.ANT > 0:
          p1.ANT -= 1
          p1.POISON = 0
          foe.TDEF = 10
          items_list = "OFF"
          print_slow(f"{p1.name} drinks an ANTIDOTE and is relieved of POISON!\n", typingActive)
      elif command == "ETHER" and p1.ETR > 0:
          heal = random.randrange(3, 6)
          p1.ETR -= 1
          p1.MP = min(max(p1.MP + heal, 0), p1.MaxMP)
          foe.TDEF = 10
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
def warrior_skill(p1, foe, typingActive):
    heal = random.randrange(p1.MaxHP // 10, p1.MaxHP // 3)
    p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
    p1.TDEF = p1.DEF * 2
    p1.MP -= 1
    foe.TDEF = 10
    print_slow(
        f'{p1.name} has bolstered their constitution. {p1.name} healed {heal} HP and shielded themp1 this turn. {p1.name} has {p1.HP}/{p1.MaxHP} HP \n', typingActive
    )

def warrior_wildstrikes(p1, foe, typingActive):
    print_slow(f'{p1.name} strikes wildly at the enemy {foe.name}.\n', typingActive)
    hit = random.randrange(0, 4)
    if hit >= 1:
        dam = random.randrange(p1.ATK // 1.5, p1.ATK)
        damage1 = max(round(dam * foe.DEF * .1 * foe.TDEF * .1), 0)
        print_slow(f'{p1.name} strikes for {damage1} damage!\n', typingActive)
    else:
        damage1 = 0
        print_slow(f'{p1.name} strikes and misses!\n', typingActive)
    hit = random.randrange(0, 4)
    if hit >= 1:
        dam = random.randrange(p1.ATK // 1.5, p1.ATK)
        damage2 = max(round(dam * foe.DEF * .1 * foe.TDEF * .1), 0)
        print_slow(f'{p1.name} strikes for {damage2} damage!\n', typingActive)
    else:
        damage2 = 0
        print_slow(f'{p1.name} strikes and misses!\n', typingActive)
        hit = random.randrange(0, 4)
    if hit >= 1:
        dam = random.randrange(p1.ATK // 1.5, p1.ATK)
        damage3 = max(round(dam * foe.DEF * .1 * foe.TDEF * .1), 0)
        print_slow(f'{p1.name} strikes for {damage3} damage!\n', typingActive)
    else:
        damage3 = 0
        print_slow(f'{p1.name} strikes and misses!\n', typingActive)
    tl_damage = damage1 + damage2 + damage3
    foe.HP = min(max(foe.HP - tl_damage, 0), foe.MaxHP)
    foe.TDEF = 10
    p1.MP -= 1
    print_slow(
        f'{foe.name} has taken {tl_damage} total damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive
    )


#Wizard skill effects
def wizard_spell(p1, foe, typingActive):
    global focus
    dam = random.randrange(p1.ATK, round(p1.ATK * 1.5))
    damage = max(round(dam * foe.DEF * 0.1 * foe.TDEF * 0.1 * focus), 0)
    foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
    foe.TDEF = 10
    focus = 1
    p1.MP -= 1
    print_slow(
        f'{p1.name} casts a magical bolt at the enemy {foe.name}.\n{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive
    )

def wizard_focus(p1, foe, typingActive):
    global focus
    focus = 1.4
    foe.TDEF = 10
    print_slow(f'{p1.name} concentrates their power.\n', typingActive)
    concentrate = random.randrange(0, 5)
    if concentrate == 0:
        conc = random.randrange(1, p1.MaxMP)
        p1.MP = min(max(p1.MP + conc, 0), p1.MaxMP)
        print_slow(
            f'{p1.name} restores some MP! {p1.name} has {p1.MP}/{p1.MaxMP} MP.\n', typingActive
        )
    else:
        p1.MP -= 1

#Thief skill effects
def thief_steal(p1, foe, typingActive):
    mug = random.randrange(0, 5)
    if mug >= 2:
        GPE = random.randrange(foe.MinGP, round(foe.MaxGP * 0.8))
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
        damage1 = random.randrange(1, 5)
    else:
        damage1 = 0
    hit = random.randrange(0, 3)
    if hit >= 1:
        foe.POISON += 2
        dagger += 1
        damage2 = random.randrange(1, 5)
    else:
        damage2 = 0
    hit = random.randrange(0, 3)
    if hit >= 1:
        foe.POISON += 2
        dagger += 1
        damage3 = random.randrange(1, 5)
    else:
        damage3 = 0
    tl_damage = damage1 + damage2 + damage3
    foe.HP = min(max(foe.HP - tl_damage, 0), foe.MaxHP)
    foe.TDEF = 10
    p1.MP -= 1
    print_slow(
        f'{p1.name} hit the enemy {foe.name} with {dagger} poison dagger(s)! The enemy {foe.name} has taken {tl_damage} total damage and is poisoned for {foe.POISON} turns. {foe.name} has {foe.HP}/{foe.MaxHP} HP\n', typingActive
    )

#Enemy skills
def enemy_skills(p1, foe, typingActive):
    global battle
  
    if foe.skill == 1:  #FLee
        foe.MP -= 1
        escape = random.randrange(0, 4)
        if escape >= 2:
            battle = 'INACTIVE'
            print_slow(
                f'The enemy {foe.name} scuttles away! You earn nothing. Sucks to suck.\n', typingActive
            )
            print_slow("**********Enemy Escape!**********\n", typingActive)
            foe.HP = foe.MaxHP
            foe.POTS = foe.MaxPOTS
        else:
            print_slow(
                f'Enemy {foe.name} attempted to escape but stumbled and failed!\n', typingActive
            )

    elif foe.skill == 2:  #Cleave
        dam = random.randrange(round(foe.ATK // 1.5), foe.ATK)
        damage = max(round(dam * p1.DEF * 0.1 * p1.TDEF * 0.1), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        foe.MP -= 1
        print_slow(f'The enemy {foe.name} strikes with a cleaving blow!\n', typingActive)
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )

    elif foe.skill == 3:  #Maul
        dam = random.randrange(foe.ATK // 2, foe.ATK)
        damage = damage = max(round(dam + 3 * p1.DEF * 0.1 * p1.TDEF * 0.1), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        foe.MP -= 1
        print_slow(f'The enemy {foe.name} charges wildly and mauls {p1.name}!\n', typingActive)
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )

    elif foe.skill == 4:  #Magic Bolt
        dam = random.randrange(foe.ATK, round(foe.ATK * 1.3))
        damage = max(round(dam * p1.DEF * 0.1 * p1.TDEF * 0.1), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        foe.MP -= 1
        print_slow(
            f'The enemy {foe.name} concentrates their power into a magic bolt and hurls it at {p1.name}!\n', typingActive
        )
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )

    elif foe.skill == 5:  #Steal
        mug = random.randrange(0, 3)
        if mug >= 2:
            GPL = random.randrange(foe.MinGP, round(foe.MaxGP // 1.5))
            p1.GP = p1.GP + GPL
            foe.MP -= 1
            print_slow(
                f'The enemy {foe.name} manages to steal {GPL}GP from {p1.name}. {p1.name} now has {p1.GP}GP.\n', typingActive
            )
        elif mug < 2:
            foe.MP -= 1
            print_slow(
                f'{foe.name} attempted to steal but failed to grab anything!\n', typingActive
            )

    elif foe.skill == 6:  #Fire Breath
        dam = random.randrange(foe.ATK, round(foe.ATK * 1.2))
        damage = max(round(dam + 6 * p1.DEF * 0.1 * p1.TDEF * 0.1), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        foe.MP -= 1
        print_slow(
            f"Fire bellows from the enemy {foe.name}'s mouth scorching '{p1.name}!\n", typingActive
        )
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP} HP remaining. \n', typingActive
        )

    elif foe.skill == 7:  #Sting
        dam = random.randrange(foe.ATK // 2 + 4, foe.ATK + 4)
        damage = max(round(dam * p1.DEF * 0.1 * p1.TDEF * 0.1), 0)
        pdamage = random.randrange(1, 3)
        p1.POISON += pdamage
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        foe.MP -= 1
        damage2 = 4
        foe.HP = min(max(foe.HP - damage2, 0), foe.MaxHP)

        if foe.HP < 0:
            foe.HP = 0

        print_slow(f'The enemy {foe.name} rushes at {p1.name} with their stinger!\n', typingActive)
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )
        print_slow(
            f'{foe.name} has taken {damage2} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP. \n', typingActive
        )
        if foe.HP <= 0:
            battle = 'INACTIVE'
            combat = 'END'
            encouter = 0
            GPE = random.randrange(foe.MinGP, foe.MaxGP)
            p1.GP = p1.GP + GPE
            p1.xp = p1.xp + foe.exp
            print_slow(f'{foe.name} killed themself.\n', typingActive)
            print_slow(
                f'{p1.name} gained {GPE}GP and {foe.exp}EXP. {p1.name} has {p1.GP}GP\n', typingActive
            )
    elif foe.skill == 8:  #Poison Mist
        pdamage = random.randrange(1, 4)
        p1.POISON += pdamage
        print_slow(
            f'{foe.name} spews a poison mist at {p1.name}! {p1.name} is poisoned for {pdamage} turns.\n', typingActive
        )

    elif foe.skill == 9:  #Quake
        damage = max(
            random.randrange(round(foe.ATK // 2), round(foe.ATK * 0.8)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        foe.MP -= 1
        print_slow(
            f'The enemy {foe.name} strikes with the ground causing a mighty quake!\n', typingActive
        )
        print_slow(
            f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive
        )

    elif foe.skill == 10:  #Summon Swarm
        print_slow(
            f'{foe.name} summons a swarm of smaller BEES to attack {foe.name}.\n', typingActive
        )

        hit = random.randrange(0, 4)
        if hit >= 1:
            dam = random.randrange(foe.ATK // 2, foe.ATK // 1.5)
            damage1 = max(round(dam * p1.DEF * 0.1 * p1.TDEF * 0.1), 0)
            p1.POISON += 1
            print_slow(f'{p1.name} is stung for {damage1} damage and is poisoned!\n', typingActive)
        else:
            damage1 = 0
            print_slow(f'{p1.name} swats a BEE away!\n', typingActive)

        hit = random.randrange(0, 4)
        if hit >= 1:
            dam = random.randrange(foe.ATK // 2, foe.ATK // 1.5)
            damage2 = max(round(dam * p1.DEF * 0.1 * p1.TDEF * 0.1), 0)
            p1.POISON += 1
            print_slow(f'{p1.name} is stung for {damage2} damage and is poisoned!\n', typingActive)
        else:
            damage2 = 0
            print_slow(f'{p1.name} swats a BEE away!\n', typingActive)

            hit = random.randrange(0, 4)
        if hit >= 1:
            dam = random.randrange(foe.ATK // 2, foe.ATK // 1.5)
            damage3 = max(round(dam * p1.DEF * 0.1 * p1.TDEF * 0.1), 0)
            p1.POISON += 1
            print_slow(f'{p1.name} is stung for {damage3} damage and is poisoned!\n', typingActive)
        else:
            damage3 = 0
            print_slow(f'{p1.name} swats a BEE away!\n', typingActive)

        tl_damage = damage1 + damage2 + damage3
        p1.HP = min(max(p1.HP - tl_damage, 0), p1.MaxHP)
        foe.MP -= 1
        print_slow(
            f'{p1.name} has taken {tl_damage} total damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.', typingActive
        )


#Help menu for combat
def combat_menu(p1, typingActive):
  if p1.job == "WARRIOR":
      print_slow(
          "Battle commands:\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nSTRIKE: Wildy strike the foe up to 3 times.\nHARDEN: Restore some HP, temp. increase def for 1 turn.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\n", typingActive
      )
  elif p1.job == "WIZARD":
      print_slow(
          "Battle commands:\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nBOLT: Cast magical bolt dealing high damage.\nFOCUS: Concentrates to increase damage of next attack. Chance to restore MP\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\n", typingActive
      )

  elif p1.job == "THIEF":
      print_slow(
          "Battle commands:\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nSTEAL: Steal GP from enemy. Chance to fail.\nTHROW: Throw up to 3 poison daggers at the enemy. Deals damage and poisons.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\n", typingActive
      )