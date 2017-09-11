/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tarefa1;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import matrix.MatrixReader;

/**
 *
 * @author guto
 */
public class SearchResults {
    
    int numerFilesRetrieved;
    String SearchString,originalSearchString;
    ArrayList<String> files = new ArrayList<>();

    public SearchResults() {
    }

    public int getNumerFilesRetrieved() {
        return numerFilesRetrieved;
    }

    public String getSearchString() {
        return SearchString;
    }

    public void setNumerFilesRetrieved(int numerFilesRetrieved) {
        this.numerFilesRetrieved = numerFilesRetrieved;
    }

    public void setSearchString(String SearchString) {
        this.SearchString = SearchString;
    }

    public ArrayList<String> getFiles() {
        return files;
    }

    public String getOriginalSearchString() {
        return originalSearchString;
    }

    public void setOriginalSearchString(String originalSearchString) {
        this.originalSearchString = originalSearchString;
    }
    
    
    
    
    public double precision(HashMap<String,HashMap> relevanceMatrix){
        double precision=0.0;
        int relevantDocuments=0;
        //System.out.print(originalSearchString+ " ORIGINAL");
         for (String file : files){
             String filename=file.split("/")[2];
             //System.out.print("File name: "+filename);
             //System.out.println(relevanceMatrix.get(filename));
             if(relevanceMatrix.get(filename).get(originalSearchString)!=null){
                if(relevanceMatrix.get(filename).get(originalSearchString).equals("1")||relevanceMatrix.get(filename).get(originalSearchString).equals("1-n")){
                    relevantDocuments+=1;
                }
             }
             
         }
         
         if(!files.isEmpty()){
            precision=relevantDocuments/(double)files.size();
         }
         
        return precision;
    }
    
    public double coverage(HashMap<String,HashMap> relevanceMatrix){
        double coverage=0.0;
        int relevantReturnedDocuments=0;
        int relevantDocuments=0;
        for (String file : files){
            String filename=file.split("/")[2];
            if(relevanceMatrix.get(filename).get(originalSearchString)!=null){
                if(relevanceMatrix.get(filename).get(originalSearchString).equals("1")){
                     relevantReturnedDocuments+=1;
                 }
            }
        }
        
        for (Map.Entry<String,HashMap> fileQuery: relevanceMatrix.entrySet()){
            if(fileQuery.getValue().get(originalSearchString)!=null){
                if(fileQuery.getValue().get(originalSearchString).equals("1")){
                    relevantDocuments+=1;
                }
            }
        }
        
        if(relevantDocuments!=0){
            coverage=(double)relevantReturnedDocuments/(double)relevantDocuments;
        }
        return coverage;
    }
    
    public double fmeasure(HashMap<String,HashMap> relevanceMatrix){
        double precision=precision(relevanceMatrix);
        double coverage=coverage(relevanceMatrix);
        return 2*precision*coverage/(precision+coverage);
    }
    
    
    
}
