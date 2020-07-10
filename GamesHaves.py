from functions.SteamBot_Have import SteamBot_Have
from functions.OpenGameLink import OpenGameLink

def steam_have(url_steam_have):
    steam = SteamBot_Have(url_steam_have)
    steam.OpenBrowser()
    steam.GetLink()
    steam.CountLinks()
    steam.SaveLinks()
    steam.CloseBrowser()

def steam_games_have(path_url_games_steam):
    
    urls_games_steam = open(path_url_games_steam,"r")

    for url_game_steam in urls_games_steam:
        if(url_game_steam != "\n"):
            openGame = OpenGameLink(url_game_steam,1)
            openGame.OpenBrowser()
            openGame.VerifyLink()
            openGame.GetInfo()
            openGame.ParseInfoSpace()
            openGame.SaveInfo()
            openGame.CloseBrowser()
    
def steam_games_have_unit(url_game):
    openGame = OpenGameLink(url_game,1)
    openGame.OpenBrowser()
    openGame.VerifyLink()
    openGame.GetInfo()
    openGame.ParseInfoSpace()
    openGame.ParseInfoReview()
    openGame.SaveInfo()
    openGame.CloseBrowser()

# url_steam = "https://steamcommunity.com/id/ahsj4/games/?tab=all&sort=name"
# steam_have(url_steam)

# steam_games_have("text/steamlink_have.txt")

# url_game = "https://store.steampowered.com/app/57300"
# steam_games_have_unit(url_game)