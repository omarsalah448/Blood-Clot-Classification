import os
import gc
import torch
import numpy as np
import pyvips
import random
import torch.nn as nn
from time import time
from PIL import Image
from tqdm import tqdm
from typing import List, Tuple
from collections import defaultdict
from torchvision import models, transforms

# from lime import lime_image
# from skimage.segmentation import mark_boundaries

from flask import Flask, jsonify, request


BLOCK_SIZE = 28
BLOCKS_PER_CROP = 8
CROP_SIZE = BLOCK_SIZE * BLOCKS_PER_CROP
BLOCK_THR = 90
CROP_THR = 0.6
MAX_CROPS_PER_IMAGE = 20
IMAGES_PER_SAMPLE = 4
SCALE_FACTOR = 24


class DataPreparation:
    def __init__(self, seed: int = 42):
        self.seed = seed

    @staticmethod
    def _get_blocks_map(image: np.ndarray) -> np.ndarray:
        pixels_diff = np.sum((image[:-1, :, :] - image[1:, :, :]) ** 2, axis=2)
        pixels_diff = np.cumsum(np.cumsum(pixels_diff, axis=0), axis=1)
        blocks_map = np.zeros((
            (image.shape[0] + BLOCK_SIZE - 1) // BLOCK_SIZE,
            (image.shape[1] + BLOCK_SIZE - 1) // BLOCK_SIZE,
        ))
        for x in range(0, pixels_diff.shape[0], BLOCK_SIZE):
            for y in range(0, pixels_diff.shape[1], BLOCK_SIZE):
                nx = min(x + BLOCK_SIZE, pixels_diff.shape[0])
                ny = min(y + BLOCK_SIZE, pixels_diff.shape[1])
                block_sum = int(pixels_diff[nx - 1, ny - 1])
                if x:
                    block_sum -= int(pixels_diff[x - 1, ny - 1])
                if y:
                    block_sum -= int(pixels_diff[nx - 1, y - 1])
                if x and y:
                    block_sum += int(pixels_diff[x - 1, y - 1])
                blocks_map[x // BLOCK_SIZE][y // BLOCK_SIZE] = \
                    (block_sum / BLOCK_SIZE / BLOCK_SIZE) > BLOCK_THR
        return blocks_map

    def _generate_crops_positions(
            self,
            image: np.ndarray,
            crop_thr: float,
    ) -> Tuple[List[Tuple[int, int]], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        blocks_map = self._get_blocks_map(image)

        good_crops_starts = []
        for x in range(0, image.shape[0] - CROP_SIZE + 1, BLOCK_SIZE):
            for y in range(0, image.shape[1] - CROP_SIZE + 1, BLOCK_SIZE):
                _x, _y = x // BLOCK_SIZE, y // BLOCK_SIZE
                crop_sum = blocks_map[_x:_x + BLOCKS_PER_CROP, _y:_y + BLOCKS_PER_CROP].sum()
                if crop_sum > BLOCKS_PER_CROP * BLOCKS_PER_CROP * crop_thr:
                    good_crops_starts.append((x, y))

        return good_crops_starts

    @staticmethod
    def _process_crop(crop: np.ndarray) -> np.ndarray:
        return crop

    def _create_crops(
        self,
        image: np.ndarray,
        crops_starts: List[Tuple[int]],
    ) -> List[np.ndarray]:
        return [
            Image.fromarray(
                self._process_crop(
                    image[x:x + CROP_SIZE, y:y + CROP_SIZE],
                )
            )
            for x, y in crops_starts
        ]

    @staticmethod
    def _get_unique_crops(crop_starts: List[Tuple[int, int]], order) -> List[Tuple[int, int]]:
        def inter_size_1d(a: int, b: int, c: int, d: int) -> int:
            return max(0, min(b, d) - max(a, c))

        def inter_size_2d(crop_start_1: Tuple[int, int], crop_start_2: Tuple[int, int]) -> int:
            return inter_size_1d(
                crop_start_1[0], crop_start_1[0] + CROP_SIZE,
                crop_start_2[0], crop_start_2[0] + CROP_SIZE,
            ) * inter_size_1d(
                crop_start_1[1], crop_start_1[1] + CROP_SIZE,
                crop_start_2[1], crop_start_2[1] + CROP_SIZE,
            )

        crop_starts_sorted = sorted(crop_starts, key=order)
        final_crop_starts = []
        for crop_start in crop_starts_sorted:
            if any(
                    inter_size_2d(crop_start, crop_start_prev) > CROP_SIZE * CROP_SIZE // 2
                    for crop_start_prev in final_crop_starts
            ):
                continue
            final_crop_starts.append(crop_start)
        return final_crop_starts

    @staticmethod
    def _read_and_resize_image(image_id: str, base_image_path: str, once_flag) -> np.ndarray:
        image_path = os.path.join(base_image_path, f'{image_id}.tif')
        if once_flag: image_path = base_image_path
        image = pyvips.Image.new_from_file(image_path, access='sequential')
        return image.resize(1.0 / SCALE_FACTOR).numpy()

    def prepare_crops(
            self,
            image_ids: List[int],
            base_image_path: str,
            once_flag,
    ) -> Tuple[List[List[np.ndarray]], List[List[Tuple[int]]], List[Tuple[np.ndarray, np.ndarray]]]:
        np.random.seed(self.seed)
        image_crops = []
        image_crops_indices = []
        for image_id in tqdm(image_ids):
            start_time = time()
            image = self._read_and_resize_image(image_id, base_image_path, once_flag)
            gc.collect()
            found_flag = False
            for crop_thr in np.arange(CROP_THR, -0.1, -0.1):
                good_crops_starts = self._generate_crops_positions(image, crop_thr)
                if len(good_crops_starts) < IMAGES_PER_SAMPLE:
                    continue

                good_crops_starts_unique = []
                for order in [
                    lambda x: (x[0], x[1]),
                    lambda x: (-x[0], -x[1]),
                ]:
                    good_crops_starts_unique.extend(self._get_unique_crops(good_crops_starts, order))
                good_crops_starts_unique = list(set(good_crops_starts_unique))

                if len(good_crops_starts_unique) < IMAGES_PER_SAMPLE:
                    continue

                good_crops_starts_sample_ids = np.random.choice(
                    list(range(len(good_crops_starts_unique))),
                    min(len(good_crops_starts_unique), MAX_CROPS_PER_IMAGE),
                    replace=False,
                )
                good_crops_starts_sample = np.array(good_crops_starts_unique)[good_crops_starts_sample_ids]
                image_crops_indices.append(good_crops_starts_sample)
                image_crops.append(self._create_crops(image, good_crops_starts_sample))
                found_flag = True
                break
            if not found_flag:
                image_crops_indices.append([])
                image_crops.append([])
        gc.collect()
        return image_crops, image_crops_indices

    def process_once(self, image_path) -> Tuple[List[List[np.ndarray]], List[List[Tuple[int]]]]:
        self.test = [("img_id", "unkown", -1)]
        return self.prepare_crops("img_id", image_path, True)
    
class ClotModelSingle(nn.Module):
    def __init__(self, encoder_model):
        super().__init__()

        if encoder_model == 'effnet_b0':
            # base_model = models.efficientnet_b0(pretrained=True)
            base_model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
            self.model = base_model.features
            in_features_cnt = base_model.classifier[1].in_features
        elif encoder_model == 'resnet18':
            base_model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
            self.model = nn.Sequential(*list(base_model.children())[:-2])
            in_features_cnt = list(base_model.children())[-1].in_features
        elif encoder_model == 'regnet_x_1_6gf':
            base_model = models.regnet_x_1_6gf(weights=models.RegNet_X_1_6GF_Weights.IMAGENET1K_V2)
            self.model = nn.Sequential(base_model.stem, base_model.trunk_output)
            in_features_cnt = base_model.fc.in_features
        else:
            raise Exception('Incorrect encoder name')

        self.head = nn.Sequential(
            nn.AdaptiveAvgPool2d(output_size=1),
            nn.Flatten(),
            nn.Linear(in_features_cnt, 1),
            nn.Sigmoid(),
        )

    def freeze_encoder(self, flag):
        for param in self.model.parameters():
            param.requires_grad = not flag

    def forward(self, x):
        return self.head(self.model(x))

    def save(self, model_path):
        weights = self.state_dict()
        torch.save(weights, model_path)

    def load(self, model_path):
        weights = torch.load(model_path, map_location='cpu')
        self.load_state_dict(weights)

class ClotImageDataset(torch.utils.data.Dataset):
    def __init__(
            self,
            image_ids: List[str],
            labels: List[str],
            image_crops: List[List[np.ndarray]],
            seed: int,
            is_test: bool,
            transformations,
    ):
        self.image_ids = image_ids
        self.labels = [float(label == 'CE') for label in labels]
        self.image_crops = image_crops
        self.seed = seed
        self.is_test = is_test
        self.transformations = transformations

        if not self.is_test:
            np.random.seed(self.seed)
            '''
            Create a dictionary
            Dictionary has two labels, each label contains the number of indices
            in which the indeces of images belong to the label
            '''
            label_to_indices = defaultdict(list)
            for i, (label, crops) in enumerate(zip(self.labels, self.image_crops)):
                if len(crops) > 0:
                    label_to_indices[label].append(i)
            '''
            get maximum number of indeces(Images for each label) multiply by 4
            and this number is the number of samples we need for each label and
            this will be done through image segmentation
            '''
            max_size = 4 * max(len(indices) for indices in label_to_indices.values())

            '''
            There will be sample_ids array, it contains all the indeces of images
            this array is balanced, if max size variable is 40 for example
            sample ids will have 80 samples and both labels must be replecated
            to reach the maximum size of sample ids
            '''
            self.sample_ids = []
            for i, indices in enumerate(label_to_indices.values()):
                np.random.shuffle(indices)
                '''
                Keep appending in sample ids till the maximum limit for the given label
                is reached then switch to next label
                '''
                while len(self.sample_ids) < max_size * (i + 1):
                    req_size = min(len(indices), max_size * (i + 1) - len(self.sample_ids))
                    self.sample_ids += indices[:req_size]
        else:
            '''
            in testing case, append all the indeces of images 20 times
            actually i don't know why but that what happened
            '''
            self.sample_ids = []
            # for _ in range(20):
            #     self.sample_ids.extend(list(range(len(self.image_ids))))
            self.sample_ids.extend(list(range(len(self.image_ids))))

        '''
        For each Tkrar of the image id in sample ids, increment the index of the
        crop that is to be processed next
        (Still i don't know why he is doing this)
        '''
        self.image_index_ids = []
        sample_id_to_image_index = defaultdict(int)
        for sample_id in self.sample_ids:
            self.image_index_ids.append(sample_id_to_image_index[sample_id])
            image_crops_cnt = len(self.image_crops[sample_id])
            if image_crops_cnt:
                sample_id_to_image_index[sample_id] = (sample_id_to_image_index[sample_id] + 1) % image_crops_cnt

    def __len__(self):
        return len(self.sample_ids)

    def __getitem__(self, idx):
        if self.is_test:
            np.random.seed(self.seed + idx)
            random.seed(self.seed + idx)
            torch.manual_seed(self.seed + idx)
        idx, image_index = self.sample_ids[idx], self.image_index_ids[idx]
        if len(self.image_crops[idx]) == 0:
            return (
                self.transformations(Image.fromarray(np.zeros((224, 224, 3)).astype(np.uint8))),
                torch.tensor(self.labels[idx]),
                self.image_ids[idx],
            )
        # image_index = np.random.randint(0, len(self.image_crops[idx]))
        return (
            self.transformations(self.image_crops[idx][image_index]),
            torch.tensor(self.labels[idx]),
            self.image_ids[idx],
        )


def get_loader(
        image_ids: List[str],
        labels: List[str],
        image_crops: List[List[np.ndarray]],
        seed: int,
        is_test: bool,
        transformations,
        shuffle: bool,
        batch_size: int,
        num_workers: int
):
    dataset = ClotImageDataset(
        image_ids, labels, image_crops, seed, is_test, transformations,
    )
    return torch.utils.data.DataLoader(dataset, shuffle=shuffle, batch_size=batch_size, num_workers=num_workers)


"""## Inference Phase"""


TEST_BATCH_SIZE = 16


def process_image(image_path):
  test_transforms = transforms.Compose([
      # transforms.RandomResizedCrop((224, 224), scale=(0.5, 1.0), ratio=(1.0, 1.0)),
      transforms.RandomAdjustSharpness(sharpness_factor=2, p=1.0),
      transforms.RandomAdjustSharpness(sharpness_factor=2, p=0.5),
      transforms.ColorJitter(brightness=0.2, saturation=0.5, hue=0.5),
      transforms.ToTensor(),
      transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
  ])
  data_prep = DataPreparation()

  image_crops, _ = data_prep.process_once(image_path)

  dataloader = get_loader(
      [image_id for image_id, _, _ in data_prep.test],
      [label for _, label, _ in data_prep.test],
      image_crops,
      seed=41,
      is_test=True,
      transformations=test_transforms,
      shuffle=False,
      batch_size=TEST_BATCH_SIZE,
      num_workers=1,
  )

  return dataloader, image_crops

def predict(image_path, model_path):
  dataloader, image_crops = process_image(image_path)
  model = torch.load(model_path, map_location=torch.device('cpu'))
  model.eval()

  with torch.no_grad():
      for image, label, image_id in dataloader:
          y_hat = model.forward(image).squeeze().cpu().detach().numpy()

  return "CE" if y_hat >= 0.5 else "LAA"


# def predict_explain(img, model_path="center_id_7_epoch_8_target_0.594.h5"):
#   model = torch.load(model_path, map_location=torch.device('cpu'))
#   img = torch.tensor(img).permute(0, 3, 1, 2)
#   return model.forward(img).detach().numpy()

# def explain(image_path, num_samples=100):
#     dataloader, image_crops = process_image(image_path)
#     torch_img = next(iter(dataloader))[0]
#     numpy_img = np.array(torch_img.permute(0, 2, 3, 1).squeeze())
#     explainer = lime_image.LimeImageExplainer()
#     explanation = explainer.explain_instance(numpy_img, predict_explain, num_samples=num_samples)
#     temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, hide_rest=False)
#     return mark_boundaries(temp / 2 + 0.5, mask)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    print("json")
    json = request.get_json()
    print(json)
    # Perform prediction using the uploaded image file
    result = predict(json["image_path"], model_path="center_id_7_epoch_8_target_0.594.h5")
    return jsonify({'prediction': result})

# @app.route('/explain', methods=['POST'])
# def explain_endpoint():
#     json = request.get_json()
#     xai_img = explain(json["image_path"], num_samples=10)
#     return jsonify({'image': "finished"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)