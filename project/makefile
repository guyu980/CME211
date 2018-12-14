CXX := g++
CXXFLAGS := -O3 -Wall -Wextra -Wconversion -std=c++11

TARGET := main
OBJS := main.o CGSolver.o COO2CSR.o matvecops.o heat.o sparse.o
INCS := CGSolver.hpp COO2CSR.hpp matvecops.hpp heat.hpp sparse.hpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

main.o: main.cpp heat.hpp
	$(CXX) -c -o main.o main.cpp $(CXXFLAGS)
CGSolver.o: CGSolver.cpp CGSolver.hpp matvecops.hpp
	$(CXX) -c -o CGSolver.o CGSolver.cpp $(CXXFLAGS)
COO2CSR.o: COO2CSR.cpp COO2CSR.hpp
	$(CXX) -c -o COO2CSR.o COO2CSR.cpp $(CXXFLAGS)
matvecops.o: matvecops.cpp matvecops.hpp
	$(CXX) -c -o matvecops.o matvecops.cpp $(CXXFLAGS)
heat.o: heat.cpp heat.hpp CGSolver.hpp matvecops.hpp
	$(CXX) -c -o heat.o heat.cpp $(CXXFLAGS)
sparse.o: sparse.cpp COO2CSR.hpp matvecops.hpp
	$(CXX) -c -o sparse.o sparse.cpp $(CXXFLAGS)

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)

