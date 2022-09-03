import random
from slowprint import *

class player:
#instance player
    def __init__(self, name, job, skills, inventory, materials, lvl, Nlvl, xp, MaxHP, HP, MaxMP, MP, ATK, DEF, TDEF, GP, MaxPOTS, POTS, MaxANT, ANT, MaxETR, ETR, MaxSMB, SMB, POISON, RJ, GR, GrLvl, gobCount, faeCount, PlantP, MonP, RareP, FaeP, DragonP, alive):
        self.name = name
        self.job = job
        self.skills = skills
        self.inventory = inventory
        self.materials = materials
        self.lvl = lvl
        self.Nlvl = Nlvl
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
        self.GR = GR
        self.GrLvl = GrLvl
        self.gobCount = gobCount
        self.faeCount = faeCount
        self.PlantP = PlantP
        self.MonP = MonP
        self.RareP = RareP
        self.FaeP = FaeP
        self.DragonP = DragonP
        self.alive = alive
       
      
#check player stats
    def stat_check(self, typingActive):
        print_slow(f'\nCurrent Stats:\n{self.name}\n{self.job} Lvl {self.lvl}\n{self.xp}/{self.Nlvl} EXP\n{self.HP}/{self.MaxHP} HP\n{self.MP}/{self.MaxMP} MP\n{self.ATK} ATK\n{(100 - self.DEF)}% DEF\n{self.GP} GP\n{self.POTS}/{self.MaxPOTS} POTIONS\n{self.ANT}/{self.MaxANT} ANTIDOTES\n{self.ETR}/{self.MaxETR} ETHERS\n{self.SMB}/{self.MaxSMB} SMOKE BOMBS \n', typingActive)
    def stat_sCheck(self, typingActive):
        print_slow(f'\nCurrent Stats:\n{self.name}\n{self.job} Lvl {self.lvl}\n{self.xp}/{self.Nlvl}EXP\n{self.HP}/{self.MaxHP} HP\n{self.MP}/{self.MaxMP} MP\n{self.ATK} ATK\n{(100 - self.DEF)}% DEF\n', typingActive)
      
#define combat structure
    def level_up(self, typingActive):
      if self.lvl == 21:
        print_slow(f'{self.name} has reached the max level. \n', typingActive)
      elif self.lvl < 21:
        while self.xp < self.Nlvl:
            print_slow(f'{self.name} has {self.xp}/{self.Nlvl} EXP. \n', typingActive)
            break
        while self.xp >= self.Nlvl:
            self.lvl += 1
            self.xp -= self.Nlvl
            if self.lvl < 21:
              self.Nlvl = round(self.Nlvl * 1.65)
            elif self.lvl == 21:
              self.Nlvl = 'MAX'
            print_slow("*****LEVEL UP!*****", typingActive)
            print_slow(f'{self.name} Leveled up! {self.name} is now {self.lvl} \n', typingActive)
            if (self.lvl % 3) != 0:
              if self.job == "WARRIOR": 
                self.MaxHP += 20
                self.HP = self.MaxHP 
                self.MP = self.MaxMP
                self.DEF = max(self.DEF - 1.5, 25)
              elif self.job == 'WIZARD' or self.job == "WITCH":
                self.MaxHP += 10
                self.HP = self.MaxHP
                self.MP = self.MaxMP
                self.ATK += 2
              elif self.job == 'THIEF':
                self.MaxHP += 15
                self.HP = self.MaxHP
                self.MP = self.MaxMP
                self.ATK += 1
                self.DEF = max(self.DEF - 1.5, 25)
                
            if (self.lvl % 3) == 0:
              if self.job == "WARRIOR": 
                self.MaxHP += 30
                self.HP = self.MaxHP
                self.MaxMP += 1
                self.MP = self.MaxMP
                self.ATK += 2
                self.DEF = max(self.DEF - 3, 25)
              elif self.job == 'WIZARD' or self.job == "WITCH":
                self.MaxHP += 20
                self.HP = self.MaxHP
                self.MaxMP += 2
                self.MP = self.MaxMP
                self.ATK += 2
                self.DEF = max(self.DEF - 3, 25)
              elif self.job == 'THIEF':
                self.MaxHP += 30
                self.HP = self.MaxHP
                self.MaxMP += 1
                self.MP = self.MaxMP
                self.ATK += 2
                self.DEF = max(self.DEF - 2, 25)
                
            if self.lvl == 2:
              if self.job == 'WARRIOR':
                self.skills.append('STRIKE')
              elif self.job == 'WIZARD' or self.job == "WITCH":
                self.skills.append('BOLT')
              elif self.job == 'THIEF':
                self.skills.append('THROW')      
            if self.lvl == 5:
              if self.job == 'WARRIOR':
                self.skills.append('BERSERK')
              elif self.job == 'WIZARD' or self.job == "WITCH":
                self.skills.append('STORM')
              elif self.job == 'THIEF':
                self.skills.append('MUG') 
            if self.lvl == 10:
              if self.job == 'WARRIOR':
                self.skills.append('BLOOD')
              elif self.job == 'WIZARD' or self.job == "WITCH":
                self.skills.append('BLAST')
              elif self.job == 'THIEF':
                self.skills.append('HASTE')
     
            self.stat_check(typingActive)
            break

    def materials_list(self):
      if self.PlantP > 0 and 'PLANT PARTS' not in self.materials:
        self.materials.append('PLANT PARTS')
      if self.MonP > 0 and 'MONSTER GUTS' not in self.materials:
        self.materials.append('MONSTER GUTS')
      if self.RareP > 0 and 'RARE MONSTER PARTS' not in self.materials:
        self.materials.append('RARE MONSTER PARTS')
      if self.FaeP > 0 and 'FAE DUST' not in self.materials:
        self.materials.append('FAE DUST')
      if self.DragonP > 0 and 'DRAGON SCALES' not in self.materials:
        self.materials.append('DRAGON SCALES')
        
    def material_print(self, typingActive):
      if "PLANT PARTS" in self.materials:
        print_slow(f'\nPLANT PARTS: {self.PlantP}', typingActive)
      if "MONSTER GUTS" in self.materials:
        print_slow(f'\nMONSTER GUTS: {self.MonP}', typingActive)
      if "RARE MONSTER PARTS" in self.materials:
        print_slow(f'\nRARE MONSTER PARTS: {self.RareP}', typingActive)
      if "FAE DUST" in self.materials:
        print_slow(f'\nFAE DUST: {self.FaeP}', typingActive)
      if "DRAGON SCALES" in self.materials:
        print_slow(f'\nDRAGON SCALES: {self.DragonP}\n\n', typingActive)
        
      
def stat_check_menu(typingActive):
    print_slow(
        'Starting STATS:\nWARRIOR\nLvl 1\n70 HP\n3 MP\n16 ATK\n30% DEF\n100 GP\n4 POTIONS\n1 ANTIDOTE\n0 ETHER\n1 SMOKE BOMBS\nHARDEN: Restores HP and raises Temp. DEF\n\nWIZARD\nLvl 1\n45 HP\n6 MP\n22 ATK\n10% DEF\n100 GP\n3 POTIONS\n1 ANTIDOTE\n1 ETHER\n1 SMOKE BOMBS\nFOCUS: Concentrate power to increase damage for next few turns.\n \nTHIEF\nLvl 1\n55 HP\n5 MP\n19 ATK\n20% DEF\n100 GP\n3 POTIONS\n2 ANTIDOTES\n1 ETHER\n3 SMOKE BOMBS\nSTEAL: Steals GP. Chance to fail.\n', typingActive
    )


class enemy:
    def __init__(self, name, skill, item, drop, exp, MaxHP, HP, MaxMP, MP, ATK, DEF, TDEF, MaxGP, MinGP, MaxPOTS, POTS, POISON, boss):
        self.name = name
        self.skill = skill
        self.item = item
        self.drop = drop
        self.exp = exp
        self.MaxHP = MaxHP
        self.HP = HP
        self.MaxMP = MaxMP
        self.MP = MP
        self.ATK = ATK
        self.DEF = DEF
        self.TDEF = TDEF
        self.MaxGP = MaxGP
        self.MinGP = MinGP
        self.MaxPOTS = MaxPOTS
        self.POTS = POTS   
        self.POISON = POISON
        self.boss = boss

    def stat_check(self, typingActive):
          print_slow(f'\n{self.name}\n{self.HP}/{self.MaxHP} HP\n', typingActive)

#item drops 1=pantp 2=monp 3=rarep 4=faep 5=dragp 6=pot 7=ant 8=etr 9=smkb

p2 = enemy("Goblin", 2, 2, 80, 20, 25, 25, 3, 3, 10, 95, 100, 20, 5, 0, 0, 0, 0)
p3 = enemy("Hobgoblin", 2, 2, 80, 25, 35, 35, 4, 4, 13, 90, 100, 30, 10, 1, 1, 0, 0)
p3b = enemy("Hobgoblin", 2, 2, 65, 25, 35, 35, 4, 4, 13, 90, 100, 30, 10, 1, 1, 0, 1)
p4 = enemy("Skeleton", 2, 2, 85, 35, 40, 40, 2, 2, 14, 80, 100, 40, 10, 2, 2, 0, 0)
p5 = enemy("Bunny", 1, 2, 100, 5, 5, 5, 1, 1, 3, 100, 100, 5, 1, 0, 0, 0, 0)
p6 = enemy("Troll", 3, 3, 85, 50, 80, 80, 2, 2, 16, 70, 100, 40, 15, 0, 0, 0, 0)
p7 = enemy("Honey Badger", 3, 2, 50, 15, 15, 15, 2, 2, 11, 90, 100, 15, 5, 1, 1, 0, 0)
p8 = enemy("Crab", 1, 2, 90, 15, 30, 30, 1, 1, 8, 70, 100, 20, 10, 0, 0, 0, 0)
p9 = enemy("Dark Mage", 4, 8, 92, 40, 40, 40, 4, 4, 18, 95, 100, 45, 25, 1, 1, 0, 0)
p10 = enemy("Wyrm", 6, 5, 99, 100, 120, 120, 3, 3, 22, 70, 100, 110, 75, 0, 0, 0, 0)
p11 = enemy("Skade", 6, 5, 99, 999, 999, 999, 99, 99, 99, 25, 100, 999, 99, 9, 9, 0, 0)
p12 = enemy("Bear", 3, 2, 55, 65, 75, 75, 3, 3, 16, 85, 100, 65, 45, 1, 1, 0, 1)
p13 = enemy("Thief", 5, 9, 95, 35, 55, 55, 3, 3, 11, 85, 100, 65, 40, 1, 1, 0, 0)
p14 = enemy("Giant Bee", 7, 2, 85, 20, 15, 15, 2, 2, 8, 90, 100, 20, 5, 0, 0, 0, 0)
p14b = enemy("Giant Bee", 7, 2, 85, 20, 15, 15, 2, 2, 8, 90, 100, 20, 5, 0, 0, 0, 1)
p15 = enemy("Giant Bee Swarm", 7, 2, 80, 50, 60, 60, 3, 3, 16, 85, 100, 20, 5, 1, 1, 0, 0)
p15b = enemy("Giant Bee Swarm", 7, 2, 80, 50, 60, 60, 3, 3, 16, 85, 100, 20, 5, 1, 1, 0, 1)
p16 = enemy("Mandragora", 8, 1, 0, 90, 120, 120, 3, 3, 24, 75, 100, 80, 65, 1, 1, 0, 1)
p17 = enemy("'Shroomling", 8, 1, 65, 30, 60, 60, 1, 1, 16, 85, 100, 30, 10, 1, 1, 0, 0)
p18 = enemy("Gnome", 5, 4, 80, 25, 35, 35, 2, 2, 9, 90, 100, 25, 5, 1, 1, 0, 0)
p19 = enemy("Zomblin", 2, 2, 80, 30, 30, 30, 2, 2, 13, 80, 100, 25, 5, 1, 1, 0, 0)
p20 = enemy("Kapa", 1, 3, 85, 25, 55, 55, 3, 3, 15, 80, 100, 30, 10, 1, 1, 0, 0)
p21 = enemy("Moldy Zomblin", 2, 1, 80, 40, 40, 40, 2, 2, 17, 75, 100, 30, 10, 1, 1, 0, 0)
p22 = enemy("Goblin Gang", 2, 2, 75, 40, 60, 60, 4, 4, 19, 85, 100, 50, 20, 1, 1, 0, 0)
p22b = enemy("Goblin Gang", 2, 2, 70, 40, 60, 60, 4, 4, 19, 85, 100, 50, 20, 1, 1, 0, 1)
p23 = enemy("Goblin Queen", 9, 3, 0, 120, 200, 200, 5, 5, 25, 80, 100, 80, 40, 0, 0, 0, 1)
p24 = enemy("Giant Bee Queen", 10, 3, 20, 130, 175, 175, 4, 4, 21, 80, 100, 60, 45, 0, 0, 0, 1)
p25 = enemy("Killer Bee", 7, 2, 80, 50, 75, 75, 5, 5, 19, 90, 100, 25, 10, 1, 1, 0, 0)
p26 = enemy("Mercenary Rat", 2, 2, 85, 35, 50, 50, 3, 3, 17, 80, 100, 50, 10, 1, 1, 0, 0)
p27 = enemy("Hawk", 1, 2, 100, 30, 40, 40, 2, 2, 15, 85, 100, 15, 5, 1, 1, 0, 0)
p28 = enemy("Traveling Merchant", 5, 5, 0, 35, 55, 55, 3, 3, 11, 85, 100, 65, 40, 1, 1, 0, 0)
p29 = enemy("Ozzing Slime", 8, 3, 90, 35, 85, 85, 3, 3, 14, 45, 100, 55, 35, 2, 2, 0, 0)
p29b = enemy("Ozzing Slime", 8, 3, 0, 35, 95, 95, 3, 3, 14, 45, 100, 55, 35, 2, 2, 0, 1)
p30 = enemy("Mandrake Child", 8, 1, 60, 45, 65, 65, 2, 2, 16, 90, 100, 45, 35, 1, 18, 0, 0)
p31 = enemy("Ogre", 11, 2, 65, 70, 100, 100, 2, 2, 20, 70, 100, 55, 25, 0, 0, 0, 0)
p32 = enemy("Suiko", 12, 3, 80, 80, 110, 110, 3, 3, 22, 70, 100, 70, 25, 0, 0, 0, 0)
p33 = enemy("Imp", 13, 4, 75, 60, 65, 65, 4, 4, 18, 80, 100, 50, 25, 1, 1, 0, 0)
p34 = enemy("Donkey", 1, 10, 0, 35, 45, 45, 1, 1, 10, 90, 100, 20, 10, 0, 0, 0, 0)
p35 = enemy("Ogre Chief", 11, 3, 0, 175, 200, 200, 2, 2, 26, 70, 100, 105, 85, 0, 0, 0, 1)
p36 = enemy("Pixie", 14, 4, 50, 45, 65, 65, 4, 4, 14, 80, 100, 35, 15, 2, 2, 0, 0)
p37 = enemy("Fairy", 14, 4, 50, 75, 95, 95, 4, 4, 18, 80, 100, 65, 35, 1, 1, 0, 0)
p38 = enemy("Nymph", 14, 4, 60, 90, 115, 115, 4, 4, 22, 75, 100, 75, 40, 1, 1, 0, 0)
p39 = enemy("Fish-Man", 15, 2, 70, 65, 80, 80, 3, 3, 19, 78, 100, 45, 25, 0, 0, 0, 0)
p40 = enemy("Dark Fairy Prince", 14, 4, 0, 155, 195, 195, 6, 6, 28, 75, 100, 85, 65, 1, 1, 0, 1)
p41 = enemy("Hexopus", 1, 2, 50, 85, 100, 100, 1, 1, 24, 80, 100, 65, 45, 1, 1, 0, 1)
p42 = enemy("Sand Squid", 1, 2, 75, 90, 110, 110, 1, 1, 22, 70, 100, 80, 50, 1, 1, 0, 1)
p43 = enemy("King Crab", 1, 2, 80, 95, 130, 130, 1, 1, 21, 60, 100, 60, 30, 0, 0, 0, 0)
p44 = enemy("Murmaider", 15, 3, 95, 105, 145, 145, 2, 2, 24, 82, 100, 80, 55, 0, 0, 0, 0)
p45 = enemy("Mangy Pirate", 5, 6, 75, 95, 80, 80, 2, 2, 19, 80, 100, 75, 50, 0, 0, 0, 0)
p46 = enemy("Wolverine", 3, 2, 50, 50, 55, 55, 2, 2, 18, 86, 100, 35, 15, 1, 1, 0, 0)
p47 = enemy("Orc Scout", 2, 2, 70, 80, 100, 100, 3, 3, 24, 78, 100, 65, 45, 0, 0, 0, 0)
p48 = enemy("Auroch", 3, 2, 60, 75, 75, 75, 2, 2, 16, 75, 100, 40, 30, 0, 0, 0, 0)
p49 = enemy("Mountain Goat", 3, 2, 70, 55, 60, 60, 2, 2, 15, 80, 100, 35, 15, 0, 0, 0, 0)
p50 = enemy("Bunny", 3, 9, 30, 80, 100, 100, 2, 2, 30, 100, 100, 50, 10, 0, 0, 0, 0)
#p28 = enemy("Smeldar", 4, 1, 300, 300, 5, 5, 24, 8, 10, 100, 50, 0, 0, 0, 1)


enemy_spawnT = [p28,p2]
enemy_spawn0 = [p2, p5, p7]  #cliff enemies
enemy_spawn1 = [p2, p3, p7, p13]  #forest enemies
enemy_spawn2 = [p2, p3, p4, p6]  #thicket enemies
enemy_spawn3 = [p5, p7, p14, p18]  #berry enemies
enemy_spawn4 = [p2, p4, p9, p19]  #shrine enemies
enemy_spawn5 = [p2, p3, p8, p20, p28]  #river enemies
enemy_spawn6 = [p2, p4, p7, p13,]  #hill enemies
enemy_spawn7 = [p2, p3, p17, p18, p21, p36]  #mushroom enemies
enemy_spawn8 = [p2, p2, p3, p3, p22]  #Goblin Den
enemy_spawn9 = [p14, p15, p26, p27, p28]  #meadow
enemy_spawn10 = [p14b, p15b] #hive enemies
enemy_spawn11 = [p3, p7, p17, p30, p36] #Rotted woods
enemy_spawn12 = [p18, p26, p29, p31, p32, p33] #Ogre Swamp 1
enemy_spawn13 = [p21, p26, p29, p31, p32, p33] #Ogre Swamp 2
enemy_spawn14 = [p21, p21, p26, p26, p29, p29, p31, p31, p32, p32, p33, p33, p34] #Ogre Swamp 3
enemy_spawn15 = [p4, p6, p9, p13, p15, p18, p36, ] #Misty Woods 1
enemy_spawn16 = [p41, p42, p43, p44, p45 ] #coast enemies
enemy_spawn17 = [p28, p46, p47, p48, p50] #plains enemies
enemy_spawn18 = [p10, p46, p47, p48, p49,] #foothills enemies