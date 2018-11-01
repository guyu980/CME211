import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import warnings
from scipy import sparse
from scipy.sparse.linalg import spsolve

class Truss:
    def __init__(self, joints_file, beams_file, output_file=False):
        self.solve(joints_file, beams_file, output_file)


    def solve(self, joints_file, beams_file, output_file):
        """ Implement all steps to do truss analysis
        Args:
            joints_file: Filename of joints data
            beams_file: Filename of beams data
            [output_file]: Filename for plot output, optional
        """
        self.load_file(joints_file, beams_file)
        self.PlotGeometry(output_file)
        self.sparse_matrix()
        self.compute_force()


    def load_file(self, joints_file, beams_file):
        """ Load the data of joints and beams from input file
        Args:
            joints_file: Filename of joints data
            beams_file: Filename of beams data
        """
        self.joints = np.loadtxt(joints_file, skiprows=1)
        self.beams = np.loadtxt(beams_file, skiprows=1)
        self.xy = {}
        self.n_joints = self.joints.shape[0]
        self.n_beams = self.beams.shape[0]
        # Extract the coordinate of joints into dictionary xy
        for i in range(self.n_joints):
            self.xy[self.joints[i, 0]] = self.joints[i, 1:3]


    def PlotGeometry(self, output_file):
        """ Plot the geometry of the truss
        Args:
            output_file: Filename for plot output
        """
        if output_file:
            plt.figure()
            # Plot beams with blue line and joints with red point
            for i in range(self.n_beams):
                joint1, joint2 = self.beams[i, 1:3]
                x, y = [self.xy[joint1][0], self.xy[joint2][0]], [self.xy[joint1][1], self.xy[joint2][1]]
                plt.plot(x, y, color='b')
                plt.scatter(x, y ,color='r')
            plt.savefig(output_file)


    def sparse_matrix(self):
        """ Create sparse matrix of the linear system of equations
        """
        # There are two types of equations in this system:
        #    (1) Equilibrium of each joint in 2 directions
        #    (2) Geometric constraints for beam force of each beam
        self.n_eqs = 2 * self.n_joints + self.n_beams
        self.delta_xy = {}
        values, rows, cols = [], [], []

        # Generate the sparse matrix in COO format
        for i in range(self.n_eqs):
            # Get entries for the submartix [0:2*n_joints, 0:2*n_beams]
            # For each beam, the beam force coefficient of the first joint is 1, and -1 for the second joint
            # For each joint, related beams can be divided into two types determined by the position of the joint
            if i < self.n_joints:
                joint = self.joints[i, 0]
                beam_pos = list(np.where(self.beams[:, 1] == joint)[0])
                beam_neg = list(np.where(self.beams[:, 2] == joint)[0])
                cols += beam_pos + beam_neg
                cols += [x + self.n_beams for x in beam_pos] + [x + self.n_beams for x in beam_neg]
                rows += list(i * np.ones(len(beam_pos) + len(beam_neg)))
                rows += list((i + self.n_joints) * np.ones(len(beam_pos) + len(beam_neg)))
                values += 2 * (list(np.ones(len(beam_pos))) + list(-np.ones(len(beam_neg))))

            # Get entries for the submartix [2*n_joints:2*n_joints+b_beams, 0:2*n_beams]
            # For each beam, the beam force coefficient of the first joint is -dy, and dx for the second joint
            elif i >= 2 * self.n_joints:
                beam = i - 2 * self.n_joints + 1
                j1 = float(self.beams[np.where(self.beams[:, 0] == beam)[0], 1])
                j2 = float(self.beams[np.where(self.beams[:, 0] == beam)[0], 2])
                self.delta_xy[beam] = self.xy[j2] - self.xy[j1]
                cols += [beam - 1 + self.n_beams, beam - 1]
                rows += [i, i]
                values += (np.array((1, -1)) * self.delta_xy[beam]).tolist()

        # Get entries for the submatrix [0:2*n_joints, 2*n_beams:2*n_beams+2*n_support]
        # For each fixed joint, the reaction force coeffcient is 1
        joints_support = self.joints[np.where(self.joints[:, -1] == 1)[0], :]
        n_support = joints_support.shape[0]
        self.n_variables = 2 * (self.n_beams + n_support)

        for i in range(n_support):
            joint = joints_support[i, 0]
            cols += [2 * self.n_beams + i, 2 * self.n_beams + i + n_support]
            rows += [joint - 1, joint - 1 + self.n_joints]
            values += [1, 1]

        # Convert sparse matrix to CSR format for computing
        self.matrix = sparse.csr_matrix((values, (rows, cols)), shape=(self.n_eqs, self.n_variables))


    def compute_force(self):
        """ Compute the beam force by solving the linear system of equations
        """
        # Report error message when the matrix is not square
        if self.n_eqs != self.n_variables:
            raise RuntimeError("Truss geometry not suitable for static equilibrium analysis")

        b = np.concatenate((-self.joints[:, 3], -self.joints[:, 4], np.zeros(self.n_beams))).reshape((self.n_eqs, 1))

        # Report error message when the matrix is singular
        try:
            warnings.filterwarnings("error")
            x = spsolve(self.matrix, b)
        except:
            raise RuntimeError("Cannot solve the linear system, unstable truss?")

        self.beam_force = np.zeros((self.n_beams, 2))

        # The beam force in two directions are: Bx=x[i], By=x[i+n_beams]
        for i in range(self.n_beams):
            beam = i + 1
            dx, dy = self.delta_xy[beam][0], self.delta_xy[beam][1]
            Bx, By = x[i], x[i + self.n_beams]

            # Determine the directional beam force by dot product
            if np.array((dx, dy)).dot(np.array((Bx, By))) > 0:
                sign = -1
            else:
                sign = 1

            self.beam_force[i, 0] = beam
            self.beam_force[i, 1] = sign * (x[i] ** 2 + x[i + self.n_beams] ** 2) ** 0.5


    def __repr__(self):
        """ Print results
        Returns:
            output: String of summary of results
        """
        output = ' Beam      Force\n------------------\n'
        for i in range(self.n_beams):
            output += "{:4d}{:13.3f}\n".format(int(self.beam_force[i, 0]), self.beam_force[i, 1])

        return output

