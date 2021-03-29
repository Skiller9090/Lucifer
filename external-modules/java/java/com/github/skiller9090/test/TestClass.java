package com.github.skiller9090.test;

public class TestClass {
    // This class is just to test if java compile, build, and run is working in lucifer.
    public int test = 0;

    public TestClass() {
        System.out.println("TestClass Constructed!");
    }

    public int getTest() {
        return this.test;
    }

    public void setTest(int var1) {
        this.test = var1;
    }
}
