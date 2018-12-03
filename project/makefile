CXX := g++
CXXFLAGS := -Wall -Wextra -Wconversion -std=c++11 
#--writeup_1
#--Instead of doing the compilation in one big line it is better to break up your 
#--makefile. This will make it easier to deal with the larger collections of .cpp files.
#--You needed to add at least a rule to create object files from cpp files.
#--START
main: main.cpp CGSolver.hpp COO2CSR.hpp matvecops.hpp
	$(CXX) $(CXXFLAGS) -o main main.cpp CGSolver.cpp COO2CSR.cpp matvecops.cpp
#--END
.PHONY: clean
clean:
	$(RM) main

