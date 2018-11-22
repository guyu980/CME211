#ifndef matvecops_hpp
#define matvecops_hpp

#include <vector>

/* Dot product of matrix with CSR format matrix and vector */
std::vector<double> matvecDot(std::vector<double> val,
                              std::vector<int>    row_ptr,
                              std::vector<int>    col_idx,
                              std::vector<double> vec);

/* Add two vectors */
std::vector<double> vecAdd(std::vector<double> vec1,
                           std::vector<double> vec2);

/* Subtract two vectors */
std::vector<double> vecSubtract(std::vector<double> vec1,
                                std::vector<double> vec2);

/* Multiply constant to vector */
std::vector<double> vecMul(double a, std::vector<double> vec);

/* Dot product of two vectors */
double vecDot(std::vector<double> vec1,
              std::vector<double> vec2);

/* L2 Norm of a vector */
double vecNorm(std::vector<double> vec);

#endif /* matvecops_hpp */

