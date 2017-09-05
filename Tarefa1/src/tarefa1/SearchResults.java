/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tarefa1;

import java.util.ArrayList;

/**
 *
 * @author guto
 */
public class SearchResults {
    
    int numerFilesRetrieved;
    String SearchString;
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
    
    
    
    
}
