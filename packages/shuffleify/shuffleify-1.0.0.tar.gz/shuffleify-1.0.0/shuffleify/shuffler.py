from random import randint

def true_shuffle(tracks, limit=None):
    randomized = []
    
    if limit == None or limit > len(tracks) or limit < 1:
        limit = len(tracks)
    
    temp = tracks.copy()
    for _ in range(limit):
        index = randint(0, len(temp) - 1)
        
        randomized.append(temp[index])
        del temp[index]
    
    return randomized

def fair_shuffle(tracks, size):
    randomized = []
    
    if size > 1:
        for _ in range(size):
            index = randint(0, len(tracks) - 1)
            randomized.append(tracks[index])