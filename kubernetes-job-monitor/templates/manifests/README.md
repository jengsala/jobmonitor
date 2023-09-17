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