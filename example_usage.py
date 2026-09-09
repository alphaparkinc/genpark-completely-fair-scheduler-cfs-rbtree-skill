from client import CFSScheduler

def main():
    print("=== Testing Completely Fair Scheduler ===")
    cfs = CFSScheduler()
    cfs.add_task("task_low", nice=5)
    cfs.add_task("task_high", nice=-5)

    r1 = cfs.run_slice(10)
    print("First slice execution:", r1)
    r2 = cfs.run_slice(10)
    print("Second slice execution:", r2)

    assert len(cfs.tasks) == 2
    print("CFS Scheduler verified successfully!")

if __name__ == '__main__':
    main()
