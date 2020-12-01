import os
import requests

def fetch(server, verbose=0):
    r = requests.get(f'{server}/viz/api/fetch').content
    if verbose:
        print('Fetched Sample')
    return r

def set_iterator(server, value, verbose=0):
    requests.get(f'{server}/viz/api/set?iterator={value}')
    if verbose:
        print(f'Set interator: {value}')

def get_filename(iterator, prefix='fetch'):
    return f'{prefix}_{iterator}.json'

def save_json(dirpath, filename, data, verbose=0):
    file = os.path.join(dirpath, filename)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(file, 'wb') as f:
        f.write(data)
    if verbose:
        print(f'Saved file: {filename}')

if __name__ == "__main__":
    server = 'http://0.0.0.0:5000'
    dirpath = '/home/Data/TSViz/Data_Samples/Fetched'
    iterator = [0,52,95,138,186,242,284,323,376,414,453,496,536,574,610,650,690,737,775,817]
    
    for i in iterator:
        set_iterator(server, i, verbose=1)
        data = fetch(server, verbose=1)
        filename = get_filename(i)
        save_json(dirpath, filename, data, verbose=1)

