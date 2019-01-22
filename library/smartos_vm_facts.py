#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Thomas Merkel <tm@core.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: smartos_vm_facts
short_description: Get SmartOS vm details.
description:
    - Retrieve facts about all installed zones on SmartOS. Facts will be
      inserted to the ansible_facts key.
version_added: "1.0"
author: Thomas Merkel (@drscream)
options:
    filters:
        description:
            - Criteria for selecting zone can be anything provided in an zone
              manifest. More informaton can be found at U(https://smartos.org/man/1m/vmadm)
              under 'vmadm lookup'.
'''

EXAMPLES = '''
# Return facts about all installed vms.
- smartos_vm_facts:

# Return all private active Linux vms.
- smartos_vm_facts: filters="os=linux state=active public=false"

# Show, how many clones does every vm have.
- smartos_vm_facts:

- debug: msg="{{ smartos_vms[item]['name'] }}-{{smartos_vms[item]['version'] }}
            has {{ smartos_vms[item]['clones'] }} VM(s)"
  with_items: "{{ smartos_vms.keys() }}"
'''

RETURN = '''
# this module returns ansible_facts
'''

import json
from ansible.module_utils.basic import AnsibleModule


class VmFacts(object):

    def __init__(self, module):
        self.module = module

        self.filters = module.params['filters']

    def return_all_installed_vms(self):
        cmd = [self.module.get_bin_path('vmadm')]

        cmd.append('lookup')
        cmd.append('-j')

        if self.filters:
            cmd.append(self.filters)

        (rc, out, err) = self.module.run_command(cmd)

        if rc != 0:
            self.module.exit_json(
                msg='Failed to get all installed vms', stderr=err)

        vms = json.loads(out)

        result = {}
        for vm in vms:
            result[vm['uuid']] = vm

        return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            filters=dict(default=None),
        ),
        supports_check_mode=False,
    )

    vm_facts = VmFacts(module)

    data = dict(smartos_vms=vm_facts.return_all_installed_vms())

    module.exit_json(ansible_facts=data)


if __name__ == '__main__':
    main()
