# Cumulative GC Skew

by Mark Chan

23 September 2020

This is a workflow documentation for obtaining a cumulative GC skew plot, used primarily for genomic island analysis. First part involves using Zisland Explorer to obtain putative genomic island coordinates, before using a simple python program to plot a *prettier* cumulative GC skew plot and obtain individual `fasta` files. Possible to run python on local terminal as it is not computationally demanding.

------

### 1. Using Zisland Explorer

Zisland explorer is supported by Windows, Mac, and Linux OS and can be downloaded from [here](http://cefg.uestc.cn/Zisland_Explorer/download.html).

It requires an `.fna` input file with an optional `.ptt` input.

![image-20200924161330999](C:\Users\markc\AppData\Roaming\Typora\typora-user-images\image-20200924161330999.png)

**Figure 1. Zisland explorer user interface**

> If the program fails to run, create a local directory and run it from there. An error usually occurs when you try to run your data from the cloud (e.g. OneDrive).

It outputs 4 files:

1. `GeneInfo.txt` which is the generated `.ptt` file if you input only the `.fna` file.
2. `Genomic_Islands.png` which contains the cumulative GC skew plot. Red points denote predicted genomic islands (ascending straight lines)
3. `Genomic_Islands.txt` which contain the positions and no. of genes of each predicted genomic island
4. `SegPoints.html` segmentation points file

![image-20200924162419917](C:\Users\markc\AppData\Roaming\Typora\typora-user-images\image-20200924162419917.png)

**Figure 2. Example Genomic_Islands.png which contains predicted genomic island in red ascending lines.** *ugly right?*

### 2. Running Cumulative GC Skew.py

Make sure [python](https://www.python.org/) is installed. Install numpy, matplotlib and pandas packages into python>scripts folder. Installation can be done using CMD.

This python script uses two files as input:

1. Same `fasta` input from Zisland Explorer

2. `Genomic_Islands.txt` which looks something like this

   ![image-20200924165826197](C:\Users\markc\AppData\Roaming\Typora\typora-user-images\image-20200924165826197.png)

This python script provides the following output files:

1. **Pretty** Cumulative GC Skew Plot
2. Individual `fasta` files for each genomic island (you have the option to include <n> nucleotides of flanking sequences of the island too in the `fasta` files)
3. `analysis_summary.txt` which includes the length and GC% of the input `fasta` file, gradient of least squares regression (used to plot the cumulative GC skew), and GC% of each predicted genomic island (including flanking sequences, if any) compared to GC% of rest of the genome

### 3. File input

1. Create working directory

2. Load both input files `.fna`, `Genomic_Islands.txt` and `Cumulative GC Skew.py` python script into working directory

3. Right click `Cumulative GC Skew.py` and edit with IDLE

4. On Ln12, enter input `fasta` file name including file format

   > ![image-20200924171305412](C:\Users\markc\AppData\Roaming\Typora\typora-user-images\image-20200924171305412.png)

5. On Ln95, enter name of `Genomic_Islands.txt`

   > ![image-20200924173222770](C:\Users\markc\AppData\Roaming\Typora\typora-user-images\image-20200924173222770.png)

6. Additional option: 

   a. You can include <n> flanking sequences of each genomic island in the output `fasta` file

   b. On Ln162, 

```python
#original line
content = seq[int(pos_arr[i][0]): ((int(pos_arr[i][1])) + 1)]

#example to include 2kb flanking sequences of each genomic island in the fasta output file
#we need to tell mr. python to include the nucleotides from position -2000 to position +2000
#updated line to incl. 2kb upstream and downstream of genomic island looks something like this
content = seq[int(pos_arr[i][0] - 1999): ((int(pos_arr[i][1])) + 2001)]

##python actually reads position 1 of the fasta file as position 0, hence the starting and ending position m and n of a genomic island is in fact (m - 1) and (n + 1) in python
##therefore the 
-1999 but + 2001
```

7. On Ln195, you can change the x-axis range depending on size of your `fasta` file. Recommend to set range as <n>+200kb:

   *Burkholderia thailandensis* Chr1 is 3.5Mb, so I set the x-axis max at 3700000

   > ![image-20200924181804734](C:\Users\markc\AppData\Roaming\Typora\typora-user-images\image-20200924181804734.png)

8. On Ln201, you can change the name of the cumulative GC skew plot

   > ![image-20200924182015740](C:\Users\markc\AppData\Roaming\Typora\typora-user-images\image-20200924182015740.png)

![image-20200924182628585](C:\Users\markc\AppData\Roaming\Typora\typora-user-images\image-20200924182628585.png)

*:D*