import json
import os

import sampling.ground_truth
import sampling.random_sampling
import sampling.stratified_sampling

import vae.train
import vae.gen
import vae.aqp
import vae.ground_truth
import vae.measure

import cvae.train
import cvae.gen
import cvae.aqp
import cvae.ground_truth
import cvae.measure

if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'config', 'main.json')) as f:
        args = json.load(f)

    if args['sampling']['ground_truth']:
        sampling.ground_truth.exact()
    if args['sampling']['random_sampling']:
        sampling.random_sampling.exact()

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
        cvae.aqp.aqp_avg()
        cvae.ground_truth.exact_avg()
        cvae.measure.measure()
    else:
        if args['cvae']['train']:
            cvae.train.train()
        if args['cvae']['gen']:
            cvae.gen.gen()
        if args['cvae']['aqp']:
            cvae.aqp.aqp_avg()
        if args['cvae']['ground_truth']:
            cvae.ground_truth.exact_avg()
        if args['cvae']['measure']:
            cvae.measure.measure()
