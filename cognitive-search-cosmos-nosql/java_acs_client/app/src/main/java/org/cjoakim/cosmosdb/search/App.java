package org.cjoakim.cosmosdb.search;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.FileWriter;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.HashMap;
import java.util.Map;

/**
 * Simple Console application to invoke Azure Cognitive Search, implemented as
 * a single class - App.
 * 
 * Command-line arguments expect an <index-name> and a <predefined-search-name>.
 * See file build.gradle
 *
 * Chris Joakim, Microsoft
 */

public class App {

    public static void main(String[] args) {

        try {
            String indexName  = args[0];
            String searchName = args[1];
            Map<String, String> postData = buildPostData(searchName);
            System.out.println("postData: " + mapToJson(postData));
            
            HttpClient client = HttpClient.newHttpClient();  // client can be a long-running object in your app
            
            long startMs = System.currentTimeMillis(); 

            HttpRequest request = buildHttpClient(indexName, postData);
            var response = client.send(request, HttpResponse.BodyHandlers.ofString());

            long elapsedMs = System.currentTimeMillis() - startMs;

            System.out.println("http statusCode: " + response.statusCode() + ", elapsed ms: " + elapsedMs);

            String prettyJson = parseResponseData(response.body());
            System.out.println(prettyJson);
            Thread.sleep(100);

            String outfile = "tmp/" + indexName + "-" + searchName + "-" + System.currentTimeMillis() + ".json";
            writeTextFile(outfile, prettyJson);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static Map<String, String> buildPostData(String searchName) {

        HashMap<String, String> postData = new HashMap<String, String>();

        switch (searchName) {

            // gradle search_all_airports --warning-mode all
            case "all_airports":
                postData.put("count", "true");
                postData.put("search", "*");
                postData.put("orderby", "pk");
                break;

            // gradle search_clt_airport --warning-mode all
            case "clt_airport":
                postData.put("queryType", "simple");
                postData.put("count", "true");
                postData.put("search", "pk eq 'CLT'");
                break;

            // gradle search_charlotte_douglas_airport --warning-mode all
            case "charlotte_douglas_airport":
                postData.put("queryType", "simple");
                postData.put("count", "true");
                postData.put("search", "pk eq 'Charlotte Douglas'");
                break;

            // gradle search_airports_eastus_cl --warning-mode all
            case "airports_eastus_cl":
                postData.put("queryType", "full");
                postData.put("count", "true");
                postData.put("search", "tz:New_York~ AND pk:CL*");
                postData.put("select", "pk,doc_id,name,city,latitude,tz");
                postData.put("orderby", "latitude desc");
                break;

            // gradle search_airports_eastus_cl_south --warning-mode all
            case "airports_eastus_cl_south":
                postData.put("queryType", "full");
                postData.put("count", "true");
                postData.put("search", "tz:New_York~ AND pk:CL*");
                postData.put("filter", "latitude lt 39.0");                // <-- numeric filter
                postData.put("select", "pk,doc_id,name,city,latitude,tz");
                postData.put("orderby", "latitude desc");
                break;

            // gradle search_routes_jfk_mia --warning-mode all
            case "routes_jfk_mia":
                postData.put("queryType", "full");
                postData.put("count", "true");
                postData.put("search", "pk:JFK\\:MIA");
                break;

            // gradle search_routes_nested --warning-mode all
            case "routes_nested":
                postData.put("queryType", "full");
                postData.put("count", "true");
                postData.put("search", "source_airport/iata:CLT AND dest_airport/country:Canada");  // <-- nested fields search
                postData.put("select", "pk,doc_id,airline,source_airport,dest_airport");
                postData.put("orderby", "dest_airport/city");                                       // <-- order by nested field
                break;

            // gradle search_routes_joakim --warning-mode all
            case "routes_joakim":
                postData.put("queryType", "simple");
                postData.put("count", "true");
                postData.put("search", "frequent_passengers/*:Joakim");  // <-- find in an array of strings
                break;

            default:
                System.out.println("undefined searchName: " + searchName);
        }
        return postData;
    }

    public static HttpRequest buildHttpClient(String indexName, Map<String, String> postDataMap) throws URISyntaxException {

        StringBuffer sb = new StringBuffer();
        sb.append(System.getenv("AZURE_SEARCH_URL"));
        sb.append("/indexes/");
        sb.append(indexName);
        sb.append("/docs/search?api-version=2021-04-30-Preview");
        String url = sb.toString();
        System.out.println("url: " + url);

        String key = System.getenv("AZURE_SEARCH_QUERY_KEY");
        String json = mapToJson(postDataMap);

        return HttpRequest.newBuilder()
                .uri(new URI(url))
                .headers("Content-Type", "application/json", "api-key", key)
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();
    }

    private static String buildSearchUrl(String indexName) {

        StringBuffer sb = new StringBuffer();
        sb.append(System.getenv("AZURE_SEARCH_URL"));
        sb.append("/indexes/");
        sb.append(indexName);
        sb.append("/docs/search?api-version=2021-04-30-Preview");
        return sb.toString();
    }

    private static String mapToJson(Map<String, String> postDataMap) {

        ObjectMapper mapper = new ObjectMapper();

        try {
            return mapper.writeValueAsString(postDataMap);
        }
        catch (JsonProcessingException e) {
            e.printStackTrace();
            return null;
        }
    }

    private static String parseResponseData(String respJson) {

        ObjectMapper mapper = new ObjectMapper();

        try {
            HashMap<Object, Object> respObj = mapper.readValue(respJson, HashMap.class);
            return  mapper.writerWithDefaultPrettyPrinter().writeValueAsString(respObj);
        }
        catch (JsonProcessingException e) {
            e.printStackTrace();
            return null;
        }
    }

    private static void writeTextFile(String outfile, String text) throws Exception {

        FileWriter fw = null;
        try {
            fw = new FileWriter(outfile);
            fw.write(text);
            System.out.println("file written: " + outfile);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        finally {
            if (fw != null) {
                fw.close();
            }
        }
    }
}
