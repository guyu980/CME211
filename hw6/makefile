CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wconversion -Wextra -pedantic
LDFLAGS := -I/usr/include -L/usr/lib -ljpeg

main: main.cpp hw6.hpp image.hpp
	$(CXX) $(CXXFLAGS) main.cpp hw6.cpp image.cpp -o main $(LDFLAGS)

.PHONY: clean
clean:
	$(RM) main

