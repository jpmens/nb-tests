#!/usr/bin/env python3

#-- begin workaround
#import django, os, sys
#sys.path.append('/opt/netbox/netbox')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netbox.settings')
#django.setup()
#-- end workaround

# python3 manage.py runscript moo.Moo

from extras.scripts import *
from core.models import DataSource, DataFile
from jinja2 import Environment, DictLoader
# import json

class Moo(Script):
    class Meta:
       name = "moo"
       description = "display cow.txt and data.json from the same datasource"
       scheduling_enabled = False
    
    airports_template = '''\
	{% for a in airports -%}
	{{ a.iata }} {{ a.name }}
	{% endfor %}
    '''

    jinja_env = Environment(loader=DictLoader({ "airports_file" : airports_template }),
                    autoescape=True,
                    lstrip_blocks=True)
    template = jinja_env.get_template("airports_file")

    def run(self, data, commit):

        source_id = DataSource.objects.get(name="nb-tests")   # e.g. 1

        cow = DataFile.objects.get(source=source_id, path="files/cow.txt")
        rhyme = cow.data_as_string

        airdata = DataFile.objects.get(source=source_id, path="files/data.json")
        # data = json.loads(airdata.data_as_string)
        fdata = airdata.get_data  # this is a method which returns safe_loaded YAML

        departures = self.template.render({"airports" : fdata()})

        # rhyme could of course be part of the template, but I separate them
        # here to illustrate the two techniques

        return rhyme + "\n-----\n" + departures
