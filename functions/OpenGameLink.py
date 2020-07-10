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
    
    def GetInfo(self):
        self.SetAge()
        sleep(1)
        self.VerifyPage()
        sleep(1)
        
        if(self.url_steam_bool == True):
            self.game_name = f"Failed: {self.url_game}"
            self.requirements_minimum = f"FAILED: {self.url_game}"
            return 
        
        try:
            gameIsDlc = self.driver.find_element_by_xpath("//div[@class='game_area_bubble game_area_dlc_bubble ']")
            self.game_dlc = True
        except:
            self.game_dlc = False
        
        try:
            self.game_name = self.driver.find_element_by_xpath("//div[@class='apphub_AppName']").text
        except:
            self.game_name = f"Failed: {self.url_game}"
                
        try:
            self.requirements_minimum = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_leftCol']/ul/ul[@class='bb_ul']").text
            self.requirements_recomend = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_rightCol']/ul/ul[@class='bb_ul']").text
        except:
            self.requirements_minimum = self.driver.find_element_by_xpath("//div[@class='game_area_sys_req_full']/ul/ul[@class='bb_ul']").text  
            self.requirements_recomend = ""          
        try:
            url_image = self.driver.find_element_by_xpath("//div[@class='game_header_image_ctn']/img[@class='game_header_image_full']")
            self.url_game_image = url_image.get_attribute("src")
        except: 
            self.url_game_image = ""
    
    def ParseInfoSpace(self):
        if(self.url_steam_bool == False):
            
            requirements_minimum = ""
            requirements_minimum_bool_gb = False
            requirements_recomend_bool_gb = False
            
            requirements_recomend_unit = ""
            
            #PART 1
            
            regex = "[a-z]+[a-z][oe]:.*[0-9]+.[gm]b|drive: [0-9][gm]b"
            regex = re.compile(rf"{regex}",flags=re.I)
            # Armazenamento:5 GB | Armazenamento: 5GB | Armazenamento: 5 GB
            # Hard Drive:2 GB | # Hard Drive: 15MB | # Hard Drive: 15 MB
            # Hard Disk Space:6 GB | Hard Disk Space: 6GB |  Hard Disk Space: 6 GB
            
            requirements_minimum = regex.findall(self.requirements_minimum)[0] #Armazenamento: 5 GB
            if(self.requirements_recomend != ""):
                requirements_recomend = regex.findall(self.requirements_recomend)[0] #Armazenamento: 5 GB
            
            #PART 2
            
            regex = "[0-9]+[ ]*[gm]b"
            regex = re.compile(rf"{regex}",flags=re.I)
            # 5 GB | 5GB 
            # 500 MB | 500MB
            
            requirements_minimum = regex.findall(requirements_minimum)[0] #5 GB
            if(self.requirements_recomend != ""):
                requirements_recomend = regex.findall(requirements_recomend)[0] #5 GB

            #PART 3

            regex = "[GM]B"
            regex = re.compile(rf"{regex}",flags=re.I)
            #GB | MB

            requirements_minimum_unit = regex.findall(requirements_minimum)[0] #GB
            if(self.requirements_recomend != ""):
                requirements_recomend_unit = regex.findall(requirements_recomend)[0] #GB
            
            if(requirements_minimum_unit == "GB"):
                requirements_minimum_bool_gb = True
            if(requirements_recomend_unit == "GB"):
                requirements_recomend_bool_gb = True
            
            #PART 4
            
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
            else:
                self.requirements = requirements_minimum    
                     
    def SaveInfo(self):
        regex = "[0-9]+"
        name_file = re.findall(rf"{regex}",self.url_game)[0]
        url_path = ""
        if(self.have_game == 1):
            url_path = f"text\games\{name_file}.txt"
        else:
            url_path = f"text\whitlist\{name_file}.tex"
        OpenGameLinkInfo = open(url_path,"w",encoding="UTF-8")
        
        OpenGameLinkInfo.writelines(self.game_name)
        OpenGameLinkInfo.writelines(f"\n{self.requirements}")
        OpenGameLinkInfo.writelines(f"\nDLC : {self.game_dlc}")
        OpenGameLinkInfo.writelines(f"\nUrl Image: {self.url_game_image}")
        OpenGameLinkInfo.close()