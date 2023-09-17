# Kubernetes job monitor

With Kubernetes cron jobs it's possible to execute (batch) jobs periodically. With a monitor dashboard it's
easy to see which jobs are running and if their latest status was "succeeded" or "failed".

The frontend is derived from the awesome Jenkins Build Monitor Plugin. The application uses kubectl inside

the container to retrieve the data from Kubernetes.
```sh
cat ~/.kube/config | base64 | tr -d '\n'
```

```sh
---
apiVersion: v1
kind: Secret
metadata:
  name: kubeconfig
type: Opaque
data:
  config: KUBECONFIG_ENCODED
```

```sh
kubectl apply -f MANIFESTS
```