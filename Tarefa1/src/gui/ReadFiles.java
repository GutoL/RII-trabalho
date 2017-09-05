/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package gui;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

/**
 *
 * @author guto
 * 
 */
public class ReadFiles {
    // Font: http://www.guj.com.br/t/ler-e-escrever-arquivo-txt/84858/4
    //private String namefile;
    private File file;
    
    public ReadFiles(String nameFile){
     
        file = new File(nameFile);
        
    }
    
	
    public ArrayList<String> read() throws IOException{
	ArrayList<String> values = new ArrayList();
        FileReader fileReader = new FileReader(file);
	BufferedReader reader = new BufferedReader(fileReader);
	String data = null;
	
        while((data = reader.readLine()) != null){
		values.add(data);
	}
	
        fileReader.close();
	reader.close();
        return values;
    }
	
}
