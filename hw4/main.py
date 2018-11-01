import sys
import truss

if len(sys.argv) < 3:
    print('Usage:')
    print('python3 main.py [joints file] [beams file] [optional plot output file]')
    sys.exit()

joints_file = sys.argv[1]
beams_file = sys.argv[2]
try:
    output_file = sys.argv[3]
except:
    output_file = False

try:
    result = truss.Truss(joints_file, beams_file, output_file)
except RuntimeError as e:
    print('Runtime Error: {}'.format(e))
    sys.exit()

print(result)

