import spacy
from spapi.parserapi import ParserAPI
from spapi.client_photolab import ClientPhotolab
import os.path
import config
import json
import random

nlp = spacy.load('en_core_web_lg')
parserapi = ParserAPI()
api = ClientPhotolab()

class SpApi(object):
    shablon = None

    def __init__(self):
        with open("/Users/dmytro/PycharmProjects/BotTell/spapi/shablon.json", "r") as read_file:
            self.shablon = json.load(read_file)

        # content_filename = 'girl.jpg'
        # if not os.path.exists(content_filename):
        #     api.download_file('http://soft.photolab.me/samples/girl.jpg', content_filename)
        #
        # content_url = api.image_upload(content_filename)
        # array_one = self.parse_text_combo('So, I decided to chech, how work my App. This text response for implementation in code. I have to write some sentences for this job.')
        # array_image = self.transform_image(array_one, content_url)
        # print(array_image)

    def pipeline_process(self, text, image):
        list_hashtag = None

        content_filename = config.photo_path + image

        if not os.path.exists(content_filename):
            api.download_file('http://soft.photolab.me/samples/girl.jpg', content_filename)

        content_url = api.image_upload(content_filename)

        # version 1 hashtag combo process
        # list_hashtag = self.parse_text(text)
        # array_id = parserapi.process_hashtag(list_hashtag)
        # result_urls = self.transform_image_combo_id(array_id, content_url)

        # version 2 correletion with template names
        array_id_templates = self.parse_text_combo(text)
        print(array_id_templates)
        if len(array_id_templates) < 4:
            array_process = array_id_templates
        else:
            array_process = random.sample(array_id_templates, 4)

        result_urls = self.transform_image(array_process, content_url)

        return result_urls

    def parse_text(self, text):
        doc = nlp(text)
        list_hash = []
        for token in doc:
            if token.tag_ == 'VBG' or token.tag_ == 'VBZ' or token.tag_ == 'NN' or token.tag_ == 'VB' or token.tag_ == 'VBN':
                list_hash.append(token.text)

        return list_hash

    def parse_text_combo(self, text):
        id_templates = []

        tokens = nlp(text)

        for elem in self.shablon:
            token = nlp(elem)
            coeff = tokens.similarity(token)
            if coeff > 0.8:
                id_templates.append(self.shablon[elem])

        return id_templates

    def transform_image(self, id_list, content_url):
        result_urls = []

        for id in id_list:
            try:
                result_url = api.template_process(id, [{
                        'url': content_url,
                        'rotate': 0,
                        'flip': 0,
                        'crop': '0,0,1,1'
                }])
            except Exception as e:
                pass

            result_urls.append(result_url)

        # try:
        #     for id in id_list:
        #         result_url = api.template_process(id, [{
        #             'url': content_url,
        #             'rotate': 0,
        #             'flip': 0,
        #             'crop': '0,0,1,1'
        #         }])
        #     result_urls.append(result_url)
        # except Exception as e:
        #     pass

        return result_urls

    def transform_image_combo_id(self, array_id, content_url):
        result_urls = []

        if not array_id:
            array_id.add(8232104)

        for combo_id in array_id:
            original_content_url = content_url
            # print('===')
            # print('start process combo_id: {}'.format(combo_id))
            i = 0
            for step in api.photolab_steps_advanced(combo_id)['steps']:
                template_name = str(step['id'])
                contents = []
                for i in range(0, len(step['image_urls'])):
                    image_url = step['image_urls'][i]
                    if len(step['image_urls'][i]) == 0:
                        image_url = original_content_url
                    contents.append({
                        'url': image_url,
                        'rotate': 0,
                        'flip': 0,
                        'crop': '0,0,1,1'
                    })
                if len(contents) == 0:
                    contents.append({
                        'url': original_content_url,
                        'rotate': 0,
                        'flip': 0,
                        'crop': '0,0,1,1'
                    })
                result_url = api.photolab_process(template_name, contents)
                i = i + 1
                if i != 0:
                    original_content_url = result_url
                # print('---for template_name: {}, result_url: {}'.format(template_name, result_url))

            result_urls.append(result_url)

        return result_urls