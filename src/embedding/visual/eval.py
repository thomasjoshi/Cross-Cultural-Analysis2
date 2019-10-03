from __future__ import print_function

import argparse
import os
import shutil
import time
import random

import torch
import numpy as np
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data as data
import torchvision.transforms as transforms
import torchvision.datasets as datasets

#import torchvision.models as models
#import models.imagenet as customized_models
import models.cifar as models

from utils import *

torch.backends.cudnn.benchmark = True
torch.backends.cudnn.enabled = True

model_names = sorted(name for name in models.__dict__
    if name.islower() and not name.startswith("__")
    and callable(models.__dict__[name]))

# Optimization options
parser = argparse.ArgumentParser(description='Visual Feature Extraction Using Classification Networks')
parser.add_argument('-d', '--data', default='path to dataset', type=str)
# Optimization options
parser.add_argument('--epochs', default=90, type=int, metavar='N',
                    help='number of total epochs to run')
parser.add_argument('--start-epoch', default=0, type=int, metavar='N',
                    help='manual epoch number (useful on restarts)')
parser.add_argument('--train-batch', default=256, type=int, metavar='N',
                    help='train batchsize (default: 256)')
parser.add_argument('--test-batch', default=200, type=int, metavar='N',
                    help='test batchsize (default: 200)')
parser.add_argument('--lr', '--learning-rate', default=0.1, type=float,
                    metavar='LR', help='initial learning rate')
parser.add_argument('--drop', '--dropout', default=0, type=float,
                    metavar='Dropout', help='Dropout ratio')
parser.add_argument('--schedule', type=int, nargs='+', default=[150, 225],
                        help='Decrease learning rate at these epochs.')
parser.add_argument('--gamma', type=float, default=0.1, help='LR is multiplied by gamma on schedule.')
parser.add_argument('--momentum', default=0.9, type=float, metavar='M',
                    help='momentum')
parser.add_argument('--weight-decay', '--wd', default=1e-4, type=float,
                    metavar='W', help='weight decay (default: 1e-4)')
# Checkpoints
parser.add_argument('-c', '--checkpoint', default='checkpoint', type=str, metavar='PATH',
                    help='path to save checkpoint (default: checkpoint)')
parser.add_argument('--resume', default='', type=str, metavar='PATH',
                    help='path to latest checkpoint (default: none)')
# Architecture
parser.add_argument('--arch', '-a', metavar='ARCH', default='resnet18',
                    choices=model_names,
                    help='model architecture: ' +
                        ' | '.join(model_names) +
                        ' (default: resnet18)')
parser.add_argument('--depth', type=int, default=29, help='Model depth.')
parser.add_argument('--cardinality', type=int, default=32, help='ResNet cardinality (group).')
parser.add_argument('--base-width', type=int, default=4, help='ResNet base width.')
parser.add_argument('--widen-factor', type=int, default=4, help='Widen factor. 4 -> 64, 8 -> 128, ...')
# Miscs
parser.add_argument('--manualSeed', type=int, help='manual seed')
parser.add_argument('--pretrained', dest='pretrained', action='store_true',
                    help='use pre-trained model')
#Device options
parser.add_argument('--gpu-id', default='0', type=str,
                    help='id(s) for CUDA_VISIBLE_DEVICES')

parser.add_argument('-e', '--evaluate', type=int, default=1, help='evaluation mode')
parser.add_argument('--workers', default='4', type=int,
                    help='number of threads for loading the dataset')
parser.add_argument('--image_height', type=int, default=256, help='Height of input image, default=256')
parser.add_argument('--image_width', type=int, default=256, help='Width of input image, default=256')
parser.add_argument('--root_dir', default = '../../dataset/', help='Default root directory for dataset')
parser.add_argument('--save_option', default = 'npy', help='save option for feature vector')
args = parser.parse_args()
state = {k: v for k, v in args._get_kwargs()}

# Use CUDA
os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu_id
use_cuda = torch.cuda.is_available()

# Random seed
if args.manualSeed is None:
    args.manualSeed = random.randint(1, 10000)
random.seed(args.manualSeed)
torch.manual_seed(args.manualSeed)
if use_cuda:
    torch.cuda.manual_seed_all(args.manualSeed)

def main():
    global best_acc
    start_epoch = args.start_epoch  # start from epoch 0 or last checkpoint epoch

    if not os.path.isdir(args.checkpoint):
        mkdir_p(args.checkpoint)

    testset = DatasetFromFolder(args.root_dir, args.image_height, args.image_width)
    testloader = data.DataLoader(dataset=testset, num_workers=args.workers, batch_size=args.test_batch, shuffle=False)

    # create model
    #if args.pretrained:
    if True:
        print("=> using pre-trained model '{}'".format(args.arch))
        model = models.__dict__[args.arch](pretrained=True)
    elif args.arch.startswith('resnext'):
        model = models.__dict__[args.arch](
                    baseWidth=args.base_width,
                    cardinality=args.cardinality,
                )
    else:
        print("=> creating model '{}'".format(args.arch))
        model = models.__dict__[args.arch]()

    if args.arch.startswith('alexnet') or args.arch.startswith('vgg'):
        model.features = torch.nn.DataParallel(model.features)
        model.cuda()
    else:
        model = torch.nn.DataParallel(model).cuda()

    print(' Total params: %.2fM' % (sum(p.numel() for p in model.parameters())/1000000.0))

    # Resume
    title = 'ImageNet-' + args.arch
    if args.resume:
        # Load checkpoint.
        print('==> Resuming from checkpoint..')
        assert os.path.isfile(args.resume), 'Error: no checkpoint directory found!'
        args.checkpoint = os.path.dirname(args.resume)
        checkpoint = torch.load(args.resume)
        best_acc = checkpoint['best_acc']
        start_epoch = checkpoint['epoch']
        model.load_state_dict(checkpoint['state_dict'])

    if args.evaluate:
        print('\nEvaluation only')
        test(testloader, model, start_epoch, use_cuda)
        return


def test(testloader, model, epoch, use_cuda):
    batch_time = AverageMeter()
    data_time = AverageMeter()
    save_path = args.root_dir
    if not os.path.isdir(save_path):
        mkdir_p(save_path)

    # switch to evaluate mode
    model.eval()

    end = time.time()
    with torch.no_grad():
        for batch in testloader:
            # measure data loading time
            data_time.update(time.time() - end)
            image, file_name = batch[0], batch[1]

            if use_cuda:
                image = image.cuda()

            image = torch.autograd.Variable(image, requires_grad=False)

            # compute output
            feature_vec = model(image)

            for i in range(0,image.size()[0]):
                if args.save_option == 'pt':
                    torch.save(feature_vec[i], save_path + "/" + file_name[i][:-4] + '.pt')
                    print('file saved: ' + save_path + "/" + file_name[i][:-4] + '.pt')
                elif args.save_option == 'npy':
                    print(feature_vec.cpu().data[i].numpy())
                    np.save(save_path + "/" + file_name[i][:-4] ,feature_vec.cpu().data[i].numpy())
                    print('file saved: ' + save_path + "/" + file_name[i][:-4] + '.npy')

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()
        return

if __name__ == '__main__':
    main()
