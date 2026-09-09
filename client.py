NICE_TO_WEIGHT = {
    -5: 3121,
    0: 1024,
    5: 335,
    10: 110,
    19: 15
}

class CFSScheduler:
    """Linux Completely Fair Scheduler (CFS) Virtual Runtime Engine."""
    def __init__(self, latency_target_ms=20, min_granularity_ms=2):
        self.tasks = []
        self.latency_target = latency_target_ms
        self.min_granularity = min_granularity_ms

    def add_task(self, pid, nice=0):
        weight = NICE_TO_WEIGHT.get(nice, 1024)
        min_vruntime = min([t['vruntime'] for t in self.tasks], default=0.0)
        self.tasks.append({
            'pid': pid,
            'nice': nice,
            'weight': weight,
            'vruntime': min_vruntime,
            'exec_time': 0.0
        })

    def pick_next(self):
        if not self.tasks:
            return None
        self.tasks.sort(key=lambda t: t['vruntime'])
        return self.tasks[0]

    def run_slice(self, delta_exec_ms):
        curr = self.pick_next()
        if not curr:
            return None

        delta_vruntime = delta_exec_ms * (1024.0 / curr['weight'])
        curr['vruntime'] += delta_vruntime
        curr['exec_time'] += delta_exec_ms
        return {
            'pid': curr['pid'],
            'vruntime': round(curr['vruntime'], 2),
            'exec_time': round(curr['exec_time'], 2)
        }
