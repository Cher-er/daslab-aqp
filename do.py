import json
import vae.train
import vae.gen
import vae.aqp
import vae.ground_truth
import vae.measure
import os
import cvae.train
import cvae.gen

if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'config', 'main.json')) as f:
        args = json.load(f)

    if args['vae']['all']:
        vae.train.train_vae()
        vae.gen.gen_sample()
        vae.aqp.aqp_avg()
        vae.ground_truth.exact_avg()
        vae.measure.measure()
    else:
        if args['vae']['train']:
            vae.train.train_vae()
        if args['vae']['gen']:
            vae.gen.gen_sample()
        if args['vae']['aqp']:
            vae.aqp.aqp_avg()
        if args['vae']['ground_truth']:
            vae.ground_truth.exact_avg()
        if args['vae']['measure']:
            vae.measure.measure()

    if args['cvae']['all']:
        cvae.train.train()
        cvae.gen.gen()
    else:
        if args['cvae']['train']:
            cvae.train.train()
        if args['cvae']['gen']:
            cvae.gen.gen()
