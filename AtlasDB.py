from pymongo import MongoClient
import os

class AtlasDB:
    def __init__(self):
        self.client = MongoClient( os.environ['PREDICTIZ_CREDENTIALS'])
        db = self.client['predictiz']
        self.tableTeam = db['team']
        self.tablePlayer = db['player']
        self.tableGame = db['game']
        self.tablePlayerStats = db['playerStats']

        
    
    def addTeam(self, name, slug):
        self.tableTeam.insert_one({'name':name, 'slug':slug})
    
    def addGame(self, csk, date , hour, visitorName, homeName, home_pts, visitor_pts):
        visitor = self.tableTeam.find_one({'name':visitorName})
        home = self.tableTeam.find_one({'name':homeName})
        if(visitor != None) & (home!= None):
            self.tableGame.insert_one({'csk': csk, 'date': date, 'hour': hour, 'visitor': visitor['_id'], 'home': home['_id'], 'homePts': home_pts, 'visitorPts': visitor_pts})

    
    def addPlayer(self, name):
        self.tablePlayer.insert_one('name')

    def addPlayerStat(self, game_csk, player_name, teamName, stats ):
        team = self.tableTeam.find_one({'name': teamName})
        game = self.tableGame.find_one({'csk':game_csk})
        player = self.tablePlayer.find_one({'name':player_name})
        if(team != None) & (game != None)& (player != None):
            self.tablePlayerStats.insert_one({'player_id':player['_id'], 'game_id':game['_id'], 'team_id':team['_id'], 'stats': stats})
    
