#include "heat.hpp"
#include "CGSolver.hpp"
#include "matvecops.hpp"
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>

HeatEquation2D::HeatEquation2D (void) {}

/* Method to setup Ax=b system */
int HeatEquation2D::Setup(std::string inputfile) {
    int n_l, n_w, n, i_A;
    double length, width, h, Tc, Th;
    std::ifstream f(inputfile);
    
    /* Load parameters from input file */
    if (f.is_open())
        f >> length >> width >> h >> Tc >> Th;
    else {
        std::cout << "Failed to open input file!" << std::endl;
        return 1;
    }

    /* Compute the number of considered points in two directions */
    /* Each point has one function in the system */
    /* The size of the sysytem is (n_points * n_points) */
    n_l = (int) (length / h);
    n_w = (int) (width / h - 1);
    n = n_l * n_w;
    A.Resize(n, n);

    /* Generate sparse matrix of the system in COO format */
    for (int j = 0; j < n_l; j++) {
        /* j=0 means the periodic boundary points */
        /* Its function variables involve special index chanching */
        if (j == 0)
            for (int i = 0; i < n_w; i++) {
                i_A = j*n_w + i;
                A.AddEntry(i_A, i_A, 4);
                /* i=0 means the first periodic boundary point */
                /* Its function includes hot isothermal boundary point */
                if (i == 0) {
                    A.AddEntry(i_A, i_A+1, -1);
                    A.AddEntry(i_A, i_A+n_w, -1);
                    A.AddEntry(i_A, n-n_w, -1);
                    b.push_back(Th);
                }
                /* 0<i<n_w-1 means the interior periodic boundary points */
                else if (i < n_w - 1) {
                    A.AddEntry(i_A, i_A-1, -1);
                    A.AddEntry(i_A, i_A+1, -1);
                    A.AddEntry(i_A, i_A+n_w, -1);
                    A.AddEntry(i_A, n-n_w+i, -1);
                    b.push_back(0);
                }
                /* i=n_w-1 means the last periodic boundary point */
                /* Its function includes cold isothermal boundary point */
                else {
                    A.AddEntry(i_A, i_A-1, -1);
                    A.AddEntry(i_A, i_A+n_w, -1);
                    A.AddEntry(i_A, n-1, -1);
                    b.push_back(T_x(j*h, length, Tc));
                }
            }
        /* 0<j<n_l-1 means the interior points */
        else if (j < n_l - 1)
            for (int i = 0; i < n_w; i++) {
                i_A = j*n_w + i;
                A.AddEntry(i_A, i_A, 4);
                /* i=0 means the first row point */
                /* Its function includes hot isothermal boundary point */
                if (i == 0) {
                    A.AddEntry(i_A, i_A+1, -1);
                    A.AddEntry(i_A, i_A+n_w, -1);
                    A.AddEntry(i_A, i_A-n_w, -1);
                    b.push_back(Th);
                }
                /* 0<i<n_w-1 means the normal interior points */
                else if (i < n_w - 1) {
                    A.AddEntry(i_A, i_A-1, -1);
                    A.AddEntry(i_A, i_A+1, -1);
                    A.AddEntry(i_A, i_A+n_w, -1);
                    A.AddEntry(i_A, i_A-n_w, -1);
                    b.push_back(0);
                }
                /* i=n_w-1 means the last row point */
                /* Its function includes cold isothermal boundary point */
                else {
                    A.AddEntry(i_A, i_A-1, -1);
                    A.AddEntry(i_A, i_A+n_w, -1);
                    A.AddEntry(i_A, i_A-n_w, -1);
                    b.push_back(T_x(j*h, length, Tc));
                }
            }
        /* j=n_l-1 means the last column of interior boundary points */
        /* Its function variables involve special index chanching */
        else
            for (int i = 0; i < n_w; i++) {
                i_A = j*n_w + i;
                A.AddEntry(i_A, i_A, 4);
                /* i=0 means the first row point */
                /* Its function includes hot isothermal boundary point */
                if (i == 0) {
                    A.AddEntry(i_A, i_A+1, -1);
                    A.AddEntry(i_A, i_A-n_w, -1);
                    A.AddEntry(i_A, i, -1);
                    b.push_back(Th);
                }
                /* 0<i<n_w-1 means the normal interior points */
                else if (i < n_w - 1) {
                    A.AddEntry(i_A, i_A-1, -1);
                    A.AddEntry(i_A, i_A+1, -1);
                    A.AddEntry(i_A, i_A-n_w, -1);
                    A.AddEntry(i_A, i, -1);
                    b.push_back(0);
                }
                /* i=n_w-1 means the last row point */
                /* Its function includes cold isothermal boundary point */
                else {
                    A.AddEntry(i_A, i_A-1, -1);
                    A.AddEntry(i_A, i_A-n_w, -1);
                    A.AddEntry(i_A, i, -1);
                    b.push_back(T_x(j*h, length, Tc));
                }
            }
    }

    /* Initialize x = 0 */
    x.insert(x.begin(), (unsigned long) n, 0);
    return 0;
}

int HeatEquation2D::Solve(std::string soln_prefix) {
    std::vector<int> row_ptr, col_idx;
    std::vector<double> val, Ax;
    int niter;
    double tol = 1.e-10;
    /* Convert system martix into CSR format */
    A.ConvertToCSR();
    val = A.get_a();
    row_ptr = A.get_i_idx();
    col_idx = A.get_j_idx();
    niter = CGSolver(val, row_ptr, col_idx, b, x, soln_prefix, tol);
    if (niter > 0) {
        std::cout << "SUCCESS: CG solver converged in " << niter << " iterations." << std::endl;
        return 0;
    }
    else
        return 1;
}

/* Method to compute the inverted Gaussian temperature */
double HeatEquation2D::T_x(double x, double L, double Tc) {
    return -Tc*(exp(-10*pow(x-L/2, 2))-2);
}

/* Method to judge whether two vectors are equal */
int HeatEquation2D::is_equal(std::vector<double> vec1, std::vector<double> vec2, double tol) {
    std::vector<double> vec;
    vec = vecSubtract(vec1, vec2);
    if (vecNorm(vec) < tol)
        return 1;
    else
        return 0;
}

/* Method to get current solution x */
std::vector<double> HeatEquation2D::get_x(void) {
    return x;
}

//--correctness_0
//--Your code meets the requirements and works well ! Be careful in your include statements !
//--END

//--style_1
//--Your code is quite well written, but you are making a copy of all the arguments before solving. This is very inefficient and makes the use of the 
//--object HeatEquation inefficient ! You should have adapter your CGSolver to be able to take a sparse matrix as input, saving a lot of copies !
//--END