#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <vector>

class SparseMatrix {
  private:
    std::vector<int> i_idx;
    std::vector<int> j_idx;
    std::vector<double> a;
    int ncols;
    int nrows;

  public:
    SparseMatrix(void);
    /* Method to modify sparse matrix dimensions */
    void Resize(int nrows, int ncols);

    /* Method to add entry to matrix in COO format */
    void AddEntry(int i, int j, double val);

    /* Method to convert COO matrix to CSR format using provided function */
    void ConvertToCSR(void);

    /* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
    std::vector<double> MulVec(std::vector<double> &vec);

    /* Method to get sparse matrix */
    std::vector<int> get_i_idx(void);
    std::vector<int> get_j_idx(void);
    std::vector<double> get_a(void);
    
};

#endif /* SPARSE_HPP */
