#include "CGSolver.hpp"
#include "matvecops.hpp"
#include <algorithm>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>

/* Function that implements the CG algorithm for a linear system */
int CGSolver(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             std::string         &soln_prefix,
             double              tol) {
    int niter = 0, nitermax = 1000;
    double alpha, beta, rn_rn, norm0, normr;
    std::vector<double> r, p, Ax, A_pn, a_p, a_A_pn, b_p;
    
    /* Initialization */
    Ax = matvecDot(val, row_ptr, col_idx, x);
    r = vecSubtract(b, Ax);
    norm0 = vecNorm(r);
    p = r;
    
    while (niter < nitermax) {
        niter += 1;
        rn_rn = vecDot(r, r);
        A_pn  = matvecDot(val, row_ptr, col_idx, p);
        /* Update alpha */
        alpha = rn_rn / vecDot(p, A_pn);
        a_p = vecMul(alpha, p);
        /* Update x */
        x = vecAdd(x, a_p);
        a_A_pn = vecMul(alpha, A_pn);
        r = vecSubtract(r, a_A_pn);
        /* Update norm of r */
        normr = vecNorm(r);
        
        if (normr / norm0 < tol) break;
        
        /* Update beta */
        beta = vecDot(r, r) / rn_rn;
        b_p = vecMul(beta, p);
        /* Update p */
        p = vecAdd(r, b_p);
        
        /* Write result in every 10 iterations */
        if (niter == 1 || niter % 10 == 0)
            writeOuput(x, soln_prefix, niter, false);
    }
    
    if (niter < nitermax) {
        writeOuput(x, soln_prefix, niter, true);
        return niter;
    }
    else
        return 0;
}

/* Method to write current solution during iteration */
void writeOuput(std::vector<double> &x, std::string &soln_prefix, int niter, bool is_converge) {
    std::string output_file = soln_prefix;
    if (is_converge) {
        output_file.insert(output_file.size(), "_converge.txt");
    }
    else {
        if (niter >= 100) {
            output_file.insert(output_file.size(), std::to_string(niter));
            output_file.insert(output_file.size(), ".txt");
        }
        else if (niter >= 10) {
            output_file.insert(output_file.size(), "0");
            output_file.insert(output_file.size(), std::to_string(niter));
            output_file.insert(output_file.size(), ".txt");
        }
        else {
            output_file.insert(output_file.size(), "00");
            output_file.insert(output_file.size(), std::to_string(niter));
            output_file.insert(output_file.size(), ".txt");
        }
    }
    
    /* Write solution into file */
    std::ofstream of(output_file);

    if (of.is_open()) {
        for  (unsigned int i = 0; i < x.size(); i++)
            of << x[i] << std::endl;
        of.close();
    }
    else {
        std::cout << "Failed to open output file!" << std::endl;
    }
}
