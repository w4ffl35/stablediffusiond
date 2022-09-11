import random

# COPY THIS FILE TO settings.py AND EDIT IT
# ALL PATHS SHOULD BE ABSOLUTE

SERVER = {
    "request_queue": {
        "name": "RabbitMQ",
        "host": "localhost",
        "queue_name": "stablediffusiond"
    },
    "response_queue": {
        "name": "RabbitMQ",
        "host": "localhost",
        "queue_name": "results"
    }
}

GENERAL = {
    "sd_scripts": "../scripts",
    "sd_python_path": "~/miniconda3/envs/ldm/bin/python",
}

SCRIPTS = {
    'txt2img': [
        ('prompt', ''),
        ('outdir', '~/.stablediffusion/txt2img'),
        ('skip_grid', ''),
        # ('skip_save', ''),
        ('ddim_steps', 50),
        ('plms', ''),
        # ('laion400m', ''),
        ('fixed_code', ''),
        ('ddim_eta', 0.0),
        ('n_iter', 1),
        ('H', 512),
        ('W', 512),
        ('C', 4),
        ('f', 8),
        ('n_samples', 1),
        ('n_rows', 0),
        ('scale', 7.5),
        # ('from-file', ''),
        ('config', 'configs/stable-diffusion/v1-inference.yaml'),
        ('ckpt', 'models/ldm/stable-diffusion-v1/model.ckpt'),
        ('seed', 42),
        ('precision', 'autocast'),
    ],
    'img2img': [
        ('prompt', ''),
        ('init-img', ''),
        ('outdir', '~/.stablediffusion/img2img'),
        ('skip_grid', True),
        ('skip_save', False),
        ('ddim_steps', 50),
        ('plms', True),
        ('fixed_code', True),
        ('ddim_eta', 0.0),
        ('n_iter', 1),
        ('C', 4),
        ('f', 8),
        ('n_samples', 2),
        ('n_rows', 0),
        ('scale', 5.0),
        ('strength', 0.75),
        ('from-file', ''),
        ('config', 'configs/stable-diffusion/v1-inference.yaml'),
        ('ckpt', 'models/ldm/stable-diffusion-v1/model.ckpt'),
        ('seed', random.randint(0, 100000)),
        ('precision', 'autocast'),
    ],
    'inpaint': [
        ('indir', '~/.stablediffusion/inpaint/input'),
        ('outdir', '~/.stablediffusion/inpaint'),
        ('steps', 50),
    ],
    'knn2img': [
        ('prompt', ''),
        ('outdir', '~/.stablediffusion/knn2img'),
        ('skip_grid', True),
        ('ddim_steps', 50),
        ('n_repeat', 1),
        ('plms', True),
        ('ddim_eta', 0.0),
        ('n_iter', 1),
        ('H', 768),
        ('W', 768),
        ('n_samples', 1),
        ('n_rows', 0),
        ('scale', 5.0),
        ('from-file', ''),
        ('config', 'configs/retrieval-augmented-diffusion/768x768.yaml'),
        ('ckpt', 'models/rdm/rdm768x768/model.ckpt'),
        ('clip_type', 'ViT-L/14'),
        ('database', 'artbench-surrealism'),
        ('use_neighbors', False),
        ('knn', 10),
    ],
    'train_searcher': [
        ('d', 'data/rdm/retrieval_database/openimages'),
        ('target_path', 'data/rdm/searchers/openimages'),
        ('knn', 20),
    ],
}