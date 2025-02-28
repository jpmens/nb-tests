#!/usr/bin/env python3

from extras.scripts import *
import requests
import os
import sys

class RunAnsible(Script):
    class Meta:
       name = "ansible"
       description = "Launch an Ansible playbook"
    
    def run(self, data, commit):
        
        url = "http://192.168.1.140:8081/job_run/one.yml"
        extra_vars = {
            "botella" : "vino tinto",
            "username": "Jane",
        }
        
        try:
            r = requests.post(url, json=extra_vars)
            # print(r.text)     # would be displayed on NetBox console
        except Exception as e:
            self.log_failure(f"Cannot connect to Ansible Runner: {e}")
            return

        return r.text    # playbook output
