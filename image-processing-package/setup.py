from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='image_processing-mauriciogianezini',
    version='0.1.1',
    author='Mauricio Gianezini',
    description='Image Processing Package using Skimage',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url="",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)