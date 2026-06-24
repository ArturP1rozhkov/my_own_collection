# Ansible Collection - my_own_namespace.yandex_cloud_elk

# yandex_cloud_elk

Test Ansible collection whis:
- custom module `my_own_module`
- role `my_own_role`
- playbook `test_role`

## Structure
- `plugins/modules/my_own_module.py` — custom module
- `roles/my_own_role` — role, used module
- `playbooks/test_role.yml` — playbook for local start

## Run

export ANSIBLE_COLLECTIONS_PATH=~/my_own_collection
ansible-playbook my_own_namespace.yandex_cloud_elk.test_role

## Result

On the first run, a file is created, on the second run, the playbook returns `changed=0`, which confirms idempotency.