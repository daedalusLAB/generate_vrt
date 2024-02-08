from setuptools import setup, find_packages

setup(
    name="generate_vrt",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "argparse",
        "spacy"
    ],
    entry_points={
        'console_scripts': [
            'generate_vrt=generate_vrt:main',
        ],
    },
    author="Raúl Sánchez",
    author_email="raul@um.es ",
    description="A tool to vrt files from json whisperX output.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/daedalusLAB/generate_vrt",
)
