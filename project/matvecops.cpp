#include <algorithm>
#include <vector>
#include <math.h>
#include <iostream>

#include "matvecops.hpp"

/* Dot product of matrix with CSR format matrix and vector */
std::vector<double> matvecDot(std::vector<double> val,
                              std::vector<int>    row_ptr,
                              std::vector<int>    col_idx,
                              std::vector<double> vec) {
    unsigned int n, idx;
    double sum;
    std::vector<double> dot;
    
    for (unsigned int i = 0; i < row_ptr.size()-1; i++) {
        sum = 0;
        n = unsigned(row_ptr[i+1] - row_ptr[i]);
        for (unsigned int j = 0; j < n; j++) {
            idx = unsigned(row_ptr[i]) + j;
            sum += val[idx] * vec[unsigned(col_idx[idx])];
        }
        dot.push_back(sum);
    }
    return dot;
}

/* Add two vectors */
std::vector<double> vecAdd(std::vector<double> vec1,
                           std::vector<double> vec2) {
    std::vector<double> vec;
    
    for (unsigned int i = 0; i < vec1.size(); i++)
        vec.push_back(vec1[i] + vec2[i]);
    
    return vec;
}

/* Subtract two vectors */
std::vector<double> vecSubtract(std::vector<double> vec1,
                                std::vector<double> vec2) {
    std::vector<double> vec;
    
    for (unsigned int i = 0; i < vec1.size(); i++)
        vec.push_back(vec1[i] - vec2[i]);
    
    return vec;
}

/* Multiply constant to vector */
std::vector<double> vecMul(double a, std::vector<double> vec) {
    std::vector<double> vec1;
    
    for (unsigned int i = 0; i < vec.size(); i++)
        vec1.push_back(a * vec[i]);
    
    return vec1;
}

/* Dot product of two vectors */
double vecDot(std::vector<double> vec1,
              std::vector<double> vec2) {
    double sum = 0;
    
    for (unsigned int i = 0; i < vec1.size(); i++)
        sum += vec1[i] * vec2[i];
    
    return sum;
}

/* L2 Norm of a vector */
double vecNorm(std::vector<double> vec) {
    double norm = 0;
    
    for (unsigned int i = 0; i < vec.size(); i++)
        norm += vec[i] * vec[i];
    
    return sqrt(norm);
}

