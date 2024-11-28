import os
import numpy as np
import imageio
import torch
import torchvision
import argparse
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def multi_view_multi_time(args):
    """
    Generating multi view multi time data
    """

    Maskrcnn = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True).cuda().eval()
    threshold = 0.2


    imgs = []
    all_files = sorted(os.listdir(os.path.join(args.data_dir, 'image')))
    print(all_files)

    for each_file in all_files:
        read_in_image = imageio.imread(os.path.join(args.data_dir, 'image', each_file))
        rgb_image = Image.fromarray(read_in_image).convert("RGB")
        rgb_image_array = np.array(rgb_image)

        imgs.append(rgb_image_array)

    imgs = np.array(imgs)
    num_frames, H, W, _ = imgs.shape

    create_dir(os.path.join(args.data_dir, 'mask'))

    for idx, img in enumerate(imgs):
        print(idx)

        # Get coarse background mask
        img = torchvision.transforms.functional.to_tensor(img).to(device)
        background_mask = torch.FloatTensor(H, W).fill_(1.0).to(device)
        objPredictions = Maskrcnn([img])[0]

        for intMask in range(len(objPredictions['masks'])):
            if objPredictions['scores'][intMask].item() > threshold:
                background_mask[objPredictions['masks'][intMask, 0, :, :] > threshold] = 0.0
                if objPredictions['labels'][intMask].item() == 1: # person
                    background_mask[objPredictions['masks'][intMask, 0, :, :] > threshold] = 0.0

        background_mask_np = ((background_mask.cpu().numpy() > 0.1) * 255).astype(np.uint8)
        imageio.imwrite(os.path.join(args.data_dir, 'mask', str(idx).zfill(3) + '.png'), background_mask_np)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default='../data/',
                        help='where to read and store data')

    args = parser.parse_args()
    args.data_dir = os.path.join(args.data_dir, "preprocessed")

    multi_view_multi_time(args)
