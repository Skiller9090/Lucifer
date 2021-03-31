#include <iostream>

extern "C" {
    int runTests();
}

int runTests(){
    int myInt = 30;
    int dINT = 30*2;
    return (dINT - 10 + (5*2));
}
