import os

os.system('git clone https://huggingface.co/AIRI-Institute/HairFastGAN')
os.system('cd HairFastGAN && git lfs pull && cd ..')
os.system('mv HairFastGAN/pretrained_models pretrained_models')
os.system('%mv HairFastGAN/input input')
os.system('rm -rf HairFastGAN')


