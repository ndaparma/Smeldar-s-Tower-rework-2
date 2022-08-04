import random

class player:
#instance player
    def __init__(self, name, job, inventory, lvl, Nlvl, xp, MaxHP, HP, MaxMP, MP, ATK, DEF, TDEF, GP, MaxPOTS, POTS, MaxANT, ANT, MaxETR, ETR, MaxSMB, SMB, POISON, RJ, GrLvl, gobCount, alive):
        self.name = name
        self.job = job
        self.lvl = lvl
        self.Nlvl = Nlvl
        self.inventory = inventory
        self.xp = xp
        self.MaxHP = MaxHP
        self.HP = HP
        self.MaxMP = MaxMP
        self.MP = MP
        self.ATK = ATK
        self.DEF = DEF
        self.TDEF = TDEF
        self.GP = GP
        self.MaxPOTS = MaxPOTS
        self.POTS = POTS
        self.MaxANT = MaxANT
        self.ANT = ANT
        self.MaxETR = MaxETR
        self.ETR = ETR
        self.MaxSMB = MaxSMB
        self.SMB = SMB
        self.POISON = POISON
        self.RJ = RJ
        self.GrLvl = GrLvl
        self.alive = alive
        self.gobCount = gobCount
      
#check player stats
    def stat_check(self):
        print('Current Stats:')
        print(self.name)
        print(f'{self.job} Lvl {self.lvl}')
        print(f'{self.xp}/{self.Nlvl}EXP')
        print(f'{self.HP}/{self.MaxHP} HP')
        print(f'{self.MP}/{self.MaxMP} MP')
        print(f'{self.ATK} ATK')
        print(f'{(10 - self.DEF) * 10}% DEF')
        print(f'{self.GP} GP')
        print(f'{self.POTS}/{self.MaxPOTS} POTIONS')
        print(f'{self.ANT}/{self.MaxANT} ANTIDOTES')
        print(f'{self.ETR}/{self.MaxETR} ETHERS')
        print(f'{self.SMB}/{self.MaxSMB} SMOKE BOMBS \n')
      
#define combat structure
    def item_check(self):
      while True:
        print(f'\nInventory: {self.inventory}')
        print('Type item name for more info or BACK to exit menu.\n')
        selc = input().upper().strip()
        if selc in self.inventory:
          print(f"\n{key_items[selc]['description']}")
        elif selc == 'BACK':
          break
        else:
          print('Invalid selection. Try again.')

    def level_up(self):
      while self.xp < self.Nlvl:
          print(f'{self.name} has {self.xp}/{self.Nlvl} EXP. \n')
          break
      while self.xp >= self.Nlvl:
          self.lvl += 1
          self.xp -= self.Nlvl
          self.Nlvl = round(self.Nlvl * 1.65)
          print("*****LEVEL UP!*****")
          print(f'{self.name} Leveled up! {self.name} is now {self.lvl} \n')
          if self.job == "WARRIOR" and (self.lvl % 2) != 0:
              self.MaxHP += 20
              self.HP = self.MaxHP 
              self.MaxMP += 0
              self.MP = self.MaxMP
              self.ATK += 0
              self.DEF = max(self.DEF - .3, 3)
          elif self.job == "WARRIOR" and (self.lvl % 3) == 0:
              self.MaxHP += 30
              self.HP = self.MaxHP
              self.MaxMP += 1
              self.MP = self.MaxMP
              self.ATK += 2
              self.DEF = max(self.DEF - .5, 3)
          elif self.job == 'WIZARD' and (self.lvl % 3) != 0:
              self.MaxHP += 10
              self.HP = self.MaxHP
              self.MaxMP += 0
              self.MP = self.MaxMP
              self.ATK += 1
              self.DEF += 0
          elif self.job == 'WIZARD' and (self.lvl % 3) == 0:
              self.MaxHP += 15
              self.HP = self.MaxHP
              self.MaxMP += 2
              self.MP = self.MaxMP
              self.ATK += 2
              self.DEF = max(self.DEF - .5, 3)
          elif self.job == 'THIEF' and (self.lvl % 3) != 0:
              self.MaxHP += 15
              self.HP = self.MaxHP
              self.MaxMP += 0
              self.MP = self.MaxMP
              self.ATK += 1
              self.DEF = max(self.DEF - .2, 3)
          elif self.job == 'THIEF' and (self.lvl % 3) == 0:
              self.MaxHP += 20
              self.HP = self.MaxHP
              self.MaxMP += 1
              self.MP = self.MaxMP
              self.ATK += 1
              self.DEF = max(self.DEF - .5, 3)
          self.stat_check()

   

      



def stat_check_menu():
    print(
        'Starting STATS:\nWARRIOR\nLvl 1\n70 HP\n3 MP\n12 ATK\n30% DEF\n100 GP\n4 POTIONS\n1 ANTIDOTE\n0 ETHER\n1 SMOKE BOMBS\nHARDEN: Restores HP and raises Temp. DEF\nSTRIKE: Wildly strike at foe up to 3 times.\n\nWIZARD\nLvl 1\n40 HP\n8 MP\n18 ATK\n10% DEF\n100 GP\n3 POTIONS\n1 ANTIDOTE\n1 ETHER\n1 SMOKE BOMBS\nBOLT: Powerful magic attack\nFOCUS: Concentrate power for next attack. Chance to restore MP.\n \nTHIEF\nLvl 1\n55 HP\n5 MP\n15 ATK\n20% DEF\n100 GP\n3 POTIONS\n2 ANTIDOTES\n1 ETHER\n3 SMOKE BOMBS\nSTEAL: Steals GP. Chance to fail.\nTHROW: Throws up to 3 daggers to inflect damage/poison.'
    )

class enemy:
    def __init__(self, name, skill, exp, MaxHP, HP, MaxMP, MP, ATK, DEF, TDEF, MaxGP, MinGP, MaxPOTS, POTS, POISON, boss):
        self.name = name
        self.exp = exp
        self.skill = skill
        self.MaxHP = MaxHP
        self.HP = HP
        self.MaxMP = MaxMP
        self.MP = MP
        self.ATK = ATK
        self.DEF = DEF
        self.TDEF = TDEF
        self.MaxGP = MaxGP
        self.MinGP = MinGP
        self.POTS = POTS
        self.MaxPOTS = MaxPOTS
        self.POISON = POISON
        self.boss = boss

    def stat_check(self):
          print(self.name)
          print(f'{self.HP}/{self.MaxHP} HP')
          print(f'{self.MP}/{self.MaxMP} MP')
          print(f'{self.ATK} ATK')
          print(f'{(10 - self.DEF) * 10}% DEF\n')



p2 = enemy("Goblin", 2, 20, 25, 25, 3, 3, 10, 9.5, 10, 20, 5, 0, 0, 0, 0)
p3 = enemy("Hobgoblin", 2, 25, 35, 35, 4, 4, 13, 9, 10, 30, 10, 1, 1, 0, 0)
p4 = enemy("Skeleton", 2, 35, 40, 40, 2, 2, 14, 8, 10, 40, 10, 2, 2, 0, 0)
p5 = enemy("Bunny", 1, 5, 5, 5, 1, 1, 3, 10, 10, 5, 1, 0, 0, 0, 0)
p6 = enemy("Troll", 3, 50, 80, 80, 2, 2, 16, 7, 10, 40, 15, 0, 0, 0, 0)
p7 = enemy("Honey Badger", 3, 15, 15, 15, 2, 2, 11, 9, 10, 15, 5, 1, 1, 0, 0)
p8 = enemy("Crab", 1, 15, 30, 30, 1, 1, 8, 7, 10, 20, 10, 0, 0, 0, 0)
p9 = enemy("Dark Mage", 4, 40, 40, 40, 4, 4, 18, 9.5, 10, 45, 25, 1, 1, 0, 0)
p10 = enemy("Dragon", 6, 100, 100, 100, 3, 3, 20, 6.5, 10, 175, 75, 0, 0, 0, 0)
p11 = enemy("Skade", 6, 999, 999, 999, 99, 99, 99, 1, 10, 999, 99, 9, 9, 0, 0)
p12 = enemy("Bear", 3, 65, 75, 75, 3, 3, 16, 8.5, 10, 65, 45, 1, 1, 0, 1)
p13 = enemy("Thief", 5, 35, 55, 55, 3, 3, 11, 8.5, 10, 65, 40, 1, 1, 0, 0)
p14 = enemy("Giant Bee", 7, 20, 15, 15, 2, 2, 8, 9, 10, 20, 5, 0, 0, 0, 0)
p15 = enemy("Giant Bee Swarm", 7, 50, 75, 75, 3, 3, 16, 8.5, 10, 20, 5, 1, 1, 0, 0)
p16 = enemy("Mandragora", 8, 90, 120, 120, 3, 3, 24, 7.5, 10, 40, 15, 1, 1, 0, 1)
p17 = enemy("'Shroomling", 8, 30, 60, 60, 1, 1, 16, 8.5, 10, 30, 10, 1, 1, 0, 0)
p18 = enemy("Gnome", 5, 25, 35, 35, 2, 2, 9, 9, 10, 25, 5, 1, 1, 0, 0)
p19 = enemy("Zomblin", 2, 30, 30, 30, 2, 2, 13, 8, 10, 25, 5, 1, 1, 0, 0)
p20 = enemy("Kapa", 1, 25, 55, 55, 3, 3, 15, 8, 10, 30, 10, 1, 1, 0, 0)
p21 = enemy("Moldy Zomblin", 2, 40, 40, 40, 2, 2, 17, 7.5, 10, 30, 10, 1, 1, 0, 0)
p22 = enemy("Goblin Gang", 2, 40, 60, 60, 4, 4, 19, 8.5, 10, 50, 20, 1, 1, 0, 0)
p23 = enemy("Goblin Queen", 9, 120, 200, 200, 5, 5, 25, 8, 10, 80, 40, 0, 0, 0, 1)
p24 = enemy("Giant Bee Queen", 10, 130, 175, 175, 4, 4, 21, 8, 10, 60, 45, 0, 0, 0, 1)
p25 = enemy("Killer Bee", 7, 50, 75, 75, 5, 5, 19, 9, 10, 25, 10, 1, 1, 0, 0)
p26 = enemy("Mercenary Rat", 2, 35, 50, 50, 3, 3, 17, 8, 10, 50, 10, 1, 1, 0, 0)
p27 = enemy("Hawk", 1, 30, 40, 40, 2, 2, 15, 8.5, 10, 15, 5, 1, 1, 0, 0)
p28 = enemy("Smeldar", 4, 1, 300, 300, 5, 5, 24, 8, 10, 100, 50, 0, 0, 0, 1)



enemy_spawn0 = [p2, p5, p7]  #cliff enemies
enemy_spawn1 = [p2, p3, p7, p13]  #forest enemies
enemy_spawn2 = [p2, p3, p4, p6]  #thicket enemies
enemy_spawn3 = [p5, p7, p14, p18]  #berry enemies
enemy_spawn4 = [p2, p4, p9, p19]  #shrine enemies
enemy_spawn5 = [p2, p3, p5, p8, p20]  #river enemies
enemy_spawn6 = [p2, p4, p7, p13]  #hill enemies
enemy_spawn7 = [p2, p3, p17, p18, p21]  #mushroom enemies
enemy_spawn8 = [p2, p2, p3, p3, p22]  #Goblin Den
enemy_spawn9 = [p14, p15, p26, p27]  #meadow
enemy_spawn10 = [p14, p15] #hive enemies