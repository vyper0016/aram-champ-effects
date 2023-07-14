from lcu_driver import Connector
import json
from champion_keys import getChampionByKey
from scrape import get_champ_effects
from my_summoner_id import MY_ID

connector = Connector()


def get_champs(champ_select_session):
    for i in champ_select_session['myTeam']:
        if i['summonerId'] == MY_ID:
            my_champ = getChampionByKey(i['championId'])


    bench_champs = []
    for i in champ_select_session['benchChampions']:
        if i['isPriority']:
            bench_champs.append(getChampionByKey(i['championId']))

    available_trades = []
    for i in champ_select_session['trades']:
        if i['state'] == 'AVAILABLE':
            available_trades.append(getChampionByKey(i['id']))

    return(my_champ, available_trades, bench_champs)


def is_aram(data):
    for key, value in zip(["allowBattleBoost", "allowDuplicatePicks", "allowLockedEvents", "allowRerolling", "allowSkinSelection"],
                          [True, False, False, True, True]):
        if data[key] != value:
            return False
    
    return True

current_champ = None
def print_effects(data):
    global current_champ
    
    champs = get_champs(data)
    my_champ = champs[0]
    # print(champs)
    if my_champ != current_champ:
        print('\n'*2)
        print('Your champ:')
        get_champ_effects(champs[0])
        current_champ = my_champ

    # print('available trades:')
    # if champs[1]:
    #     for i in champs[1]:
    #         print(i)
    #         get_champ_effects(i)

    # print('available on bench:')
    # if champs[2]:
    #     for i in champs[2]:
    #         print(i)
    #         get_champ_effects(i)


async def print_current_effects(connection):
    global current_champ
    champ = await connection.request('get', '/lol-champ-select/v1/current-champion')
    champ = await champ.json()
    name = getChampionByKey(champ)
    if name != current_champ:
        current_champ = name
        get_champ_effects(name)


@connector.ready
async def connect(connection):
    print('connected') 
    cs = await connection.request('get', '/lol-champ-select/v1/session')
    if cs.status == 200:
        json_ = await cs.json()
        if is_aram(json_):
            await cs_created(connection, json_)


@connector.ws.register('/lol-champ-select/v1/session', event_types=('CREATE',))
async def cs_created(connection, event):
    try:
        data = event.data
    except AttributeError:
        data = event

    if not is_aram(data):
        return
    print('created!')
#    print_effects(data)


@connector.ws.register('/lol-champ-select/v1/session', event_types=('DELETE',))
async def cs_deleted(connection, event):
    data = event.data
    if not is_aram(data):
        return


@connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
async def get_champ_select(connection, event):
    data = event.data
    if not is_aram(data):
        return   

    await print_current_effects(connection)
#    print_effects(data) 


@connector.close
async def disconnect(connection):
    print('Finished task')
    quit()

connector.start()
