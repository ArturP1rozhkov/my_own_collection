#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Create a text file on the remote host from path whis data from content


version_added: "1.0.0"

description: - Creates a text file on the remote host.
             - The file path in C(path), and data from C(content).
             - Supports check mode.

options:
    path:
        description:
            - Absolute path to the file
        required: true
        type: str
    content:
        description:
            - Text content to write into the file.
        required: true
        type: str

extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Artur
notes:
    - Supports check_mode.
'''

EXAMPLES = r'''
- name: Create file with content
  my_own_module:
    path: /tmp/test.txt
    content: "hello! Iam your custom module"

'''

RETURN = r'''
path:
    description: Path to the file.
    type: str
    returned: always
    sample: /tmp/test.txt
content:
    description: Content written to the file.
    type: str
    returned: always
    sample: hello! Iam your custom module
message:
    description: Module execution message.
    type: str
    returned: always
    sample: File created successfully
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        path='',
        content='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    result['path'] = path
    result['content'] = content

    current_content = None
    file_exists = os.path.exists(path)

    if file_exists:
        try:
            with open(path, 'r') as f:
                current_content = f.read()
        except Exception as e:
            module.fail_json(msg=f'Failed to read existing file: {e}', **result)

    if (not file_exists) or (current_content != content):
        result['changed'] = True

        if module.check_mode:
            result['message'] = 'File would be created or updated'
            module.exit_json(**result)

        try:
            with open(path, 'w') as f:
                f.write(content)
        except Exception as e:
            module.fail_json(msg=f'Failed to write file: {e}', **result)

        if file_exists:
            result['message'] = 'File updated successfully'
        else:
            result['message'] = 'File created successfully'
    else:
        result['message'] = 'File already exists with the desired content'

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()