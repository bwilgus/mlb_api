import requests, pandas as pd, sys
from pprint import pprint as pp
from bs4 import BeautifulSoup

def find_player_name(player_name):
    params = {'sport_code':'mlb'
              ,'active_sw':'Y'
              ,'name_part':"'"+player_name+"'"
              }

    r = requests.get("http://lookup-service-prod.mlb.com/json/named.search_player_all.bam"
                     ,params = params
                     )

    p_id = r.json()['search_player_all']['queryResults']['row']['player_id']

    return(p_id)

def find_player_team(player_name):
    params = {'sport_code':'mlb'
              ,'active_sw':'Y'
              ,'name_part':"'"+player_name+"'"
              }

    r = requests.get("http://lookup-service-prod.mlb.com/json/named.search_player_all.bam"
                     ,params = params
                     )

    team_abbrev = r.json()['search_player_all']['queryResults']['row']['team_abbrev']

    return(team_abbrev)

def player_info(df):
    player_dic = {}
    for p in df['player']:
        params = {'sport_code':"'mlb'"
                  ,'active_sw':"'Y'"
                  ,'name_part':"'"+p+"'"
                  }
        r = requests.get("http://lookup-service-prod.mlb.com/json/named.search_player_all.bam"
                         ,params = params
                         )
        team_abbrev = r.json()['search_player_all']['queryResults']['row']['team_abbrev']
        p_id = r.json()['search_player_all']['queryResults']['row']['player_id']

        player_dic[p] = {'team':team_abbrev
                         ,'player_id':p_id
                         }

    df['player_id'] = df['player'].apply(lambda x: player_dic[x]['player_id'])
    df['team'] = df['player'].apply(lambda x: player_dic[x]['team'])

    return(df)

url = "http://lookup-service-prod.mlb.com/json/named."
scrape_type = {'Hit Stat Scrape':'sport_hitting_tm.bam'
               ,'Pitch Stat Scrape':'sport_hitting_tm.bam'
               }

proj_scrape_type = {'Proj Pitch Stat':'proj_pecota_pitching.bam'
                    ,'Proj Hit Stat':'proj_pecota_hitting.bam'
                    }

df = pd.read_excel('my roster.xlsx')

player_stat = {}
hit_stats = ['h','r','hr','rbi','so','sb','avg','ops']
pitch_stats = ['ip','w','l','sv','era','whip','k9']


for p in df.player_id:
    ## Past Year Hit Stats
    params = {'game_type':"'R'"
              ,'league_list_id':"'mlb'"
              ,'season':"'2018'"
              ,'player_id':"'"+str(p)+"'"
              }
    stats = {}

    r = requests.get(url + scrape_type['Hit Stat Scrape']
                     ,params=params)
    
    for h in hit_stats:
        row = r.json()['sport_hitting_tm']['queryResults']['row']
        if type(r.json()['sport_hitting_tm']['queryResults']['row']) == list:
            stat = []
            for n in row:
                stat.append(float(n[h]))
            stats[h] = sum(stat)
        else:
            stats[h] = r.json()['sport_hitting_tm']['queryResults']['row'][0][h]

    sys.exit()

    ## Past Year Pitch Stats
    r = requests.get(url + scrape_type['Pitch Stat Scrape']
                     ,params=params)
    for p in pitch_stats:
        stats[p] = r.json()['sport_pitching_tm']['queryResults']['row'][0][h]
        
    ## Projected Year stats
    params = {'game_type':"'R'"
          ,'season':"'2019'"
          ,'player_id':"'"+p+"'"
              }


