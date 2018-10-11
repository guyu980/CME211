import sys
import time

# Print useful message if no arguments given
if len(sys.argv) < 4:
    print("Usage:")
    print("  $ python3 processdata.py <ref_file> <reads_file> <align_file>")
    sys.exit()

# Extract arguments from sys.argv
ref_file = sys.argv[1]
reads_file = sys.argv[2]
align_file = sys.argv[3]

# Load reference, reads and parameters
with open(ref_file, 'r') as f:
    ref = f.read().strip()

with open(reads_file, 'r') as f:
    reads = [x.strip() for x in f.readlines()]

ref_length = len(ref)
nreads = len(reads)

# Count the number of reads in each type
naligns_0 = 0
naligns_1 = 0
naligns_2 = 0

for i in range(nreads):
    position = ref.find(reads[i])
    if position >= 0:
        if ref.find(reads[i], position+1) >= 0:
            naligns_2 += 1
        else:
            naligns_1 += 1
    else:
        naligns_0 += 1
t3 = time.time()

# Process data into aligns and caculate elapsed time
timeStart = time.time()
aligns = []
#--correctness_0
#--Even though this work, why do you first compute the number of 
#--times each read appears, and then find them again to output the position ?
#--You basically perform the same read twice, which is suboptimal...
#-_START
for read in reads:
    position = ref.find(read)
    align = read + ' ' + str(position)
    if ref.find(read, position+1) >= 0:
        align += ' ' + str(ref.find(read, position+1))
    aligns.append(align)
#--END
timeEnd = time.time()
timeElapsed = timeEnd - timeStart

# Write aligns into file
with open(align_file, 'w') as f:
    for align in aligns:
        f.write(align+'\n')

# Print summary
print("reference length: {}".format(ref_length))
print("number reads: {}".format(nreads))
print("aligns 0: {}".format(naligns_0/nreads))
print("aligns 1: {}".format(naligns_1/nreads))
print("aligns 2: {}".format(naligns_2/nreads))
print("elapsed time: {}".format(timeElapsed))


#--correctness_0
#--Even if you have a suboptimality, your program outputs the correct result in a decent time. Good job !
#--END

#--style_0
#--Your coding style is easy to follow, with good comments and clear variable naminf. Great !
#--END
