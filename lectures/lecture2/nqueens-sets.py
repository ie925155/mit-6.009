##With the solution represented as a vector with one queen in each row,
##we don't have to check to see if two queens are on the same row. By using
##a permutation generator, we know that no value in the vector is repeated,
##so we don't have to check to see if two queens are on the same column.
##Since rook moves don't need to be checked, we only need to check bishop moves.
##The technique for checking the diagonals is to add or subtract the column number
##from each entry, so any two entries on the same diagonal will have the same value
##(in other words, the sum or difference is unique for each diagonal).
##Now all we have to do is make sure that the diagonals for each of the eight
##queens are distinct. So, we put them in a set (which eliminates duplicates)
##and check that the set length is eight (no duplicates were removed).
##Any permutation with non-overlapping diagonals is a solution. So, we
##print it and continue checking other permutations.
##One disadvantage with this solution is that we can't simply "skip" all
##the permutations that start with a certain prefix, after discovering that
##that prefix is incompatible. For example, it is easy to verify that no
##permutation of the form (1,2,...) could ever be a solution, but since we
##don't have control over the generation of the permutations, we can't just
##tell it to "skip" all the ones that start with (1,2).

from itertools import permutations

#Tight code for n queens
def board(vec, n):
    for i in vec:
        print('.' * i + 'Q' + '.' * (n-i-1))

def nqueensSets(n):

    cols = range(n)
    for vec in permutations(cols):
        #print (vec)
        left_diagonal = set()
        right_diagonal = set()
        for i in cols:
            left_diagonal.add(vec[i]+i)
            right_diagonal.add(vec[i]-i)

        if (n == len(left_diagonal) and n == len(right_diagonal)):
            board (vec, n)
            return

nqueensSets(8)
