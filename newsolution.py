import sys

def firstItem(list):
  return list[0]

def lastItem(list):
   numelements = len(list)
   return list[numelements-1]

def read_flight_paths(r):
   '''NEW CHANGE:
   Read flight paths data from reader r, returning lists of start, 
   finish, and energy in sorted order.  This is more efficient than the first solution'''
  
   starts = []
   finishes = []
   energies = []
   triplelist = []
   for line in r:
     start, finish, energy = line.split()
     tripledata = [int(start), int(finish), int(energy)]
     triplelist.append(tripledata)

   triplelist = sorted(triplelist, key = firstItem)
   
   for i in range(0, len(triplelist)):
     list = triplelist[i]
     starts.append(list[0])
     finishes.append(list[1])
     energies.append(list[2])
   
   return (starts, finishes, energies)
def reducePathLists(listoflists,cost, max):
   mincostlistadded=0
   newlistoflists=[]
   newcost=[]
   i=0
   mincost=cost[i]
   minindex=i
   thislist = listoflists[i]
   thisindex = lastItem(thislist)
   for i in range(1, len(listoflists)):
       newlist = listoflists[i]
       newindex = lastItem(newlist)
       if ( newindex == thisindex ):
          if ( cost[i] < mincost ):
             mincost = cost[i]
             minindex=i
       else:
          newlistoflists.append(newlist)
          newcost.append(cost[i])
   ''' We should use mincost list only once. For example if [0,5],[2,5],[3,5] are checked
       add mincost only once'''
   if ( mincostlistadded == 0 ):
     newlistoflists.append(listoflists[minindex])
     newcost.append(cost[minindex]) 
     mincostlistadded = 1
   return (newlistoflists, newcost)

def process_flight_paths(starts,finishes,energies, energyOverhead):
   '''Return the paths that is optimal. Came home late last night,
      therefore will be working on this today/tomorrow whenever time permits. '''
  
   constliteral = " And "
   costliteral =  " Costs now are "
   check = " check"
   numpaths = 1
   listoflists = []
   cost = [energies[0]]

   found=0
   i=0
   mincost=99999
   minindex=-1
   list = [i]
   listoflists.append(list)

   ''' not only finishes[i], but also from finishes of list's end value's finishes 
       loop through listoflists, get list within them, find the last element and that will be the index
       use that index to determine the finishes[index] and see if that is equal to or smaller than
       starts[i+1]   If it is then add that data row to the list. We need to remove that from listoflists
       and then add the new list to listoflists
       If none of those finishes[index] is equal to or smaller then need to create a new list and add that
       to listoflists. (While doing all these, cost should also be updated)
       Using the word cost synonymously to energy usage
   '''
   print "Number of data rows = ",len(starts)
   for i in range(0, len(starts)-1):
     for j in range(0, len(listoflists)):
        found=0
        thislist = listoflists[j]
        thisindex = lastItem(thislist)
        if ( finishes[thisindex] <= starts[i+1]):
           found=1
           thislist.append(i+1)
           cost[j] = cost[j]+(starts[i+1]-finishes[thisindex])*energyOverhead+energies[i+1] 
           listoflists[j] = thislist
     if ( found == 0):   
        list = [i+1]
        listoflists.append(list)
        '''cost[0]'''
        cost.append((starts[i+1]-starts[0])*energyOverhead+energies[i+1]) 
   
   listoflists, cost = reducePathLists(listoflists, cost, len(starts)-1)

   mincost = cost[0]
   minindex=0
   for i in range(1, len(cost)):
     if ( cost[i] < mincost ):
         mincost = cost[i]
         minindex= i
   newlistoflists=[]  
   newcost=[]
   newcost.append(cost[minindex])
   thislist = listoflists[minindex]
   for i in range(0,len(thislist)):
      id = thislist[i]
      newlistoflists.append((starts[id], finishes[id]))

   '''newlistoflists.append(listoflists[minindex])'''

   print newlistoflists
   return newcost

if __name__ == "__main__":
   input_file = open(sys.argv[1], "r")
   energyOverhead = int(input_file.readline())
   starts, finishes, energies = read_flight_paths(input_file)
   print process_flight_paths(starts, finishes, energies, energyOverhead)
   input_file.close()
