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

    if 'SMTP_SERVER' in os.environ:
        SMTP_SERVER = os.environ['SMTP_SERVER']
    else:
        SMTP_SERVER = "smtp.digitastuces.com"

    if 'SMTP_PORT' in os.environ:
        SMTP_PORT = os.environ['SMTP_PORT']
    else:
        SMTP_PORT = 587

    if 'SMTP_USER' in os.environ:
        SMTP_USER = os.environ['SMTP_USER']
    else:
        SMTP_USER = "agnes.dupont@digitastuces.com"

    if 'SMTP_PASSWORD' in os.environ:
        SMTP_PASSWORD = os.environ['SMTP_PASSWORD']
    else:
        SMTP_PASSWORD = 'TO_BE_CHANGED_ON_SECRETS'

    if 'SMTP_SENDER' in os.environ:
        SMTP_SENDER = os.environ['SMTP_SENDER']
    else:
        SMTP_SENDER = 'no-reply@digitastuces.com'

    if 'SMTP_RECIPIENTS' in os.environ:
        SMTP_RECIPIENTS = os.environ['SMTP_RECIPIENTS']
    else:
        SMTP_RECIPIENTS = 'all@digitastuces.com'