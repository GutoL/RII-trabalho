/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package tarefa1;


import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.Date;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;

/** Simple command-line based search demo. */
public class SearchFiles {

    public SearchFiles() {}

    /** Simple command-line based search demo. */
    public SearchResults search(String line, char stopWords, char steamming, int hitsPerPage) throws Exception {
    
        String indexPath;
        String field = "contents";
        String queries = null;
        int repeat = 0;
        boolean raw = false;
        String queryString = null;
        //int hitsPerPage = 10;//200
        int max = 1000;//200
        //int numberFilesRetrieved = 0;
    
        SearchResults searchResults = new SearchResults();
        searchResults.setOriginalSearchString(line);
    
    
        Analyzer analyzer;
    
        if(stopWords=='0' && steamming=='0'){
          
            indexPath = "index/0/";
            analyzer = new StandardAnalyzer(CharArraySet.EMPTY_SET);     // without stopwords filter/without stemming
          
        }else if(stopWords=='1' && steamming=='0'){
          
            indexPath = "index/1/";
            analyzer = new StandardAnalyzer();                           // with stopwords filter/without stemming
          
        }else if(stopWords=='0' && steamming=='1'){
          
            indexPath = "index/2/";
            analyzer = new  EnglishAnalyzer(CharArraySet.EMPTY_SET);     // without stopwords filter/ with stemming
          
        }else{
          
            indexPath = "index/3/";
            analyzer = new EnglishAnalyzer();                            // with stop words/with stemming
        }
    
        IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(indexPath)));
        IndexSearcher searcher = new IndexSearcher(reader);
        QueryParser parser = new QueryParser(field, analyzer);
        
        line = line.trim();
       
        Query query = parser.parse(line);
        
        searchResults.setSearchString(query.toString(field));
        
        TopDocs results = searcher.search(query, max);
        
        ScoreDoc[] hits = results.scoreDocs;
        int numTotalHits = results.totalHits;
        
        searchResults.setNumerFilesRetrieved(numTotalHits);
        
        
        int end = Math.min(numTotalHits, hitsPerPage);
        
        int cont = 0;
        
        for (int i = 0; i < end; i++) {
            
            Document doc = searcher.doc(hits[i].doc);
            String path = doc.get("path");

            if (path != null) {
              
              searchResults.files.add(path);
              String title = doc.get("title");
              cont++;
            }
            
      }
        
    searchResults.setNumerFilesRetrieved(cont);
    
    reader.close();
    return searchResults;
    
  }

  
}


