#!/usr/bin/env python

from __future__ import print_function
import atexit
import argparse
import getpass
import re

from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim

from ansible.module_utils.basic import *
from ansible.module_utils.facts import *

vcenters=["vcenter1", "vcenter2", "vcenter2"]

def find_datacenter(virtual_machine):
     #from vm object to datacenter 
     datacenter = virtual_machine.runtime.host.parent.parent.parent.name
     return datacenter

def vm_info_for_ansible(virtual_machine, user, password):
    try:
        for vcenter in vcenters:
            #connection to vcenter
            service_instance = connect.SmartConnectNoSSL(host=vcenter,
                                                         user=user,
                                                         pwd=password)
              
            atexit.register(connect.Disconnect, service_instance)
            content = service_instance.RetrieveContent()
            container = content.rootFolder  # starting point to look into
            viewType = [vim.VirtualMachine]  # object types to look for
            recursive = True  # whether we should look into it recursively
            containerView = content.viewManager.CreateContainerView(
               container, viewType, recursive)
            children = containerView.view
            pat = re.compile(virtual_machine, re.IGNORECASE)
            for child in children:
                if pat.search(child.summary.config.name) is not None:
                   datacenter = find_datacenter(child)
                   return datacenter, vcenter

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

def main():
    fields = {
    "vmname": {"required": True, "type": "str"},
    "username": {"required": True,  "type": "str"},
    "password": {"required": True,  "type": "str", "no_log": True}
    }

    module = AnsibleModule(argument_spec=fields)
    datacenter, vcenter = vm_info_for_ansible(module.params['vmname'], module.params['username'], module.params['password'])
    module.exit_json(changed=False, vm_datacenter=datacenter, vm_vcenter=vcenter)

# Start program
if __name__ == "__main__":
    main()
