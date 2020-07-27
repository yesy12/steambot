from selenium import webdriver
from selenium.webdriver.support.select import Select
from time import sleep
from datetime import datetime
from pymongo import MongoClient
# from .InfoDb import InfoDb
import re


class OpenGameLink:
    
    def __init__ (self,url_game,have_game=1):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-br")
        url_drive = executable_path=r"./../../../driver/chromedriver.exe"
        
        # info = InfoDb()
        
        username = "info.getUsername()"
        password = "info.getPassword()"
        dbName = "info.getDbName()"
        url = f"mongodb+srv://{username}:{password}@cluster0-nth3w.mongodb.net/{dbName}?retryWrites=true&w=majority"
        
        client = MongoClient(url)
        db = client["gamesBotSave"]
        
        self.games = db.gamesBotSave
        
        self.driver = webdriver.Chrome(url_drive)
        self.url_game = url_game
        self.agecheck = False
        self.title = ""
        self.space = ""
        self.unity = ""
        self.game_dlc = False
        self.url_steam_bool = False
        self.requirements_minimum = 0
        self.requirements_recomend = ""
        self.have_game = have_game
        self.urlGameImage = ""
        self.gameReview = ""
        self.price = ""
        
        
    def OpenBrowser(self):
        self.driver.get(self.url_game)
    
    def CloseBrowser(self):
        self.driver.close()
        
    def VerifyLink(self):
        palavra = re.search(r"agecheck",self.driver.current_url)
        if(palavra):
            self.agecheck = True

    def SetAge(self):
        if(self.agecheck == True):
            ageDay = self.driver.find_element_by_name("ageDay")
            selectAgeDay = Select(ageDay)
            selectAgeDay.select_by_value("10")
            
            ageMonth = self.driver.find_element_by_name("ageMonth")
            selectAgeMonth = Select(ageMonth)
            selectAgeMonth.select_by_value("March")
            
            ageYear = self.driver.find_element_by_name("ageYear")
            selectAgeYear = Select(ageYear)
            selectAgeYear.select_by_value("2000")
            
            acessToPage = self.driver.find_element_by_xpath("//a[@class='btnv6_blue_hoverfade btn_medium']")
            acessToPage.click()
            
            self.agecheck = False
            #Cookies 
            """
            {
                lastagecheckage:"1-0-2000"
            }
            """
    
    def VerifyPage(self)->bool:
        current_url = self.driver.current_url
        url_steam = "https://store.steampowered.com/"
        if(current_url == url_steam):
            self.url_steam_bool = True
        return self.url_steam_bool
    
    def GameIgnoreName(self,name_game)->bool:
        ignore_game = open("text\ignore.txt","r")
        
        regex = re.compile(rf"{name_game}",flags=re.I)
        for line in ignore_game:
            info = regex.findall(line)
            if(len(info)>0):
                ignore_game.close()
                return True

        ignore_game.close()
        return False
    
    def GetInfo(self):
        self.SetAge()
        sleep(1)
        
        if(self.VerifyPage() == True):
            self.title = ""
            self.space = 0
            self.unity = "QB"
            self.urlGameImage = ""
            self.gameReview = ""
            self.price = ""
            return 
        
        #gameIsDlc
        try:
            gameIsDlc = self.driver.find_element_by_xpath("//div[@class='game_area_bubble game_area_dlc_bubble ']")
            self.game_dlc = True
        except:
            self.game_dlc = False
        
        #gameTitle
        try:
            self.title = self.driver.find_element_by_xpath("//div[@class='apphub_AppName']").text
        except:
            self.title = ""
        
        ignore_game = self.GameIgnoreName(self.title)
        if(ignore_game):
            return
        
        #space     
        try:
            self.requirements_minimum = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_leftCol']/ul/ul[@class='bb_ul']").text
            self.requirements_recomend = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_rightCol']/ul/ul[@class='bb_ul']").text
        except:
            try:
                self.requirements_minimum = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_full']/ul/ul[@class='bb_ul']").text  
                self.requirements_recomend = ""          
            except:
                try:
                    self.requirements_minimum = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_full']/ul").text
                    self.requirements_recomend = ""
                except:
                    self.requirements_minimum = ""
                    self.requirements_recomend = ""
        
        #url_image
        try:
            url_image = self.driver.find_element_by_xpath("//div[@class='game_header_image_ctn']/img[@class='game_header_image_full']")
            self.urlGameImage = url_image.get_attribute("src")
        except: 
            self.urlGameImage = ""
        
        #review
        try:
            gameReview = self.driver.find_element_by_xpath("//div[@class='summary column']/span")
            self.gameReview = gameReview.get_attribute("class")
        except:
            self.gameReview = ""

        #price
        if(self.have_game == 0):
            try:
                price = self.driver.find_element_by_xpath("//div[@class='game_purchase_price price']")
                self.price = price.text
            except:
                try:
                    self.price = self.driver.find_element_by_xpath("//div[@class='game_area_comingsoon game_area_bubble']/div[@class='content']/h1").text
                except:
                    self.price = ""
                          
    def ParseInfoReview(self):
        #game_review_summary positive = Extremamente positivas | Ligeiramente positivas | Muito positivas
        #game_review_summary mixed = Neutras
        #game_review_summary = Ligeiramente negativas

        regex = "positive|mixed"
        regex = re.compile(rf"{regex}",flags=re.I)
        find = regex.search(self.gameReview)

        if(find):
            review = regex.findall(self.gameReview)[0]
            self.gameReview = review
        elif(self.gameReview == ""):
            self.gameReview = "in soon"
        else:
            self.gameReview = "negative"
            
    def ParseInfoSpace(self):
        if(self.VerifyPage() == False):
            requirements_minimum_unity = ""
            requirements_recomend_unity = ""
            requirements_minimum_space = 0
            requirements_recomend_space = 0
            
            #PART 1
            
            regex = "[a-z]*[tcv][eo]:.*[gm]b"
            # regex = "[a-z]+[a-z][oe]:.*[0-9]+.[gm]b|drive: [0-9][gm]b"
            regex = re.compile(rf"{regex}",flags=re.I)
            # Armazenamento:5 GB | Armazenamento: 5GB | Armazenamento: 5 GB
            # Hard Drive:2 GB | # Hard Drive: 15MB | # Hard Drive: 15 MB
            # Hard Disk Space:6 GB | Hard Disk Space: 6GB |  Hard Disk Space: 6 GB
            
            try:
                self.requirements_minimum = regex.findall(self.requirements_minimum) #Armazenamento: 5 GB
                self.requirements_minimum = self.requirements_minimum[0]
                
                if(self.requirements_recomend != ""):
                    try:
                        self.requirements_recomend = regex.findall(self.requirements_recomend)[0] #Armazenamento: 5 GB
                    except:
                        self.requirements_recomend = ""      
            except:  
                self.requirements_minimum = ""
            
            #PART 2
            
            regex = "[0-9]+[ ]*[gm]b"
            regex = re.compile(rf"{regex}",flags=re.I)
            # 5 GB | 5GB 
            # 500 MB | 500MB
 
            try:
                self.requirements_minimum = regex.findall(self.requirements_minimum)[0] #5 GB
                
                if(self.requirements_recomend != ""):
                    try:
                        self.requirements_recomend = regex.findall(self.requirements_recomend)[0] #5 GB
                    except:
                        self.requirements_recomend = ""
            except:
                self.requirements_minimum = ""
                
                
            #PART 3

            regex = "[GM]B"
            regex = re.compile(rf"{regex}",flags=re.I)
            #GB | MB
            
            
            try:
                requirements_minimum_unity = regex.findall(self.requirements_minimum)[0] #GB

                if(self.requirements_recomend != ""):
                    try:
                        requirements_recomend_unity = regex.findall(self.requirements_recomend)[0] #GB
                    except:
                        requirements_recomend_unity = ""
            except:
                requirements_minimum_unity = ""
                
                
            #PART 4
            regex = "[0-9]*"
            regex = re.compile(rf"{regex}")
                
            requirements_minimum_space = int(regex.findall(self.requirements_minimum)[0]) #5
                
            try:
                requirements_recomend_space = int(regex.findall(self.requirements_recomend)[0]) #5
            except:
                requirements_recomend_space = 0
                            
            if(requirements_minimum_unity == requirements_recomend_unity):# GB and GB # MB and MB
                    
                if(requirements_minimum_space >= requirements_recomend_space):
                    self.space = requirements_minimum_space
                    self.unity = requirements_minimum_unity
                        
                elif(requirements_recomend_space > requirements_minimum_space):
                    self.space = requirements_recomend_space
                    self.unity = requirements_recomend_unity
            
            elif(requirements_minimum_unity == "GB"): # only GB or GB and MB
                self.space = requirements_minimum_space
                self.unity = requirements_minimum_unity
                
            elif(requirements_recomend_unity == "GB"): # only GB or GB and MB
                self.space = requirements_recomend_space
                self.unity = requirements_recomend_unity
                
            elif(requirements_minimum_unity == "MB"): # MB only
                self.space = requirements_minimum_space
                self.unity = requirements_minimum_unity 
                
            elif(requirements_recomend_unity == "MB"): # MB only
                self.space = requirements_recomend_space
                self.unity = requirements_recomend_unity                

    def SaveInfo(self):
        
        games_data = {
            "title": self.title,
            "space": self.space,
            "unity": self.unity,
            "dlc ": self.game_dlc,
            "plataform": "steam",
            "urlGame": self.url_game,
            "urlImagem": self.urlGameImage,
            "review": self.gameReview,
            "price" : self.price,
            "dateCreation": datetime.utcnow()
        }
        
        result = self.games.insert_one(games_data)