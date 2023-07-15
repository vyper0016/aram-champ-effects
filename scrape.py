
import bs4 as bs
import urllib.request
import json
import champion_keys
import os
import requests


URL = 'https://leagueoflegends.fandom.com/wiki/ARAM#Mode-Specific_Changes'
CHAMP_ICONS_URL = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/'
DB_NAME = 'champs.json'
ICONS_PATH = './gui/icons/'


def extract_text(soup:bs.BeautifulSoup):
    text = soup.find_all(string=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style'
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    
    return output.strip()


def get_name(soup):
    s = str(soup)
    closing_a = s.find('>')
    opening_br = s[1:].find('<')
    return s[closing_a+1:opening_br+1]


def download_icon(url):
    file_name = url.split('/')[-1]
    champ_name = champion_keys.getChampionByKey(file_name.split('.')[0])
    if champ_name:
        file_name = champ_name + '.png'
    file_path = ICONS_PATH + file_name
    custom_headers={'User-Agent': 'My Custom User Agent'}
    opener = urllib.request.build_opener()
    opener.addheaders = [(key, value) for key, value in custom_headers.items()]

    # Use the custom opener to retrieve the file
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, file_path)


def update_champion_icons():

    # API endpoint to get the contents of a directory in a repository
    api_url = "https://api.github.com/repos/InFinity54/LoL_DDragon/contents/latest/img/champion"
    
    # Make a GET request to the API
    response = requests.get(api_url)
    response_json = response.json()

    # Iterate over the contents of the directory
    for item in response_json:
        if item["type"] == "file":
            # Download each file in the directory
            download_url = item["download_url"]
            file_name = champion_keys.matchId(item['name'].replace('.png', '')) + '.png'
            file_path = os.path.join(ICONS_PATH, file_name)
            response = requests.get(download_url)
            with open(file_path, "wb") as f:
                f.write(response.content)


def update_db(update_icons=True):
    champion_keys.getLatestDDragon()
    if update_icons:
        update_champion_icons()
    source = urllib.request.urlopen(URL).read()
    soup = bs.BeautifulSoup(source,'html.parser')

    table = soup.find('table', attrs={'cellspacing':'1', 'cellpadding':'1', 'border':'0'})
    table = table.find('tbody')

    rows = table.find_all('tr')

    champs = {}

    for r in rows[1:]:
        columns = r.find_all('td')

        name = columns[0].find('span', attrs={'style':'white-space:normal;'}).find('a').text
        name = champion_keys.getChampionId(name)
        
        dmg_dealt = columns[1].text
        dmg_received = columns[2].text
        other_effects = extract_text(columns[3])

        champs[name] = {'dmg_dealt': dmg_dealt,
                        'dmg_received': dmg_received,
                        'other': other_effects}

    with open('ddragon.json', 'r') as f:
        champions_dd = json.load(f)

    for c in champions_dd:
        if c not in champs:
            champs[c] = {}

    with open(DB_NAME, 'w') as f:
        json.dump(champs, f, indent=3)


def get_champ(name:str):
    with open(DB_NAME, 'r') as f:
        champs = json.load(f)
    
    for c in champs:
        if name.upper() == c.upper():
            path = r"C:\Users\boon\Documents\python\aram effects\icons/"+c+'.png'
            os.startfile(path)
            return champs[c]
    
    return 'champion not found'


def test_db():
    icons = [file for file in os.listdir(ICONS_PATH) if os.path.isfile(os.path.join(ICONS_PATH, file))]
    with open(DB_NAME, 'r') as f:
        champions = json.load(f)
    for i in icons:
        name = i.replace('.png', '')
        print(champions[name])


def get_champ_effects(champ:str):
    with open('ddragon.json', 'r') as f:
        champions = json.load(f)
    
    champ_id = None
    for _, championData in champions.items():
        if championData["id"].upper() == champ.upper() or championData["name"].upper() == champ.upper():
            champ_id = championData['id']
    
    if not champ_id:
        print('could not find', champ)
        return

    with open(DB_NAME, 'r') as f:
        effects = json.load(f)
    
    champ_effects = effects[champ_id]

    if champ_effects == {}:
        print(f'{champ}: no changes')
        return
    else:
        print(champ + ': ')

        if champ_effects["dmg_dealt"]:
            print(f'damage dealt:\t\t{champ_effects["dmg_dealt"]}')
        else:
            print(f'damage dealt:\t\tno changes')

        if champ_effects["dmg_received"]:
            print(f'damage received:\t{champ_effects["dmg_received"]}')
        else:
            print(f'damage received:\tno changes')

        if champ_effects['other']:
            print('extra:')
            print(champ_effects['other'])


if __name__ == '__main__':
    update_db()
