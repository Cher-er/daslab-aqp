import json
import vae.train
import vae.gen
import vae.aqp
import vae.ground_truth
import os
import cvae.data.prepare_data
import cvae.impute

if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'config', 'main.json')) as f:
        args = json.load(f)

    if args['vae']['train']:
        vae.train.train_vae()
    if args['vae']['gen']:
        vae.gen.gen_sample()
    if args['vae']['aqp']:
        vae.aqp.aqp_avg()
    if args['vae']['ground_truth']:
        vae.ground_truth.exact_avg()
    if args['cvae']['pre_data']:
        cvae.data.prepare_data.prepare_data()
    if args['cvae']['train']:
        cvae.impute.train()
