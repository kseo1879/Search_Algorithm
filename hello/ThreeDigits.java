import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;
 
class Node{
    private Node parent;
    private int changedDigit;
    private int value;
    private int depth;
 
    public Node(int value,Node parent, int changedDigit){
        this.value = value;
        this.parent = parent;
        this.changedDigit = changedDigit;
        if(parent == null){
            this.depth = 0;
        }
        else{
            this.depth = this.parent.getDepth()+1;
        }
    }
 
    public ArrayList<Node> getChildren(){
        ArrayList<Node> childrens = new ArrayList<>();
        addFirstChildrens(childrens);
        addSecondChildrens(childrens);
        addThirdChildrens(childrens);
        return childrens;
    }
 
    private void addFirstChildrens(ArrayList<Node> childrens){
        if(changedDigit != 1){
            if(this.value < 100){
                childrens.add(new Node(this.value + 100, this, 1));
                return;
            }
            int firstDigit = (this.value/100)%10;
            if(firstDigit >= 1){
                childrens.add(new Node(this.value - 100, this, 1));
            }
            if(firstDigit < 9){
                childrens.add(new Node(this.value + 100, this, 1));
            }
        }
    }
 
    private void addSecondChildrens(ArrayList<Node> childrens){
        if(changedDigit != 2){
            if(this.value < 10){
                childrens.add(new Node(this.value + 10, this, 2));
                return;
            }
            int secondDigit = (this.value/10)%10;
            if(secondDigit >= 1){
                childrens.add(new Node(this.value - 10, this, 2));
            }
            if(secondDigit < 9){
                childrens.add(new Node(this.value + 10, this, 2));
            }
        }
    }
 
    private void addThirdChildrens(ArrayList<Node> childrens){
        if(changedDigit != 3){
            if(this.value == 0){
                childrens.add(new Node(this.value + 1, this, 3));
                return;
            }
            int thirdDigit = this.value%10;
            if(thirdDigit >= 1){
                childrens.add(new Node(this.value - 1, this, 3));
            }
            if(thirdDigit < 9){
                childrens.add(new Node(this.value + 1, this, 3));
            }
        }
    }
 
    public int getDepth() {
        return depth;
    }
 
    public Node getParent() {
        return parent;
    }
 
    public int getValue() {
        return value;
    }
 
    public int getChangedDigit() {
        return changedDigit;
    }
 
    public int getDistance(int goal){
        return(Math.abs( (this.value%10) - (goal%10) ) + Math.abs( ( (this.value/10)%10 ) - ( (goal/10)%10) ) + Math.abs( ( (this.value/100)%10 ) - ( (goal/100) %10) ) );
    }
 
}
 
/**
 * ThreeDigits
 */
public class ThreeDigits {
 
    private static String notFoundString = "No solution found";
 
    public static void main(String[] args) {
        String algorithmType = args[0];
        String fileLocation = args[1];
        File file = new File(fileLocation);
        try{
            Scanner scanner = new Scanner(file);
            int start = Integer.parseInt(scanner.nextLine());
            int goal = Integer.parseInt(scanner.nextLine());
            List<Integer> forbidden = new ArrayList<>();
                
            //split and parse the forbidden values into forbidden List of integers
            if(scanner.hasNextLine()){
                String[] forbiddenString = scanner.nextLine().split(",");
                for(String forbiddenValue: forbiddenString){
                    forbidden.add(Integer.parseInt(forbiddenValue));
                }
            }
            scanner.close();
                
            // if else statements to find out what algorithms to run
            if(algorithmType.equals("B")){bfsSearch(start,goal,forbidden);}
            else if(algorithmType.equals("D")){dfsSearch(start,goal,forbidden);}
            else if(algorithmType.equals("I")){idsSearch(start,goal,forbidden);}
            else if(algorithmType.equals("G")){greedySearch(start,goal,forbidden);}
            else if(algorithmType.equals("A")){aStarSearch(start,goal,forbidden);}
            else if(algorithmType.equals("H")){hillClimbingSearch(start,goal,forbidden);}
    
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
 
    /**
     * Find path from Start to Goal using BFS Search Algorithm
     * @param start     The starting value, root value
     * @param goal      The goal value, to compare
     * @param forbidden The Three digit forbidden values we should avoid.
     */
    public static void bfsSearch(int start, int goal, List<Integer> forbidden){
        ArrayList<Node> expanded = new ArrayList<>();
        ArrayList<Node> fringe = new ArrayList<>();
        Node node = new Node(start, null, 0);
        fringe.add(node);
        boolean found = false;
 
        // Upper bounding the number of loops to max 1000 cycle
        while(expanded.size() <=1000 && fringe.isEmpty() == false){
 
 
            // Get the first node from the fringe and check if it is the goal node
            Node temp = fringe.get(0);
            expanded.add(temp);
            fringe.remove(temp);
            if(temp.getValue() == goal){
                complete(temp, expanded);
                found = true;
                break;
            }
 
            // Expand the child by adding the childrens to the end of the fringe.
            ArrayList<Node> childrens = temp.getChildren();
            for(Node child: childrens){
                /**
                 * Check whether
                 *  1. we have already expanded on the child to avoid loops.
                 *  2. the given child holds forbidden value.
                 */
                if(forbidden.contains(child.getValue()) == false && inList(child, expanded) == false &&inList(child, fringe) == false){
                    fringe.add(child);
                }
            }
        }
        if(found == false){
            System.out.println(notFoundString);
            printExpanded(expanded);
        }
    }
 
    /**
     * Find path from Start to Goal using DFS Search Algorithm
     * @param start     The starting value, root value
     * @param goal      The goal value, to compare
     * @param forbidden The Three forbidden values we should avoid.
     */
    public static void dfsSearch(int start, int goal, List<Integer> forbidden){
        ArrayList<Node> expanded = new ArrayList<>();
        ArrayList<Node> fringe = new ArrayList<>();
        Node node = new Node(start, null, 0);
        fringe.add(node);
        boolean found = false;
 
        // Upper bounding the number of loops to max 1000 cycle
        while(expanded.size() < 1000){
            if(fringe.isEmpty()){
                break;
            }
 
            // Get the first node from the fringe and check if it is the goal node
            Node temp = fringe.get(0);
            expanded.add(temp);
            fringe.remove(temp);
            if(temp.getValue() == goal){
                complete(temp, expanded);
                found = true;
                break;
            }
 
            // Expand the child by adding the childrens to the front of the fringe.
            ArrayList<Node> childrens = temp.getChildren();
            Collections.reverse(childrens);
            for(Node child: childrens){
                /**
                 * Check whether
                 *  1. we have already expanded on the child to avoid loops.
                 *  2. the given child holds forbidden value.
                 */
                if(forbidden.contains(child.getValue()) == false && inList(child, expanded) == false){
                    fringe.add(0,child);
                }
            }
        }
        if(found == false){
            System.out.println(notFoundString);
            printExpanded(expanded);
        }
 
    }
 
    /**
     * Find path from Start to Goal using IDS Search Algorithm
     * @param start     The starting value, root value
     * @param goal      The goal value, to compare
     * @param forbidden The Three forbidden values we should avoid.
     */
    public static void idsSearch(int start, int goal, List<Integer> forbidden){
        ArrayList<ArrayList<Node>> expanded = new ArrayList<>();
        ArrayList<Node> fringe = new ArrayList<>();
        Node node = new Node(start, null, 0);
        fringe.add(node);
        int level = 0;
        int expandedSearches = 0;
        boolean found = false;
 
        // Upper bounding the number of loops to max 1000 cycle
        while(expandedSearches <= 999){
 
            //Conducting DLS for each level;
            int retVal = depthLimitedSearch(start, goal, level, expanded, 
                                        forbidden, 999 - expandedSearches );
            
            // if retVal is negative, it means that the goal was found, therefore the algorithm should finish.
            if(retVal < 0){
                found = true;
                break;
            }
            else{
                // Update expandedSearches so that the number of expanded nodes are updated properly.
                expandedSearches += retVal;
            }
            level++;
        }
        if(found == false){
            System.out.println("No solution found.");
            ArrayList<Node> expandedToReturn = concatAllList(expanded);
            printExpanded(expandedToReturn);
        }
    }
 
    /**
     * Try and construct path between start and goal with Depth Limited Search algorithm with level that is given.
     * @param start     The starting value, root value
     * @param goal      The goal value, to compare
     * @param level     The level in which DLS should limit to.
     * @param expanded  The total list of expanded node lists.
     * @param forbidden The Three forbidden values we should avoid.
     * @return
     */
    public static int depthLimitedSearch(int start, int goal, int level, 
                        ArrayList<ArrayList<Node>> expanded, List<Integer> forbidden, int upperBound){
        ArrayList<Node> fringe = new ArrayList<>();
        ArrayList<Node> expandedPerLevel = new ArrayList<>();
 
        Node node = new Node(start, null, 0);
        fringe.add(node);
 
        while(fringe.isEmpty() == false && expandedPerLevel.size() <= upperBound ){
 
            Node temp = fringe.get(0);
            fringe.remove(0);
            if(inList(temp,expandedPerLevel) == false){
                expandedPerLevel.add(temp);
 
                if(temp.getValue() == goal){
                    expanded.add(expandedPerLevel);
                    ArrayList<Node> expandedToReturn = concatAllList(expanded);
                    complete(temp, expandedToReturn);
                    return -1;
                }
                if(temp.getDepth() < level){
                    ArrayList<Node> childrens = temp.getChildren();
                    Collections.reverse(childrens);
                    for(Node child: childrens){
                        if(forbidden.contains(child.getValue()) == false){
                            fringe.add(0,child);
                        }
                    }
                }
            }
        }
        expanded.add(expandedPerLevel);
        return expandedPerLevel.size();
    }
 
    /**
     * A function to call to merge all the lists together.
     * @param expanded  The list of total expanded nodes.
     * @return  ArrayList holding all the expanded nodes in order of expansion.
     */
    public static ArrayList<Node> concatAllList(ArrayList<ArrayList<Node>> expanded){
        ArrayList<Node> expandedToReturn = new ArrayList<>();
        for(ArrayList<Node> list: expanded){
            for(Node child: list){
                expandedToReturn.add(child);
            }
        }
        return expandedToReturn;
    }
 
    /**
     * Find the path from start to the goal Appplying Greedy Search Algorithm
     * @param start     The Starting value, the root
     * @param goal      The goal value that we should try and achieve.
     * @param forbidden The 3 forbidden values we should avoid to expand.
     */
    public static void greedySearch(int start, int goal, List<Integer> forbidden){
        ArrayList<Node> expanded = new ArrayList<>();
        ArrayList<Node> fringe = new ArrayList<>();
        Node node = new Node(start, null, 0);
        fringe.add(node);
 
        // Upper bounding the number of loops to max 1000 cycle
        while(expanded.size() <= 1000){
 
            if(fringe.isEmpty()){
                System.out.println(notFoundString);
                printExpanded(expanded);
                break;
            }
 
            Node temp = fringe.get(0);
            fringe.remove(temp);
            expanded.add(temp);
 
            // Check whether the current node's value is the goal.
            if(temp.getValue() == goal){
                complete(temp, expanded);
                break;
            }
 
            // Expand the child list according to the Greedy Search Algorithm
            greedySearchExpansion(expanded, fringe, temp.getChildren(), goal, forbidden);
        }
    }
 
    /**
     * The function used to expand the child nodes of the expanded node,
     * @param expanded  The list of node reflecting the expanded nodes from the Greedy Search Algorithm
     * @param fringe    The list of nodes reflecting the fringe of the Greedy Search Algorithm
     * @param childrens The childrens to expand onto
     * @param goal      The goal value to calculate distance heuristic function
     * @param forbidden The forbidden values that greedySearch should avoid.
     */
    public static void greedySearchExpansion(ArrayList<Node> expanded, ArrayList<Node> fringe, ArrayList<Node> childrens, int goal, List<Integer> forbidden){
        for(Node child: childrens){
            /**
             * Check whether
             *      1. we have already expanded on the child to avoid loops.
             *      2. the given child holds forbidden value.
             */
            if(forbidden.contains(child.getValue()) == false && inList(child, expanded) == false){
                // Find the appropriate Index using greedyFindIndex function and assign it to the fringe list.
                int index = greedyFindIndex(child, goal, fringe);
                fringe.add(index, child);
            }
        } 
    }
 
 
    /**
     * Calculate the distance using Manhatten distance as Heuristic function and find appropriate Index to put the child in
     * @param child     The child to enter into the fringe
     * @param goal      The goal value used to calculate the distance
     * @param fringe    The fringe that child needs to enter
     * @return          The index appropriate for the child, if none: return -1;
     */
    public static int greedyFindIndex(Node child, int goal, ArrayList<Node> fringe){
 
        // For each value in fringe, compare the distance to check whether the child can enter before
        if(fringe.isEmpty()){
            return 0;
        }
        for(int i = 0; i < fringe.size();i++){
            if(fringe.get(i).getDistance(goal) >= child.getDistance(goal)){
                return i;
            }
        }
        return fringe.size();
    }
 
    
    /**
     * The function that uses A* Algorithm search the path from Start value to Goal Value avoiding the forbidden values
     * @param start Start value we need to put as root 
     * @param goal  Goal value we need to achieve.
     * @param forbidden The three forbidden values that we should avoid
     */
    public static void aStarSearch(int start, int goal, List<Integer> forbidden){
        ArrayList<Node> expanded = new ArrayList<>();
        ArrayList<Node> fringe = new ArrayList<>();
        Node node = new Node(start, null, 0);
        fringe.add(node);
 
        // Upper bounding the number of loops to max 1000 cycle
        while(expanded.size() <= 1000){
 
            if(fringe.isEmpty()){
                System.out.println(notFoundString);
                printExpanded(expanded);
                break;
            }
 
            // Get the first element in the fringe to expand upon.
            Node temp = fringe.get(0);
            fringe.remove(temp);
            expanded.add(temp);
 
            // Check whether the currently expanded node holds the goal value.
            if(temp.getValue() == goal){
                complete(temp, expanded);
                break;
            }
            else{
                // Expand and add the children of the current node according to A* algorithm.
                aStarAppend(fringe, expanded, temp.getChildren(), goal, forbidden);
            }
        }
    }
    
    /**
     * Goes through the provided children list and added them to the correlating position in fringe.
     * @param fringe The fringe that will be used to go through the A* Algorithm
     * @param expanded  The List of Node representing the expanded list done by A* Algorithm and used to add child node
     * @param childrens The list of Children Nodes that needs to be added
     * @param goal  The goal value that is used to find Distance Heuristic Analysis
     * @param forbidden The forbidden values that can't be expanded into.
     */
    public static void aStarAppend(List<Node> fringe, List<Node> expanded, List<Node> childrens,int goal, List<Integer> forbidden){
        for(Node child: childrens){
 
            //Checking if each childrens are either forbidden value or already expanded. If so, pass
            if(forbidden.contains(child.getValue()) == false && inList(child, expanded) == false){
                int index = aStarPositionFinder(fringe, child, goal);
                fringe.add(index, child);
            }
        } 
    }
 
    /**
     * Goes through the fringe and finds the correct index to put the child in.
     * @param fringe The fringe of the A* Algorithm
     * @param child The child node we are trying to fit into the fringe
     * @param goal The goal value for Distance Calculation
     * @return Integer value representing the appropriate index, if it is to be put at the end of the list, it returns -1;
     */
    public static int aStarPositionFinder(List<Node> fringe, Node child, int goal){
        if(fringe.isEmpty()){
            return 0;
        }
        for(int i = 0; i < fringe.size();i++){
            // The use of Manhattan Distance method to conduct Heuristic Analysis
            if(( fringe.get(i).getDistance(goal) + fringe.get(i).getDepth() ) >=( child.getDistance(goal) + child.getDepth() ) ){
                return i;
            }
        }
        return fringe.size();
    }
 
    /**
     * Application of Hill climbing search algorithm to find goal value given starting value. 
     * @param start The Starting value given for the Hill Climbing Search Algorithm
     * @param goal The Goal value given for the Hill Climbing Search Algorithm 
     * @param forbidden The Three Digit forbidden value that cannot be expanded
     */
    public static void hillClimbingSearch(int start, int goal, List<Integer> forbidden){
        ArrayList<Node> expanded = new ArrayList<>();
        Node currentNode = new Node(start, null, 0);
        
        // Upper bound the loop to be 1000 cycles
        while(expanded.size() <= 1000){
            expanded.add(currentNode);
 
            //Checking if current node is the goal node
            if(currentNode.getValue() == goal){
                complete(currentNode, expanded);
                break;
            }
 
            //Child expansion
            ArrayList<Node> childrens = currentNode.getChildren();
            boolean changed = false;
            for(Node node: childrens){
                //If the distance is shorter than current node and it satisfies the Task restriction 2, and doesnt expand forbidden add to expand
                if(node.getDistance(goal) <= currentNode.getDistance(goal) && forbidden.contains(node.getValue()) == false && inList(node, expanded) == false){
                    changed = true;
                    currentNode = node;
                }
            }
            // If changed is faulse, it means it is at it's local max. The loop breaks after.
            if(changed == false){
                System.out.println(notFoundString);
                printExpanded(expanded);
                break;
            }
        }
    }
 
    /**
     * The Function to check whether the node in focus is in the list
     * @param nodeToCheck The node to look for
     * @param listToLook  The list of nodes to look into
     * @return  boolean value of true: if the node IS in the list, false: if the node is NOT in the list
     */
    public static Boolean inList(Node nodeToCheck, List<Node> listToLook){
        for(Node child: listToLook){
            /**
             * Checks whether the node is the same by 
             * 1. Comparing the value 
             * 2. Comparing the changed digit
             *      If changed digit is the same, the childrens would be the same therefore it would be the same Node.
             */
            if(child.getValue() == nodeToCheck.getValue() && child.getChangedDigit() == nodeToCheck.getChangedDigit()){
                return true;
            }
        }
        return false;
    }
 
 
    /**
     * The Function that formats the output as expected
     * @param goal Goal Node that we can traverse up it's heritage to find the path
     * @param expanded  List of Node representing the expanded nodes from the algorithm
     */
    public static void complete(Node goal, ArrayList<Node> expanded){
        Node temp = goal;
        ArrayList<Integer> goalToStart = new ArrayList<>();
        while(temp.getParent() != null){
            goalToStart.add(temp.getValue());
            temp = temp.getParent();
        }
        goalToStart.add(temp.getValue());
        Collections.reverse(goalToStart);
        String str = "";
        for(int i = 0; i < goalToStart.size();i++){
            str = str.concat(String.format("%03d", goalToStart.get(i)));
            if(i+1 != goalToStart.size()){
                str = str.concat(",");
            }
        }
        System.out.println(str);
        printExpanded(expanded);
    }
 
    
    /**
     * The Function that formats the list of expanded node in correct expected 
     * @param expanded  List of node that represents the expanded nodes 
     */
    public static void printExpanded(ArrayList<Node> expanded){
        String str = "";
        for(int i = 0; i < expanded.size();i++){
            str = str.concat(String.format("%03d", expanded.get(i).getValue()));
            if(i+1 != expanded.size()){
                str = str.concat(",");
            }
        }
        System.out.println(str);
    }
}