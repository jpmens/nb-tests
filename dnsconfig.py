#!/usr/bin/env python3

from pathlib import Path

from netbox_dns.models import View, Zone, Record

from extras.scripts import Script, StringVar, BooleanVar
from jinja2 import Environment, DictLoader


# def rm_tree(path):
#     for child in path.iterdir():
#         if child.is_file():
#             child.unlink()
#         else:
#             rm_tree(child)
# 
#     path.rmdir()
# 

name = "NetBox DNScontrol Exporters"

class DNScontrolExporter(Script):

    class Meta:
        name = "Zone Exporter"
        description = "This custom script can be used to export zone data in dnsconfig.js format to the file system"
        commit_default = True

    zone_template = '''\
    ;
    ; Zone file for zone {{ zone.name }} [{{ zone.view.name }}]
    ;

    $TTL {{ zone.default_ttl }}

    {% for record in records -%}
    {{ record.name.ljust(32) }}    {{ (record.ttl|string if record.ttl is not none else '').ljust(8) }} IN {{ record.type.ljust(8) }}    {{ record.value }}
    {% endfor %}\
    '''

    jinja_env = Environment(loader=DictLoader({"zone_file": zone_template}),
                autoescape=True,
                lstrip_blocks=True)
    template = jinja_env.get_template("zone_file")

    def run(self, data, commit):
        views = View.objects.all()

        # export_path = Path(data["export_path"]) / "netbox-dns-exporter"
        export_path = "/tmp/dns"

        try:
            export_path.mkdir(parents=False, exist_ok=True)
        except OSError as exc:
            self.log_failure(f"Could not create the export path {exc}")
            return

#        for view in views:
#            zones = Zone.objects.filter(view=view, active=True)
#            if len(zones):
#                self.log_info(f"Exporting zones for view '{view.name}'")
#                self.export_zones(zones, view.name, export_path)

        zones = Zone.objects.filter(name="example", active=True)
        self.log_info(f"Exporting zones for view '{view.name}'")
        self.export_zones(zones, "blaView", export_path)

    def export_zones(self, zones, view_name, export_path):
        view_path = export_path / view_name

        try:
            view_path.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            self.log_failure(f"Could not create directory {view_path}: {exc}")
            return

        for zone in zones:
            self.log_info(f"Exporting zone {zone}")
            records = Record.objects.filter(zone=zone, active=True)

            zone_data = self.template.render({"zone": zone, "records": records})

            zone_file_path = view_path / f"{zone.name}.db"
            try:
                zone_file = open(zone_file_path, "wb")
                zone_file.write(zone_data.encode("UTF-8"))
                zone_file.close()
            except OSError as exc:
                self.log_failure(f"Could not create zone file {zone_file_path}: {exc}")
                continue
