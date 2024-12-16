from setuptools import setup, find_packages

setup(
    name="fanparsai",
    version="0.0.8",
    packages=find_packages(), 
    install_requires=[
        "asteroid-filterbanks==0.4.0",
    ],
    include_package_data=True,
    package_data={
        "fanparsai.fpvad": ["ERI_VAD.pth"],  
        # "fanparsai.KWS": ["WideResNet12WithEMA.pth"],  
    },
    author="FanPars",
    description="FanPars Library for Various Models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
