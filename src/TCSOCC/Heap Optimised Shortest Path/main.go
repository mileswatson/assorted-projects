
package main

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import (
    "fmt"       // for formatting strings
    "os"        // to allow file opening
    "bufio"     // allows reading of file line by line
    "strings"   // allows splitting of strings into slices
    "strconv"   // converts strings to integers
    "time"      // measure time taken
)

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

type node struct {              // node struct that holds data about a single node
    name        string
    connections map[*node]int   // a dictionary that maps a node (*node) to a distance (int)
    distance    int             // the shortest distance away from the starting point
    open        bool            // whether the node is currently in the 'open' heap
    closed      bool            // whether the node has been in the 'open' heap, but isn't anymore 
    pos         int             // the last position of the node in the 'open' heap
}

func newNode(n string) *node {      // constructor returns a pointer to a new node, initialised with a new dictionary, a distance of zero and a status of 'unused'
    return &node{
        name: n,
        connections: make(map[*node]int),
        distance: 0,
        open: false,
        closed: false,
        pos: 0,
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

type heap struct {      // a heap structure that holds all the nodes open to evaluation
    values  []*node
}

func newHeap() *heap {      // constructor to return a new heap
    return &heap{[]*node{}}
}

func (h *heap) push(n *node) {          // pushes a new node onto the minimum heap, retaining the heap structure
    n.open = true
    n.closed = false
    h.values = append(h.values, n)
    var child, parent int
    child = len(h.values) - 1
    for child != 0 {
        parent = (child - 1) / 2
        if n.distance < h.values[parent].distance {
            h.values[child] = h.values[parent]
            h.values[child].pos = child
        } else {
            h.values[child] = n
            n.pos = child
            break
        }
        child = parent
    }
    if child == 0 {
        h.values[0] = n
        n.pos = 0
    }
}

func (h *heap) pop(pos int) *node {         // removes the item at index pos from the heap and returns its value, whilst retaining the heap structure
    store := h.values[pos]
    store.closed = true
    store.open = false
    h.values[pos] = h.values[len(h.values)-1]
    h.values[pos].pos = pos
    h.values = h.values[:len(h.values)-1]
    var parent, aChild, bChild int
    parent = pos
    aChild = (parent * 2) + 1
    bChild = aChild + 1
    for aChild < len(h.values) {
        if bChild < len(h.values) {
            if h.values[parent].distance > h.values[aChild].distance && h.values[bChild].distance >= h.values[aChild].distance {
                h.values[parent], h.values[aChild] = h.values[aChild], h.values[parent]
                h.values[parent].pos = parent
                h.values[aChild].pos = aChild
                parent = aChild
            } else if h.values[parent].distance > h.values[bChild].distance {
                h.values[parent], h.values[bChild] = h.values[bChild], h.values[parent]
                h.values[parent].pos = parent
                h.values[bChild].pos = bChild
                parent = bChild
            } else {
                break
            }
        } else {
            if h.values[parent].distance > h.values[aChild].distance {
                h.values[parent], h.values[aChild] = h.values[aChild], h.values[parent]
                h.values[parent].pos = parent
                h.values[aChild].pos = aChild
            }
            break
        }
        aChild = (parent * 2) + 1
        bChild = aChild + 1
    }
    return store
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

type graph struct {             // a graph struct that holds a collection of nodes
    nodes map[string]*node      // a dictionary that maps a name (string) to a node (*node or node pointer)
}

func newGraph(filename string) *graph {                     // constructor to create a new graph
    file, _ := os.Open(filename)                            // opens file to read data from
    defer file.Close()                                      // defers closing file until function ends
    scanner := bufio.NewScanner(file)                       // allows reading of file line by line
    g := &graph{make(map[string]*node)}                     // creates a new graph, and sets 'g' to its pointer
    for scanner.Scan() {                                    // scans a new line
        g.nodes[scanner.Text()] = newNode(scanner.Text())   // creates a new node with the name being the contents of the new line
    }
    return g
}

func (g *graph) addConnections(filename string) {                                       // adds connections file to graph
    file, _ := os.Open(filename)                                                        // opens file
    defer file.Close()                                                                  // defers closing file until end of function
    var items []string                                                          
    scanner := bufio.NewScanner(file)                                                   // allows reading of file line by line
    for scanner.Scan() {                                                                // scans new line
        items = strings.Split(scanner.Text()," ")                                       // splits the new line into a slice by spaces
        g.nodes[items[0]].connections[g.nodes[items[1]]], _ = strconv.Atoi(items[2])    // sets first connection
        g.nodes[items[1]].connections[g.nodes[items[0]]], _ = strconv.Atoi(items[2])    // sets second connection
    }
}

func (g *graph) find(start string, finish string) string {                                                          // sets the minimum distances to each node in graph from start
    var currentNode *node
    var open *heap = newHeap()                                                                                      // creates a new minimum heap for open nodes
    open.push(g.nodes[start])
    for len(open.values) > 0 {                                                                                      // repeats while there is at least one open node
        currentNode = open.pop(0)                                                                                   // removes the closest node from the open heap
        if currentNode.name == finish {
            break
        }
        for testingNode, v := range currentNode.connections {                                                       // iterates through all connections in currentNode
            if (!(testingNode.open || testingNode.closed)) || (currentNode.distance + v < testingNode.distance) {   // checks if it can update the shortest distance
                testingNode.distance = currentNode.distance + v                                                     // if it can, it updates the testingNode distance
                if testingNode.open {                                                                               // before pushing it back onto the open heap
                    open.push(open.pop(testingNode.pos))
                } else {
                    open.push(testingNode)
                }
            }
        }
    }
    path := finish
    var minimumNode *node
    var minimumDistance int = 0
    var first bool
    for {                                                                                       // calculates the path from the evaluated node map
        minimumDistance = 0
        first = true
        for testingNode, _ := range currentNode.connections {
            if testingNode.closed && (first || (testingNode.distance < minimumDistance)) {
                minimumDistance = testingNode.distance
                minimumNode = testingNode
                first = false
            }
        }
        currentNode = minimumNode
        path = currentNode.name + path
        if currentNode.distance == 0 {
            return path
        }
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

func main() {
    var g *graph = newGraph("names1.txt")           // creates a new graph with the town names in 'names.txt'
    g.addConnections("connections1.txt")            // adds connections in 'connections.txt' to the graph
    start := time.Now()                             // starts timing
    result := g.find("a","z")                       // finds the shortest path in average of O(|E| + |V|log|V|)
    elapsed := time.Since(start)                    // calculates time passed
    fmt.Printf("Search took %s\n", elapsed)         // prints time passed
    fmt.Printf("Path: %s\n",result)
}