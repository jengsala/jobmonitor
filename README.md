## Docker

```sh
cd kubernetes-job-monitor

docker build -t digitastuces/jobmonitor:1.0 .
docker push digitastuces/jobmonitor:1.0
```

> Utiliser l'image buildé dans le chart jobmonitor


```sh
image:
  repository: digitastuces/jobmonitor
  pullPolicy: Always
  tag: "1.0"
```

## SOPS

```sh
sops -e secrets.yaml > config-enc.yaml
```

## Helm / Helmfile

```yaml
releases:
- name: "jobmonitor"
  chart: ./jobmonitor
....
  secrets:
  - ./config-enc.yaml
```

- Déploiement 

```sh
cd jobmonitor

helmfile -n jobmonitor apply
```

## Exemples de CronJobs


```sh
kubectl apply -f ./cronjobs
```

[Monitor](https://monitor.digitastuces.com/)

## Kubernetes


```sh
kubectl -n jobmonitor get po,deploy,svc
NAME                                          READY   STATUS    RESTARTS   AGE
pod/kubernetes-job-monitor-56c56649c4-fxnkk   1/1     Running   0          32s

NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kubernetes-job-monitor   1/1     1            1           33s

NAME                             TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
service/kubernetes-job-monitor   ClusterIP   10.3.217.89   <none>        80/TCP    34s
```

## Logs

```sh
kubectl -n jobmonitor logs -f pod/kubernetes-job-monitor-56c56649c4-fxnkk 
```

- Sortie logs

```sh
k -n jobmonitor logs -f pod/kubernetes-job-monitor-56c56649c4-fxnkk
2023-09-17 18:18:43,538 INFO Set uid to user 0 succeeded
2023-09-17 18:18:43,544 INFO RPC interface 'supervisor' initialized
2023-09-17 18:18:43,544 INFO supervisord started with pid 1
2023-09-17 18:18:44,547 INFO spawned: 'gunicorn' with pid 7
2023-09-17 18:18:44,549 INFO spawned: 'nginx' with pid 8
2023/09/17 18:18:44 [notice] 8#8: using the "epoll" event method
2023/09/17 18:18:44 [notice] 8#8: nginx/1.25.2
2023/09/17 18:18:44 [notice] 8#8: built by gcc 12.2.1 20220924 (Alpine 12.2.1_git20220924-r10) 
2023/09/17 18:18:44 [notice] 8#8: OS: Linux 5.15.0-82-generic
2023/09/17 18:18:44 [notice] 8#8: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2023/09/17 18:18:44 [notice] 8#8: start worker processes
2023/09/17 18:18:44 [notice] 8#8: start worker process 9
2023/09/17 18:18:44 [notice] 8#8: start worker process 10
2023-09-17 18:18:45,645 INFO success: gunicorn entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
2023-09-17 18:18:45,645 INFO success: nginx entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
[2023-09-17 18:18:46 +0000] [7] [INFO] Starting gunicorn 21.2.0
[2023-09-17 18:18:46 +0000] [7] [INFO] Listening at: http://127.0.0.1:8000 (7)
[2023-09-17 18:18:46 +0000] [7] [INFO] Using worker: sync
[2023-09-17 18:18:46 +0000] [11] [INFO] Booting worker with pid: 11
...
51.79.31.60 - - [17/Sep/2023:18:21:19 +0000] "GET / HTTP/1.1" 200 10743 "-" "kube-probe/1.26"
10.2.9.15 - - [17/Sep/2023:18:21:28 +0000] "GET / HTTP/1.1" 200 10743 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
....
10.2.9.15 - - [17/Sep/2023:18:21:29 +0000] "GET /static/themes/kubernetes/Roboto-Regular.woff2 HTTP/1.1" 200 64184 "https://monitor.digitastuces.com/static/themes/kubernetes.css" "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
.....
{'name': 'namespace-a / job-d', 'url': 'https://rancher.digitastuces.com/dashboard/c/local/explorer/batch.cronjob/namespace-a/job-d#jobs', 'status': 'successful running', 'hashCode': 68459899, 'progress': 100, 'estimatedDuration': '31s', 'headline': '', 'lastBuild': {'timeElapsedSince': '63', 'duration': '31s', 'description': '', 'name': 'job-d', 'url': 'https://rancher.digitastuces.com/dashboard/c/local/explorer/batch.cronjob/namespace-a/job-d#jobs'}, 'debug': {'elapsed_seconds': 33, 'prev_elapsed_seconds': 31}}
{'name': 'namespace-a / job-f', 'url': 'https://rancher.digitastuces.com/dashboard/c/local/explorer/batch.cronjob/namespace-a/job-f#jobs', 'status': 'successful running', 'hashCode': 57603286, 'progress': 68, 'estimatedDuration': '48s', 'headline': '', 'lastBuild': {'timeElapsedSince': '46', 'duration': '48s', 'description': '', 'name': 'job-f', 'url': 'https://rancher.digitastuces.com/dashboard/c/local/explorer/batch.cronjob/namespace-a/job-f#jobs'}, 'debug': {'elapsed_seconds': 33, 'prev_elapsed_seconds': 48}}
EXECUTION FAILING !
{'id': 'job-g', 'job_name': 'namespace-a / job-g', 'job_namespace': 'namespace-a', 'start_timestamp': '2023-09-17T18:20:02Z', 'status': 'failed', 'active': False, 'end_timestamp': '2023-09-17T18:20:39Z'}
```
