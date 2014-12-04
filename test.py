import sys

def findStartIndex(j, starts):
   i=0
   found=0
   retval = -1

   while ( i < 5000 and (found==0) ):
      if ( starts[i] == j ):
          found = 1
          retval = i
      i = i+1

   return retval

def sortFinish(largstr, starts, finishes, energies):
   sortedstarts = sorted(starts)
   i=0
   arindex=0

   rstarts = []
   rfinishes = []
   renergies = []

   print "len = ",len(sortedstarts)
   for i in range(0, len(sortedstarts)):
         arindex = findStartIndex(sortedstarts[i],starts)
         if ( arindex > -1 ):
           rstarts.append(starts[arindex])
           rfinishes.append(finishes[arindex])
           renergies.append(energies[arindex])

   return (rstarts, rfinishes, renergies)

def read_flight_paths(r):
   '''Read flight paths data from reader r, returning lists of start,
   finish, and energy.'''

   starts = []
   finishes = []
   energies = []
   largstr = 0
   
   for line in r:
     start, finish, energy = line.split()
     starts.append(int(start))
     finishes.append(int(finish))
     energies.append(int(energy))
     if ( start > largstr ):
       largstr = start

   starts,finishes,energies = sortFinish(largstr,starts,finishes, energies)
   return (starts, finishes, energies)

def lastItem(list):
   numelements = len(list)
   return list[numelements-1]

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
   minindex=0
   mincost=99999
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
     minindex=-1
     for j in range(0, len(listoflists)):
        found=0
        thislist = listoflists[j]
        thisindex = lastItem(thislist)
        if ( finishes[thisindex] <= starts[i+1] ):
           found=1
           thislist.append(i+1)
           cost[j] = cost[j]+(starts[i+1]-finishes[thisindex])*energyOverhead+energies[i+1]
           listoflists[j] = thislist
     if ( found == 0):
        list = [i+1]
        listoflists.append(list)
        cost.append(cost[0]+(starts[i+1]-starts[0])*energyOverhead+energies[i+1])
   listoflists, cost = reducePathLists(listoflists, cost, len(starts)-1)

   print listoflists
   return cost

if __name__ == "__main__":
   input_file = open(sys.argv[1], "r")
   energyOverhead = int(input_file.readline())
   starts, finishes, energies = read_flight_paths(input_file)
   print process_flight_paths(starts, finishes, energies, energyOverhead)
   input_file.close()

