#%%
import brawlstats
from pathlib import Path
import dateutil
import pytz
import pandas as pd
from tqdm import tqdm

class brawlparser:
    def __init__(self,token_path,tag):
        self.token  = open(Path(token_path)).read().strip()
        self.client = brawlstats.Client(self.token)
        self.tag    = tag
        
        
    def parse_all_users(self,tags):

        if type(tags) ==str: # 하나만 parsing
            init_tag = tags
            parsed_logs = parse_single_user(self,init_tag)

        else:                # 리스트형태 parsing
            init_tag  = tags[0]
            parsed_logs = []
              
            for tag in tqdm(tags[1:]):
                try:
                    parsed_logs.extend(parse_single_user(self,tag))
                except:
                    pass

        return parsed_logs

def parse_single_user(self,tag):
    parsed_logs = []
    battles = self.client.get_battle_logs(tag)

    for battle in battles:
        if battle["event"]["mode"] == "gemGrab":

            battle_info = {
                "battle_time": dateutil.parser.parse(battle['battle_time']).astimezone(pytz.timezone("Asia/Seoul")),
                "map_id": battle['event']['id'],
                "battle_map": battle['event']['map'],
                "duration": battle['battle']['duration']
            }

            star_player_tag = battle['battle']['star_player']['tag']
            teams           = battle['battle']['teams']
                  

            for team in teams:
                players = [log['tag'][1:] for log in team]
                side = 1 if tag in players else 0 # 1: ours, 2: theirs

                for player in team:

                    player_info     = self.client.get_profile(player['tag'][1:])
                    player_brawlers = sorted(player_info.brawlers, key = lambda x: x['trophies'],reverse=True)
                    
                    for brawler in player_brawlers:
                        if brawler["id"] == player["brawler"]["id"]:
                            gadget     = 1 if brawler["gadgets"] else 0
                            star_power = 1 if brawler["star_powers"] else 0

                    team_info = {
                            "player_tag" : player['tag'],
                            "player_name": player["name"],
                            "player_trophies": player_info.trophies,                    # 전체 트로피
                            "player_top_brawler": player_brawlers[0]["name"],
                            "star_player": 1 if player["tag"] == star_player_tag else 0,
                            "team": side,
                            "result": battle["battle"]["result"],
                            "brawler_id": player["brawler"]["id"],
                            "brawler_name": player["brawler"]["name"],
                            "brawler_power": player["brawler"]["power"],
                            "brawler_star_power": star_power,
                            "brawler_gadget": gadget,
                            "brawler_trophies": player["brawler"]["trophies"],
                    }
                    parsed_logs.append({**battle_info,**team_info})
    return parsed_logs
