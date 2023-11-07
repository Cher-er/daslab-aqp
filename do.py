import json
import vae.train
import os

if __name__ == '__main__':
    print(os.getcwd())
    
    with open('config/main.json') as f:
        args = json.load(f)

    if args['vae']['train']:
        vae.train.train()
