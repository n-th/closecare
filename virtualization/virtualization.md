# Namespace + ConfigMap

Pros

High isolation
Easy to develop (modular and reusable)
Easy to monitor from a resource perspective
Independent resource management that can be suited for different organizations
Independent scaling that can be suited for different metrics between each organization
Secure (namespace isolation)
Low latency (nodes can be independently created near to the organization region)

--

Cons

Hard to manager for multiple organization
Admin dependent
Hard to update

# Scaling through metrics
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