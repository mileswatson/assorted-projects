package main

import (
    "fmt"       // for printing things nicely
    "os"        // for accessing os.stdin
)

type grid struct {      // struct that holds an array of integers
    values  [][]int
}

func newGrid() *grid {      // returns a pointer to a new grid of dimensions 9 x 9
    a := make([][]int, 9)
    for i := range a {
        a[i] = make([]int, 9)
    }
    return &grid{a}
}

func (g *grid) clear() {                // redundant function, only used during testing
    for i, outer := range g.values {
        for j := range outer {
            g.values[i][j] = 0
        }
    }
}

func (g *grid) add(x int, y int, height int) {      // increments the point (x,y) on the grid g by height
    if x >= -4 && x <= 4 && y >= -4 && y <= 4 {
        g.values[4-y][x+4] += height
    }
}

func (g *grid) str(aBank int, bBank int) string {       // nicely formats the grid
    aBank += 4
    bBank += 4
    returnString := ""
    for row := range g.values {
        for column := range g.values[row] {
            if column == aBank || column == bBank {
                returnString += "x"
            } else if g.values[row][column] < 0 {
                returnString += "o"
            } else if g.values[row][column] > 0 {
                returnString += "*"
            } else {
                returnString += "-"
            }
        }
        returnString += "\n"
    }
    return returnString[:len(returnString)-1]
}

//////////////////////////////////////////////////////////////////////////

type wave struct {          // holds information about a wave
    x       int
    y       int
    time    int
    height  int
}

func newWave(x int, y int, time int, height int) *wave {        // returns a pointer to a new wave
    return &wave{x, y, time, height}
}

/////////////////////////////////////////////////////////////////////////

func abs(x int) int {           // easier than using the default one
    if x < 0 {
        return -x
    }
    return x
}

func main() {

    var numPebbles, x, y, time, radius, x1, x2, aBank, bBank, leftPos, rightPos int
    var leftReflect, rightReflect bool

    fmt.Fscanln(os.Stdin,&numPebbles)           // scan stdin for an integer, and place it in numPebbles

    waves := make([]*wave, numPebbles * 2)      // make an array of pointers to waves with length numPebbles * 2

    for i := 0; i < numPebbles; i++ {
        fmt.Fscanln(os.Stdin, &x, &y, &time)    // scan stdin for 3 integers, and place them in x, y, and time

        waves[2*i] = newWave(x, y, time, 1)     // creates the initial raised wave at time t

        waves[(2*i) + 1] = newWave(x, y, time + 2, -1)  // creates the secondary lowered wave at time t+2
    }
    fmt.Fscanln(os.Stdin, &aBank, &bBank)   // reads two integers from stdin, places them in the variables aBank and bBank
    fmt.Fscanln(os.Stdin, &time)    // reads the time frame
    
    g := newGrid()                  // declares and initialises g as a new grid
    for _, w := range waves {       // iterates through all waves 'w' in 'waves'
        leftReflect = false
        rightReflect = false        // finds which direction to reflect the waves, will probably rewrite (it works)
        if aBank < bBank {
            if bBank < w.x {
                leftReflect = true
                leftPos = bBank
            } else if aBank < w.x {
                leftReflect = true
                leftPos = aBank
                if bBank > w.x {
                    rightReflect = true
                    rightPos = bBank
                }
            } else {
                rightReflect = true
                rightPos = aBank
            }
        } else {
            if aBank < w.x {
                leftReflect = true
                leftPos = aBank
            } else if bBank < w.x {
                leftReflect = true
                leftPos = bBank
                if aBank > w.x {
                    rightReflect = true
                    rightPos = aBank
                }
            } else {
                rightReflect = true
                rightPos = bBank
            }
        }
        radius = time - w.time              // calculates the radius of the taxicab circle
        if radius == 0 {
            g.add(w.x,w.y,w.height)
        } else if radius > 0 {
            for i := -4; i <= 4; i++ {              // iterates through all y values that are in range -5 < y < 5
                if abs(w.y - i) == radius {
                    g.add(w.x,i,w.height)
                } else if abs(w.y-i) < radius {     // only evaluates the point if the y value is within the radius
                    x1 = w.x + radius - abs(i - w.y)        // the left x value that corresponds to the y value
                    for (leftReflect && x1 <= leftPos) || (rightReflect && x1 >= rightPos) {    // repeatedly reflects until within the boundary
                        if leftReflect && (x1 <= leftPos) {
                            x1 = leftPos + (leftPos - x1) + 1
                        }
                        if rightReflect && (x1 >= rightPos) {
                            x1 = rightPos + (rightPos - x1) - 1
                        }
                    }
                    x2 = w.x - (radius - abs(i - w.y))      // the right x value that corresponds to the y value
                    for (leftReflect && x2 <= leftPos) || (rightReflect && x2 >= rightPos) {    // repeatedly reflects until within the boundary
                        if leftReflect && (x2 <= leftPos) {
                            x2 = leftPos + (leftPos - x2) + 1
                        }
                        if rightReflect && (x2 >= rightPos) {
                            x2 = rightPos + (rightPos - x2) - 1
                        }
                    }
                    g.add(x1,i,w.height)            // renders points on the grid
                    g.add(x2,i,w.height)
                }
            }
        }
    }
    fmt.Println(g.str(aBank, bBank))
}