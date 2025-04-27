import time
import matplotlib.pyplot as plt

# Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

# Arrays (reversed)
Arr1 = list(reversed([1,2,3,4,5]))
Arr2 = list(reversed([1,2,3,4,5,6,7,8,9,10]))
Arr3 = list(reversed(list(range(1, 51))))
Arr4 = list(reversed(list(range(1, 101))))
arrays = [Arr1, Arr2, Arr3, Arr4]
array_sizes = [len(Arr1), len(Arr2), len(Arr3), len(Arr4)]

# Measure time
def measure_time(arr):
    runs = 5
    total_time = 0
    for _ in range(runs):
        copied_arr = arr.copy()
        start = time.perf_counter()
        insertion_sort(copied_arr)
        end = time.perf_counter()
        total_time += (end - start)
    return (total_time / runs) * 1e6  # microseconds

insertion_times = [measure_time(arr) for arr in arrays]

# Plot
plt.figure(figsize=(8,5))
plt.plot(array_sizes, insertion_times, marker='o', color='green', label='Insertion Sort')
plt.title('Insertion Sort Time Complexity')
plt.xlabel('Input Size (N)')
plt.ylabel('Average Execution Time (µs)')
plt.grid(True)
plt.legend()
plt.show()
