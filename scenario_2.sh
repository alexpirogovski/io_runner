#!/bin/bash

#export ANSIBLE_COW_SELECTION=elephant
export ANSIBLE_NOCOWS=1
ansible-playbook -i inventory/hosts.ini plays/items_with_attr.yml
