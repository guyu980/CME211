CXX := g++
#--writeup_2
#--You needed to include an optimization flag to make the program run 
#--fast. You also needed to write a rule to create object files from cpp files.
#--And remove these files with clean. Now you need to recompile all your code even if you change only
#--one small thing.
#--START
CXXFLAGS := -O3 -std=c++11 -Wall -Wconversion -Wextra -pedantic
LDFLAGS := -I/usr/include -L/usr/lib -ljpeg
main: main.cpp hw6.hpp image.hpp
	$(CXX) $(CXXFLAGS) main.cpp hw6.cpp image.cpp -o main $(LDFLAGS)

.PHONY: clean
clean:
	$(RM) main
#--END

