#include <algorithm>
#include <vector>

#include "CGSolver.hpp"
#include "matvecops.hpp"

//--style_1
//--There are no comments!
//--END
int CGSolver(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             double              tol) {
    int niter = 0, nitermax = 100;
    double alpha, beta, rn_rn, norm0, normr;
    std::vector<double> r, p, A_pn;
    
    r = vecSubtract(b, matvecDot(val, row_ptr, col_idx, x));
    norm0 = vecNorm(r);
    p = r;
    
    while (niter < nitermax) {
        niter += 1;
        rn_rn = vecDot(r, r);
        A_pn  = matvecDot(val, row_ptr, col_idx, p);
        alpha = rn_rn / vecDot(p, A_pn);
        x = vecAdd(x, vecMul(alpha, p));
        r = vecSubtract(r, vecMul(alpha, A_pn));
        normr = vecNorm(r);
        
        if (normr / norm0 < tol) break;
        
        beta = vecDot(r, r) / rn_rn;
        p = vecAdd(r, vecMul(beta, p));
    }
    return niter;
}

