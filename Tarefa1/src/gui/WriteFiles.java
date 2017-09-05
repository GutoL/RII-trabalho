/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package gui;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;

/**
 *
 * @author guto
 */
public class WriteFiles {
    
    private String path;

    public WriteFiles(String path) {
        this.path = path;
    }
    
    
    public void write(String number) throws IOException {
    	File file = new File(path);
	
	BufferedWriter writer = new BufferedWriter(new FileWriter(file));
	writer.write(number);
	
	writer.flush();
	writer.close();
	
    }
}
