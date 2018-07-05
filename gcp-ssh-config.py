#!/usr/bin/env python
import os
from os.path import expanduser
from shutil import copyfile

import googleapiclient.discovery
from google.cloud import resource_manager


def hosts():
    gcp_hosts = []
    compute = googleapiclient.discovery.build('compute', 'v1')
    client = resource_manager.Client()
    for project in client.list_projects():
        try:
            regions = compute.regions().list(project=project.project_id).execute()
            for region in regions['items']:
                use_region = False
                for quota in region['quotas']:
                    if quota['usage'] != 0.0:
                        use_region = True

                if use_region:
                    zones = [zone.split('/')[-1] for zone in region['zones']]
                    for zone in zones:
                        result = compute.instances().list(project=project.project_id, zone=zone).execute()
                        if 'items' in result and result['items']:
                            for item in result['items']:
                                gcp_hosts.append("Host %s.c.%s.internal" % (item['name'], project.project_id))
        except googleapiclient.http.HttpError:
            # ignore
            continue
    return gcp_hosts


def main():
    open_tag = "### GCP hosts (DO NOT REMOVE)\n"
    close_tag = "### GCP hosts end (DO NOT REMOVE)\n"
    hosts_tag = hosts()

    # copy file to location where we can work on it
    copyfile('%s/.ssh/config' % expanduser("~"), '%s/.ssh/config.gcp.tmp' % expanduser("~"))

    opened = False
    with open('%s/.ssh/config' % expanduser("~"), 'r') as f:
        lines = f.readlines()
        if open_tag in lines and close_tag in lines:
            # remove current
            with open('%s/.ssh/config.gcp.tmp' % expanduser("~"), 'w') as output:
                for line in lines:
                    if line == open_tag:
                        opened = True
                    if line == close_tag:
                        opened = False

                    if not opened and line != close_tag:
                        output.write(line)

        # append
        with open('%s/.ssh/config.gcp.tmp' % expanduser("~"), 'a') as output:
            output.write(open_tag)
            for host in hosts_tag:
                output.write(host + "\n")
            output.write(close_tag)

    # copy working file back to correct place
    copyfile('%s/.ssh/config.gcp.tmp' % expanduser("~"), '%s/.ssh/config' % expanduser("~"))
    os.unlink('%s/.ssh/config.gcp.tmp' % expanduser("~"))


if __name__ == '__main__':
    main()
