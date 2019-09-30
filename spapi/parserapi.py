import cgi
from spapi.parser import Parser
import random

form = cgi.FieldStorage()
#print form["username"]
#print request.POST['username'] # for POST form method
parser = Parser()

class ParserAPI(object):
    num_toSelect = 5

    def process_hashtag(self, tags):
        map_tags_template = []
        union = set()

        # if you want to have a map with tags and ids
        # for tag in tags:
        #     self.map_tags_template.append(parser.parse(tag))

        for tag in tags:
            map_tags_template += parser.parse(tag)[1]

        un_one = set(map_tags_template)
        un_two = set(map_tags_template)
        union = un_one.intersection(un_two)
        print(union)
        if len(union) < self.num_toSelect:
            list_of_random_items = union
        else:
            list_of_random_items = random.sample(union, self.num_toSelect)

        union.clear()

        return list_of_random_items

