package main

import (
    "fmt"
    "strconv"
)
type polynomial []float64

func newPolynomial(values ...float64) polynomial {
    for i := len(values)/2-1; i >= 0; i-- {
        opp := len(values)-1-i
        values[i], values[opp] = values[opp], values[i]
    }
    return polynomial(values)
}

func add(a, b polynomial) polynomial {
    for len(a) < len(b) {
        a = append(a,0)
    }
    for i, v := range b {
        a[i] += v
    }
    return a
}

func sub(a, b polynomial) polynomial {
    for len(a) < len(b) {
        a = append(a,0)
    }
    for i, v := range b {
        a[i] -= v
    }
    return a
}

func multiply(a, b polynomial) polynomial {
    var temp polynomial
    answer := newPolynomial()
    for _, v := range a {
        temp = make(polynomial,len(b))
        for j, w := range b {
            temp[j] = w * v
        }
        answer = add(answer,temp)
        b = append( []float64{0}, b... )
    }
    return answer
}

func fstr(f float64) string {
    if f > 0 {
        return " + " + strconv.FormatFloat(f, 'f', -1, 64)
    } else if f < 0 {
        return " - " + strconv.FormatFloat(f, 'f', -1, 64)[1:]
    }
    return ""
}

func pstr(p polynomial) string {
    result := ""
    for i, v := range p {
        if i == 0 {
            result = fstr(v) + result
        } else if i == 1 && v != 0{
            result = fstr(v) + "x" + result
        } else if v != 0{
            result = fstr(v) + "x^" + strconv.Itoa(i) + result
        }
    }
    return "(" + result[1:] + ")"
}

func main() {
    a := newPolynomial(-3,5)
    b := newPolynomial(3,5)
    fmt.Println( pstr(a), "*", pstr(b), "=", pstr( multiply( a, b ) ) )
}