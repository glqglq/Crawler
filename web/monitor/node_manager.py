# -*- coding: utf-8 -*-

import docker

class MyDocker(object):
    def __init__(self):
        self.client = docker.from_env(version = '1.27')
        self.containers = []
    def start_new_node(self):
        try:
            new_container = self.client.containers.run(image = "spider:6",detach=True,stdin_open = True,name = 'spider_%02d'%(len(self.client.containers.list()) + 1),tty = True)
            if new_container.status == 'created':
                return True
            else:
                new_container.remove(force = True)
                return False
        except:
            return False

    def delete_node(self,id):
        container_to_delete = self.client.containers.get(id)
        try:
            container_to_delete.stop(timeout = 1)
        except:
            pass
        container_to_delete.remove(force = True)

    def get_status(self):
        status = []
        for container in  self.client.containers.list():
            status_dict = {}
            status_dict['id'] = container.short_id
            status_dict['name'] = container.name
            if container.status == 'running':
                status_dict['status'] = 1
            else:
                status_dict['status'] = 0
            status += [status_dict]
        return status

if __name__ == '__main__':
    d = MyDocker()
    d.start_new_node()