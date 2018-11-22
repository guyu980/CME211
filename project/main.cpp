#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "COO2CSR.hpp"
#include "CGSolver.hpp"

int main(int argc, const char * argv[]) {
    int n_row, n_col, row, col, niter;
    double value, tol = 1.e-5;
    std::vector<int> i_idx, j_idx, row_ptr, col_idx;
    std::vector<double> val, b, x;
    std::string matrix_file, solution_file;
    
    if (argc < 3) {
        std::cout << "Usage:" << std::endl
                  << "  ./main <inpiut matrix file name> <output solution file name>" << std::endl;
        return 0;
    }
    else {
        matrix_file = argv[1];
        solution_file = argv[2];
    }
    
    // Read the matrix data in COO format
    std::ifstream f(matrix_file);
    
    if (f.is_open()) {
        f >> n_row >> n_col;
        while (f >> row >> col >> value) {
            i_idx.push_back(row);
            j_idx.push_back(col);
            val.push_back(value);
        }
        f.close();
    }
    else {
        std::cout << "Failed to open input file!" << std::endl;
        return 0;
    }
    
    // Convert the matrix into CSR format
    COO2CSR(val, i_idx, j_idx);
    row_ptr = i_idx;
    col_idx = j_idx;
    
    // Initialize b and starting guess for x
    for (int i = 0; i < n_row; i++) {
        b.push_back(0);
    }
    
    for (int i = 0; i < n_col; i++) {
        x.push_back(1);
    }

    // Run the CG solver
    niter = CGSolver(val, row_ptr, col_idx, b, x, tol);
    std::cout << "SUCCESS: CG solver converged in " << niter << " iterations." << std::endl;
    
    // Write solution into file
    std::ofstream of(solution_file);
    
    if (of.is_open()) {
        of.setf(std::ios::scientific, std::ios::floatfield);
        of.precision(4);
        for (unsigned int i = 0; i < x.size(); i++)
            of << x[i] << std::endl;
        f.close();
    }
    else {
        std::cout << "Failed to open output file!" << std::endl;
        return 0;
    }
    return 0;
}

