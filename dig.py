#!/usr/bin/env python3

from extras.scripts import *
from netbox_dns.choices import RecordTypeChoices
import os
import sys
from subprocess import Popen, PIPE

CHOICES = (
  ('A', 'A'),
  ('AAAA', 'AAAA'),
  ('TXT', 'TXT'),
  ('DNSKEY', 'DNSKEY'),
)

class MyDig(Script):
    class Meta:
       name = "dig"
       description = "perform a DNS query"
       scheduling_enabled = False
    
    qname = StringVar(
        description="domain name to query",
        required=True
    )
    qtype = ChoiceVar(
        choices=RecordTypeChoices, # CHOICES,
        description="query type",
        required=True
    )

    def run(self, data, commit):
        qname = data["qname"]
        qtype = data["qtype"]

        username = self.request.user.username
        ip_address = self.request.META.get('HTTP_X_FORWARDED_FOR') or \
                   self.request.META.get('REMOTE_ADDR')
        self.log_info(f"I am user {username} (IP: {ip_address})...")

        process = Popen(['dig', '+multiline', '-t', qtype, qname], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        return stdout.decode("utf-8")
