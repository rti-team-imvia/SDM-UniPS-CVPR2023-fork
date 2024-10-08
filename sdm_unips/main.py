"""
Scalable, Detailed and Mask-free Universal Photometric Stereo Network (CVPR2023)
# Copyright (c) 2023 Satoshi Ikehata
# All rights reserved.
"""

from __future__ import print_function, division
from modules.model.model_utils import *
from modules.builder import builder
from modules.io import dataio
import sys
import argparse
import time
from pathlib import Path

# Dynamically add the parent directory to sys.path for importing modules
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir.parent))

# Argument parser
parser = argparse.ArgumentParser()

# Properties
parser.add_argument('--session_name', default='sdm_unips')
parser.add_argument('--target', default='normal_and_brdf', choices=['normal', 'brdf', 'normal_and_brdf'])
parser.add_argument('--checkpoint', type=Path, default=Path('checkpoint'))

# Data Configuration
parser.add_argument('--max_image_res', type=int, default=4096)
parser.add_argument('--max_image_num', type=int, default=10)
parser.add_argument('--test_ext', default='.data')
parser.add_argument('--test_dir', type=Path, default=Path('DefaultTest'))
parser.add_argument('--test_prefix', default='L*')
parser.add_argument('--mask_margin', type=int, default=8)

# Network Configuration
parser.add_argument('--canonical_resolution', type=int, default=256)
parser.add_argument('--pixel_samples', type=int, default=10000)
parser.add_argument('--scalable', action='store_true')


def main():
    print('================================================================')
    print('                         Running sdm_unips/main.py              ')
    print('================================================================')

    args = parser.parse_args()

    # Resolve paths to make them absolute
    args.checkpoint = args.checkpoint.resolve()
    args.test_dir = args.test_dir.resolve()

    print(f'\nStarting a session: {args.session_name}')
    print(f'Target: {args.target}\n')

    # Detect GPU or fall back to CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Initialize the model builder
    sdf_unips = builder.builder(args, device)
    
    # Load the test data
    test_data = dataio.dataio('Test', args)

    start_time = time.time()

    # Run the model on the test data
    sdf_unips.run(testdata=test_data,
                  max_image_resolution=args.max_image_res,
                  canonical_resolution=args.canonical_resolution,
                  )
    
    end_time = time.time()
    print(f"Prediction finished (Elapsed time: {end_time - start_time:.3f} sec)")

    # Instructions for running relighting script
    print("\nExecute the following script to render a video under new lighting conditions based on the generated BRDF and normal map.\n")
    print(f"        python sdm_unips/relighting.py --datadir ./{args.session_name}/results/{test_data.data.objname}\n")


if __name__ == '__main__':
    main()
