#!/usr/bin/env python

import pandas as pd
import argparse
import json
import spacy

# Author: Raúl Sánchez <raul@um.es>
# generates a VRT (Verticalized Text) representation from a given JSON file, which primarily contains aligned transcriptions with timestamps. 
# json file is generated by the whisper tool (we are using whisperX)
# The code utilizes the spaCy library to extract linguistic features such as POS tags, lemmas, and dependency relationships.


class VRTGenerator:
    ''' Initializes the VRTGenerator class'''
    def __init__(self, input_json_file, output_vrt_file, uuid=None):
        self.input_json_file = input_json_file
        self.output_vrt_file = output_vrt_file
        self.uuid = uuid
        self.aligned_transcription = self.extract_timestamps()
        self.language = self.get_language()
        self.nlp = self.load_spacy_model()
        self.metadata = self.get_metadata()


    ''' Returns a list of words and their timestamps from a JSON file'''
    def extract_timestamps(self):
        # Read the JSON file
        with open(self.input_json_file, 'r') as f:
            json_data = json.load(f)

        # Initialize an empty list to store the extracted data
        extracted_data = []
        
        # Initialize variables to store previous timestamps
        prev_start = 0.0
        prev_end = 0.0

        # Loop through each segment in the JSON data
        for segment in json_data['segments']:
            # Loop through each word in the segment
            for word_data in segment['words']:
                # Extract the word
                word = word_data['word']
                
                # Check if 'start' and 'end' keys exist
                if 'start' in word_data and 'end' in word_data:
                    start = word_data['start']
                    end = word_data['end']
                    # Update previous timestamps
                    prev_start = start
                    prev_end = end
                else:
                    # Use previous timestamps for words without their own timestamps
                    start = prev_start
                    end = prev_end                
                # Append the data to the list
                extracted_data.append([word, start, end])

        # Create a DataFrame from the list
        df = pd.DataFrame(extracted_data, columns=['word', 'start', 'end'])
        return df


    ''' Returns the language of the transcription from the input JSON file'''
    def get_language(self):
        # Read the JSON file
        with open(self.input_json_file, 'r') as f:
            json_data = json.load(f)
        # Return the language
        return json_data['language']


    ''' Load spacy model for the language of the transcription'''
    def load_spacy_model(self):
        # switch case for different languages
        if self.language == 'en':
            nlp = spacy.load('en_core_web_trf')
        elif self.language == 'de':
            nlp = spacy.load('de_core_news_trf')
        elif self.language == 'es':
            nlp = spacy.load('es_dep_news_trf')
        else:
            print('Language not supported')
            exit(0)
        return nlp

    ''' Private function to get seconds from a timestamp'''
    def get_secs(self, timestamp):
        # split the timestamp at the dot and return the left part (before the dot)
        return str(int(str(timestamp).split('.')[0]))
    
    ''' Private function to get milliseconds from a timestamp'''
    def get_msecs(self, timestamp):
        # split the timestamp at the dot and return the right part (after the dot)
        return str(int(str(timestamp).split('.')[1]))
        

    ''' Map the tokens to the words in the aligned transcription'''
    def map_tokens_to_words_time(self, word_timings):
        word_timings_dict = word_timings.to_dict('records')
        text = self.aligned_transcription['word'].str.cat(sep=' ')
        doc = self.nlp(text)
        results = []
        sentence = []

        external_char_idx = 0  # Initialize external character index

        for sent in doc.sents:
            sentence_doc = self.nlp(sent.text)
    
            for token in sentence_doc:
                internal_char_idx = token.idx  # Internal character index for the sentence
                char_idx = external_char_idx + internal_char_idx  # Actual character index in the original document

                #word = text[char_idx:char_idx+len(token.text)]
                word_index = text[:char_idx].count(' ')

                token_info = {
                    "word": token.text,
                    "pos": token.pos_,
                    "lemma": token.lemma_,
                    "lemma_pos": token.lemma_ + "_" + token.pos_,
                    "lower": token.lower_,
                    "prefix": token.prefix_,
                    "suffix": token.suffix_,
                    "is_digit": str(token.is_digit),
                    "like_num": str(token.like_num),
                    "dep": token.dep_,
                    "shape": str(token.shape_),
                    "tag": str(token.tag_),
                    "sentiment": str(token.sentiment),
                    "is_alpha": str(token.is_alpha),
                    "is_stop": str(token.is_stop),
                    "head": token.head.text,
                    "head_pos": token.head.pos_,
                    "children": str([child for child in token.children]),
                    "lefts": str([child for child in token.lefts]),
                    "rights": str([child for child in token.rights]),
                    "n_lefts": str(token.n_lefts),
                    "n_rights": str(token.n_rights),
                    "ent_type": str(token.ent_type_),
                    "ent_iob": str(token.ent_iob_),
                    "morph": str(token.morph),
                    "start_secs": self.get_secs(word_timings_dict[word_index]["start"]),
                    "start_msecs": self.get_msecs(word_timings_dict[word_index]["start"]),
                    "end_secs": self.get_secs(word_timings_dict[word_index]["end"]),
                    "end_msecs": self.get_msecs(word_timings_dict[word_index]["end"])
                }
                sentence.append(token_info)

            external_char_idx += len(sent.text) + 1  # Update external character index for next sentence, +1 for space
            # append to results all tokens in the sentence
            results.append(sentence)
            sentence = []

        return results

    ''' Write vrt header to the output file'''
    def get_metadata(self):
        # extract metadata from teh file name
        # file without extension and path
        filename = self.input_json_file.split('/')[-1].split('.')[0]
        # sub - for _ in filename
        filename = filename.replace('-', '_')  
        filename_with_ext = self.input_json_file.split('/')[-1]
        # filename with extension: 2016-01-01_0000_US_MSNBC_Hardball_with_Chris_Matthews.json
        # date and time: 2016-01-01_0000
        date_time = filename_with_ext.split('_')[0] + '_' + filename_with_ext.split('_')[1]
        # channel: MSNBC
        channel = filename_with_ext.split('_')[3]
        # title: Hardball_with_Chris_Matthews from 2016-01-01_0000_US_MSNBC_Hardball_with_Chris_Matthews.json
        title = '_'.join(filename_with_ext.split('_')[4:]).split('.')[0]  
        # year: 2016
        year = date_time.split('-')[0]
        # month: 01
        month = date_time.split('-')[1]
        # day: 01
        day = date_time.split('-')[2].split('_')[0]
        # time: 0000
        time = date_time.split('-')[2].split('_')[1]
        # country: US
        country = filename_with_ext.split('_')[2]
        #return { "filename": filename, filename_with_ext, date_time, channel, country, title, year, month, day, time}
        return { "filename": filename, 
                "filename_with_ext": filename_with_ext, 
                "date_time": date_time, 
                "channel": channel, 
                "country": country, 
                "title": title, 
                "year": year, 
                "month": month, 
                "day": day, 
                "time": time
                }

    ''' Write vrt header to the output file getting the output file handler'''
    def write_vrt_header(self, vrt_file):
        # if uuid is None, uuid will be filename
        if self.uuid is None:
            self.uuid = self.metadata['filename']
        # write the vrt header to the file        
        vrt_file.write('<text id="' + self.uuid  +  '" '  + 'file="' + self.metadata['filename_with_ext'] + '" '  + ' language="' + self.language + '" ' + \
            'collection="Daedalus Red Hen" ' + 'date="' + self.metadata['date_time'] + '" ' + 'channel="' + self.metadata['channel'] + '" ' + 'country="' + self.metadata['country'] + '" ' + \
            'title="' + self.metadata['title'] + '" ' + 'year="' + self.metadata['year'] + '" ' + 'month="' + self.metadata['month'] + '" ' + 'day="' + self.metadata['day'] + '" ' + 'time="' + self.metadata['time'] + '" ' + '>\n')
        
    ''' Write vrt sentence to the output file'''
    def write_vrt_sentence(self, sentence, sentence_id, vrt_file):
        # write the sentence id, filename and start and end timestamps to the file
        vrt_file.write('<s id="' + str(sentence_id) + '" reltime="' + sentence[0]['start_secs'] + '.' + sentence[0]['start_msecs'] + '">\n')
        # loop through the words in the sentence
        for token in sentence:
            # write the word to the file
            vrt_file.write(token['word'] + '\t' + token['pos'] + '\t' + token['lemma'] + '\t' + token['lemma_pos'] + '\t' + token['lower'] + '\t' + token['prefix'] + '\t' + \
                            token['suffix'] + '\t' + token['is_digit'] + '\t' + token['like_num'] + '\t' + token['dep'] + '\t' + token['shape'] + '\t' + token['tag'] + '\t' + \
                            token['sentiment'] + '\t' + token['is_alpha'] + '\t' + token['is_stop'] + '\t' + token['head'] + '\t' + token['head_pos'] + '\t' + token['children'] + '\t' + \
                            token['lefts'] + '\t' + token['rights'] + '\t' + token['n_lefts'] + '\t' + token['n_rights'] + '\t' + token['ent_type'] + '\t' + token['ent_iob'] + '\t' + \
                            token['morph'] + '\t' + token['start_secs'] + '\t' + token['start_msecs'] + '\t' + token['end_secs'] + '\t' + token['end_msecs'] + '\n')
        # write the end of the sentence to the file
        vrt_file.write('</s>\n')
        

    ''' Write vrt output file from the list of sentences with timestamps per word'''
    def write_vrt_file(self, sentences):
        # open the output file
        vrt_file = open(self.output_vrt_file, 'w')
        # write the vrt header
        self.write_vrt_header(vrt_file)
        # initialize sentence id
        sentence_id = 0        
        # loop through the sentences
        for sentence in sentences:
            # increment sentence id
            sentence_id += 1
            # write the sentence to the file
            self.write_vrt_sentence(sentence, sentence_id, vrt_file)
        # close the file
        vrt_file.write('</text>\n')
        vrt_file.close()


def get_uuid(uuid_list, json_file):
    # Read the UUIDs and filenames and return the UUID. Original uuid file looks like this:
    # 2021-08-07_2300_US_KNBC_NBC_4_News_at_4pm.txt,32a48b4e-f7d3-11eb-bfc9-089e01ba0326
    # 2021-08-07_2330_BR_Globo_Jornal_nacional.txt,0f896a7e-f7df-11eb-a642-37204764a089
    # 2021-08-08_0000_US_FOX-News_Watters_World.txt,93aeaba6-f7db-11eb-b0a5-2c600c9500f4
    # 2021-08-08_0000_US_KNBC_NBC_4_News_at_5pm.txt,93f5dcb0-f7db-11eb-8357-089e01ba0326
    with open(uuid_list, 'r') as f:
        uuids = f.read().splitlines()
    # generate original filename from json file
    json_file = json_file.split('/')[-1]
    json_file = json_file.split('.')[0]
    json_file = json_file  + '.txt'
    # loop through the UUIDs and return the UUID for the file
    for uuid in uuids:
        if json_file in uuid:
            uuid = uuid.split(',')[1]
            return uuid
    return None

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description='Generate .vrt file from Whisper .json file')
    parser.add_argument('--input_json_file', '-i', help='Input .json file from whisper', required=True)
    parser.add_argument('--output_vrt_file', '-o', help='Output .vrt file', required=True)
    parser.add_argument('--uuid_list', '-u', help='List of UUIDs to process', required=False)
    args = parser.parse_args()

    # If the UUID list is provided, get the UUID for the input JSON file
    if args.uuid_list:
        uuid = get_uuid(args.uuid_list, args.input_json_file)
    else:
        uuid = None
    # Initialize the VRTGenerator class
    vrt_generator = VRTGenerator(args.input_json_file, args.output_vrt_file, uuid)
    # Map the tokens to the words in the aligned transcription and return the sentences
    sentences = vrt_generator.map_tokens_to_words_time(vrt_generator.aligned_transcription)
    # Write the vrt file
    vrt_generator.write_vrt_file(sentences)

 
if __name__ == "__main__":
    main()
