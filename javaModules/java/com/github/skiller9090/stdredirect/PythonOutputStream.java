package com.github.skiller9090.stdredirect;

import java.io.IOException;
import java.io.OutputStream;

import com.github.skiller9090.stdredirect.PythonPipe;


public class PythonOutputStream extends OutputStream {
    private PythonPipe stdoutPythonPipe;
    private String buffer = "";

    public void setPythonStdout(PythonPipe pythonPipe){
        stdoutPythonPipe = pythonPipe;
    }

    public void write(int arg0) throws IOException{
        if (arg0 == 13){  // Disallow carriage returns for now
            return;
        }
        buffer += Character.toString((char) arg0);
    }

    @Override
    public void write(byte[] b, int off, int len) throws IOException, NullPointerException, IndexOutOfBoundsException {
        if (off < 0 || len < 0 || off + len > b.length){
            throw new ArrayIndexOutOfBoundsException ();
        }
        for (int i = 0; i < len; ++i){
            write (b[off + i]);
        }
    }

    @Override
    public void write (byte[] b) throws IOException, NullPointerException {
         write (b, 0, b.length);
    }

    @Override
    public void flush(){
        String toWrite = buffer;
        buffer = "";
        stdoutPythonPipe.write(toWrite);
    }
}
