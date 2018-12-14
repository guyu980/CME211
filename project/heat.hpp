#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{
  private:
    SparseMatrix A;
    std::vector<double> b, x;

  public:
    HeatEquation2D(void);
    /* Method to setup Ax=b system */
    int Setup(std::string inputfile);

    /* Method to solve system using CGsolver */
    int Solve(std::string soln_prefix);

    /* Method to compute the inverted Gaussian temperature */
    double T_x(double x, double L, double Tc);
    
    /* Method to judge whether two vectors are equal */
    int is_equal(std::vector<double> vec1, std::vector<double> vec2, double tol);
    
    /* Method to get current solution x */
    std::vector<double> get_x(void);
};

#endif /* HEAT_HPP */
