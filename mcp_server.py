import sys
import json
from client import CFSScheduler

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "schedule":
        cfs = CFSScheduler()
        for t in params.get("tasks", []):
            cfs.add_task(t.get("pid"), t.get("nice", 0))
        res = []
        for _ in range(params.get("slices", 5)):
            res.append(cfs.run_slice(10))
        return {"runs": res}
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
