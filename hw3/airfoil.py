import glob
import math
import os

class Airfoil():
    """ Define a class Airfoil to deal with the whole problem 

    Example usage:
        > a = Airfoil(inputdir)
        > print(a)
    """

    def __init__(self, inputdir):
        """ Initialize variables and run the whole process

        Args:
            inputdir: Input data directory
        """
        # Strip '/' first and then add back in case that input directory doesn't have '/'
        self.inputdir = inputdir.strip('/')+'/'
        self.xy = None
        self.cp = {}
        self.cl = {}
        self.stagnation_pt = {}
        self.load_data()
        self.compute_chord()
        for alpha in self.cp:
            cx, cy = self.cp_decomposition(alpha)
            self.compute_lift_coef(cx, cy, alpha)
            self.find_stagnation_point(alpha)
        self.summary()


    def load_data(self):
        """ Load coordinate and pressure coefficient data from input directory
        """
        # Get the xy and cp data file name from directory
        # Report error message when directory is invalid
        if os.path.isdir(self.inputdir) is False:
            raise RuntimeError("The directory is invalid")
        xy_data = glob.glob(self.inputdir+'xy.dat')
        cp_data = glob.glob(self.inputdir+'alpha*.dat')

        # Report error message when no required data file in the directory
        if len(xy_data) == 0:
            raise RuntimeError("No required xy data file found in the directory")
        elif len(cp_data) == 0:
            raise RuntimeError("No required cp data file found in the directory")

        # Read xy data into list with length of m, and y[i] is point [x, y] as a list
        # Read cp data into dictionary, and cp[alpha] is list with length of m-1
        # Convert all data to float
        # Report error message when having trouble with reading data file
        try:
            with open(xy_data[0]) as f:
                self.xy = [x.strip().split() for x in f.readlines()]
                self.xy = [list(map(float, x)) for x in self.xy[1:]]
        except:
            raise RuntimeError("Error in reading xy data file")

        try:
            # Define some keywords from file name to be deleted to get the alpha value
            keywords = [self.inputdir, 'alpha', '.dat']
            for data in cp_data:
                with open(data) as f:
                    for kw in keywords:
                        data = data.replace(kw, '')
                    alpha = float(data)
                    self.cp[alpha] = [x.strip().split() for x in f.readlines()]
                    self.cp[alpha] = [float(x[0]) for x in self.cp[alpha][1:]]
        except:
            raise RuntimeError("Error in reading cp data file")


    def compute_chord(self):
        """ Compute the chord length by xy data
        """
        x = [x[0] for x in self.xy]
        # Get leading and tailing edge point
        leading, trailing = x.index(max(x)), x.index(min(x))
        self.chord = math.sqrt(sum([(self.xy[leading][i] - self.xy[trailing][i]) ** 2 for i in range(2)]))


    def cp_decomposition(self, alpha):
        """ Do pressure coefficient decomposition for each panel, calculate total Cartesian force coefficients

        Args:
            alpha: Angle of attack
        Returns:
            sum(cx): Total Cartesian force coefficients on direction x
            sum(cy): Total Cartesian force coefficients on direction y
        """
        cp = self.cp[alpha]
        cx, cy = [], []
        n = len(cp)
        for i in range(n):
            pt1, pt2 = self.xy[i], self.xy[i+1]
            delta_x, delta_y = pt2[0] - pt1[0], pt2[1] - pt1[1]
            cx.append(-cp[i] * delta_y / self.chord)
            cy.append(cp[i] * delta_x / self.chord)

        return sum(cx), sum(cy)


    def compute_lift_coef(self, cx, cy, alpha):
        """ Compute lift coefficient

        Args:
            cx: Total Cartesian force coefficients on direction x
            cy: Total Cartesian force coefficients on direction y
            alpha: Angle of attack
        """
        self.cl[alpha] = cy * math.cos(math.radians(alpha)) - cx * math.sin(math.radians(alpha))


    def find_stagnation_point(self, alpha):
        """ Find the stagnation point

        Args:
            alpha: Angle of attack
        """
        cp = self.cp[alpha]
        # Find the point with its cp value closest to 1.0
        distance_to_1 = [abs(x - 1) for x in cp]
        index = distance_to_1.index(min(distance_to_1))
        pt1, pt2 = self.xy[index], self.xy[index+1]
        x, y = (pt2[0] + pt1[0])/2, (pt2[1] + pt1[1])/2
        self.stagnation_pt[alpha] = [x, y, cp[index]]


    def summary(self):
        """ Print results
        """
        print("alpha     cl           stagnation pt      ")
        print("-----  -------  --------------------------")
        alphaList = list(self.cp.keys())
        alphaList.sort()
        for alpha in alphaList:
            pt = self.stagnation_pt[alpha]
            print("{:5.2f}  {:7.4f}  ({:7.4f}, {:7.4f}) {:7.4f}".format(alpha, self.cl[alpha], pt[0], pt[1], pt[2]))

