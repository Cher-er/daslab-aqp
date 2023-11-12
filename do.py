import json
import vae.train
import vae.score
import os
import cvae.data.prepare_data
import cvae.impute

if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'config', 'main.json')) as f:
        args = json.load(f)

    if args['vae']['train']:
        vae.train.train_vae()
    if args['vae']['gen']:
        vae.score.gen_sample()
    if args['cvae']['pre_data']:
        cvae.data.prepare_data.prepare_data()
    if args['cvae']['train']:
        cvae.impute.train()
