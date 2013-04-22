#!/usr/bin/env python
# coding:utf-8

import os
try:
    import json
except ImportError:
    import simplejson as json
import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://localhost:8000', verbose=True, allow_none=True)

def record(info_dict):
    info_dict['ANSIBLE_DEVOPS_SPACE'] = os.environ.get('ANSIBLE_DEVOPS_SPACE')
    info_str = json.dumps(info_dict, True)
    proxy.echo(info_str)
    

class CallbackModule(object):

    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        if ignore_errors:
            return
        record({'stats': 'runner_on_failed', 'host':host, 'result':res})

    def runner_on_ok(self, host, res):
        record({'stats': 'runner_on_ok', 'host':host, 'result':res})

    def runner_on_error(self, host, msg):
        record({'stats': 'runner_on_error', 'host':host, 'message': msg})

    def runner_on_skipped(self, host, item=None):
        record({'stats': 'runner_on_skipped', 'host':host, 'item': item})

    def runner_on_unreachable(self, host, res):
        record({'stats': 'runner_on_unreachable', 'host':host, 'result':res})

    def runner_on_no_hosts(self):
        record({'stats': 'runner_on_no_hosts'})

    def runner_on_async_poll(self, host, res, jid, clock):
        record({'stats': 'runner_on_async_poll', 'host':host, 'result':res, 'jid': jid, 'clock': clock})

    def runner_on_async_ok(self, host, res, jid):
        record({'stats': 'runner_on_async_ok', 'host':host, 'result':res, 'jid': jid})

    def runner_on_async_failed(self, host, res, jid):
        record({'stats': 'runner_on_async_failed', 'host':host, 'result':res, 'jid': jid})

    def playbook_on_start(self):
        record({'stats': 'playbook_on_start'})

    def playbook_on_notify(self, host, handler):
        record({'stats': 'playbook_on_notify', 'host':host, 'handler': handler})

    def on_no_hosts_matched(self):
        record({'stats': 'on_no_hosts_matched'})

    def on_no_hosts_remaining(self):
        record({'stats': 'on_no_hosts_remaining'})

    def playbook_on_task_start(self, name, is_conditional):
        record({'stats': 'playbook_on_task_start', 'name': name, 'is_conditional': is_conditional})

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        record({'stats': 'playbook_on_vars_prompt', 'varname': varname, 'private': private, 'prompt':prompt, 'encrypt':encrypt, 'confirm':confirm, 'salt_size':salt_size, 'salt':salt, 'default': default})

    def playbook_on_setup(self):
        record({'stats': 'playbook_on_setup'})

    def playbook_on_import_for_host(self, host, imported_file):
        record({'stats': 'playbook_on_import_for_host', 'host':host, 'imported_file': imported_file})

    def playbook_on_not_import_for_host(self, host, missing_file):
        record({'stats': 'playbook_on_not_import_for_host', 'host':host, 'missing_file': missing_file})

    def playbook_on_play_start(self, pattern):
        record({'stats': 'playbook_on_play_start', 'pattern': pattern})

    def playbook_on_stats(self, stats):
        result = {}
        for host in stats.processed:
            result[host] = stats.summarize(host)
        record({'stats': 'playbook_on_stats', 'summary': result})
