from lcu_driver import Connector
import json
from champion_keys import getChampionByKey, getChampionIdByKey, getChampionById
from scrape import get_champ_effects, DB_NAME
import multiprocessing

connector = Connector()

# Initialize Eel GUI
def init_gui(queue):
    import gui
    gui.setup(queue)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    communication_queue = multiprocessing.Queue()
    # Start the Eel GUI in a separate process
    gui_process = multiprocessing.Process(target=init_gui, args=(communication_queue,))
    gui_process.start()

    async def get_champs(connection, champ_select_session):
        my_champ = await connection.request('get', '/lol-champ-select/v1/current-champion')
        my_champ = await my_champ.json()
        my_champ = getChampionIdByKey(my_champ)

        bench_champs = []
        for i in champ_select_session['benchChampions']:
            bench_champs.append(getChampionIdByKey(i['championId']))

        available_trades = []
        for i in champ_select_session['trades']:
            if i['state'] == 'AVAILABLE':
                trade_id = i['cellId']
                for j in champ_select_session['myTeam']:
                    if j['cellId'] == trade_id:
                        available_trades.append(getChampionIdByKey(j['championId']))


        return(my_champ, available_trades, bench_champs)


    async def get_champs_web(connection, champ_select_session):
        champs = await get_champs(connection, champ_select_session)

        with open(DB_NAME, 'r') as f:
            effects = json.load(f)


        data = {'mine': None,
                'tradable': [],
                'bench': []}

        dmg_dealt = ''
        dmg_received = ''
        other = ''
        if effects[champs[0]]:
            dmg_dealt = effects[champs[0]]['dmg_dealt']
            dmg_received = effects[champs[0]]['dmg_received']
            other = effects[champs[0]]['other']

        data['mine'] = {'name': getChampionById(champs[0]), 'icon': f'/icons/{champs[0]}.png', 'dmg_dealt': dmg_dealt,
                        'dmg_received': dmg_received, 'other': other}

        for i in champs[1]:
            dmg_dealt = ''
            dmg_received = ''
            other = ''
            try:
                effects[i]
            except KeyError:
                print("\033[91m" + f"'\nerrors:', {champs}" + "\033[0m")
                print(champ_select_session)
            if effects[i]:
                dmg_dealt = effects[i]['dmg_dealt']
                dmg_received = effects[i]['dmg_received']
                other = effects[i]['other']

            data_i = {'name': getChampionById(i), 'icon': f'/icons/{i}.png', 'dmg_dealt': dmg_dealt,
                      'dmg_received': dmg_received, 'other': other}
            data['tradable'].append(data_i)

        for i in champs[2]:
            dmg_dealt = ''
            dmg_received = ''
            other = ''
            if effects[i]:
                dmg_dealt = effects[i]['dmg_dealt']
                dmg_received = effects[i]['dmg_received']
                other = effects[i]['other']

            data_i = {'name': getChampionById(i), 'icon': f'/icons/{i}.png', 'dmg_dealt': dmg_dealt,
                      'dmg_received': dmg_received, 'other': other}
            data['bench'].append(data_i)

        return data


    def is_aram(data):
        for key, value in zip(["allowBattleBoost", "allowDuplicatePicks", "allowLockedEvents", "allowRerolling", "allowSkinSelection"],
                              [True, False, False, True, True]):
            if data[key] != value:
                return False

        return True


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


    @connector.ws.register('/lol-champ-select/v1/session', event_types=('DELETE',))
    async def cs_deleted(connection, event):
        data = event.data
        if not is_aram(data):
            return


    @connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE', 'CREATE'))
    async def get_champ_select(connection, event):
        try:
            data = event.data
        except AttributeError:
            data = event

        if not is_aram(data):
            return

        print('update')
        to_queue = await get_champs_web(connection, data)
        # with open('sample_out.json', 'r') as f:
        #     to_queue = json.load(f)
        communication_queue.put(to_queue)



    @connector.close
    async def disconnect(connection):
        print('Finished task')
        communication_queue.put('quit')
        gui_process.join()
        quit()


    connector.start()
