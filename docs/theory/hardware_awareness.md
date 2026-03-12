# Hardware Awareness

We model compute and memory costs using simple throughput and bandwidth equations:
- compute latency = FLOPs / peak throughput
- memory latency = bytes / bandwidth
- runtime = max(compute latency, memory latency)
