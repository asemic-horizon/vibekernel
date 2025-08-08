"""
Entry point for running VibeKernel directly with python -m vibekernel.kernel
"""

from .kernel import VibeKernel

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=VibeKernel)