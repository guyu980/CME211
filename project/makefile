CXX := g++
CXXFLAGS := -Wall -Wextra -Wconversion -std=c++11 -fsanitize=address

main: main.cpp CGSolver.hpp COO2CSR.hpp matvecops.hpp
	$(CXX) $(CXXFLAGS) -o main main.cpp CGSolver.cpp COO2CSR.cpp matvecops.cpp

.PHONY: clean
clean:
	$(RM) main

