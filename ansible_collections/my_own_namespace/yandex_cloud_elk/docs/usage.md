# Usage

## Local run

export ANSIBLE_COLLECTIONS_PATH=~/my_own_collection
ansible-playbook my_own_namespace.yandex_cloud_elk.test_role

## What it does
Role `my_own_role` calls custom module `my_own_namespace.yandex_cloud_elk.my_own_module` and creates a file with content from role defaults.

## Idempotency
Repeated run returns `ok` and `changed=0`.