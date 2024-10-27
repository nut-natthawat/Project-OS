import random
from collections import deque

def first_come_first_serve(processes):
    processes = [proc.copy() for proc in processes]
    n = len(processes)
    processes.sort(key=lambda x: x['arrival_time'])
    waiting_time = [0] * n
    turnaround_time = [0] * n
    gantt_chart = []
    completed_time = 0

    for i in range(n):
        process = processes[i]
        if completed_time < process['arrival_time']:
            gantt_chart.append("Idle")
            completed_time = process['arrival_time']
        
        waiting_time[i] = max(0, completed_time - process['arrival_time'])
        turnaround_time[i] = waiting_time[i] + process['burst_time']
        completed_time += process['burst_time']
        gantt_chart.append(f"P{process['id']}")

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    print("\nFirst Come First Serve (FCFS) Scheduling")
    print(f"{'Process':<10}{'Arrival Time':<15}{'Burst Time':<15}{'Waiting Time':<15}{'Turnaround Time':<15}")
    for i, process in enumerate(processes):
        print(f"{process['id']:<10}{process['arrival_time']:<15}{process['burst_time']:<15}{waiting_time[i]:<15}{turnaround_time[i]:<15}")

    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print("\nGantt Chart:")
    print(" | ".join(gantt_chart))

def round_robin(processes, time_quantum):
    processes = [proc.copy() for proc in processes]
    n = len(processes)
    queue = deque(processes)
    completed_time = 0
    gantt_chart = []
    waiting_time = {proc['id']: 0 for proc in processes}
    turnaround_time = {proc['id']: 0 for proc in processes}
    original_burst_times = {proc['id']: proc['burst_time'] for proc in processes}
    
    while queue:
        process = queue.popleft()
        
        if completed_time < process['arrival_time']:
            gantt_chart.append("Idle")
            completed_time = process['arrival_time']
        
        actual_burst = min(time_quantum, process['burst_time'])
        gantt_chart.append(f"P{process['id']}")
        process['burst_time'] -= actual_burst
        completed_time += actual_burst

        if process['burst_time'] > 0:
            queue.append(process)
        else:
            turnaround_time[process['id']] = completed_time - process['arrival_time']
            waiting_time[process['id']] = turnaround_time[process['id']] - original_burst_times[process['id']]

    avg_waiting_time = sum(waiting_time.values()) / n
    avg_turnaround_time = sum(turnaround_time.values()) / n

    print("\nRound Robin (RR) Scheduling")
    print(f"{'Process':<10}{'Waiting Time':<15}{'Turnaround Time':<15}")
    for proc in processes:
        print(f"{proc['id']:<10}{waiting_time[proc['id']]:<15}{turnaround_time[proc['id']]:<15}")

    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print("\nGantt Chart:")
    print(" | ".join(gantt_chart))

def shortest_job_first(processes):
    processes = [proc.copy() for proc in processes]
    n = len(processes)
    processes.sort(key=lambda x: x['arrival_time'])
    waiting_time = [0] * n
    turnaround_time = [0] * n
    gantt_chart = []
    completed_time = 0
    completed_processes = []

    while len(completed_processes) < n:
        arrived_processes = [p for p in processes if p['arrival_time'] <= completed_time and p not in completed_processes]
        
        if not arrived_processes:
            gantt_chart.append("Idle")
            completed_time += 1
            continue

        arrived_processes.sort(key=lambda x: (x['burst_time'], x['arrival_time']))
        current_process = arrived_processes[0]

        completed_processes.append(current_process)

        index = current_process['id'] - 1
        waiting_time[index] = max(0, completed_time - current_process['arrival_time'])
        turnaround_time[index] = waiting_time[index] + current_process['burst_time']

        completed_time += current_process['burst_time']
        gantt_chart.append(f"P{current_process['id']}")

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    print("\nShortest Job First (SJF) Scheduling")
    print(f"{'Process':<10}{'Arrival Time':<15}{'Burst Time':<15}{'Waiting Time':<15}{'Turnaround Time':<15}")
    for process in processes:
        index = process['id'] - 1
        print(f"{process['id']:<10}{process['arrival_time']:<15}{process['burst_time']:<15}{waiting_time[index]:<15}{turnaround_time[index]:<15}")

    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print("\nGantt Chart:")
    print(" | ".join(gantt_chart))


def shortest_remaining_job_first(processes):
    n = len(processes)
    remaining_times = [proc['burst_time'] for proc in processes]
    complete = 0
    time = 0
    min_time = float('inf')
    shortest = 0
    check = False
    waiting_time = [0] * n
    turnaround_time = [0] * n
    gantt_chart = []

    while complete != n:
        for i in range(n):
            if (processes[i]['arrival_time'] <= time and
                remaining_times[i] < min_time and
                remaining_times[i] > 0):
                min_time = remaining_times[i]
                shortest = i
                check = True

        if not check:
            time += 1
            gantt_chart.append("Idle")
            continue

        gantt_chart.append(f"P{processes[shortest]['id']}")
        remaining_times[shortest] -= 1
        min_time = remaining_times[shortest]
        if min_time == 0:
            min_time = float('inf')

        if remaining_times[shortest] == 0:
            complete += 1
            check = False
            finish_time = time + 1
            waiting_time[shortest] = (finish_time - processes[shortest]['burst_time'] - 
                                      processes[shortest]['arrival_time'])
            if waiting_time[shortest] < 0:
                waiting_time[shortest] = 0
            turnaround_time[shortest] = finish_time - processes[shortest]['arrival_time']

        time += 1

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    print("\nShortest Remaining Job First (SRJF) Scheduling")
    print(f"{'Process':<10}{'Arrival Time':<15}{'Burst Time':<15}{'Waiting Time':<15}{'Turnaround Time':<15}")
    for i in range(n):
        print(f"{processes[i]['id']:<10}{processes[i]['arrival_time']:<15}{processes[i]['burst_time']:<15}{waiting_time[i]:<15}{turnaround_time[i]:<15}")

    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print("\nGantt Chart:")
    print(" | ".join(gantt_chart))


def priority_scheduling(processes):
    processes = [proc.copy() for proc in processes]
    n = len(processes)
    processes.sort(key=lambda x: (x['arrival_time'], x['priority']))
    waiting_time = [0] * n
    turnaround_time = [0] * n
    gantt_chart = []
    completed_time = 0
    completed_processes = []

    while len(completed_processes) < n:
        arrived_processes = [p for p in processes if p['arrival_time'] <= completed_time and p not in completed_processes]
        
        if not arrived_processes:
            gantt_chart.append("Idle")
            completed_time += 1
            continue

        arrived_processes.sort(key=lambda x: (x['priority'], x['arrival_time']))
        current_process = arrived_processes[0]

        completed_processes.append(current_process)

        index = current_process['id'] - 1
        waiting_time[index] = max(0, completed_time - current_process['arrival_time'])
        turnaround_time[index] = waiting_time[index] + current_process['burst_time']

        completed_time += current_process['burst_time']
        gantt_chart.append(f"P{current_process['id']}")

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    print("\nPriority Scheduling")
    print(f"{'Process':<10}{'Arrival Time':<15}{'Burst Time':<15}{'Priority':<10}{'Waiting Time':<15}{'Turnaround Time':<15}")
    for process in processes:
        index = process['id'] - 1
        print(f"{process['id']:<10}{process['arrival_time']:<15}{process['burst_time']:<15}{process['priority']:<10}{waiting_time[index]:<15}{turnaround_time[index]:<15}")

    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print("\nGantt Chart:")
    print(" | ".join(gantt_chart))


def highest_response_ratio_next(processes):
    n = len(processes)
    time = 0
    completed = 0
    waiting_time = [0] * n
    turnaround_time = [0] * n
    gantt_chart = []
    is_completed = [False] * n

    while completed != n:
        highest_response_ratio = -1
        index = -1

        for i in range(n):
            if (processes[i]['arrival_time'] <= time) and not is_completed[i]:
                response_ratio = ((time - processes[i]['arrival_time']) + processes[i]['burst_time']) / processes[i]['burst_time']
                if response_ratio > highest_response_ratio:
                    highest_response_ratio = response_ratio
                    index = i

        if index == -1:
            gantt_chart.append("Idle")
            time += 1
            continue

        gantt_chart.append(f"P{processes[index]['id']}")
        time += processes[index]['burst_time']
        waiting_time[index] = time - processes[index]['arrival_time'] - processes[index]['burst_time']
        if waiting_time[index] < 0:
            waiting_time[index] = 0
        turnaround_time[index] = waiting_time[index] + processes[index]['burst_time']
        is_completed[index] = True
        completed += 1

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    print("\nHighest Response Ratio Next (HRRN) Scheduling")
    print(f"{'Process':<10}{'Arrival Time':<15}{'Burst Time':<15}{'Waiting Time':<15}{'Turnaround Time':<15}")
    for i, process in enumerate(processes):
        print(f"{process['id']:<10}{process['arrival_time']:<15}{process['burst_time']:<15}{waiting_time[i]:<15}{turnaround_time[i]:<15}")

    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print("\nGantt Chart:")
    print(" | ".join(gantt_chart))


def multilevel_queue_feedback(processes):
    queues = [deque(), deque(), deque()]
    time_quantum = [4, 8, float('inf')] 
    time = 0
    gantt_chart = []
    waiting_time = {proc['id']: 0 for proc in processes}
    turnaround_time = {proc['id']: 0 for proc in processes}
    original_burst_times = {proc['id']: proc['burst_time'] for proc in processes}
    
    processes.sort(key=lambda x: x['arrival_time'])
    i = 0
    while i < len(processes) and processes[i]['arrival_time'] <= time:
        queues[0].append(processes[i])
        i += 1

    while any(queue for queue in queues) or i < len(processes):
        executed = False
        
        for level in range(len(queues)):
            if queues[level]:
                process = queues[level].popleft()
                actual_burst = min(time_quantum[level], process['burst_time'])
                gantt_chart.append(f"P{process['id']}")
                
                time += actual_burst
                process['burst_time'] -= actual_burst
                executed = True
                
                while i < len(processes) and processes[i]['arrival_time'] <= time:
                    queues[0].append(processes[i])
                    i += 1

                if process['burst_time'] > 0:
                    next_level = min(level + 1, len(queues) - 1)
                    queues[next_level].append(process)
                else:
                    turnaround_time[process['id']] = time - process['arrival_time']
                    waiting_time[process['id']] = turnaround_time[process['id']] - original_burst_times[process['id']]
                break
        
        if not executed:
            gantt_chart.append("Idle")
            time += 1

            while i < len(processes) and processes[i]['arrival_time'] <= time:
                queues[0].append(processes[i])
                i += 1

    avg_waiting_time = sum(waiting_time.values()) / len(processes)
    avg_turnaround_time = sum(turnaround_time.values()) / len(processes)

    print("\nMultilevel Queue with Feedback Scheduling")
    print(f"{'Process':<10}{'Waiting Time':<15}{'Turnaround Time':<15}")
    for proc in processes:
        print(f"{proc['id']:<10}{waiting_time[proc['id']]:<15}{turnaround_time[proc['id']]:<15}")

    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print("\nGantt Chart:")
    print(" | ".join(gantt_chart))
    
def get_random_time_quantum(processes):
    average_burst_time = sum(proc['burst_time'] for proc in processes) / len(processes)
    time_quantum = random.randint(max(1, int(average_burst_time / 3)), int(average_burst_time / 2))
    print(f"Randomly chosen time quantum for Round Robin: {time_quantum}")
    return time_quantum

def get_user_input():
    num_processes = int(input("Enter the number of processes: "))
    choice = input("Do you want to enter processes manually? (y/n): ").lower()

    processes = []

    if choice == 'y':
        for i in range(num_processes):
            arrival_time = int(input(f"Enter arrival time for Process {i + 1}: "))
            burst_time = int(input(f"Enter burst time for Process {i + 1}: "))
            priority = int(input(f"Enter priority for Process {i + 1} (1 is highest priority): "))
            processes.append({
                'id': i + 1,
                'arrival_time': arrival_time,
                'burst_time': burst_time,
                'priority': priority
            })
    else:
        for i in range(num_processes):
            arrival_time = random.randint(0, 10)  
            burst_time = random.randint(1, 10)   
            priority = random.randint(1, 5)      
            processes.append({
                'id': i + 1,
                'arrival_time': arrival_time,
                'burst_time': burst_time,
                'priority': priority
            })

    print("\nGenerated Processes:")
    for proc in processes:
        print(f"Process {proc['id']}: Arrival Time = {proc['arrival_time']}, Burst Time = {proc['burst_time']}, Priority = {proc['priority']}")

    return processes

def main():
    processes = get_user_input()
    time_quantum = get_random_time_quantum(processes)
    
    print("\n=== Comparing SRJF, Priority, HRRN, and Multilevel Queue with Feedback Scheduling ===")
    print("_______________________________________________________________________________________")
    print("\nRunning First Come First Serve (FCFS) Scheduling...")
    first_come_first_serve(processes[:])
    print("_______________________________________________________________________________________")
    print("\nRunning Round Robin (RR) Scheduling...")
    round_robin(processes[:], time_quantum)
    print("_______________________________________________________________________________________")
    print("\nRunning Shortest Job First (SJF) Scheduling...")
    shortest_job_first(processes[:])
    print("_______________________________________________________________________________________")
    print("\nRunning SRJF Scheduling...")
    shortest_remaining_job_first(processes[:])
    print("_______________________________________________________________________________________")
    print("\nRunning Priority Scheduling...")
    priority_scheduling(processes[:])
    print("_______________________________________________________________________________________")
    print("\nRunning HRRN Scheduling...")
    highest_response_ratio_next(processes[:])
    print("_______________________________________________________________________________________")
    print("\nRunning Multilevel Queue with Feedback Scheduling...")
    multilevel_queue_feedback(processes[:])


main()
