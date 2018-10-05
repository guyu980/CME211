import random
import sys
import time

# Print useful message if no arguments given
if len(sys.argv) < 6:
    print("Usage:")
    print("  $ python3 generatedata.py <ref_length> <nreads> <read_len> <ref_file> <reads_file>")
    sys.exit()

# Extract arguments from sys.argv
ref_length = int(sys.argv[1])
nreads = int(sys.argv[2])
read_len = int(sys.argv[3])
ref_file = sys.argv[4]
reads_file = sys.argv[5]

# Generate first 75% reference by adding random number string
ref = ''
for i in range(int(0.75*ref_length)):
    ref += str(random.randint(0, 3))

# Generate last 25% reference by copying last part of randomly generated reference
ref += ref[int(0.5*ref_length):]

# Define a function to transform number 0, 1, 2, 3 into letter A, C, G, T
def transform(x):

    x = list(x)
    for i in range(len(x)):
        if x[i] == '0':
            x[i] = 'A'
        elif x[i] == '1':
            x[i] = 'C'
        elif x[i] == '2':
            x[i] = 'G'
        else:
            x[i] = 'T'
    x =  ''.join(x)

    return x

ref = transform(ref)

# Generate reads, track the number of read in each type and caculate elapsed time
timeStart = time.time()
reads = []
naligns_0 = 0
naligns_1 = 0
naligns_2 = 0

for i in range(nreads):
    r = random.random()
    # Generate 15% reads align 0
    if r < 0.15:
        while True:
            read = ''
            for j in range(read_len):
                read += str(random.randint(0, 3))
            if ref.find(read) == -1:
                reads.append(transform(read))
                naligns_0 += 1
                break
 
    # Generate 75% reads align 1 by start position at first 50% of reference
    elif r < 0.9:
        start = int(0.5*random.random()*ref_length)
        reads.append(ref[start:start+read_len])
        naligns_1 += 1
    # Generate 10% reads align 2 by start position at last 25% of reference
    else:
         while True:
            start = int((0.75+0.25*random.random())*ref_length)
            # Avoid postion close to the end of reference
            if start + read_len < ref_length:
                reads.append(ref[start:start+read_len])
                naligns_2 += 1
                break

timeEnd = time.time()
timeElapsed = timeEnd - timeStart

# Write reference and reads into file
with open(ref_file, 'w') as f:
    f.write(ref+'\n')

with open(reads_file, 'w') as f:
    for read in reads:
        f.write(read+'\n')

# Print summary
print("reference length: {}".format(ref_length))
print("number reads: {}".format(nreads))
print("read length: {}".format(read_len))
print("aligns 0: {}".format(naligns_0/nreads))
print("aligns 1: {}".format(naligns_1/nreads))
print("aligns 2: {}".format(naligns_2/nreads))
print("elapsed time: {}".format(timeElapsed))
