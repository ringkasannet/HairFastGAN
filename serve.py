from hair_swap import HairFast, get_parser
from torchvision.utils import save_image
import torch


# Init HairFast
hair_fast = HairFast(get_parser().parse_args([]))

# Inference
print("trying.....")
photos=[["/home/HairFastGAN/input/6.png","/home/HairFastGAN/input/7.png","/home/HairFastGAN/input/8.png"],["/home/HairFastGAN/input/5.jpg","/home/HairFastGAN/input/4.jpg","/home/HairFastGAN/input/3.jpg"]]
for index,item in enumerate(photos):
    print(f'In {1} image')
    print(item)
    result_image = hair_fast.swap(item[0], item[1],item[2])
    print("saving...")

    if isinstance(result_image, torch.Tensor):
        save_image(result_image, f'/home/HairFastGAN/HairFast_result{index}.png')
    else:
        result_image.save(f'/home/HairFastGAN/HairFast_result{index}.png')

