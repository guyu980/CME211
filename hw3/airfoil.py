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
        self.cl = {}
        self.stagnation_pt = {}
        # Strip '/' first and then add back in case that input directory doesn't have '/'
        xy, cp = self.load_data(inputdir.strip('/')+'/')
        self.chord = self.compute_chord(xy)
        for alpha in cp:
            cx, cy = self.cp_decomposition(xy, cp[alpha])
            self.cl[alpha] = self.compute_lift_coef(cx, cy, alpha)
            self.stagnation_pt[alpha] = self.find_stagnation_point(xy, cp[alpha])


    def load_data(self, inputdir):
        """ Load coordinate and pressure coefficient data from input directory

        Args:
            inputdir: Input data directory
        Returns:
            xy: Coordinate of panel points
            cp: Dictionary of pressure coefficient of each panel under different degree of attack
        """
        # Get the xy and cp data file name from directory
        # Report error message when directory is invalid
        if os.path.isdir(inputdir) is False:
            raise RuntimeError("The directory is invalid")
        xy_data = glob.glob(inputdir+'xy.dat')
        cp_data = glob.glob(inputdir+'alpha*.dat')

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
                xy = [x.strip().split() for x in f.readlines()]
                xy = [list(map(float, x)) for x in xy[1:]]
        except:
            raise RuntimeError("Error in reading xy data file")

        try:
            cp = {}
            # Define some keywords from file name to be deleted to get the alpha value
            keywords = [inputdir, 'alpha', '.dat']
            for data in cp_data:
                with open(data) as f:
                    for kw in keywords:
                        data = data.replace(kw, '')
                    alpha = float(data)
                    cp[alpha] = [x.strip().split() for x in f.readlines()]
                    cp[alpha] = [float(x[0]) for x in cp[alpha][1:]]
        except:
            raise RuntimeError("Error in reading cp data file")

        return xy, cp


    def compute_chord(self, xy):
        """ Compute the chord length by xy data

        Args:
            xy: Coordinate of panel points
        Returns:
            chord: Chord length of an airfoil
        """
        x = [x[0] for x in xy]
        # Get leading and tailing edge point
        leading, trailing = x.index(max(x)), x.index(min(x))
        return math.sqrt(sum([(xy[leading][i] - xy[trailing][i]) ** 2 for i in range(2)]))


    def cp_decomposition(self, xy, cp):
        """ Do pressure coefficient decomposition for each panel, calculate total Cartesian force coefficients

        Args:
            xy: Coordinate of panel points
            cp: Pressure coefficient of each panel under specific degree of attack
        Returns:
            sum(cx): Total Cartesian force coefficients on direction x
            sum(cy): Total Cartesian force coefficients on direction y
        """
        cx, cy = [], []
        n = len(cp)
        for i in range(n):
            pt1, pt2 = xy[i], xy[i+1]
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
        Returns
            cl: Life coefficient of an airfoil under specific degree of attack
        """
        return cy * math.cos(math.radians(alpha)) - cx * math.sin(math.radians(alpha))


    def find_stagnation_point(self, xy, cp):
        """ Find the stagnation point

        Args:
            xy: Coordinate of panel points
            cp: Pressure coefficient of each panel under specific degree of attack
        Returns:
            List contained coordinate and pressure coefficient of a stagnation point
        """
        # Find the point with its cp value closest to 1.0
        distance_to_1 = [abs(x - 1) for x in cp]
        index = distance_to_1.index(min(distance_to_1))
        pt1, pt2 = xy[index], xy[index+1]
        x, y = (pt2[0] + pt1[0])/2, (pt2[1] + pt1[1])/2

        return [x, y, cp[index]]


    def __repr__(self):
        """ Print results

        Returns:
            summary: String of summary of results
        """
        summary = "alpha     cl           stagnation pt      \n" + \
                  "-----  -------  --------------------------\n"
        alphaList = list(self.cl.keys())
        alphaList.sort()
        for alpha in alphaList:
            pt = self.stagnation_pt[alpha]
            summary += "{:5.2f}  {:7.4f}  ({:7.4f}, {:7.4f}) {:7.4f}\n".format(alpha, self.cl[alpha], pt[0], pt[1], pt[2])

        return summary

