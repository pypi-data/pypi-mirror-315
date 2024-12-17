from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ParticleInteractionSimulationSystem',
    version='0.3',
    packages=find_packages(),
    description='A Lightweight Pygame Particle System',
    author='SirBilby',
    license='MIT',
    install_requires=[
        'pygame'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)