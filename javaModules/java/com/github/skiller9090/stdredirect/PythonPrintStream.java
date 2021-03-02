package com.github.skiller9090.stdredirect;

import java.io.PrintStream;
import java.io.OutputStream;


public class PythonPrintStream extends PrintStream {
    public PythonPrintStream(){
        super(new PythonOutputStream(), true);
    }

    public void setPythonStdout(PythonPipe pythonPipe){
        if (out instanceof PythonOutputStream) {
            PythonOutputStream pythonOutputStream = (PythonOutputStream) out;
            pythonOutputStream.setPythonStdout(pythonPipe);
        }
    }
}
