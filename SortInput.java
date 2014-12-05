import java.util.*;
import java.text.*;
import java.io.*;

public class SortInput{

    public String inputFile="";
    private String ouyputFile="";

    private int overheadEnergyCost;
    private Vector<String> sortedData = new Vector<String>();

    public int getOverheadEnergyCost(){
        return this.overheadEnergyCost;
    }

    public Vector<String> getSortedData(){
       return this.sortedData;
    }

    public void sortData(){
        HashMap<Integer, ArrayList<String>> map = new HashMap<Integer, ArrayList<String>>();
        Vector<Integer> keys = new Vector<Integer>();
        ArrayList<String> dataList;

        String s1 = "", id="", str="", sid="";
        String heading="", sortheading="";
        int pos, count=1, len=0;
        try {
            InputStreamReader is = new InputStreamReader(new FileInputStream(new File(inputFile)));
            BufferedReader bufferedreader = new BufferedReader(is);
            id = bufferedreader.readLine();
            this.overheadEnergyCost = Integer.parseInt(id);
            while( (s1 = bufferedreader.readLine()) != null) {
               s1 = s1.trim();
               pos = s1.indexOf(" ");
               str = s1.substring(0, pos);
               len = Integer.parseInt(str);
               if ( !keys.contains(len) )
                 keys.add(len);
               if ( map.get(len) == null ){
                  dataList = new ArrayList<String>();
                  dataList.add(s1);
                  map.put(len, dataList);
               } else {
                  dataList = map.get(len);
                  if ( !dataList.contains(s1) ){
                    dataList.add(s1);
                    map.put(len, dataList);
                  }
               }
            }

        } catch(FileNotFoundException fnfx){
           fnfx.printStackTrace();
        } catch(IOException ioex){
           ioex.printStackTrace();
        }finally {
            Collections.sort(keys);
            int siz = keys.size();
            for(int i=0; i<siz; i++){
               dataList = map.get(keys.elementAt(i));
               for(String data: dataList){
                 sortedData.add(data);
                 System.out.println(data);
               }
            }
        }
   }

   /*
     Tested separately
   */
   /*public static void main(String args[]){
        SortInput psf = new SortInput();
        psf.inputFile = args[0];
        psf.sortData();
   }*/
}               
