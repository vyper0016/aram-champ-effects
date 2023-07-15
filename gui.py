import eel
from multiprocessing import Queue

eel.init('gui')

communication_queue = None

def setup(queue):
    global communication_queue
    communication_queue = queue
    eel.start('waiting.html')

started_champs = False
last_update = None
def check_queue():
    global communication_queue, started_champs, last_update

    if communication_queue is not None:
        while not communication_queue.empty():
            message = communication_queue.get()
            if message == 'quit':
                quit()
            
            if not started_champs:
                eel.goToChamps()
                started_champs = True  
                eel.sleep(0.4)              
                eel.updateTable(message)
                print('first update table')
                print(message)
                last_update = message
                eel.sleep(0.3)
                eel.updateTable(message)

            if message != last_update:
                eel.updateTable(message)
                print('updated table')
                last_update = message

    # Schedule the next check
    eel.sleep(0.3)
    eel.spawn(check_queue)

def goToChamps():
    # Your implementation for the 'goToChamps' function
    print("Going to Champs")

# Call check_queue to start checking the queue for messages
eel.spawn(check_queue)
