DASHBOARD= "https://rancher.digitastuces.com/"
CLUSTER_NAME= "local"
NAMESPACE= "namespace-a"
JOB_NAME = "job-a"

prev_url = '{}/dashboard/c/{}/explorer/batch.cronjob/{}/{}#jobs'.format(DASHBOARD,CLUSTER_NAME,NAMESPACE,JOB_NAME)

# https://rancher.digitastuces.com/dashboard/c/local/explorer/batch.job?q=job-a
# https://rancher.digitastuces.com/dashboard/c/local/explorer/batch.cronjob/namespace-a/job-a#jobs

print(prev_url)