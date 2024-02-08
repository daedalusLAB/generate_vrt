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

To upgrade to the latest version:

```bash
pip install --upgrade git+https://github.com/daedalusLAB/generate_vrt.git
```

### Spacy Models

After installing the package, you will need to download the Spacy models for the languages you want to use. For example, to download the models for English, German and Spanish, you can run the following commands:

```
python -m spacy download en_core_web_trf
python -m spacy download de_dep_news_trf
python -m spacy download es_dep_news_trf

```


## Usage
To run the generate_vrt tool, you can use the following command:

```bash
generate_vrt -i sample.json -o sample.vrt
```

This will generate a VRT file sample.vrt based on the JSON data in sample.json.

If you want to get the uuid of the video from an external file, you can use the following command:

```bash
generate_vrt -i sample.json -o sample.vrt -u filename_uuid_list.txt
```

filename_uuid_list.txt should be a file with the following format:

```
2021-08-07_2300_US_KNBC_NBC_4_News_at_4pm.txt,32a48b4e-f7d3-11eb-bfc9-089e01ba0326
2021-08-07_2330_BR_Globo_Jornal_nacional.txt,0f896a7e-f7df-11eb-a642-37204764a089
2021-08-08_0000_US_FOX-News_Watters_World.txt,93aeaba6-f7db-11eb-b0a5-2c600c9500f4
2021-08-08_0000_US_KNBC_NBC_4_News_at_5pm.txt,93f5dcb0-f7db-11eb-8357-089e01ba0326
```


### Pipeline script

Usually you will use it inside a pipeline, for example:
[Pipeline](pipeline_videos.py)

Create a Huggingface token and accept the conditions for using silero vad before running the pipeline and change the hf_token in the code.
In my pc takes about 6:30 minutes to process a 1 hour of video.

```bash
./pipeline_videos.py -i videos_to_process -l en
```



## Contributing

To contribute, please fork the repository and submit a pull request.

## Contact

For any questions or issues, contact:

Raúl Sánchez
Email: raul@um.es
