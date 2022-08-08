# import some sorcery
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# write analysis
fa = open("analysis_summary.txt", "w")


# open file and assign DNA sequence to variable seq
print("\nReading file...")

#fa.write("\nReading file...")
while True:
    inputfasta = input("Please enter fasta file name with format (case-sensitive):\n")
    if(os.path.exists(inputfasta)):
        f=open(inputfasta, "r")
        seq = f.read()
        f.close()
        break
    else:
        print("ze file doez not ezizt \n")

count = list(range(1,len(seq) + 1))

# declare variables
a_count = 0
t_count = 0
c_count = 0
g_count = 0
result = 0 # this is Zn
arr = []

# go through each nucleotide in the DNA sequence
for nucleotide in seq:
    if nucleotide == "A":
        a_count = a_count + 1
    elif nucleotide == "T":
        t_count = t_count + 1
    elif nucleotide == "C":
        c_count = c_count + 1
    elif nucleotide == "G":
        g_count = g_count + 1

    # if we reach here it means we have up-to-date number of nucleotides
    result = (a_count + t_count) - (c_count + g_count)
    arr.append(result)
    # screen saver time, delete the # for screen saver
    # print(result)

total = a_count + t_count + c_count + g_count

gc = g_count + c_count
print("\nlength of sequence = " + str(total) + " bp")
print("gc% = " + str("{:.2f}".format(100*gc/total)) + "%")

# if we reach here it means we have an array full of data points
# change arrays to numpy arrays
y = np.array(arr)
x = np.array(count)

# least squares regression line
print("\nCalculating slope...")
#fa.write("\nCalculating slope...")
y_mean = np.mean(y)
x_mean = np.mean(x)
num = 0 # numerator
den = 0 # denominator
for i in range(len(x)):
    num += (x[i] - x_mean)*(y[i] - y_mean)
    den += (x[i] - x_mean)**2

m = num / den # m = gradient = k
c = y_mean - m*x_mean
print("Gradient of least squares regression: " + str(m) +"\n")
fa.write("\nGradient of least squares regression: " + str(m) +"\n\n")
#fa.write("\nRetrieving genomic islands...")

# Calculate Z'n
# reset variables
new_arr = []
#n = 1 # count

# Go through each Zn
#for z in y:
    #new_arr.append(z - m*n)
    #n = n + 1

for n in range(len(x)):
    new_arr.append(y[n] - m*n)

# if we reach here it means we have Z'n values inside arr

# get position of genomic islands from file
# read file

while True:
    zislandoutput = input("Please enter ZIsland Explorer genomic island summary file name with format:\n")
    if(os.path.exists(zislandoutput)):
        f = open(zislandoutput, "r")
        fa.write(f.read())
        f.close()
        break
    else:
        print("oui oui baguette hon hon hon\n")

count = list(range(1,len(seq) + 1))
print("Retrieving genomic islands...")

with open(zislandoutput, "r") as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)


# get rid of first line and last 2 lines
d.pop(len(d)-1)
d.pop(len(d)-1)
d.pop(0)

# define positions of genomic islands into array
pos_arr = []
for i in range(len(d)): 
    start_stop = d[i][1].split("..")
    pos_arr.append(start_stop)

# get GC%
# set variables
temp_a_count = 0 # total ATCG counts of all genomic islands
temp_t_count = 0
temp_c_count = 0
temp_g_count = 0
gi_a_count = 0 # total ATCG counts of each genomic island
gi_t_count = 0
gi_c_count = 0
gi_g_count = 0
gc_ratio_arr = []
total_gc_ratio = 0 # GC% of sequence excluding all genomic islands



for a in pos_arr:
    gi = seq[int(a[0]): (int(a[1])+1)]
    for nucleotide in gi:
        if nucleotide == "A":
            temp_a_count = temp_a_count + 1
            gi_a_count = gi_a_count + 1
        elif nucleotide == "T":
            temp_t_count = temp_t_count + 1
            gi_t_count = gi_t_count + 1
        elif nucleotide == "C":
            temp_c_count = temp_c_count + 1
            gi_c_count = gi_c_count + 1
        elif nucleotide == "G":
            temp_g_count = temp_g_count + 1
            gi_g_count = gi_g_count + 1
    gi_total = gi_a_count + gi_t_count + gi_c_count + gi_g_count
    gc_ratio = (gi_c_count + gi_g_count)/gi_total
    gc_ratio_arr.append(gc_ratio)
    # reset variables
    gi_a_count = 0
    gi_t_count = 0
    gi_c_count = 0
    gi_g_count = 0


# if we reach here we will have gc_ratio_arr ready,
# as well as total ATCG of all genomic islands.

# to include flanking sequence of n nucleotides upstream and downstream
# change content = seq[int(pos_arr[i][0]): ((int(pos_arr[i][1])) + 1)] to content = seq[int(pos_arr[i][0])-2000: ((int(pos_arr[i][1])) + 1+2000)]
# for an example n = 2000
# flanking seqeunce will not be reflected in red region of Z'n plot

file = open("genomicisland.fa", "w")

for i in range(len(gc_ratio_arr)):
    percentage = "{:.2%}".format(gc_ratio_arr[i])
    print("GC% of genomic island " + str(i+1) + " is: " + percentage)
    fa.write("\nGI" + str(i+1) + " GC% is: " + percentage)
    name = ">GI" + str(i+1)
    content = seq[int(pos_arr[i][0]): ((int(pos_arr[i][1])) + 1)]
    file.write("%s\n" % name)
    file.write("%s\n" % content)
    
file.close()
    
# can proceed to get GC% of sequence excluding genomic island nucleotides
total_gc_num = c_count - temp_c_count + g_count - temp_g_count
temp_total = temp_a_count + temp_t_count + temp_c_count + temp_g_count
total_gc_den = total - temp_total
total_gc_ratio = total_gc_num/total_gc_den
total_percentage = "{:.2%}".format(total_gc_ratio)
print("GC% of remaining sequence is: " + total_percentage + "\n")
fa.write("\nGC% of remaining sequence is: " + total_percentage + "\n")

# plot the curve
print("Plotting...")
#fa.write("\nPlotting...")
new_y = np.array(new_arr)
plt.plot(x, new_y, "-b", label="rest region")

# plot red lines
# only need one label
switch = 0
for a in pos_arr:
    x = range(int(a[0]), int(a[1])+1)
    y = new_y[int(a[0]): (int(a[1])+1)]
    if switch == 0:
        plt.plot(x, y, "-r", label="genomic islands")
        switch = 1
    else:
        plt.plot(x, y, "-r")



#plotting
plt.xticks(np.arange(0, total + 200000, step=100000))
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
plt.xlabel("n (Mb)")
plt.ylabel("Cumulative GC Profile (bp)")
plt.title("Cumulative GC Plot", fontsize=20, y=1.05)
plt.grid()
plt.legend(loc='lower left', bbox_to_anchor= (0.0, 1), ncol=2,
            borderaxespad=0, frameon=False)
print("Plotting complete!\n")
#fa.write("\nPlotting complete!\n")
fa.close()
plt.savefig("Cumulative GC Profile Plot.png")
plt.show()


#np.savetxt("yeet.csv", y, delimiter=",")

# to read the .csv into an array, do the following
# some_new_array = np.genfromtxt("yeet.csv", delimiter=",")


