from functions.SteamBot_WishList import SteamBot_WishList
from functions.OpenGameLink import OpenGameLink
from time import sleep

def steam_wishList(url_steam_wishlist):
    steam_wishList = SteamBot_WishList(url_steam_wishlist)
    steam_wishList.OpenBrowser()
    steam_wishList.GetLinks()
    steam_wishList.SaveLinks()
    steam_wishList.CloseBrowser()

def steam_games_wishList(path_url_games_steam):
    urls_games_steam = open(path_url_games_steam,"r")
    
    for url_game_steam in urls_games_steam:
        if(url_game_steam != "\n"):
            print(url_game_steam)
            openGame = OpenGameLink(url_game_steam,0)
            openGame.OpenBrowser()
            openGame.VerifyLink()
            openGame.GetInfo()
            openGame.ParseInfoSpace()
            openGame.ParseInfoReview()
            openGame.SaveInfo()
            openGame.CloseBrowser()
            
def steam_games_wishList_unit(url_game):
    openGame = OpenGameLink(url_game,0)
    openGame.OpenBrowser()
    openGame.VerifyLink()
    openGame.GetInfo()
    openGame.ParseInfoSpace()
    openGame.ParseInfoReview()
    openGame.SaveInfo()
    openGame.CloseBrowser()


# url_game = "https://store.steampowered.com/app/514900/"

# url_steam_wishlist = "https://store.steampowered.com/wishlist/profiles/76561198208574821/#sort=name"
# url_steam_wishlist = "https://store.steampowered.com/wishlist/id/yesy12/#sort=name"
# steam_games_wishList(url_steam_wishlist)


# steam_games_wishList("text/steamlink_wishlist.txt")

url_steam_wishlist = "https://store.steampowered.com/app/897730/"
steam_games_wishList_unit(url_steam_wishlist)