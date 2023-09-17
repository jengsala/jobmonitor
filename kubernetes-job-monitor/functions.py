import datetime
import json
import math
import subprocess
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# import os
# cluster_name = os.environ['CLUSTER_NAME']

def get_jobs(namespace=None, selector=None):
    """
    Gets jobs from Kubernetes
    :param namespace: string
    :param selector: string
    :return: dict
    """
    jobs = {}

    command = ['get', 'jobs', '--sort-by', '.status.startTime']

    if namespace:
        command.append('--namespace')
        command.append(namespace)
    else:
        command.append('--all-namespaces')

    if selector:
        command.append('--selector')
        command.append(selector)

    data = kubectl(command, 'json', False)

    if data and 'items' in data:
        for item in data['items']:
            job_name = None

            # Determine job name from CronJob name, skip non CronJob jobs
            if 'ownerReferences' in item['metadata']:
                owner_reference = item['metadata']['ownerReferences'][0]
                if owner_reference['kind'] == 'CronJob':
                    job_name = owner_reference['name']

            if not job_name:
                continue

            if 'status' in item and 'startTime' in item['status']:
                start_timestamp = item['status']['startTime']
            else:
                # Skip because the job is created, but not started yet
                continue

            job_namespace = item['metadata']['namespace']
            if job_namespace not in jobs:
                jobs[job_namespace] = {}

            if job_name not in jobs[job_namespace]:
                jobs[job_namespace][job_name] = {}

            if ('execution' in jobs[job_namespace][job_name]
                    and not jobs[job_namespace][job_name]['execution']['active']):
                jobs[job_namespace][job_name]['prev_execution'] = jobs[job_namespace][job_name]['execution']

            if 'completionTime' in item['status'] and item['status']['completionTime']:
                end_timestamp = item['status']['completionTime']
            else:
                end_timestamp = None

            if 'succeeded' in item['status'] and item['status']['succeeded'] == 1:
                status = 'succeeded'
            elif 'failed' in item['status'] and item['status']['failed'] == 1:
                status = 'failed'
                try:
                    end_timestamp = item['status']['conditions'][0]['lastTransitionTime']
                except (TypeError, KeyError):
                    pass
            else:
                status = 'unknown'

            if 'active' in item['status'] and item['status']['active'] == 1:
                active = True
                status = 'running'
            else:
                active = False

            jobs[job_namespace][job_name]['execution'] = {
                'id': job_name,
                'job_name': '{} / {}'.format(job_namespace, job_name),
                'job_namespace': job_namespace,
                'start_timestamp': start_timestamp,
                'status': status,
                'active': active
            }
            if end_timestamp:
                jobs[job_namespace][job_name]['execution']['end_timestamp'] = end_timestamp

    return jobs


def get_job_view(execution, prev_execution, kubernetes_dashboard_url,cluster_name, smtp_server, smtp_port, smtp_user, smtp_password, smtp_sender, smtp_recipients):
    """
    Gets a job view from the specified execution and previous execution
    :param execution: dict
    :param prev_execution: dict
    :param kubernetes_dashboard_url: string
    :return: dict
    """

    current_time = datetime.datetime.utcnow()
    hash_code = abs(hash(execution['job_name'])) % (10 ** 8)
    estimated_duration = ''
    prev_time_elapsed_since = ''

    if execution and 'start_timestamp' in execution:
        start_time = datetime.datetime.strptime(execution['start_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        elapsed_seconds = int((current_time - start_time).total_seconds())
    else:
        elapsed_seconds = 0

    if prev_execution and 'start_timestamp' in prev_execution and 'end_timestamp' in prev_execution:
        prev_start_time = datetime.datetime.strptime(prev_execution['start_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        prev_end_time = datetime.datetime.strptime(prev_execution['end_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        prev_elapsed_seconds = int((prev_end_time - prev_start_time).total_seconds())
    else:
        prev_elapsed_seconds = 0

    if prev_execution:
        prev_build_name = prev_execution['id']

        if 'end_timestamp' in prev_execution:
            prev_end_time = datetime.datetime.strptime(prev_execution['end_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
            prev_time_elapsed_since = int((current_time - prev_end_time).total_seconds())

        estimated_duration = '{}s'.format(prev_elapsed_seconds)

        # prev_url = '{}/#!/cronjob/{}/{}?namespace={}'.format(kubernetes_dashboard_url,
        #                                                      prev_execution['job_namespace'],
        #                                                      prev_execution['id'],
        #                                                      prev_execution['job_namespace'])
        
        # prev_url = '{}/#!/cronjob/{}/{}?namespace={}'.format(kubernetes_dashboard_url,
        #                                                      prev_execution['job_namespace'],
        #                                                      prev_execution['id'],
        #                                                      prev_execution['job_namespace'])
        prev_url = '{}/dashboard/c/{}/explorer/batch.cronjob/{}/{}#jobs'.format(kubernetes_dashboard_url,cluster_name,prev_execution['job_namespace'],prev_execution['id'])
        # https://rancher.digitastuces.com/dashboard/c/local/explorer/batch.job?q=job-a
    else:
        prev_build_name = ''
        prev_url = ''

    prev_build_duration = estimated_duration
    progress = 0

    FAIL_STATUS=False
    _data = {}
    if execution['status'] == 'succeeded':
        status = 'successful'
    elif execution['status'] == 'failed':
        status = 'failing'
        FAIL_STATUS=True
        print("EXECUTION FAILED !")
        print(execution)

        _data = execution
        

        print(30*'-')
    elif execution['status'] == 'running':
        if prev_execution and prev_execution['status'] == 'failed':
            status = 'failing running'
            print("EXECUTION FAILING !")
            print(prev_execution)
            #job_data = prev_execution
            print(30*'=')
            # ENVOYER UNE ALERTE (MAIL | SLACK | SERVICE NOW)
        elif prev_execution and prev_execution['status'] == 'succeeded':
            status = 'successful running'
        else:
            status = 'unknown running'

        if prev_execution and (prev_execution['status'] == 'failed' or prev_execution['status'] == 'succeeded'):
            if prev_elapsed_seconds > 0:
                progress = int(math.floor((float(elapsed_seconds) / float(prev_elapsed_seconds)) * 100))

                if progress > 100:
                    progress = 100
            else:
                progress = 100
        else:
            progress = 100
    else:
        status = 'unknown'
    
    # url = '{}/#!/cronjob/{}/{}?namespace={}'.format(kubernetes_dashboard_url,
    #                                                 execution['job_namespace'],
    #                                                 execution['id'],
    #                                                 execution['job_namespace'])

    url = '{}/dashboard/c/{}/explorer/batch.cronjob/{}/{}#jobs'.format(kubernetes_dashboard_url,cluster_name,execution['job_namespace'],execution['id'])
    
    if FAIL_STATUS:
        _data['url'] = url

        subject = """CronJOb {} {} - {}""".format(_data['id'], str(_data['status']).upper(), _data['end_timestamp'])

        body=("""<span><h2>CronJOb {} <em style="color:red">{}</em> !</h2></span>
            <ul>
                <li>Namespace :  <strong>{}</strong></li>
                <li>Status    :  <strong>{}</strong></li>
                <li>Active    :  <strong>{}</strong></li>
                <li>Start     :  <strong>{}</strong></li>
                <li>End       :  <strong>{}</strong></li>
                <li>Cluster   :  <strong>{}</strong></li>
                <li>Dashboard : <em>{}</em>.</li>
            </ul>
            """.format(_data['id'],
                        str(_data['status']).upper(),
                        _data['job_namespace'],
                        _data['status'],
                        _data['active'],
                        _data['start_timestamp'],
                        _data['end_timestamp'],
                        cluster_name,
                        _data['url']))

        sendMailAlert(smtp_server=smtp_server, smtp_port=smtp_port,
                    email_address=smtp_user, email_password=smtp_password,
                    subject=subject, body=body,
                    sender=smtp_sender, recipients=smtp_recipients)

    job_view = {
        'name': execution['job_name'],
        'url': url,
        'status': status,
        'hashCode': hash_code,
        'progress': progress,
        'estimatedDuration': estimated_duration,
        'headline': '',
        'lastBuild': {
            "timeElapsedSince": str(prev_time_elapsed_since),
            "duration": prev_build_duration,
            "description": '',
            "name": prev_build_name,
            "url": prev_url,
        },
        'debug': {
            'elapsed_seconds': elapsed_seconds,
            'prev_elapsed_seconds': prev_elapsed_seconds,
        }
    }

    print(job_view)
    return job_view

def kubectl(command, output_format=None, print_output=True):
    """
    Executes kubectl commands with configured parameters
    :param command: list
    :param output_format: None Default human terminal output, but can also be json, yaml etc.
    :param print_output: bool
    :return: dict|bool
    """
    command.insert(0, 'kubectl')
    command.append('--kubeconfig=/etc/.kube/config')

    if output_format:
        command.append('--output={}'.format(output_format))

    result = exec_command(command, False, print_output)

    if result and output_format == 'json':
        if result['stdout']:
            return json.loads(result['stdout'])
        else:
            return False
    else:
        return result


def exec_command(command, shell=False, print_output=True):
    """
    Executes a command
    :param command: list
    :param shell: bool
    :param print_output: bool
    :return: False|dict
    """
    p = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate()

    # Decode byte string to string
    stdout = stdout.decode()
    stderr = stderr.decode()

    if print_output:
        # Write subprocess stdout to stdout
        sys.stdout.write(stdout)

        if stderr:
            # Write subprocess stderr to stderr
            sys.stderr.write("stderr:\n")
            sys.stderr.write(stderr)

    if p.returncode > 0:
        return False
    else:
        return {
            'stdout': stdout,
            'stderr': stderr,
            'returncode': p.returncode,
        }

{'id': 'job-g', 'job_name': 'namespace-k / job-g', 'job_namespace': 'namespace-k', 'start_timestamp': '2023-09-17T15:36:03Z', 'status': 'failed', 'active': False, 'end_timestamp': '2023-09-17T15:36:53Z'}


def sendMailAlert(smtp_server, smtp_port, email_address, email_password, subject, body, sender, recipients):
    try:        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipients
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.send_message(msg)
        
        print('Email sent successfully !')
    except Exception as x:
        print(x)