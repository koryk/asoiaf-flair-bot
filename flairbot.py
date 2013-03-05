# -*- coding: utf-8 -*-

import json
import badwords
import urllib
import urllib2
import cookielib
import string
import re
import StringIO
import csv
import CsvUnicode
import ConfigParser
from pprint import pprint
from urllib import quote_plus
from string import maketrans

reddit = "http://www.reddit.com"
config = ConfigParser.ConfigParser()
config.read("./config.ini")
subreddit = config.get("user","subreddit") 
credentials = {'user': config.get("user","username"), 'passwd': config.get("user","passwd")}


user_agent = "ASOIF Flair Bot"
flairs = {
    'empty': {'css_class': "empty"},
    'sellsword': {'css_class': "Sellsword"},                
    'targaryen': {'css_class': "Targaryen"},                
    'kingsguard': {'css_class': "Kingsguard"},              
    'nightswatch': {'css_class': "NightsWatch"},                
    'warriorssons': {'css_class': "WarriorsSons"},              
    'poorfellows': {'css_class': "PoorFellows"},                
    'rykkerofduskendale': {'css_class': "RykkerOfDuskendale"},          
    'rosbyofthatilk': {'css_class': "RosbyOfThatIlk"},              
    'hayfordofthatilk': {'css_class': "HayfordOfThatIlk"},          
    'masseyofstonedance': {'css_class': "MasseyOfStonedance"},          
    'stokeworthofthatilk': {'css_class': "StokeworthOfThatIlk"},            
    'chyttering': {'css_class': "Chyttering"},              
    'stauntonofrooksnest': {'css_class': "StauntonOfRooksNest"},            
    'buckwelloftheantlers': {'css_class': "BuckwellOfTheAntlers"},          
    'harte': {'css_class': "Harte"},                    
    'chelsted': {'css_class': "Chelsted"},              
    'mallery': {'css_class': "Mallery"},                
    'bruneofthedyreden': {'css_class': "BruneOfTheDyreDen"},            
    'langward': {'css_class': "Langward"},              
    'thorne': {'css_class': "Thorne"},                  
    'manning': {'css_class': "Manning"},                
    'hollard': {'css_class': "Hollard"},                
    'rollingford': {'css_class': "Rollingford"},                
    'wendwater': {'css_class': "Wendwater"},                
    'follard': {'css_class': "Follard"},                
    'edgerton': {'css_class': "Edgerton"},              
    'rambton': {'css_class': "Rambton"},                
    'cressey': {'css_class': "Cressey"},                
    'farring': {'css_class': "Farring"},                
    'bruneofbrownhollow': {'css_class': "BruneOfBrownhollow"},          
    'hoggofsowshorn': {'css_class': "HoggOfSowsHorn"},              
    'gaunt': {'css_class': "Gaunt"},                    
    'byrch': {'css_class': "Byrch"},                    
    'blount': {'css_class': "Blount"},                  
    'pyle': {'css_class': "Pyle"},                  
    'bywater': {'css_class': "Bywater"},                
    'cole': {'css_class': "Cole"},                  
    'cargyll': {'css_class': "Cargyll"},                
    'blackfyre': {'css_class': "Blackfyre"},                
    'darklynofduskendale': {'css_class': "DarklynOfDuskendale"},            
    'velaryonofdriftmark': {'css_class': "VelaryonOfDriftmark"},            
    'celtigarofclawisland': {'css_class': "CeltigarOfClawIsland"},          
    'baremmonofsharppoint': {'css_class': "BarEmmonOfSharpPoint"},          
    'sunglassofsweetportsound': {'css_class': "SunglassOfSweetportSound"},      
    'lannister': {'css_class': "Lannister"},                
    'crakehallofthatilk': {'css_class': "CrakehallOfThatIlk"},          
    'marbrandofashemark': {'css_class': "MarbrandOfAshemark"},          
    'braxofhornvale': {'css_class': "BraxOfHornvale"},              
    'lyddenofthedeepden': {'css_class': "LyddenOfTheDeepDen"},          
    'banefortofthatilk': {'css_class': "BanefortOfThatIlk"},            
    'plumm': {'css_class': "Plumm"},                    
    'farmanoffaircastle': {'css_class': "FarmanOfFaircastle"},          
    'leffordofthegoldentooth': {'css_class': "LeffordOfTheGoldenTooth"},        
    'serrettofsilverhill': {'css_class': "SerrettOfSilverhill"},            
    'kenningofkayce': {'css_class': "KenningOfKayce"},              
    'jast': {'css_class': "Jast"},                  
    'swyftofcornfield': {'css_class': "SwyftOfCornfield"},          
    'estrenofwyndhall': {'css_class': "EstrenOfWyndhall"},          
    'stackspear': {'css_class': "Stackspear"},              
    'presteroffeastfires': {'css_class': "PresterOfFeastfires"},            
    'westerlingofthecraig': {'css_class': "WesterlingOfTheCraig"},          
    'moreland': {'css_class': "Moreland"},              
    'sarsfieldofthatilk': {'css_class': "SarsfieldOfThatIlk"},          
    'payne': {'css_class': "Payne"},                    
    'garner': {'css_class': "Garner"},                  
    'hamell': {'css_class': "Hamell"},                  
    'ferren': {'css_class': "Ferren"},                  
    'drox': {'css_class': "Drox"},                  
    'yarwyck': {'css_class': "Yarwyck"},                
    'turnberry': {'css_class': "Turnberry"},                
    'doggett': {'css_class': "Doggett"},                
    'algood': {'css_class': "Algood"},                  
    'myatt': {'css_class': "Myatt"},                    
    'falwell': {'css_class': "Falwell"},                
    'hawthorne': {'css_class': "Hawthorne"},                
    'lorch': {'css_class': "Lorch"},                    
    'greenfieldofthatilk': {'css_class': "GreenfieldOfThatIlk"},            
    'vikary': {'css_class': "Vikary"},        
    'ruttiger': {'css_class': "Ruttiger"},              
    'yew': {'css_class': "Yew"},                    
    'hetherspoon': {'css_class': "Hetherspoon"},                
    'clegane': {'css_class': "Clegane"},                
    'broom': {'css_class': "Broom"},                    
    'bettley': {'css_class': "Bettley"},                
    'foote': {'css_class': "Foote"},                    
    'peckledon': {'css_class': "Peckledon"},                
    'spicer': {'css_class': "Spicer"},                  
    'reyneofcastamere': {'css_class': "ReyneOfCastamere"},          
    'tarbeckoftarbeckhall': {'css_class': "TarbeckOfTarbeckHall"},          
    'parren': {'css_class': "Parren"},                  
    'arryn': {'css_class': "Arryn"},                    
    'royceofrunestone': {'css_class': "RoyceOfRunestone"},          
    'waynwoodofironoaks': {'css_class': "WaynwoodOfIronOaks"},          
    'redfortofthatilk': {'css_class': "RedfortOfThatIlk"},          
    'belmoreofstrongsong': {'css_class': "BelmoreOfStrongsong"},            
    'hunteroflongbowhall': {'css_class': "HunterOfLongbowHall"},            
    'graftonofgulltown': {'css_class': "GraftonOfGulltown"},            
    'corbrayofheartshome': {'css_class': "CorbrayOfHeartsHome"},            
    'templetonofninestars': {'css_class': "TempletonOfNinestars"},          
    'melcolmofoldanchor': {'css_class': "MelcolmOfOldAnchor"},          
    'hersyofnewkeep': {'css_class': "HersyOfNewKeep"},              
    'coldwaterofcoldwaterburn': {'css_class': "ColdwaterofColdwaterBurn"},      
    'lynderlyofsnakewood': {'css_class': "LynderlyOfSnakewood"},            
    'shettofgulltower': {'css_class': "ShettOfGullTower"},          
    'tollettofthegreyglen': {'css_class': "TollettOfTheGreyGlen"},          
    'waxleyofwickenden': {'css_class': "WaxleyOfWickenden"},            
    'ruthermont': {'css_class': "Ruthermont"},              
    'hardyng': {'css_class': "Hardyng"},                
    'sunderlandofthe3sisters': {'css_class': "SunderlandOfThe3Sisters"},        
    'longthorpeoflongsister': {'css_class': "LongthorpeOfLongSister"},          
    'borrellofsweetsister': {'css_class': "BorrellOfSweetSister"},          
    'torrentoflittlesister': {'css_class': "TorrentOfLittleSister"},            
    'moore': {'css_class': "Moore"},                    
    'pryorofpebble': {'css_class': "PryorOfPebble"},                
    'upcliff': {'css_class': "Upcliff"},                
    'eleshamofthepaps': {'css_class': "EleshamOfThePaps"},          
    'donniger': {'css_class': "Donniger"},              
    'egen': {'css_class': "Egen"},                  
    'wydman': {'css_class': "Wydman"},                  
    'roycejuniorline': {'css_class': "RoyceJuniorLine"},            
    'baelishold': {'css_class': "BaelishOld"},              
    'baelishnew': {'css_class': "BaelishNew"},              
    'tyrell': {'css_class': "Tyrell"},                  
    'hightowerofoldtown': {'css_class': "HightowerOfOldtown"},          
    'redwyneofthearbor': {'css_class': "RedwyneOfTheArbor"},            
    'rowanofgoldengrove': {'css_class': "RowanOfGoldenGrove"},          
    'oakheartofoldoak': {'css_class': "OakheartOfOldOak"},          
    'tarlyofhornhill': {'css_class': "TarlyOfHornHill"},            
    'vyrwellofdarkdell': {'css_class': "VyrwellOfDarkDell"},            
    'florentofbrightwater': {'css_class': "FlorentOfBrightwater"},          
    'varner': {'css_class': "Varner"},                  
    'blackbarofbandallon': {'css_class': "BlackbarOfBandallon"},            
    'footlyoftumbleton': {'css_class': "FootlyOfTumbleton"},            
    'shermerofsmithyton': {'css_class': "ShermerOfSmithyton"},          
    'beesburyofhoneyholt': {'css_class': "BeesburyOfHoneyholt"},            
    'mullendoreofuplands': {'css_class': "MullendoreOfUplands"},            
    'merrywetheroflongtable': {'css_class': "MerrywetherOfLongtable"},          
    'craneofredlake': {'css_class': "CraneOfRedLake"},              
    'ashfordofthatilk': {'css_class': "AshfordOfThatIlk"},          
    'fossowayofciderhall': {'css_class': "FossowayOfCiderHall"},            
    'fossowayofnewbarrel': {'css_class': "FossowayOfNewBarrel"},            
    'gracefordofholyhall': {'css_class': "GracefordOfHolyHall"},            
    'risley': {'css_class': "Risley"},                  
    'roxtonofthering': {'css_class': "RoxtonOfTheRing"},            
    'oldflowers': {'css_class': "Oldflowers"},              
    'bulwerofblackcrown': {'css_class': "BulwerOfBlackcrown"},          
    'orme': {'css_class': "Orme"},                  
    'pommingham': {'css_class': "Pommingham"},              
    'appletonofthatilk': {'css_class': "AppletonOfThatIlk"},            
    'meadowsofgrassyvale': {'css_class': "MeadowsOfGrassyVale"},            
    'kidwellofivyhall': {'css_class': "KidwellOfIvyHall"},          
    'hastwyck': {'css_class': "Hastwyck"},              
    'cuyofsunflowerhall': {'css_class': "CuyOfSunflowerHall"},          
    'caswellofbitterbridge': {'css_class': "CaswellOfBitterbridge"},            
    'costayneofthethreetowers': {'css_class': "CostayneOfTheThreeTowers"},      
    'butterwell': {'css_class': "Butterwell"},              
    'graves': {'css_class': "Graves"},                  
    'cordwaynerofhammerhal': {'css_class': "CordwaynerOfHammerhal"},            
    'cockshaw': {'css_class': "Cockshaw"},              
    'hutcheson': {'css_class': "Hutcheson"},                
    'lowther': {'css_class': "Lowther"},                
    'leygood': {'css_class': "Leygood"},                
    'middlebury': {'css_class': "Middlebury"},              
    'sloane': {'css_class': "Sloane"},                  
    'bridges': {'css_class': "Bridges"},                
    'dunn': {'css_class': "Dunn"},                  
    'ambrose': {'css_class': "Ambrose"},                
    'peakeofstarpike': {'css_class': "PeakeOfStarpike"},            
    'ball': {'css_class': "Ball"},                  
    'willum': {'css_class': "Willum"},                  
    'redding': {'css_class': "Redding"},                
    'serryofsouthshield': {'css_class': "SerryOfSouthshield"},          
    'chesterofgreenshield': {'css_class': "ChesterOfGreenshield"},          
    'hewettofoakenshield': {'css_class': "HewettOfOakenshield"},            
    'grimmofgreyshield': {'css_class': "GrimmOfGreyshield"},            
    'webberofcoldmoat': {'css_class': "WebberOfColdmoat"},          
    'osgreyofstandfast': {'css_class': "OsgreyOfStandfast"},            
    'lyberr': {'css_class': "Lyberr"},                  
    'inchfield': {'css_class': "Inchfield"},                
    'yelshire': {'css_class': "Yelshire"},              
    'westbrook': {'css_class': "Westbrook"},                
    'wythers': {'css_class': "Wythers"},                
    'bushy': {'css_class': "Bushy"},                    
    'uffering': {'css_class': "Uffering"},              
    'norridge': {'css_class': "Norridge"},              
    'hunt': {'css_class': "Hunt"},                  
    'woodwright': {'css_class': "Woodwright"},              
    'norcross': {'css_class': "Norcross"},              
    'gardenerofhighgarden': {'css_class': "GardenerOfHighgarden"},          
    'rhysling': {'css_class': "Rhysling"},              
    'baratheon': {'css_class': "Baratheon"},                
    'caronofnightsong': {'css_class': "CaronOfNightsong"},          
    'swannofstonehelm': {'css_class': "SwannOfStonehelm"},          
    'conningtonofgriffinsroost': {'css_class': "ConningtonOfGriffinsRoost"},        
    'dondarrionofblackhaven': {'css_class': "DondarrionOfBlackhaven"},          
    'grandisonofgrandview': {'css_class': "GrandisonOfGrandview"},          
    'felloffelwood': {'css_class': "FellOfFelwood"},                
    'staedmonofbroadarch': {'css_class': "StaedmonOfBroadArch"},            
    'tarthofevenfallhall': {'css_class': "TarthOfEvenfallHall"},            
    'cafferenoffawnton': {'css_class': "CafferenOfFawnton"},            
    'bucklerofbronzegate': {'css_class': "BucklerOfBronzegate"},            
    'errolofhaystackhall': {'css_class': "ErrolOfHaystackHall"},            
    'estermontofgreenstone': {'css_class': "EstermontOfGreenstone"},            
    'penroseofparchments': {'css_class': "PenroseOfParchments"},            
    'wensington': {'css_class': "Wensington"},              
    'morrigenofcrowsnest': {'css_class': "MorrigenOfCrowsNest"},            
    'lonmouth': {'css_class': "Lonmouth"},              
    'wyldeofrainhouse': {'css_class': "WyldeOfRainHouse"},          
    'trantofgallowsgrey': {'css_class': "TrantOfGallowsgrey"},          
    'mertynsofmistwood': {'css_class': "MertynsOfMistwood"},            
    'rogersofamberly': {'css_class': "RogersOfAmberly"},            
    'horpe': {'css_class': "Horpe"},                    
    'selmyofharvesthall': {'css_class': "SelmyOfHarvestHall"},          
    'gower': {'css_class': "Gower"},                    
    'tudbury': {'css_class': "Tudbury"},                
    'peaseburyofpoddingfield': {'css_class': "PeaseburyOfPoddingfield"},        
    'hasty': {'css_class': "Hasty"},                    
    'musgood': {'css_class': "Musgood"},                
    'wagstaff': {'css_class': "Wagstaff"},              
    'swygert': {'css_class': "Swygert"},                
    'bolling': {'css_class': "Bolling"},                
    'herston': {'css_class': "Herston"},                
    'kellington': {'css_class': "Kellington"},              
    'toyne': {'css_class': "Toyne"},                    
    'stark': {'css_class': "Stark"},                    
    'manderlyofwhiteharbor': {'css_class': "ManderlyOfWhiteHarbor"},            
    'boltonofthedreadfort': {'css_class': "BoltonOfTheDreadfort"},          
    'karstarkofkarhold': {'css_class': "KarstarkOfKarhold"},            
    'umberoflasthearth': {'css_class': "UmberOfLastHearth"},            
    'flintofwidowswatch': {'css_class': "FlintOfWidowsWatch"},          
    'dustinofbarrowton': {'css_class': "DustinOfBarrowton"},            
    'ryswelloftherills': {'css_class': "RyswellOfTheRills"},            
    'hornwoodofthatilk': {'css_class': "HornwoodOfThatIlk"},            
    'lockeofoldcastle': {'css_class': "LockeOfOldcastle"},          
    'cerwynofthatilk': {'css_class': "CerwynOfThatIlk"},            
    'mormontofbearisland': {'css_class': "MormontOfBearIsland"},            
    'flintofflintsfinger': {'css_class': "FlintOfFlintsFinger"},    
    'stoutofgoldgrass': {'css_class': "StoutOfGoldgrass"},          
    'gloverofdeepwoodmotte': {'css_class': "GloverOfDeepwoodMotte"},            
    'woolfield': {'css_class': "Woolfield"},                
    'tallhartoftorrhenssquare': {'css_class': "TallhartOfTorrhensSquare"},      
    'wells': {'css_class': "Wells"},                    
    'marsh': {'css_class': "Marsh"},                    
    'reedofgreywaterwatch': {'css_class': "ReedOfGreywaterWatch"},          
    'fenn': {'css_class': "Fenn"},                  
    'whitehill': {'css_class': "Whitehill"},                
    'condon': {'css_class': "Condon"},                  
    'ironsmith': {'css_class': "Ironsmith"},                
    'lake': {'css_class': "Lake"},                  
    'moss': {'css_class': "Moss"},                  
    'lightfoot': {'css_class': "Lightfoot"},                
    'overton': {'css_class': "Overton"},                
    'mollen': {'css_class': "Mollen"},                  
    'slate': {'css_class': "Slate"},                    
    'waterman': {'css_class': "Waterman"},              
    'cassel': {'css_class': "Cassel"},                  
    'poole': {'css_class': "Poole"},                    
    'burley': {'css_class': "Burley"},                  
    'harclay': {'css_class': "Harclay"},                
    'norrey': {'css_class': "Norrey"},                  
    'liddle': {'css_class': "Liddle"},                  
    'knott': {'css_class': "Knott"},                    
    'wull': {'css_class': "Wull"},                  
    'magnarofkingshouse': {'css_class': "MagnarOfKingshouse"},          
    'crowlofdeepdown': {'css_class': "CrowlOfDeepdown"},            
    'tully': {'css_class': "Tully"},                    
    'whentofharrenhal': {'css_class': "WhentOfHarrenhal"},          
    'brackenofstonehedge': {'css_class': "BrackenOfStoneHedge"},            
    'blackwoodofraventreehall': {'css_class': "BlackwoodOFRaventreeHall"},      
    'vanceofatranta': {'css_class': "VanceOfAtranta"},              
    'vanceofwayfarersrest': {'css_class': "VanceOfWayfarersRest"},          
    'freyofthecrossing': {'css_class': "FreyOfTheCrossing"},            
    'mootonofmaidenpool': {'css_class': "MootonOfMaidenpool"},          
    'mallisterofseagard': {'css_class': "MallisterOfSeagard"},          
    'piperofpinkmaiden': {'css_class': "PiperOfPinkmaiden"},            
    'vypren': {'css_class': "Vypren"},                  
    'shawney': {'css_class': "Shawney"},                
    'smallwoodofacornhall': {'css_class': "SmallwoodOfAcornHall"},          
    'darryofthatilk': {'css_class': "DarryOfThatIlk"},              
    'lychester': {'css_class': "Lychester"},                
    'goodbrook': {'css_class': "Goodbrook"},                
    'rooteoflordharrowaystwn': {'css_class': "RooteOfLordHarrowaysTwn"},        
    'keath': {'css_class': "Keath"},                    
    'terrick': {'css_class': "Terrick"},                
    'blanetree': {'css_class': "Blanetree"},                
    'lolliston': {'css_class': "Lolliston"},                
    'paege': {'css_class': "Paege"},                    
    'coxofsaltpans': {'css_class': "CoxOfSaltpans"},                
    'rygerofwillowwood': {'css_class': "RygerOfWillowWood"},            
    'charlton': {'css_class': "Charlton"},              
    'erenford': {'css_class': "Erenford"},              
    'haigh': {'css_class': "Haigh"},                    
    'grell': {'css_class': "Grell"},                    
    'wode': {'css_class': "Wode"},                  
    'wayn': {'css_class': "Wayn"},                  
    'muddofoldstones': {'css_class': "MuddOfOldstones"},            
    'teague': {'css_class': "Teague"},                  
    'fisher': {'css_class': "Fisher"},                  
    'justman': {'css_class': "Justman"},                
    'hoareofharrenhall': {'css_class': "HoareOfHarrenhall"},            
    'qoherysofharrenhal': {'css_class': "QoherysOfHarrenhal"},          
    'towersofharrenhal': {'css_class': "TowersOfHarrenhal"},            
    'harrowayofharrenhal': {'css_class': "HarrowayOfHarrenhal"},            
    'strongofharrenhal': {'css_class': "StrongOfHarrenhal"},            
    'lothstonofharrenhal': {'css_class': "LothstonOfHarrenhal"},            
    'butterwellofwhitewalls': {'css_class': "ButterwellOfWhitewalls"},          
    'greyjoy': {'css_class': "Greyjoy"},                
    'harlawoftentowers': {'css_class': "HarlawOfTenTowers"},            
    'goodbrotherofhammerhorn': {'css_class': "GoodbrotherOfHammerhorn"},        
    'orkwoodoforkmont': {'css_class': "OrkwoodOfOrkmont"},          
    'drummofoldwyk': {'css_class': "DrummOfOldWyk"},                
    'saltcliffeofthatilk': {'css_class': "SaltcliffeOfThatIlk"},            
    'blacktydeofthatilk': {'css_class': "BlacktydeOfThatIlk"},          
    'wynchofironholt': {'css_class': "WynchOfIronHolt"},            
    'volmark': {'css_class': "Volmark"},                
    'kenning': {'css_class': "Kenning"},                
    'myre': {'css_class': "Myre"},                  
    'sparr': {'css_class': "Sparr"},                    
    'stonetree': {'css_class': "Stonetree"},                
    'merlynofpebbleton': {'css_class': "MerlynOfPebbleton"},            
    'sunderly': {'css_class': "Sunderly"},              
    'botleyoflordsport': {'css_class': "BotleyOfLordsport"},            
    'tawney': {'css_class': "Tawney"},                  
    'stonehouse': {'css_class': "Stonehouse"},              
    'farwyndofsealskinpoint': {'css_class': "FarwyndOfSealskinPoint"},          
    'goodbrotherofshatterstone': {'css_class': "GoodbrotherOfShatterstone"},        
    'harlawofgreygarden': {'css_class': "HarlawOfGreyGarden"},          
    'harlawofglimmering': {'css_class': "HarlawOfGlimmering"},          
    'harlawyofharlawhall': {'css_class': "HarlawyOfHarlawHall"},            
    'harlawofharridanhill': {'css_class': "HarlawOfHarridanHill"},          
    'farwyndoflonelylight': {'css_class': "FarwyndOfLonelyLight"},          
    'greyironoforkmont': {'css_class': "GreyironOfOrkmont"},            
    'hoareoforkmont': {'css_class': "HoareOfOrkmont"},              
    'martell': {'css_class': "Martell"},                
    'yronwoodofthatilk': {'css_class': "YronwoodOfThatIlk"},            
    'dayneofstarfall': {'css_class': "DayneOfStarfall"},            
    'blackmontofthatilk': {'css_class': "BlackmontOfThatIlk"},          
    'allyrionofgodsgrace': {'css_class': "AllyrionOfGodsgrace"},            
    'ullerofhellholt': {'css_class': "UllerOfHellholt"},            
    'manwoodyofkingsgrave': {'css_class': "ManwoodyOfKingsgrave"},          
    'tolandofghosthill': {'css_class': "TolandOfGhostHill"},            
    'wyloftheboneway': {'css_class': "WylOfTheBoneway"},            
    'qorgyleofsandstone': {'css_class': "QorgyleOfSandstone"},          
    'gargalenofsaltshore': {'css_class': "GargalenOfSaltShore"},            
    'fowlerofskyreach': {'css_class': "FowlerOfSkyreach"},          
    'jordayneofthetor': {'css_class': "JordayneOfTheTor"},          
    'vaithofrealdunes': {'css_class': "VaithOfRealDunes"},          
    'daltoflemonwood': {'css_class': "DaltOfLemonwood"},            
    'santagarofspottswood': {'css_class': "SantagarOfSpottswood"},
    'seaworthofrainwood': {'css_class': "SeaworthOfRainwood"},                
    'bronnoftheblackwater': {'css_class': "BronnOfTheBlackwater"},               
    'theimp': {'css_class': "TheImp"},                     
    'joffrey': {'css_class': "Joffrey"},                    
    'stannisofdragonstone': {'css_class': "StannisOfDragonstone"},               
    'theyoungwolf': {'css_class': "TheYoungWolf"},                       
    'theblackfish': {'css_class': "TheBlackfish"},                       
    'restoredblackfyre': {'css_class': "RestoredBlackfyre"},          
    'bittersteel': {'css_class': "Bittersteel"},                        
    'bloodraven': {'css_class': "Bloodraven"},                 
    'maekar': {'css_class': "Maekar"},                     
    'aerionbrightflame': {'css_class': "AerionBrightflame"},          
    'fireball': {'css_class': "Fireball"},                   
    'euroncrowseye': {'css_class': "EuronCrowsEye"},                      
    'kettleblack': {'css_class': "Kettleblack"},                        
    'slynt': {'css_class': "Slynt"},                              
    'therainbowguard': {'css_class': "TheRainbowGuard"},            
    'theknightofthelaughingtree': {'css_class': "TheKnightOfTheLaughingTree"},  
    'arlanofpennytree': {'css_class': "ArlanOfPennytree"},           
    'duncanthetall': {'css_class': "DuncanTheTall"},                      
    'thebravecompanions': {'css_class': "TheBraveCompanions"},            
    }
naughty = badwords.naughty

spoiler = badwords.spoiler


successFlairReply = """When you play the game of flair, you either win or you die.

You won.

Thanks for using A Bot of Ice and Fire!

***
This message was sent by A Bot of Ice and Fire and cannot accept replies. If you have any comments, questions, or problems, please [message the maesters of r/asoiaf](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Issue).
"""

tooLongFlairReply = """Our ravens can't carry messages that large.

Your requested flair text was too long. Please reduce the number of characters to below 40 and resubmit your request to A Bot of Ice and Fire.

Thank you!

***
This message was sent by A Bot of Ice and Fire and cannot accept replies. If you have any comments, questions, or problems, please [message the maesters of r/asoiaf](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Issue).
"""

spoilerFlairReply = """Posting spoilers in flair text is against the spoiler policy of /r/asoiaf.

If you know what the offending word or phrase was, please edit your spoiler out and resubmit your request to A Bot of Ice and Fire.

If you believe that your desired flair text was erroneously caught in the filter, please [send a raven to the maesters](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Filter%20Mistake).



***
This message was sent by A Bot of Ice and Fire and cannot accept replies. If you have any comments, questions, or problems, please [message the maesters of r/asoiaf](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Issue).
"""

naughtyFlairReply = """Posting offensive words or swearing out of context in flair text is against the rules of /r/asoiaf.

If you know what the offending words or phrase was, please edit your spoiler out and resubmit your request to A Bot of Ice and Fire.

If you believe that your desired flair text was erroneously caught in the filter, please [send a raven to the maesters](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Filter%20Mistake).

***
This message was sent by A Bot of Ice and Fire and cannot accept replies. If you have any comments, questions, or problems, please [message the maesters of r/asoiaf](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Issue).
"""

noShieldFlairReply = """M'lord,

Sansa would have known whose heraldry you were requesting but much like Arya, I have never taken much interest in titles and sigils. Whenever Septa Mordane had gone on about the history of this house and that house, I was inclined to drift and dream and wonder when the lesson would be done.

So, I'm sorry, m'lord, I don't recognize that sigil.

Please try to choose your flair shield and text again. Remember not to alter the subject line in any way.

If you find you're still having problems, please [send a raven to the maesters](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Unrecognized%20Shield%20Problem).


***
This message was sent by A Bot of Ice and Fire and cannot accept replies. If you have any comments, questions, or problems, please [message the maesters of r/asoiaf](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Issue).
"""

clearFlairReply = """Headed to Braavos to become Faceless? Exiled in shame? Taking the black?

For whatever reason you requested it, your shield and title flair have been removed. Feel free to swear allegiance again at any time.


***
This message was sent by A Bot of Ice and Fire and cannot accept replies. If you have any comments, questions, or problems, please [message the maesters of r/asoiaf](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Issue).

"""

allCapsFlairReply = """M'lord,

Your flair text should not sound like a rendition of *The Bear and the Maiden Fair*. That is, YOU SHOULDN'T BE YELLING IT.

Please resubmit your flair request without any title text in all caps for your change to go through successfully.

If you believe that your desired flair text was erroneously caught in the ALL CAPS filter, please [send a raven to the maesters](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Filter%20Mistake).

***
This message was sent by A Bot of Ice and Fire and cannot accept replies. If you have any comments, questions, or problems, please [message the maesters of r/asoiaf](http://www.reddit.com/message/compose?to=%2Fr%2Fasoiaf&amp;subject=Flair%20Issue).
"""
def hasBadWord(phrase, badWordList):

    strip_unicode = re.compile("[-. !@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\{\}\|\?\<\>]")
    transPhrase = strip_unicode.sub('', phrase).lower()
    #pprint(transPhrase)

    for badWord in badWordList:
        transBadWord = strip_unicode.sub('', badWord).lower()

        if -1 != string.find(transPhrase,transBadWord):
            # Badword Found 
            pprint("Found the word \"%s\" in \"%s\"" % (badWord, phrase))
            return True

    return False

def isCaps(phrase):
    return phrase == phrase.upper() and phrase != phrase.lower()

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict


def reddit_api(action, params=None): 
    if params:
#        req = urllib2.Request(reddit + action, urllib.urlencode(params))
        req = urllib2.Request(reddit + action, urllib.urlencode(encoded_dict(params)))
    else:
        req = urllib2.Request(reddit + action)
    response = urllib2.urlopen(req)
    text = response.read()
    #pprint(text)
    return json.loads(text)

def main():
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    opener.addheaders = [('User-agent', user_agent)]
    urllib2.install_opener(opener)
    # Login to Reddit API
    reddit_api("/api/login", credentials)
    successful = False
    for cookie in cookies:
        if cookie.name == 'reddit_session':
            successful = True
    if not successful:
        print "Login failure"
        exit(1)
    # Obtain unread messages
    unread = reddit_api("/message/unread/.json")
    #unread = reddit_api("/message/inbox/.json")
    #pprint(unread)

    modhash = unread['data']['modhash']
    read = []
    csvStringIo = StringIO.StringIO()
    csvWriter = CsvUnicode.UnicodeWriter(csvStringIo)


    # Iterate though messages
    messages = unread['data']['children']
    cmp_by_time = lambda x, y: cmp(x['data']['created'], y['data']['created'])
    for message in sorted(messages, cmp_by_time):
        read.append(message['data']['name'])

        # Determine if valid flair
        shield = message['data']['subject'].lower()
        title = message['data']['body']
        user = message['data']['author']

        flair = flairs.get(shield, None)

        mailParams = {}


        if hasBadWord(title, spoiler):
            print("Spoiler message %s, title = %s, shield = %s" % (user, title, shield))
            mailParms = {'to': user,    
                         'uh': modhash,
                         'subject': "Shield and Title Not Updated -- Spoiler Policy Violation", 
                         'text': spoilerFlairReply}

        elif hasBadWord(title, naughty):
            print("Naughty message %s, title = %s, shield = %s" % (user, title, shield))
            mailParms = {'to': user,    
                         'uh': modhash,
                         'subject': "Shield and Title Not Updated -- Flair Rule Violation", 
                         'text': naughtyFlairReply}

        elif isCaps(title):
            print("%s all caps flair %s" % (user, title))
            mailParms = {'to': user,    
                         'uh': modhash,
                         'subject': "Shield and Title Not Updated -- Flair Rule Violation", 
                         'text': allCapsFlairReply}
        elif shield.lower() == "clear":
            print("%s cleared the title and shield" % (user))
            mailParms = {'to': user,    
                         'uh': modhash,
                         'subject': "Your Title and Shield Have Been Removed", 
                         'text': clearFlairReply}
            csvWriter.writerow([user,"",""])

        elif len(title) > 40:
            print("Message too long = %s, title = %s, shield = %s" % (user, title, shield))
            mailParms = {'to': user,    
                         'uh': modhash,
                         'subject': "Shield and Title Not Updated", 
                         'text': tooLongFlairReply}
        elif not flair:
            print("invalid message user = %s, title = %s, shield = %s" % (user, title, shield))
            mailParms = {'to': user,    
                         'uh': modhash,
                         'subject': "Flair and Title Not Updated -- Unrecognized Shield Name", 
                         'text': noShieldFlairReply}
        else:
            mailParms = {'to': user,    
                          'uh': modhash,
                          'subject': "Shield and Title Changed Successfully!", 
                          'text': successFlairReply}

            csvWriter.writerow([user, title, flair['css_class']])

        reddit_api("/api/compose", mailParms)

    csvString = csvStringIo.getvalue()

    # Update flairs
    if csvString != "":
        print("Csv String %s" % (csvString))
        reddit_api("/api/flaircsv.json",
                   {'r': subreddit, 'flair_csv': csvString, 'uh': modhash})

    # Mark messages as read
    if read:
        reddit_api("/api/read_message", {'id': ','.join(read), 'uh': modhash})

if __name__ == "__main__":
    main()
