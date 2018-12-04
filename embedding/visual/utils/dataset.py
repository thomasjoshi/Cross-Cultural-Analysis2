import numpy
from os import listdir
from os.path import join
from PIL import Image
import torch.utils.data as data
from torchvision import transforms

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

def load_img(filepath):
    img = Image.open(filepath).convert('RGB')
    return img

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in [".png", ".jpg"])

class DatasetFromFolder(data.Dataset):
    def __init__(self, data_dir, height, width):
        super(DatasetFromFolder, self).__init__()
        self.image = join(data_dir, "image")
        #self.transcript = join(image_dir, "transcript")
        #self.description = join(image_dir, "description")

        self.image_filenames = [x for x in listdir(self.image) if is_image_file(x)]

        self.transform = transforms.Compose([
            transforms.Resize(size=(height,width)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225]),
        ])

    def __getitem__(self, index):
        # Load Image
        file_name = self.image_filenames[index]
        image = load_img(join(self.image, self.image_filenames[index]))
        image = self.transform(image)

        return image, file_name

    def __len__(self):
        return len(self.image_filenames)
