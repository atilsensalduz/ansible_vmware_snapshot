# vmware_snapshot_playbook

this playbook for take,get and delete snapshot in the vcenter   
Playbook has two custom module fist one is a find datacenter and vcenter name via ansible_hostname variable and second one is find vm disk size as GB for doesn't take snapshot which vm has huge disk size(10TB).
