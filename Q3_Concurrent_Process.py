#Question 3: Concurrent Process
import threading
import time

NUMBERS = [35, 38, 40]  #Fibonacci numbers to calculate
ROUNDS = 10             #Number of testing rounds

#Fibonacci Function
def fibonacci(n):
    if n<=1:
        return n                                #Base case: Fib(0) = 0, Fib(1) = 1
    return fibonacci(n - 1) + fibonacci(n - 2)  #Fib(n) = Fib(n-1) + Fib(n-2)

#Thread task: calculate one Fibonacci number and record its own start and end time
def fibonacci_task(n, index, results, start_times, end_times):
    start_times[index] = time.time_ns() #Records the current sys time in nanoseconds before the calculation starts
    results[index] = fibonacci(n)       #Store the result at position index in results
    end_times[index] = time.time_ns()   #Records the curr sys time after the calculation finishes

#With Multithreading: one thread per number
def run_with_threads():
    #Each thread writes only to its own index, so threads never overwrite each other
    results = [0] * len(NUMBERS)
    start_times = [0] * len(NUMBERS)
    end_times = [0] * len(NUMBERS)

    #Create one thread for each number
    threads = []
    for index in range(len(NUMBERS)):
        thread = threading.Thread(target=fibonacci_task, args=(NUMBERS[index], index, results, start_times, end_times))
        threads.append(thread)

    #Start all threads, then wait for all of them to finish
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    #Total elapsed time: T = latest thread end time - earliest thread start time
    time_elapsed = max(end_times) - min(start_times)
    return results, time_elapsed

#Without Multithreading: calculate the numbers one after another
def run_without_threads():
    results = []
    start_time = time.time_ns()
    for n in NUMBERS:
        results.append(fibonacci(n))
    end_time = time.time_ns()
    return results, end_time - start_time

#Format the results of one round
def format_results(results):
    text = ""
    for index in range(len(NUMBERS)):
        if index > 0:
            text += ", "
        text += f"Fib({NUMBERS[index]})={results[index]}"
    return text

#Run an experiment for all rounds and return the average time
def run_experiment(title, run_function):
    print(f"\n=== Fibonacci Computation ({title}) ===")
    total_time = 0
    for round_number in range(1, ROUNDS + 1):
        results, time_elapsed = run_function()
        total_time += time_elapsed
        print(f"Round {round_number:<2}: {format_results(results)} | T = {time_elapsed:,} ns")
    print(f"Total T ({title})   : {total_time:,} ns")
    average_time = total_time // ROUNDS
    print(f"Average T ({title}) : {average_time:,} ns")
    return average_time

def main():
    average_with_threads = run_experiment("With Multithreading", run_with_threads)
    average_without_threads = run_experiment("Without Multithreading", run_without_threads)

    #Compare the two averages
    difference = (average_without_threads - average_with_threads) / average_without_threads * 100
    if difference > 0:
        print(f"\nObservation: Multithreading reduced the average completion time by approximately {difference:.1f}%.")
    else:
        print(f"\nObservation: Multithreading increased the average completion time by approximately {-difference:.1f}%.")

if __name__ == '__main__':
    main()