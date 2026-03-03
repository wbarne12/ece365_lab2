CXX=		gcc
CXXFLAGS=	-g -Wall -std=c11
SHELL=		bash
PROGRAMS=	main

all:            main

main: main.c
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(PROGRAMS)