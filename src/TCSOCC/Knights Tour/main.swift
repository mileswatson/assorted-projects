/*
struct Fract {
    var n: Int
    var d: Int

    func simplify() -> Fract {
        var a = abs(n)
        var b = abs(d)
        var temp: Int
        while b != 0 {
            temp = b
            b = a % b
            a = temp
        }
        return Fract(n: n / a, d: d / a)
    }
    func string() -> String {
        return String(n) + "/" + String(d)
    }
}

func *(a: Fract, b: Fract) -> Fract {
    return Fract(n: a.n * b.n, d: a.d * b.d)
}

func /(a: Fract, b: Fract) -> Fract {
    return Fract(n: a.n * b.d, d: a.d * b.n)
}

func +(a: Fract, b: Fract) -> Fract {
    return Fract(n: a.n * b.d + b.n * a.d, d: a.d * b.d)
}

func -(a: Fract, b: Fract) -> Fract {
    return Fract(n: a.n * b.d - b.n * a.d, d: a.d * b.d)
}
*/


class Space : Equatable {

    let row: Int
    let column: Int
    let board: Board
    var connections: [Space]

    init(row: Int, column: Int, board: Board) {
        self.row = row
        self.column = column
        self.board = board
        self.connections = []
    }

    static func ==(a: Space, b: Space) -> Bool {
        return (a.row == b.row) && (a.column == b.column) && (a.board.size == b.board.size)
    }

    func evaluateConnections() {
        var tempRow: Int
        var tempColumn: Int
        for check in board.checks {
            tempRow = row + check.0
            tempColumn = column + check.1
            if board.isValid(dim: tempRow) && board.isValid(dim: tempColumn) {
                connections.append(board.board[tempRow][tempColumn])
            }
        }
    }

    func recursiveSearch(depth: Int, path: [Space]) -> Int {
        let p = path + [self]
        if depth == 0 && row == 1 && column == 2 {
            var s = "found: "
            for i in p {
                s += "(\(i.row),\(i.column)) "
            }
            print(s)
            return 1
        } else {
            var total = 0
            for connection in connections {
                if !p.contains(connection) || depth == 1 {
                    total += connection.recursiveSearch(depth: depth - 1, path: p)
                }
            }
            return total
        }
    }

}

class Board {

    let size: Int
    let checks: [(Int, Int)]
    var board: [[Space]]
    
    init(order: Int) {
        size = order
        checks = [
            ( 1, 2),
            ( 1,-2),
            ( 2, 1),
            ( 2,-1),
            (-1, 2),
            (-1,-2),
            (-2, 1),
            (-2,-1)
        ]
        board = []
        for row in 0 ..< size {
            board.append([])
            for column in 0 ..< size {
                board[row].append(Space(row: row, column: column, board: self))
            }
        }
        for row in 0 ..< size {
            for column in 0 ..< size {
                board[row][column].evaluateConnections()
            }
        }
    }

    func isValid(dim: Int) -> Bool {
        if dim >= 0 && dim < size {
            return true
        }
        return false
    }

    func tour() -> Int {
        return board[0][0].recursiveSearch(depth: size * size, path: [])
    }

}

print("Enter order of board: ")
let answer = readLine()
if answer != nil {
    let order = Int(answer!)
    if order != nil {
        if order! < 6 || order! % 2 == 1 {
            print("No solutions found.")
        } else {
            var b = Board(order: order!)
            print("Finding solutions...")
            print(b.board[2][1].recursiveSearch(depth: order! * order! - 2, path: [b.board[0][0]])*2, "solutions found.")
        }
    } else {
        print("NaN")
    }
} else {
    print("NaN")
}