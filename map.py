blank_map1 = """
_________^[N]^________
|                    |
|                    |
<[W]                 >
<                 [E]>
|                    |
|                    |
|________v[S]v_______|

"""

camp_map1 = """
_________^[N]^________
|  YY Y          YY Y|
|Y                 Y |
<[W]              Y  |
<         (#)   Y  Y |
| Y Y     ===     Y  |
|Y              Y  Y |
|_Y_Y____v[S]v____Y__|

"""

camp_map2 = """
_________^[N]^________
|  YY Y          YY Y|
|Y                 Y |
<[W]              Y  |
<         ( )   Y  Y |
| Y Y     ===     Y  |
|Y              Y  Y |
|_Y_Y____v[S]v____Y__|

"""

cliff_map1 = """
______________________
|!         Y     !   |
| !       ,|       ! |
|  !                 >
| !                [E]>
| !                  |
|  ! !               |
|______!_____________|

"""

cliff_map2 = """
______________________
|!         Y     !   |
| !        |       ! |
|  !                 >
| !                [E]>
| !                  |
|  ! !               |
|______!_____________|

"""

town_map1 = """
_________^[N]^________
|/_\            /_\ Y|
||D|     ____   |D|  |
<[W]    / /\ \       >
<       \_\/_/    [E]>
|Y                   |
|=======|`````|======|
|_______|v[S]v|______|

"""

shop_map1 = """
______________________
|          ||++++ ++ |
|          || counter|
<[W]       |_========|
<                    |
|                    |
|   |     |     |    |
|___|_____|_____|____|

"""


inn_map1 = """
______________________
|         o ||counter|
|   o   o[]o|_=======|
|  o[]o   o    o o o >
|   o             [E]>
|_______________     |
|| | | | | | | |     |
|____________________|

"""

castle_map1 = """
________^[N]^_________
|   | K|:::::|K  |   |
|---   |:::::|    ---|
|      |:::::|       |
|      |:::::|       |
|      |:::::|       |
|___  K|::Ü::|K   ___|
|___|____________|___|

"""

forest_map1 = """
_________^[N]^_________
|Y YY Y          Y Y Y|
|Y  Y          YY YY Y|
<[W]      [~]         >
<          |       [E]>
|Y YYY          YY YY |
| Y Y            Y  Y |
|YY___Y__v[S]v__Y___Y_|

"""

hill_map1 = """
________^.[N].^_______
|Y Y Y           xxxx|
|Y Y  Y        xxxxx |
<[W]          xxxxxx >
<                 [E]>
|YY Y Y        xxxxx |
|Y Y Y  ZZZZZZZ xxxxx|
|YY_Y_Y__v[S]v_Y__YY_|

"""

hill_map2 = """
_________^[N]^________
|Y Y Y           xxxx|
|Y Y  Y        xxxxx |
<[W]          xxxxxx >
<                 [E]>
|YY Y Y        xxxxx |
|Y Y Y          xxxxx|
|YY_Y_Y__v[S]v_Y__YY_|

"""

shrine_map1 = """
______________________
| Y   __/\__   Y  Y  |
| Y  //_/\_\\\      YY|
|Y  /|::::::|\       |
|  * |:/&&\:| *      |
|  ............      |
|    ........     Y  |
|Y__Y___v[S]v___X_xx_|

"""

berry_map1 = """
_________^[N]^________
|Y Y Y         BRB YB|
|Y BBB          BB  Y|
|Y YBB            '''>
| Y  B            [E]>
| Y BBB  BBB       ''|
|YY  B   BB   BB Y Y |
|Y_Y_Y_Y__Y_Y___Y__Y_|

"""

meadow_map1 = """
_________^[N]^________
|YY'''''''''''''Y''YY|
|Y '''''''''''''''' Y|
<[W] ''''''''''''''  >
< ''''''''''''''  [E]>
|  '''''''''''''''' Y|
|Y'''''''''''''''  Y |
|YYY__Y__v[S]v_YY_Y_Y|

"""

witch_map1 = """
______________________
| Y      s       Y  z|
| z  Y  _|/^\._   Y  |
|Y   ___ |_D_| ___   |
|Y  | U   ...  ? ?| Z|
| Y |(#)  ...  ? ?|  |
|Y        ...       Y|
|_Y__Y___v[S]v___Y_Y_|

"""

oak_map1 = """
______________________
|Y Y  ***\ \|[C] |//*|
|Y     ***\   H   /**|
<[W]       |  H  | Y |
<          |  H  |  Y|
|Y         |  H  |  Y|
| Y        |  H  | Y |
|YY_______/...H...\_Y|

"""

hive_map1 = """
______________________
|0000____________0000|
|000/     __     \\000|
|00/    / RR \    \\00|
|0/     \ __ /     \\0|
|0\                /0|
|00\              /00|
|000\____v[C]v___/000|

"""

hive_map2 = """
______________________
|0000____________0000|
|000/     __     \000|
|00/    /    \    \00|
|0/     \ __ /     \0|
|0\                /0|
|00\              /00|
|000\____v[C]v___/000|

"""

village_map1 = """
_________^[N]^________
|/ \_           _/ \_|
|[_]B Y         B[_]B|
<[W]                 >
<                 [E]>
| _/ \_              |
| y[_]         Y _/ \|
|Y_______v[S]v____[_]|

"""

tavern_map1 = """
_________^[N]^________
|8    |o        o| c |
|_  __|[]o      o| o |
|   \  o        o| u |
|                | n |
|_\  __  o       | t |
|     | o[]o    o| e |
|____8|__o______o|_r_|

"""

smith_map1 = """
______________________
| S  SS             o|
|  ()          ======|
| (C))               >
|                 [E]>
|       |            |
| o|7   |     o[]o   |
|_______|8___________|

"""

farm_map1 = """
______________________
|  y  y y y  /\\\\\\\\\\\\\|
|y  y       _|D|====||
<[W]       / /TTTTTTT|
<                    |
|???  ?????  ?????  ?|
|???  ?????  ?????  ?|
|???__?????__?????__?|

"""
cave_map1 = """
______________________
|XXXxxxxxxxXXXxXXxxXX|
|XX            xxxxXX|
<[W]                 >
<           <\    [E]>
|X                XXX|
|XXpp           XXxXX|
|XXXxXXXxXXxxxxXXXXXX|

"""
cave_map2 = """
______________________
|XXXxxxxxxxXXXxXXxxXX|
|XX            xxxxXX|
<[W]                 >
<                 [E]>
|X                XXX|
|XXpp           XXxXX|
|XXXxXXXxXXxxxxXXXXXX|

"""


cave1_map1 = """
_________^[N]^________
|XXXxxxx        XxxXX|
|XXxxxXXXx     xxxxXX|
<[W]              xXX|
<                xXXX|
|XXXXxxXXXx       XXX|
|XXxxXXx        XXxXX|
|XXXxXxX_v[S]v_XxxXXX|

"""

cave2_map1 = """
______________________
|xXXxxXXXXxxXXxXXXXXX|
|Xxx++   ++   ++ xXXx|
|xX ++ ++  +  ++  xxX|
|Xxx+ +  {-} +  ++ xX|
|X +  +            Xx|
|xx             XXxxX|
|XxxXxxX_v[S]v_XXxXxX|

"""

cave2_map2 = """
______________________
|xXXxxXXXXxxXXxXXXXXX|
|Xxx++   ++   ++ xXXx|
|xX ++ ++  +  ++  xxX|
|Xxx+ +  {o} +  ++ xX|
|X +  +            Xx|
|xx             XXxxX|
|XxxXxxX_v[S]v_XXxXxX|

"""

cave3_map1 = """
_________^[N]^________
|XXXxxxx        XxxXX|
|XXxxxXXXx       xxXX|
|XXxxxXXx      xXXxXX|
|xxXXXxX      xxxxXXX|
|XXxxxX       XxXxXXX|
|XXxxXXx        XXxXX|
|XXXxXXX_v[S]v_XxxXXX|

"""

cave4_map1 = """
_________^[N]^________
|XxxXxx         XxxXX|
|XxxxX           xxXX|
|XX  !               >
|Xxx !            [E]>
|Xx    !          XXX|
|XX      !!!!!! xXxXX|
|XXXx__________!xxXXX|

"""


cave5_map1 = """
______________________
|xxxXXXxxXxXXXxXXxxXX|
|XXxxX         xxxxXX|
<[W]              XXX|
<                 xXX|
|Xxx             xXXX|
|XXxxXXXx       XXxXX|
|XXXxXXXxXXxxxxXXXXXX|

"""

river_map1 = """
_________^[N]^________
| y  |   \        Y Y|
|    |    |        YY|
|y  /    /           >
|  /    / z       [E]>
|  |    |           Y|
|  |    |         Y Y|
|y_|____|v[S]v_____YY|

"""

waterfall_map1 = """
_________^[N]^________
|  |    |        YY Y|
|  |    |          YY|
| /      \        Y Y|
|/       x\      Y YY|
||       X|         Y|
|X\&&&&&&/X        YY|
|Xx|&&&&|x________Y_Y|

"""

lake_map1 = """
_________^[N]^________
|         \        YY|
|           \     Y Y|
|           |      @@>
|          /      [E]>
|         /        YY|
|___/\    |       YY |
|y___|___/v[S]v___Y_Y|

"""

lake_map2 = """
_________^[N]^________
|         \        YY|
|           \     Y Y|
|           |        >
|          /      [E]>
|         /        YY|
|___/\    |       YY |
|y___|___/v[S]v___Y_Y|

"""

boat_map1 = """
_____________________
|    _/\_     |Y YYY|
| ___|__|__  /  Y  Y|
|   \____H/ /     Y |
|   [::::::]       Y|
|          /      YY|
|         /      Y Y|
|________/v[S]v__YY_|

"""

mushroom_map1 = """
_________^[N]^________
|Y M m  m    m   m Mm|
| Y   M         m  mM|
<[W]  m   m   M  mm Y|
<          m    m  MY|
|Y  mmm      m     mM|
|Y Y Mm          Mm Y|
|Y_MYm_M_v[S]v_M__m_M|

"""

fairy_map1 = """
_________^[N]^________
|   Y  Y      M   Y  |
| Y  '''' mmm ''''  Y|
| Y '' mm ''' mm '' Y|
|Y  '' m ''''' m ' Y |
|M ''' mm ''' mm '' Y|
|Y ''''   mmm  '''' Y|
|__Y__Y__Y____M___Y__|

"""

fairy_map2 = """
_________^[N]^________
|   Y  Y      M   Y  |
| Y       mmm       Y|
| Y    mm     mm    Y|
|Y     m       m   Y |
|M     mm     mm    Y|
|Y        mmm       Y|
|__Y__Y__Y____M___Y__|

"""

rot_map1 = """
_________^[N]^________
| Y Y Z         Z  Y |
|Y   Z Z       Z    Z|
<[W]    Z     ZY   Z |
<                   Z|
|[/             ZZ Z |
| |  Y        Y M  Y |
|Y_ZM_Y__v[S]v_Y_M_Z_|

"""

swamp1_map1 = """
______________________
|   !!!!!   Z  Z   y |
|!!!     zZ      Z Zz|
<[W]                 >
<                 [E]>
|   Y     !X         |
|!!  !!!!! !!   !!!!Z|
|__!!_______ !!!_____|

"""

swamp2_map1 = """
______________________
| Y   Y   Y     z! Y |
|z           Z    !!!|
<[W]                 >
<                 [E]>
|  Y                 |
| Z z            Y X!|
|_____Y__v[S]v__Z_!!_|

"""

swamp3_map1 = """
_________^[N]^________
|¿ ¿!!Xx         Z   |
| ¿!  x ZZ         z |
|  ! z       Y       >
| ! Z             [E]>
|  !                Y|
|  !   Y          Z  |
|¿__!Zz__v[S]v_____Y_|

"""

swamp4_map1 = """
______________________
| Z  Y       Y   Z Y |
| Y        ZZ        |
|Z   {-}       {-}  Y|
|                    |
|! Y               Z |
| !Z             Y   |
|__!!__Y_v[S]v____Y__|

"""

swamp4_map2 = """
______________________
| Z  Y       Y   Z Y |
| Y        ZZ        |
|Z   {o}       {-}  Y|
|                    |
|! Y               Z |
| !Z             Y   |
|__!!__Y_v[S]v____Y__|

"""
swamp4_map3 = """
______________________
| Z  Y       Y   Z Y |
| Y        ZZ        |
|Z   {-}       {o}  Y|
|                    |
|! Y               Z |
| !Z             Y   |
|__!!__Y_v[S]v____Y__|

"""

swamp4_map4 = """
______________________
| Z  Y       Y   Z Y |
| Y        ZZ        |
|Z   {o}       {o}  Y|
|                    |
|! Y               Z |
| !Z             Y   |
|__!!__Y_v[S]v____Y__|

"""

swamp5_map1 = """
_________^[N]^________
|¿   !!          Z   |
|!!!!             z  |
<[W]    z            >
<       Zx        [E]>
|Z      Z       Y   Y|
|!Z              Y Y!|
|_!Z_____v[S]v__Z__!_|

"""

swamp6_map1 = """
_________^[N]^________
| Z Y x            Y |
|    Z              !|
<[W]            !!!! |
<    .        z!     |
| Y   .  !!!  !   ¿¿ |
|  Y !!!!¿¿ !!    ¿  |
|__z!________________|

"""

swamp7_map1 = """
______________________
|  !   ¿ !¿!    ¿¿¿  |
|!! !!  !   !!!!!!!!!|
| !   !!             >
| !               [E]>
|! Z                 |
| ! Z !!!! !!!     !!|
|__!!!__¿_!!__!!!!!__|

"""

swamp8_map1 = """
_________^[N]^________
| ¿ !              ! |
|  !                !|
| !                 !|
| !        Z     !! !|
|!         Z     ! !!|
| !!!      Z!!!!!   ¿|
|____!!!!!!__________|

"""

swamp8_map2 = """
_________^[N]^________
| ¿ !              ! |
|  !                !|
| !                 !|
| !              !! !|
|!               ! !!|
| !!!      Z!!!!!!  ¿|
|____!!!_v[S]v_______|

"""

marsh_map1 = """
______________________
| s    ¿   __  ¿  ¿  |
| ||__    [::]       |
| (_D_) ¿ [::]  ¿    >
|¿ \::\   [:::::::[E]>
|   \::\  [:::] ¿    |
| ¿  [::::::::::]  ¿ |
|____¿___|v[S]v|_¿___|

"""
plains_map1 = """
_________^[N]^________
|   !                |
|  !                 |
<[W]                 >
<::::]            [E]>
|   !                |
|     !              |
|_______!_Y__ZZ__ZY_Z|

"""

foothills_map1 = """
_________^[N]^________
|                x  x|
|                  x |
<[W]               x |
<                x   |
|                 x  |
|                x x |
|ZZ__ZY_Y_Z__YZ__Z__Z|

"""

shipwreck_map1 = """
______________________
|          /       __|
|____     /_)     /x |
<[W]+\__________/   x|
<    +  +    +  +  x |
|    +     +   +  x  |
|                 x  |
|________v[S]v_____x_|


"""

coast_map1 = """
______________________
|__                  |
|  \       __     ___|
<[W]\_____/  \___/   >
<                 [E]>
|                    |
|                    |
|________v[S]v_______|

"""

harbor1_map1 = """
_________^[N]^________
| Y  |\_        _/| Y|
|  Y |D_|      |_D|  |
<[W]                 >
<                 [E]>
| s            s    s|
| |\_        _/|  _/||
|Y|D_|______|_D|Y|_D||

"""

harborinn_map1 = """
______________________
|(-)88  |o[]o|COUNTER|
|       |o[]o|-------|
|__  ___|            >
| /               [E]>
|___  /    o _\  ____|
|     |  o[]o|      8|
|8____|___o__|_______|

"""

harbormarket_map1 = """
______________________
|   |:|   |:|   |:|  |
|___|:|___|:|___|:|__|
<[W]    $%   $%%   $%|
<                    |
|  $%  $+         $%+|
|  ++  ++           +|
|_%$___$%_v[S]v__+$%+|

"""

harborship_map1 = """
______________________
|       |:|  |:|   |:|
|T____  |:|__|:|___|:|
|__/____\            >
|:::::::          [E]>
|-------|     s      |
|       |++   |\_    |
|_______|++___|D_|___|

"""

woodsBend_map1 = """
_________^[N]^________
|Y Y YY Y      Y  Y Y|
|YY Y  Y        YY Y |
<[W]              Y Y|
<                   Y|
|Y Y   Y        Y  YY|
|Y Y YY  Y  Y YY  Y Y|
|_YY_Y_YY_YY_Y__Y__Y_|

"""

_map1 = """
______________________
|                    |
|___/\___            |
||-T  T-|            |
|                    |
|                    |
|                    |
|____________________|

"""