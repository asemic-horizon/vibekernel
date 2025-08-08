"""
Installation script for VibeKernel
"""

import json
import os
import sys
import argparse
from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory


def install_kernel_spec(user=True, prefix=None, name=None):
    """Install the VibeKernel kernelspec."""
    if name is None:
        name = 'vibekernel'
    
    with TemporaryDirectory() as td:
        kernel_dir = os.path.join(td, name)
        os.makedirs(kernel_dir)
        
        # Create kernel.json
        kernel_spec = {
            'argv': [
                sys.executable,
                '-m', 'vibekernel.kernel',
                '-f', '{connection_file}'
            ],
            'display_name': 'Hy',
            'language': 'hy',
            'interrupt_mode': 'signal',
        }
        
        with open(os.path.join(kernel_dir, 'kernel.json'), 'w') as f:
            json.dump(kernel_spec, f, indent=2)
        
        # Install the kernelspec
        ksm = KernelSpecManager()
        ksm.install_kernel_spec(kernel_dir, name, user=user, prefix=prefix)
        
        print(f"Installed vibekernel kernel as '{name}'")


def install():
    """Command-line entry point for installing the kernel."""
    parser = argparse.ArgumentParser(
        prog='install-vibekernel',
        description='Install the VibeKernel for Jupyter'
    )
    parser.add_argument(
        '--user',
        action='store_true',
        help='Install for the current user instead of system-wide'
    )
    parser.add_argument(
        '--name',
        type=str,
        default='vibekernel',
        help='Name to use for the kernelspec (default: vibekernel)'
    )
    parser.add_argument(
        '--prefix',
        type=str,
        help='Prefix to use for installation'
    )
    
    args = parser.parse_args()
    
    try:
        install_kernel_spec(
            user=args.user or args.prefix is None,
            prefix=args.prefix,
            name=args.name
        )
    except Exception as e:
        print(f"Error installing kernel: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    install()