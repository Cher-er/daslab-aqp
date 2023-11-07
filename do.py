import json
import vae.train

if __name__ == '__main__':
    with open('config/main.json') as f:
        args = json.load(f)

    if args['vae']['train']:
        vae.train.train()
