# setup.py
from setuptools import setup, find_packages

setup(
    name='AlloySustainability',
    version='0.1.0',
    description='Compute and visualize the sustainability impacts of alloys',
    author='Votre Nom',
    author_email='votre.email@example.com',
    url='https://github.com/votrecompte/AlloySustainability',  # votre repo GitHub
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
)
