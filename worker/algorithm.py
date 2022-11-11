from subprocess import Popen, PIPE, STDOUT
import os

def inference_diffusion_projected_gan(result_dir_path, target_data_num, cls, model_weight_path):
    cmd = 'python -u Diffusion-GAN/diffusion-projected-gan/gen_images.py --outdir="{}" --seeds=1-{} --class={} --network={}'.format(os.path.join(result_dir_path, str(cls)), target_data_num, str(cls), model_weight_path)
    env = os.environ.copy()

    process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, env=env)

    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            print(line.decode("utf-8").strip())

    process.wait()