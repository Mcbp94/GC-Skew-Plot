#
import os
import matplotlib.pyplot as plt

while True:
    filename = input("Enter fasta file name with format: ")
    if(os.path.exists(filename)):
        f = open(filename, "r")
        next(f)
        seq = f.readline()
        f.close()
        break
    else:
        print("找不到" + filename)

while True:
    window_size = input("Enter sliding window size: ")
    if window_size.isnumeric():
        break
    else:
        print("他妈的叫你打号码你给我打" + window_size)

while True:
    step_size = input("Enter step size: ")
    if step_size.isnumeric():
        break
    else:
        print("他妈的叫你打号码你给我打" + step_size)
    
window_size = int(window_size)
step_size = int(step_size)
window_start = 0
window_end = window_size
loop = 1

arr = []
c_count = 0
g_count = 0

while loop:
    for c in seq[window_start:window_end]:
        if c == "C":
            c_count += 1
        elif c == "G":
             g_count += 1
         
    window_start += step_size
    if (window_end + step_size) > len(seq):
        loop = 0
    else:
        window_end += step_size
    result = ((g_count - c_count)/(c_count + g_count))*100
    arr.append(result)
    c_count = 0
    g_count = 0

remainder = len(seq) - window_end
diff = window_size - remainder
seq = seq + seq[:diff]
for c in seq[window_start:]:
    if c == "C":
        c_count += 1
    elif c == "G":
         g_count += 1
result = ((g_count - c_count)/(c_count + g_count))*100
arr.append(result)

idx = []
if arr[0] > 0:
    value = "positive"
else:
    value = "negative"
for x in arr:
    if x > 0:
        val = "positive"
    else:
        val = "negative"
    if val != value:
        idx.append(arr.index(x) - 1)
        value = val

print(idx)

#window = seq[0:window_size]

#for c in window:
#    if c == "C":
#        c_count += 1
#    elif c == "G":
#        g_count += 1
#
#result = (c_count - g_count)/(c_count + g_count)
#arr.append(result)
#
#for c in seq[window_size:]:
#    if c == "C":
#        c_count += 1
#    elif c == "G":
#        g_count += 1
#    if window[0] == "C":
#        c_count -= 1
#    elif window[0] == "G":
#        g_count -= 1
#    window = window[1:] + c
#    result = (c_count - g_count)/(c_count + g_count)
#    arr.append(result)

plt.axhline(linewidth=2, color='r')
plt.plot(arr)
plt.show()
