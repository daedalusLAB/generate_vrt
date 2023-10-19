# Generate VRT

## Description

`generate_vrt` is a Python package designed to convert JSON files from WhisperX output into VRT (Verticalized Text) format.

## Installation

### From Source
To install from source, clone the repository and run:

```bash
git clone https://github.com/daedalusLAB/generate_vrt.git
cd generate_vrt
pip install .
```

### From GitHub
To install directly from GitHub:

```bash
pip install git+https://github.com/daedalusLAB/generate_vrt.git
```


### Spacy Models

After installing the package, you will need to download the Spacy models for the languages you want to use. For example, to download the models for English, German and Spanish, you can run the following commands:

```
python -m spacy download en_core_web_trf
python -m spacy download de_core_news_trf
python -m spacy download es_dep_news_trf

```


## Usage
To run the generate_vrt tool, you can use the following command:

```bash
generate_vrt -i sample.json -o sample.vrt
```

This will generate a VRT file sample.vrt based on the JSON data in sample.json.


## Contributing

To contribute, please fork the repository and submit a pull request.

## Contact

For any questions or issues, contact:

Raúl Sánchez
Email: raul@um.es