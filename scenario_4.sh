#!/bin/bash

#export ANSIBLE_COW_SELECTION=elephant
export ANSIBLE_NOCOWS=1
ansible-playbook -i inventory/hosts.ini plays/oos_obj_put_get.yml
