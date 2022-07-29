def solution(start,end):
    board = [Cell(x) for x in range(0,64)]
    adjMat= {}
    for cell in board:
        adjMat[cell.num]=cell.adjacents
    return BFS(adjMat, start, end)

class Cell():
    def __init__(self, num):
        self.num=num
        self.row = sum([1 if num>=x else 0 for x in [56,48,40,32,24,16,8]])
        self.col = num%8
        self.adjacents=[]
        targets = [num-17,num-15,num-6,num+10,num+17,num+15,num+6,num-10]
        # excluding adjacents if they are outside the board/wrap around
        # if the target is <0 or > 63, its wrong
        # if the target is in the same row or column as u, its wrong
        # if target is more than 2 rows or cols away from you, its wrong
        for value in targets:
            if value <0 or value > 63:
                continue
            targRow = sum([1 if value>=x else 0 for x in [56,48,40,32,24,16,8]])
            targCol = value%8
            if targRow == self.row or targCol==self.col:
                continue
            elif abs(targRow-self.row) > 2 or abs(targCol-self.col) > 2:
                continue
            self.adjacents.append(value)

def BFS(adj, start, end):
    d = {start:0}
    qq = [start]
    if start == end:
        return 0
    while qq != []:
        curr = qq.pop(0)
        for neigh in adj[curr]:
            if neigh not in list(d.keys()):
                d[neigh] = d[curr]+1
                qq.append(neigh)
                if neigh == end:
                    return d[neigh]


print(solution(10,10))

# -------------------------
# | 0| 1| 2| 3| 4| 5| 6| 7|
# -------------------------
# | 8| 9|10|11|12|13|14|15|
# -------------------------
# |16|17|18|19|20|21|22|23|
# -------------------------
# |24|25|26|27|28|29|30|31|
# -------------------------
# |32|33|34|35|36|37|38|39|
# -------------------------
# |40|41|42|43|44|45|46|47|
# -------------------------
# |48|49|50|51|52|53|54|55|
# -------------------------
# |56|57|58|59|60|61|62|63|
# -------------------------