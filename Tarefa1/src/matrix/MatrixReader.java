/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package matrix;


import com.opencsv.CSVReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author demis
 */
public class MatrixReader {
    private final String PATH="relevance-matrix.csv";
    
    /**
     * Read the relevance matrix and put it in a HashMap
     * Source: https://pt.stackoverflow.com/questions/27013/como-ler-arquivos-csv-em-java
     * @return 
     */
    public HashMap<String,HashMap> readMatrix(){
        try {
            HashMap<String,HashMap> relevantDocuments=new HashMap<>();
            HashMap<Integer,String> indexToQuery=new HashMap<>();
            CSVReader reader = new CSVReader(new FileReader(PATH));
            String [] nextLine;
            boolean firstLine=true;
            try {
                while ((nextLine = reader.readNext()) != null) {
                    // relevances of queries
                    //position 0 for first query
                    //position 1 for second query and so on
                    HashMap<String,String> relevances=new HashMap<>();
                    if (!firstLine){
                        for(int i=1;i<nextLine.length;i++){
                            relevances.put(indexToQuery.get(i),nextLine[i]);
                        }
                        relevantDocuments.put(nextLine[0], relevances);
                    }
                    else{
                        for(int i=1;i<nextLine.length;i++){
                            indexToQuery.put(i, nextLine[i]);
                        }
                        
                        firstLine=false;
                    }
                }
                //System.out.print(relevantDocuments.get("1709.00411.json"));
                return relevantDocuments;
            } catch (IOException ex) {
                Logger.getLogger(MatrixReader.class.getName()).log(Level.SEVERE, null, ex);
                return null;
            }
        } catch (FileNotFoundException ex) {
            Logger.getLogger(MatrixReader.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }
    }
    
}
