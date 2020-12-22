import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
from AtlasDB import AtlasDB 




def main():
    db = AtlasDB() 
    teamNames = getTeamNames()
    for team in teamNames:
        db.addTeam(team['name'], team['nick'])
    
    games =  getGames('2020')
    for game in games:
        db.addGame(game['csk'], game['date'], game['hour'], game['visitor'],game['home'], game['visitorPts'], game['homePts'] )
        stats = getGameStatsPerPlayer(game['home'], game['visitor'], game['csk'])
        for stat in stats[0]:
            db.addPlayerStat(game['csk'], stat['name'], game['home'], stat)
        for stat in stats[1]:
            db.addPlayerStat(game['csk'], stat['name'], game['visitor'], stat)
        

def getTeamNames():
    teams = []
    req = requests.get('https://www.basketball-reference.com/teams/')
    soup = BeautifulSoup(req.text, 'html.parser')
    table = soup.find(id="teams_active")
    rows = table.find_all("th", {"data-stat":"franch_name"})
    for row in rows:
        team = {}
        if(row.a != None ): 
            nick = row.a['href'][7:-1]
            team['nick'] = nick
            team['name'] = row.a.text
            teams.append(team)
    return teams

    
def getGames(year):
    games = []
    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september']
    for month in months:
        req = requests.get('https://www.basketball-reference.com/leagues/NBA_' + year + '_games-'+ month+'.html')
        if(req.status_code != 404):
            soup = BeautifulSoup(req.text, 'html.parser')
            table = soup.find('table', id="schedule")
            if(table != None):    
                rows = table.find_all('tr', class_= lambda x: x != 'thead')
                for row in rows:
                    
                    game = {}
                    dateTh = row.find('th', {"data-stat":"date_game"}, class_='left' )
                    if(dateTh != None):
                        game['csk'] = dateTh['csk']
                        game['date'] = dateTh.a.text

                        gameHour = row.find('td',{"data-stat":"game_start_time"})
                        if(gameHour != None):
                            game['hour'] = gameHour.text

                        visitorNick = row.find('td',{"data-stat":"visitor_team_name"})
                        if(visitorNick != None):
                            game['visitor'] = visitorNick.a['href'][7:10]

                        homeNick = row.find('td',{"data-stat":"home_team_name"})
                        if(homeNick != None):
                            game['home'] = homeNick.a['href'][7:10]

                        homePts = row.find('td',{"data-stat":"home_pts"})
                        if(homePts != None):
                            game['homePts'] = homePts.text

                        visitorPts = row.find('td',{"data-stat":"visitor_pts"})
                        if(homePts != None):
                            game['visitorPts'] = visitorPts.text
                        games.append(game)
    return games               


def getGameStatsPerPlayer(home, visitor, csk):
    playersHome = []
    playersVisitor = []
    req = requests.get('https://www.basketball-reference.com/boxscores/'+csk+'.html')
    if(req.status_code == 404):
        return
    soup = BeautifulSoup(req.text, 'html.parser')
    simpleTableHome = soup.find(id="box-"+home+"-game-basic")
    simpleTableVisitor = soup.find(id="box-"+visitor+"-game-basic")
    advancedTableHome = soup.find(id="box-"+home+"-game-advanced")
    advancedTableVisitor = soup.find(id="box-"+visitor+"-game-advanced")
    if(simpleTableHome != None):    
        rows = simpleTableHome.find_all('tr', class_= lambda x: x != 'thead')
        for row in rows:    
            player = {}
            playerTh = row.find('th', {"data-stat":"player"})
            if(playerTh != None):
                if(playerTh.text != "Team Totals") & (playerTh.text != "Starters") & (playerTh.text != "Reserves"):
                    player['name'] = playerTh.text
                    stats = row.find_all('td')
                    for stat in stats:
                        player[stat['data-stat']] = stat.text
                    playersHome.append(player)
    if(advancedTableHome != None): 
        rows = advancedTableHome.find_all('tr', class_= lambda x: x != 'thead')
        for row in rows:    
            playerTh = row.find('th', {"data-stat":"player"})
            if(playerTh != None):
                if(playerTh.text != "Team Totals") & (playerTh.text != "Starters") & (playerTh.text != "Reserves"):
                    player = next((player for player in playersHome if player["name"] == playerTh.text), None)
                    if(player != None):
                        stats = row.find_all('td')
                        for stat in stats:
                            player[stat['data-stat']] = stat.text

    if(simpleTableVisitor != None):    
        rows = simpleTableVisitor.find_all('tr', class_= lambda x: x != 'thead')
        for row in rows:    
            player = {}
            playerTh = row.find('th', {"data-stat":"player"})
            if(playerTh != None):
                if(playerTh.text != "Team Totals") & (playerTh.text != "Starters") & (playerTh.text != "Reserves"):
                    player['name'] = playerTh.text
                    stats = row.find_all('td')
                    for stat in stats:
                        player[stat['data-stat']] = stat.text
                    playersVisitor.append(player)
    if(advancedTableVisitor != None): 
        rows = advancedTableVisitor.find_all('tr', class_= lambda x: x != 'thead')
        for row in rows:    
            playerTh = row.find('th', {"data-stat":"player"})
            if(playerTh != None):
                if(playerTh.text != "Team Totals") & (playerTh.text != "Starters") & (playerTh.text != "Reserves"):
                    player = next((player for player in playersVisitor if player["name"] == playerTh.text), None)
                    if(player != None):
                        stats = row.find_all('td')
                        for stat in stats:
                            player[stat['data-stat']] = stat.text

    return (playersHome, playersVisitor)





# Entry Point for the application
if __name__ == '__main__':
    main()
