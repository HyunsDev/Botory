import pickle, os

GlobalDB = dict()

def loadDB():
    global GlobalDB
    print('Loading Global DB ...')
    if os.path.isfile('GlobalDB.db'):
        with open('GlobalDB.db', 'rb') as f:
            GlobalDB = pickle.load(f)
        print('GlobalDB.db loaded!')
        return
    print('GlobalDB.db not found!')
    initDB()

def initDB():
    global GlobalDB
    GlobalDB['StoryGuildID'] = 775210688183664640
    GlobalDB['IgnoreChannels'] = set()

def saveDB():
    global GlobalDB
    print('Saving GlobalDb.db ...')
    with open('GlobalDB.db', 'wb') as f:
        pickle.dump(GlobalDB, f)
    print('GlobalDB.db saved!')
