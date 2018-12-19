#ifndef CGSOLVER_HPP
#define CGSOLVER_HPP

#include <vector>

//--correctness_0
//--Your code does not compile without the include<string> flag...
//--END

/* Function that implements the CG algorithm for a linear system
 *
 * Ax = b
 *
 * where A is in CSR format.  The starting guess for the solution
 * is provided in x, and the solver runs a maximum number of iterations
 * equal to the size of the linear system.  Function returns the
 * number of iterations to converge the solution to the specified
 * tolerance, or -1 if the solver did not converge.
 */

int CGSolver(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             std::string         &output_file,
             double              tol);

/* Method to write current solution during iteration */
void writeOuput(std::vector<double> &x,
                std::string         &output_file,
                int                 niter,
                bool                is_converge);
#endif /* CGSOLVER_HPP */
