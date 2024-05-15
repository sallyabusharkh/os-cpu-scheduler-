
class Process:
    def __init__(self, ID, arr_time, burst):
        self.ID = ID
        self.arr_time = arr_time
        self.burst = burst
        self.size = 0
        self.time_left = 0
        self.info = Info()

class Info:
    def __init__(self):
        self.wt = 0  # waiting time
        self.Ta_time = 0  # turnaround time
        self.f_time = 0  # finish time

total_wt = 0
total_Ta_time = 0
total_burst = 0
process = [Process(0, 0, 0) for _ in range(5)]
nr_proc = 5
q, cs = 0, 0
cpu_utilization = 0.0
currentTime = 0

def read_file():
    global q, cs, process
    path = "C:\\Users\\Sally\\os\\input.txt"
    try:
        with open(path, 'r') as myfile:
            data = myfile.readlines()
            if len(data) < 1:
                print("File is empty!")
                exit(EXIT_FAILURE)
            q, cs = map(int, data[0].split())
            process = [Process(*map(int, line.split())) for line in data[1:]]
    except FileNotFoundError:
        print("File Not Exist!")
        exit(1)


def sort():
    swapped = True
    while swapped:
        swapped = False
        for i in range(nr_proc - 1):
            if process[i].arr_time > process[i + 1].arr_time:
                process[i], process[i + 1] = process[i + 1], process[i]
                swapped = True

def gantt_chart():
    global currentTime
    print("\n--------------------------------------")
    print("Gantt Chart")
    print("--------------------------------------")
    for p in process:
        print(f"({currentTime})|==P{p.ID}==|", end='')
        currentTime += p.burst + cs
    currentTime -= cs
    print(f"({currentTime})")

def get_info():
    global total_wt, total_Ta_time, total_burst, cpu_utilization
    gantt_chart()
    total_burst = 0
    process[0].info.f_time = process[0].burst
    process[0].info.wt = 0
    process[0].info.Ta_time = process[0].info.f_time - process[0].arr_time

    for i in range(1, nr_proc):
        total_burst += process[i - 1].burst
        process[i].info.f_time = process[i - 1].info.f_time + cs + process[i].burst
        process[i].info.wt = process[i - 1].info.f_time + cs - process[i].arr_time
        process[i].info.Ta_time = process[i].info.f_time - process[i].arr_time

    process[4].info.f_time -= cs
    for p in process:
        total_wt += p.info.wt
        total_Ta_time += p.info.Ta_time
    total_burst += process[nr_proc - 1].burst
    cpu_utilization = total_burst * 100.0 / currentTime

    print("\n\n-----------------------------------------------------")
    print("Process\t|TurnAround Time|Waiting Time\t|Finish Time")
    print("--------+---------------+-------------+--------------")
    
    for p in process:
        print(f"P({p.ID})\t|\t{p.info.Ta_time}\t|\t{p.info.wt}\t|\t{p.info.f_time}")
    print("----------------------------------------------------\n")
    print(f"Average Wating Time: ={total_wt / 5.0}")
    print(f"Average Turnaround Time: ={total_Ta_time / 5.0}")
    print(f"Cpu Utilization {cpu_utilization} %")
    return

def FCFS():
    print("\n--------------------------------------")
    print("1//First Come First Served")
    print("--------------------------------------")
    sort()  
    get_info()  
    print("--------------------------------------")
    print("First Come First Served Scheduling complete")

def SJF():
    print("\n--------------------------------------")
    print("2//Shortest-Job-First Scheduling (nonpreemptive)")
    sort()
    check = 0
    for i in range(nr_proc - 1):
        check += process[i].burst
        for k in range(i + 1, nr_proc - 1):
            if check >= process[k + 1].arr_time and process[k].burst > process[k + 1].burst:
                process[k], process[k + 1] = process[k + 1], process[k]
    get_info()
    print("----------------------------------------------------")

    print("Shortest-Job-First Scheduling complete")

def RR():
    sort()
    print("\n--------------------------------------")
    print("Round Robin")
    print("--------------------------------------")
    totalProcessTime, remain_processes, flag = 0, nr_proc, 0
    for p in process:
        p.time_left = p.burst
    global currentTime
    print("\n--------------------------------------")
    print("Gantt Chart")
    print("--------------------------------------")
    for currentTime, i in zip(range(0, nr_proc), range(nr_proc)):
        print(f"({currentTime})|==P{process[i].ID}==|", end='')
        if process[i].time_left <= q and process[i].time_left > 0:
            currentTime += process[i].time_left + cs
            process[i].time_left = 0
            flag = 1
        elif process[i].time_left > 0:
            process[i].time_left -= q
            currentTime += q + cs
        if process[i].time_left == 0 and flag == 1:
            remain_processes -= 1
            process[i].info.f_time = currentTime - cs
            process[i].info.Ta_time = currentTime - process[i].arr_time
            process[i].info.wt = currentTime - process[i].arr_time
            flag = 0
        if i == nr_proc - 1:
            i = 0
        elif process[i + 1].arr_time <= currentTime:
            i += 1
        else:
            i = 0
    print(f"({currentTime})")
    print("\n\n--------------------------------------------------------")
    print("Process\t|TurnAround Time| Waiting Time  |  Finish Time")
    print("--------+---------------+---------------+---------------")
    total_burst = 0
    for p in process:
        p.info.Ta_time = p.info.wt + p.burst
        print(f"P({p.ID})\t|\t{p.info.Ta_time}\t|\t{p.info.wt}\t|\t{p.info.f_time}")
        total_burst += p.burst
    print("--------------------------------------------------------\n")
    print(f"Avg Waiting time = {total_wt * 1.0 / nr_proc}")
    print(f"Avg Turnaround time = {total_Ta_time / nr_proc}")
    cpu_utilization = total_burst * 100.0 / (currentTime)
    print(f"Cpu Utilization {cpu_utilization} %")
    print("Round Robin scheduling complete")

if __name__ == "__main__":
    read_file()
    print("\n--------------------------------------")
    print("Process\t| Arrival Time  | Burst Time")
    print("--------+---------------+-------------")
    for p in process:
        print(f"P({p.ID})\t|\t{p.arr_time}\t|\t{p.burst}")
    FCFS()
    SJF()
    RR()
