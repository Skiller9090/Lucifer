#include <stdio.h>
#include "importTest/importTest.h"


int runSimpleMathTest(){
    int doMultiply = 20 * 2;
    int doDivide = 40 / 2;
    int doSub = subMagic(doMultiply, doDivide);
    int doAddition = addMagic(doMultiply, doSub);
    return doAddition;
}

int runTests(){
    int output = runSimpleMathTest();
    return output;  // should be 60
}
