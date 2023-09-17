import os


class Configuration(object):

    if 'KUBERNETES_DASHBOARD_URL' in os.environ:
        KUBERNETES_DASHBOARD_URL = os.environ['KUBERNETES_DASHBOARD_URL']
    else:
        KUBERNETES_DASHBOARD_URL = 'http://my-kubernetes-cluster.local'

    if 'CLUSTER_NAME' in os.environ:
        CLUSTER_NAME = os.environ['CLUSTER_NAME']
    else:
        CLUSTER_NAME = 'myclustername'

