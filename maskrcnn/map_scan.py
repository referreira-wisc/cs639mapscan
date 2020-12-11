
import os
import sys
import cv2
import glob
import datetime
import numpy as np
import skimage.draw

# Root directory of the project
ROOT_DIR = os.path.abspath("")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")

# Results directory
# Save submission files here
RESULTS_DIR = os.path.join(ROOT_DIR, "results")

n_classes = 8



############################################################
#  Configurations
############################################################

class MapScanConfig(Config):
    """
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "map_scan"

    # Number of classes (including background)
    NUM_CLASSES = n_classes + 1

    # Skip detections with < 0% confidence
    DETECTION_MIN_CONFIDENCE = 0.0
    
    # Backbone network architecture
    # Supported values are: resnet50, resnet101
    BACKBONE = "resnet50"
    
    # Input image resizing
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512

    # Use original masks
    #USE_MINI_MASK = False



############################################################
#  Dataset
############################################################

class MapScanDataset(utils.Dataset):

    def load_map_scan(self, dataset_dir, subset):
        """Load a subset of the MapScan dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # Add classes
        self.add_class("mapscan", 0, "urban")
        self.add_class("mapscan", 1, "forest")
        self.add_class("mapscan", 2, "crop1")
        self.add_class("mapscan", 3, "crop2")
        self.add_class("mapscan", 4, "crop3")
        self.add_class("mapscan", 5, "river")
        self.add_class("mapscan", 6, "lake")
        self.add_class("mapscan", 7, "grass")

        # Train or validation dataset?
        assert subset in ["train", "val"]
        dataset_dir = os.path.join(dataset_dir, subset, "images")
        
        # Get image ids from directory names
        image_ids = os.listdir(dataset_dir)

        # Add images
        for image_id in image_ids:
            self.add_image(
                "mapscan",
                image_id=image_id[:-4],  # use file name as a unique image id
                path=os.path.join(dataset_dir, image_id))

    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        info = self.image_info[image_id]
        # Get mask directory from image path
        mask_dir = os.path.join(os.path.dirname(os.path.dirname(info['path'])), "masks")
        
        # Read mask files from .csv image
        mask = []
        class_ids = []
        mask_files = glob.glob(os.path.join(mask_dir, info['id'] + '*'))
        for mask_file in mask_files:
            f = os.path.basename(mask_file)
            c = f.split('_')[1].split('.')[0]
            with open(os.path.join(mask_dir, f), 'r') as file:
                current_mask = []
                for row in file:
                    current_mask.append([c == '1' for c in row.strip()])
            mask.append(current_mask)
            class_ids.append(c)
        mask = np.stack(mask, axis=-1)
        class_ids = np.array(class_ids, dtype=np.int32)
        # Return mask, and array of class IDs of each instance.
        return mask, class_ids

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "mapscan":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)



############################################################
#  Training
############################################################

def train(model):
    """Train the model."""
    # Training dataset.
    dataset_train = MapScanDataset()
    dataset_train.load_map_scan(args.dataset, "train")
    dataset_train.prepare()

    # Validation dataset
    dataset_val = MapScanDataset()
    dataset_val.load_map_scan(args.dataset, "val")
    dataset_val.prepare()

    # *** This training schedule is an example. Update to your needs ***
    # Since we're using a very small dataset, and starting from
    # COCO trained weights, we don't need to train too long. Also,
    # no need to train all layers, just the heads should do it.
    print("Training network heads")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=60,
                layers='heads')



############################################################
#  Detection
############################################################

def detect(model, dataset_dir):
    """Run detection on images in the given directory."""
    print("Running on {}".format(dataset_dir))

    # Create directory
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    submit_dir = "submit_{:%Y%m%dT%H%M%S}".format(datetime.datetime.now())
    submit_dir = os.path.join(RESULTS_DIR, submit_dir)
    os.makedirs(submit_dir)

    # Read dataset
    dataset = MapScanDataset()
    dataset.load_map_scan(dataset_dir, "val")
    dataset.prepare()
    
    class_colors = [(255,0,0), (0,64,0), (255,255,0), (128,255,0), (0,192,0), (0,0,96), (0,0,255), (255,128,0)]
    # Load over images
    for image_id in dataset.image_ids:
        # Load image and run detection
        image = dataset.load_image(image_id)
        # Detect objects
        r = model.detect([image], verbose=0)[0]

        gt_splash = image.copy()
        pred_splash = image.copy()
        image_path = dataset.image_info[image_id]["path"]
        mask_dir = os.path.join(os.path.dirname(os.path.dirname(image_path)), "masks")
        for c in range(n_classes):
            mask = (np.sum(r['masks'][:,:,r['class_ids']==c], -1, keepdims=True) >= 1)
            # Save detected mask
            if np.max(mask):
                with open("{}/{}_{}.txt".format(submit_dir, dataset.image_info[image_id]["id"], str(c)), "w") as f:
                    for row in mask[:,:,0]:
                        f.write("".join(row.astype(int).astype(str)) + '\n')
            # Save splash images
            # Build ground truth splash
            gt_file = os.path.basename(image_path)[:-4] + "_" + str(c) + ".txt"
            if os.path.isfile(os.path.join(mask_dir, gt_file)):
                with open(os.path.join(mask_dir, gt_file), 'r') as file:
                    gt_mask = []
                    for row in file:
                        gt_mask.append([c == '1' for c in row.strip()])
                gt_mask = np.stack(gt_mask, axis=0)
                this_mask = gt_splash.copy()
                this_mask[gt_mask] = class_colors[c]
                gt_splash = cv2.addWeighted(gt_splash, 0.2, this_mask, 0.8, 0)
            # Build prediction splash
            pred_mask = mask.squeeze()
            this_mask = pred_splash.copy()
            this_mask[pred_mask] = class_colors[c]
            pred_splash = cv2.addWeighted(pred_splash, 0.2, this_mask, 0.8, 0)
        
        file_name = "splash_" + dataset.image_info[image_id]["id"] + "_gt.png"
        skimage.io.imsave(os.path.join(submit_dir, file_name), gt_splash)
        file_name = "splash_" + dataset.image_info[image_id]["id"] + "_pred.png"
        skimage.io.imsave(os.path.join(submit_dir, file_name), pred_splash)
       


############################################################
#  Command Line
############################################################

if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Train Mask R-CNN to detect biomes.')
    parser.add_argument("command",
                        metavar="<command>",
                        help="'train', 'splash', or 'detect'")
    parser.add_argument('--dataset', required=False,
                        metavar="/path/to/balloon/dataset/",
                        help='Directory of the Balloon dataset')
    parser.add_argument('--weights', required=True,
                        metavar="/path/to/weights.h5",
                        help="Path to weights .h5 file or 'coco'")
    parser.add_argument('--logs', required=False,
                        default=DEFAULT_LOGS_DIR,
                        metavar="/path/to/logs/",
                        help='Logs and checkpoints directory (default=logs/)')
    parser.add_argument('--image', required=False,
                        metavar="path or URL to image",
                        help='Image to apply the color splash effect on')
    args = parser.parse_args()

    # Validate arguments
    if args.command == "train":
        assert args.dataset, "Argument --dataset is required for training"
    elif args.command == "splash":
        assert args.image, "Provide --image to apply color splash"
    elif args.command == "detect":
        assert args.dataset, "Provide --dataset to run prediction on"

    print("Weights: ", args.weights)
    print("Dataset: ", args.dataset)
    print("Logs: ", args.logs)

    # Configurations
    if args.command == "train":
        class TrainingConfig(MapScanConfig):
            # Images used per GPU per Batch
            IMAGES_PER_GPU = 2
            # Number of training and validation steps per epoch
            n_train = len(os.listdir(os.path.join(args.dataset, "train", "images")))
            n_val = len(os.listdir(os.path.join(args.dataset, "val", "images")))
            STEPS_PER_EPOCH = n_train // IMAGES_PER_GPU
            VALIDATION_STEPS = n_val // IMAGES_PER_GPU
        config = TrainingConfig()
    else:
        class InferenceConfig(MapScanConfig):
            # Set batch size to 1 since we'll be running inference on
            # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1
        config = InferenceConfig()
    config.display()

    # Create model
    if args.command == "train":
        model = modellib.MaskRCNN(mode="training", config=config,
                                  model_dir=args.logs)
    else:
        model = modellib.MaskRCNN(mode="inference", config=config,
                                  model_dir=args.logs)

    # Select weights file to load
    if args.weights.lower() == "coco":
        weights_path = COCO_WEIGHTS_PATH
        # Download weights file
        if not os.path.exists(weights_path):
            utils.download_trained_weights(weights_path)
    elif args.weights.lower() == "last":
        # Find last trained weights
        weights_path = model.find_last()
    elif args.weights.lower() == "imagenet":
        # Start from ImageNet trained weights
        weights_path = model.get_imagenet_weights()
    else:
        weights_path = args.weights

    # Load weights
    print("Loading weights ", weights_path)
    if args.weights.lower() == "coco":
        # Exclude the last layers because they require a matching
        # number of classes
        model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])
    else:
        model.load_weights(weights_path, by_name=True)

    # Train or evaluate
    if args.command == "train":
        train(model)
    elif args.command == "detect":
        detect(model, args.dataset)
    else:
        print("'{}' is not recognized. "
              "Use 'train', 'splash', or 'detect'".format(args.command))
