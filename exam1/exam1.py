#!/usr/bin/env python3
#
# CME 211, Fall 2018
# Python Midterm Exam
#

# You can use some or all of these modules
import copy
import math
import sys
import time


class Vector:
    def __init__(self, size, val):
        self.__data=[val]*size
    def __len__(self):
        return len(self.__data)
    def get(self, i):
        return self.__data[i]
    def put(self, i, val):
        self.__data[i] = val

## Your code here ##

#--design_2
#--Accesing internal member from Vector class in
#-- areEqual function.
#--END

#--functionality_3
#--Due to floating point errors, it is possible that both your SparseMatrix and DenseMatrix
#--return the correct solution but u.__data[i] == v.__data[i] returns False, so you should
#--allow a small error.
#--START
def areEqual(u, v):
    return u._Vector__data == v._Vector__data
#--END        


class Matrix:
    def importMatrix(self, filename):
        raise RuntimeError("Not implemented yet")

    def get(self, i, j):
        raise RuntimeError("Not implemented yet")
    
    def entryset(self, i, j, x):
        raise RuntimeError("Not implemented yet")
    
    def matvec(self, v):
        raise RuntimeError("Not implemented yet")
    
    def numCols(self):
        raise RuntimeError("Not implemented yet")
    

class DenseMatrix(Matrix):
    def importMatrix(self, filename):
        with open(filename, 'r') as f:
            data = [x.strip().split() for x in f.readlines() if x[0] != '%']
            data = [list(map(float, x)) for x in data]
        
        data[0][0:2] = [int(x) for x in data[0][0:2]]
        m, n = data[0][0:2]
        matrix = []
        for i in range(m):
            matrix.append([0] * n)
        
        for i in range(1, len(data)):
            matrix[int(data[i][0]-1)][int(data[i][1]-1)] = data[i][2]
        
        self.matrix_size = data[0][0:2]
        self.matrix = matrix

    def get(self, i, j):
        return self.matrix[i][j]

    def entryset(self, i, j, x):
        self.matrix[i, j] = x

    def matvec(self, v):
        m, n = self.matrix_size
        result = Vector(m, 0)
        for i in range(m):
            dot = 0
            for j in range(n):
                dot += self.matrix[i][j] * v.get(j)
            result.put(i, dot)
            
        return result

    def numCols(self):
        return self.matrix_size[1]


class SparseMatrix(Matrix):    
    def importMatrix(self, filename):
        with open(filename, 'r') as f:
            data = [x.strip().split() for x in f.readlines() if x[0] != '%']
            data = [list(map(float, x)) for x in data]
        
        data[0][0:2] = [int(x) for x in data[0][0:2]]
        m, n = data[0][0:2]
        matrix = {}
        
        for i in range(1, len(data)):
            row = int(data[i][0]-1)
            col = int(data[i][1]-1)
            value = data[i][2]
            if row not in matrix:
                matrix[row] = {}
            matrix[row][col] = value
        
        values = []
        colind = []
        rowptr = [0]
        
        for row in matrix:
            colind += list(matrix[row].keys())
            values += list(matrix[row].values())
            rowptr.append(rowptr[-1] + len(matrix[row]))
        
        for i in range(m):
            if i not in matrix:
                rowptr.insert(rowptr[i-1], i)
                
        self.matrix_size = data[0][0:2]
        self.values = values
        self.colind = colind
        self.rowptr = rowptr

    def get(self, i, j):
        output = 0
        if self.rowptr[i+1] > self.rowptr[i]:
            index = self.colind[self.rowptr[i]:self.rowptr[i+1]].index(j)
            if index > -1:
                output = self.values[index]
         
        return output

    def entryset(self, i, j, x):
        if self.rowptr[i+1] == self.rowptr[i]:
            self.colind.insert(self.rowptr[i+1], j)
            self.values.insert(self.rowptr[i+1], x)
            for k in range(i+1, len(self.rowptr)):
                self.rowptr[k] += 1
                
        else:
            if j in self.colind[self.rowptr[i]:self.rowptr[i+1]]:
                index = self.colind[self.rowptr[i]:self.rowptr[i+1]].index(j)
                self.values[index] = x
            else:
                self.colind.insert(self.rowptr[i+1], j)
                self.values.insert(self.rowptr[i+1], x)
        
    def matvec(self, v):
        m, n = self.matrix_size
        result = Vector(m, 0)
        for i in range(m):
            dot = 0
            if self.rowptr[i+1] > self.rowptr[i]:
                for j in range(n):
                    if j in self.colind[self.rowptr[i]:self.rowptr[i+1]]:
                        index = self.colind[self.rowptr[i]:self.rowptr[i+1]].index(j)
                        dot += self.values[self.rowptr[i]+index] * v.get(j)
            result.put(i, dot)
            
        return result

    def numCols(self):
        return self.matrix_size[1]



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage:')
        print('  python {} <matrix market file>'.format(sys.argv[0]))
        sys.exit(0)

    matrixdata = sys.argv[1]

    #
    # The code below this will not work until you implement
    # all `*Matrix` classes and `areEqual` function. You may comment
    # out portions of the code while you are developing and testing
    # your classes and the function. 
    #

    # Declare dense and sparse matrix
    M = DenseMatrix()
    S = SparseMatrix()

    # Load dense matrix
    M.importMatrix(matrixdata)

    # Load sparse matrix
    S.importMatrix(matrixdata)

    # Create vector for testing matvec method
    v = Vector(M.numCols(), 0.1)

    # Dense matrix-vector multiplication
    r = M.matvec(v)

    # Sparse matrix-vector multiplication
    q = S.matvec(v)

    # Verify sparse matrix vector multiplication against the dense one
    if areEqual(r,q):
        print("Sparse matvec verified!")
    else:
        print("Sparse matvec verification failed!")

#--functionality_0
#--Great job!
#--END
