import math
import matplotlib.pyplot as plt
import numpy as np
import sys

def load_data(input_file, solution_file):
    # Load the input data and converged solution, get parameters of the system
    with open(input_file, 'r') as f:
        length, width, h, Tc, Th = [float(x) for x in f.read().split()]
    solution = np.loadtxt(solution_file)

    # Adding the upper, lower, right bound to the solution matrix
    n_l = int(length/h) + 1
    n_w = int(width/h) + 1
    solution = solution.reshape((n_l-1, n_w-2)).T

    # Upper bound is Th
    # Lower bound is Gaussian temperature T(x)
    # Right bound is the same as the lexft bound
    upper_bound = np.array([Th] * n_l).reshape((1, n_l))
    lower_bound = np.array([-Tc*(math.exp(-10*pow(x*h-length/2, 2))-2) for x in range(n_l)]).reshape((1, n_l))
    right_bound = solution[:, 0].reshape((n_w-2, 1))
    solution = np.concatenate((solution, right_bound), axis=1)
    solution = np.concatenate((upper_bound, solution, lower_bound), axis=0)

    return solution


# Plot the temperature distribution within the pipe wall and mean temperature isoline
def plot(solution):
    # Compute the relative y coordinate of mean temperature in each column
    ratio = solution.shape[0] / solution.shape[1]
    mean = np.mean(solution)
    print("Mean Temperature: {:.5f}".format(mean))

    # Assume the mean temperature is beteween solution[i-1, j] and solution[i, j]
    # The first part is the relative y coordinate of i
    diff = solution - mean
    diff[diff>0] = -100
    idx = np.argmax(diff, axis=0)
    y_idx = (solution.shape[0] - idx) / solution.shape[1]

    # The second part is the ratio that mean temperature in this interval
    for i in range(solution.shape[1]):
        y_idx[i] += (mean - solution[idx[i], i]) / (solution[idx[i]-1, i] - solution[idx[i], i]) / solution.shape[1]

    # Plot the result
    plt.figure(figsize=(8, 6))
    plt.imshow(solution, extent = (0, 1, 0, ratio) , cmap = plt.cm.jet)
    plt.plot(np.arange(0, 1, 1/solution.shape[1]), y_idx, 'k')
    plt.colorbar()
    plt.axis('equal')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def main():
    # Print useful message if no arguments given
    if len(sys.argv) < 2:
        print("Usage:")
        print("  $ python3 postprocess.py <input_file>, <solution_file> (solution_converge.txt)")
        sys.exit()

    # Extract arguments from sys.argv
    input_file = sys.argv[1]
    solution_file = sys.argv[2]

    print("Input file processed: {}".format(input_file))
    solution = load_data(input_file, solution_file)
    plot(solution)


if __name__ == '__main__':
    main()