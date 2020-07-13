from selenium import webdriver
from selenium.webdriver.support.select import Select
from time import sleep
import re

class OpenGameLink:
    
    def __init__ (self,url_game,have_game=1):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-br")
        url_drive = executable_path=r"./../../driver/chromedriver.exe"
        
        self.driver = webdriver.Chrome(url_drive)
        self.url_game = url_game
        self.agecheck = False
        self.game_name = ""
        self.requirements = ""
        self.game_dlc = False
        self.url_steam_bool = False
        self.requirements_minimum = ""
        self.requirements_recomend = ""
        self.have_game = have_game
        self.url_game_image = ""
        self.game_review = ""
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
    
    def VerifyPage(self):
        current_url = self.driver.current_url
        url_steam = "https://store.steampowered.com/"
        if(current_url == url_steam):
            self.url_steam_bool = True
        else:
            self.url_steam_bool = False
    
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
        self.VerifyPage()
        sleep(1)
        
        
        if(self.url_steam_bool == True):
            self.game_name = f"Failed: {self.url_game}"
            self.requirements_minimum = f"FAILED: {self.url_game}"
            self.url_game_image = ""
            self.game_review = ""
            return 
        
        #gameIsDlc
        try:
            gameIsDlc = self.driver.find_element_by_xpath("//div[@class='game_area_bubble game_area_dlc_bubble ']")
            self.game_dlc = True
        except:
            self.game_dlc = False
        
        #gameName
        try:
            self.game_name = self.driver.find_element_by_xpath("//div[@class='apphub_AppName']").text
        except:
            self.game_name = f"Failed: {self.url_game}"
        
        ignore_game = self.GameIgnoreName(self.game_name)
        if(ignore_game):
            return
        
        #requirements     
        try:
            self.requirements_minimum = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_leftCol']/ul/ul[@class='bb_ul']").text
            self.requirements_recomend = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_rightCol']/ul/ul[@class='bb_ul']").text
        except:
            try:
                self.requirements_minimum = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_full']/ul/ul[@class='bb_ul']").text  
                self.requirements_recomend = ""          
            except:
                self.requirements_minimum = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_full']/ul").text
                self.requirements_recomend = ""
        
        #url_image
        try:
            url_image = self.driver.find_element_by_xpath("//div[@class='game_header_image_ctn']/img[@class='game_header_image_full']")
            self.url_game_image = url_image.get_attribute("src")
        except: 
            self.url_game_image = ""
        
        #review
        try:
            game_review = self.driver.find_element_by_xpath("//div[@class='summary column']/span")
            self.game_review = game_review.get_attribute("class")
        except:
            self.game_review = ""

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
        find = regex.search(self.game_review)

        if(find):
            review = regex.findall(self.game_review)[0]
            self.game_review = review
        elif(self.game_review == ""):
            self.game_review = "in soon"
        else:
            self.game_review = "negative"
            
    def ParseInfoSpace(self):
        if(self.url_steam_bool == False):
            
            requirements_minimum = ""
            requirements_minimum_bool_gb = False
            requirements_recomend_bool_gb = False
            
            requirements_recomend_unit = ""
            
            #PART 1
            
            regex = "[a-z]*[tcv][eo]:.*[gm]b"
            # regex = "[a-z]+[a-z][oe]:.*[0-9]+.[gm]b|drive: [0-9][gm]b"
            regex = re.compile(rf"{regex}",flags=re.I)
            # Armazenamento:5 GB | Armazenamento: 5GB | Armazenamento: 5 GB
            # Hard Drive:2 GB | # Hard Drive: 15MB | # Hard Drive: 15 MB
            # Hard Disk Space:6 GB | Hard Disk Space: 6GB |  Hard Disk Space: 6 GB
            try:
                requirements_minimum = regex.findall(self.requirements_minimum)[0] #Armazenamento: 5 GB
                if(self.requirements_recomend != ""):
                    try:
                        requirements_recomend = regex.findall(self.requirements_recomend)[0] #Armazenamento: 5 GB
                    except:
                        requirements_recomend = ""      
            except:  
                requirements_minimum = ""
            #PART 2
            
            regex = "[0-9]+[ ]*[gm]b"
            regex = re.compile(rf"{regex}",flags=re.I)
            # 5 GB | 5GB 
            # 500 MB | 500MB
            try:
                requirements_minimum = regex.findall(requirements_minimum)[0] #5 GB
                if(self.requirements_recomend != ""):
                    try:
                        requirements_recomend = regex.findall(requirements_recomend)[0] #5 GB
                    except:
                        requirements_recomend = ""
            except:
                requirements_minimum = ""
                
                
            #PART 3

            regex = "[GM]B"
            regex = re.compile(rf"{regex}",flags=re.I)
            #GB | MB
            try:
                requirements_minimum_unit = regex.findall(requirements_minimum)[0] #GB
                if(self.requirements_recomend != ""):
                    try:
                        requirements_recomend_unit = regex.findall(requirements_recomend)[0] #GB
                    except:
                        requirements_recomend_unit = ""
                                
                if(requirements_minimum_unit == "GB"):
                    requirements_minimum_bool_gb = True
                if(requirements_recomend_unit == "GB"):
                    requirements_recomend_bool_gb = True
            except:
                requirements_minimum = ""
                
            #PART 4
            try:
                if(self.requirements_recomend != ""):
                    if(requirements_minimum_bool_gb == requirements_recomend_bool_gb):
                        regex = "[0-9]*"
                        regex = re.compile(rf"{regex}")
                        
                        requirements_minimum_int = int(regex.findall(requirements_minimum)[0]) #5
                        requirements_recomend_int = int(regex.findall(requirements_recomend)[0]) #5
                        
                        if(requirements_minimum_int == requirements_recomend_int):
                            self.requirements = requirements_minimum
                        elif(requirements_recomend_int > requirements_minimum_int):
                            self.requirements = requirements_recomend
                        
                    elif(requirements_minimum_bool_gb == True):
                        self.requirements = requirements_minimum
                    elif(requirements_recomend_bool_gb == True):
                        self.requirements = requirements_recomend
                elif(requirements_minimum == ""):
                    self.requirements = f"FAILED GB: {self.url_game}"
                else:
                    self.requirements = requirements_minimum    
            except:
                self.requirements = f"FAILED GB: {self.url_game}"
            
    def SaveInfo(self):
        regex = "[0-9]+"
        name_file = re.findall(rf"{regex}",self.url_game)[0]
        url_path = ""
        if(self.have_game == 1):
            url_path = f"text\games\{name_file}.txt"
        else:
            url_path = f"text\wishlist\{name_file}.txt"
        OpenGameLinkInfo = open(url_path,"w",encoding="UTF-8")
        
        OpenGameLinkInfo.writelines(self.game_name)
        OpenGameLinkInfo.writelines(f"\n{self.requirements}")
        OpenGameLinkInfo.writelines(f"\nDLC : {self.game_dlc}")
        OpenGameLinkInfo.writelines(f"\nUrl Image: {self.url_game_image}")
        OpenGameLinkInfo.writelines(f"\nReview: {self.game_review}")
        
        if(self.have_game == 0):
            OpenGameLinkInfo.writelines(f"\nPrice: {self.price}")
        OpenGameLinkInfo.close()