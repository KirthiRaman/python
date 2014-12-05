import java.util.ArrayList;
import java.util.Vector;

public class FindOptimalCostPath {

  private ArrayList<ArrayList<Integer>> pathlist = new ArrayList<ArrayList<Integer>>();
  private ArrayList<Integer> costlist  = new ArrayList<Integer>();

  private Vector<String> inputList = new Vector<String>();

  public String inputFileName="";

  private int overheadEnergyCost;

  private Vector<Integer> starts   = new Vector<Integer>();
  private Vector<Integer> finishes = new Vector<Integer>();
  private Vector<Integer> energies = new Vector<Integer>();

    private void populatePathData(){
        for(String dataTriple : inputList){
          String row[] = dataTriple.split(" ");
          starts.add(Integer.parseInt(row[0]));
          finishes.add(Integer.parseInt(row[1]));
          energies.add(Integer.parseInt(row[2]));
        }
    }

    private void reducePathLists(){
       boolean mincostlistadded = false;
       ArrayList<ArrayList<Integer>> newpathlist = new ArrayList<ArrayList<Integer>>();
       ArrayList<Integer> newcostlist = new ArrayList<Integer>();

       int i=0;
       int mincost = costlist.get(i);
       int newindex, minindex = i;
       ArrayList<Integer> thislist = pathlist.get(i);
       int thisindex = thislist.get(thislist.size()-1);
       for (i=1; i<pathlist.size(); i++){
           ArrayList<Integer> newlist = pathlist.get(i);
           newindex = newlist.get(newlist.size()-1);
           if ( newindex == thisindex ){
              if ( costlist.get(i) < mincost ){
                mincost = costlist.get(i);
                minindex = i;
              }
           } else {
             newpathlist.add(newlist);
             newcostlist.add(costlist.get(i));
           }
         if ( !mincostlistadded ){
            newpathlist.add(pathlist.get(minindex));
            newcostlist.add(costlist.get(minindex));
            mincostlistadded = true;
         }
       }
 
       pathlist = newpathlist;
       costlist = newcostlist;
    }

    public void findOptimalPath(){
         int siz = 0, thisindex, thissize;
         boolean found = false;
         ArrayList<Integer> thislist;

         SortInput sinp = new SortInput();
         sinp.inputFile = inputFileName;
         sinp.sortData();
         this.overheadEnergyCost = sinp.getOverheadEnergyCost();
         this.inputList = sinp.getSortedData();
         populatePathData();

         siz = inputList.size();
         ArrayList headlist = new ArrayList();
         headlist.add(0);
         pathlist.add(headlist);
         costlist.add(energies.get(0));

         for(int i=0; i<siz-1; i++){
          for(int j=0; j<pathlist.size(); j++){
             found = false;
             thislist = pathlist.get(j);
             thissize = thislist.size();
             thisindex = thislist.get(thislist.size()-1);
             if ( finishes.get(thisindex) <= starts.get(i+1) ){
                 found = true;
                 thislist.add(i+1);
                 costlist.set(j,costlist.get(j)+(starts.get(i+1)-finishes.get(thisindex))*overheadEnergyCost+energies.get(i+1));
                 pathlist.set(j, thislist);
             }
          }
          if ( !found ){
            ArrayList<Integer> newlist = new ArrayList();
            newlist.add(i+1);
            pathlist.add(newlist);
            costlist.add((starts.get(i+1)-starts.get(0))*overheadEnergyCost+energies.get(i+1));
          }
        }
         reducePathLists();

         int mincost = costlist.get(0);
         int minindex = 0;
         for(int i=1; i<costlist.size(); i++){
            if ( costlist.get(i) < mincost ){
               mincost = costlist.get(i);
               minindex = i;
            }
         }
         ArrayList<ArrayList<Integer>> newlistoflist = new ArrayList<ArrayList<Integer>>();
         ArrayList<Integer> newcostlist = new ArrayList<Integer>();
         newcostlist.add(costlist.get(minindex));
         newlistoflist.add(pathlist.get(minindex));

         pathlist = newlistoflist;
         int count=0;
         System.out.println("[");
           siz = pathlist.size();
           for(int i=0; i<siz; i++){
              thislist = pathlist.get(i);
              for(int j=0; j<thislist.size(); j++){
                 if ( i == siz-1 && j == thislist.size()-1 )
                   System.out.print("("+starts.get(thislist.get(j))+","+finishes.get(thislist.get(j))+")");
                 else
                   System.out.print("("+starts.get(thislist.get(j))+","+finishes.get(thislist.get(j))+"), ");
                 count++;
                 if ( count%6 == 0 )
                   System.out.println();
              }
           }
         System.out.print("]");
         System.out.println();
         System.out.println(newcostlist);
    }


   static public void main(String args[]){
       FindOptimalCostPath fcp = new FindOptimalCostPath();
       fcp.inputFileName = args[0];
       fcp.findOptimalPath();
   }
}
