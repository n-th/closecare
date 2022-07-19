```
eksctl create cluster --name cool-cluster --region us-east-1 --ssh-access --ssh-public-key ./ssh.pub --managed 
```

# Namespace + ConfigMap

Pros

- High isolation
- Easy to develop (modular and reusable)
- Easy to monitor from a resource perspective
- Independent resource management that can be suited for different organizations
- Independent scaling that can be suited for different metrics between each organization
- Secure (namespace isolation)
- Low latency (nodes can be independently created near to the organization region)
- Allow single db or multiple dbs usage (one in a single namespace or one in each namespace)

Cons

- Admin dependent for onboarding and management
- Hard to manage SSL

# Scaling through metrics

https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/

```
- type: External
  external:
    metric:
      name: queue_messages_ready
      selector:
        matchLabels:
          queue: "worker_tasks"
    target:
      type: AverageValue
      averageValue: 30
```

## Security

https://kubernetes.io/docs/concepts/security/pod-security-standards

```
apiVersion: v1
kind: Namespace
metadata:
  name: my-baseline-namespace
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/enforce-version: v1.24
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: v1.24
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: v1.24
```


Profile	Descriptions:
Privileged:	Unrestricted policy, providing the widest possible level of permissions. This policy allows for known privilege escalations.
Baseline:	Minimally restrictive policy which prevents known privilege escalations. Allows the default (minimally specified) Pod configuration.
Restricted:	Heavily restricted policy, following current Pod hardening best practices.



## Ingress


apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wildcard-host
  namespace: ingress  # needs a way to get services from multiple namespaces
spec:
  rules:
  - host: n-th.me
    https:
      paths:
      - path: /org_1
        pathType: Prefix
        backend:
          service:
            name: flask-service
            port:
              number: 5000
      - path: /org_2
        pathType: Prefix
        backend:
          service:
            name: flask-service
            port:
              number: 5001