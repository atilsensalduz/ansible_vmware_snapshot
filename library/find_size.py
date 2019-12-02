#!bin/env python

 

from ansible.module_utils.basic import *

from ansible.module_utils.facts import *

import json

import array

 

def find_disk_size():

    diskSize = 0

    with open("/tmp/disk_fact.json") as disk_fact_file:

      data = json.load(disk_fact_file)

      for p in data['guest_disk_facts']:

        diskSize += data['guest_disk_facts'][p]['capacity_in_kb']

    diskSizeToGB = diskSize/1024/1024

    return diskSizeToGB

 

def main():

    module = AnsibleModule(argument_spec={})

    ansible_vm_disk_size =  find_disk_size()

    module.exit_json(changed=False, size=ansible_vm_disk_size)

 

if __name__ == '__main__':

    main()
