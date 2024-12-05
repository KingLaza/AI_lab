from itertools import product
import math

Counter = 0
# Konstantni podaci za magični kvadrat 4x4
N = 3  # Dimenzija matrice
SUM = N * (N**2 + 1) // 2  # Ciljni zbir za redove, kolone i dijagonale

def forward_check(matrix, domain, row, col, value):
    if not is_over(matrix, row, col):
        return None
    domain_copy = {k: set(v) for k, v in domain.items()}

    # Ukloni vrednost iz domena susednih polja u istom redu i koloni
    for i in range(N):
        domain_copy[(row, i)].discard(value)
        domain_copy[(i, col)].discard(value)

    # Ukloni vrednost iz domena polja na dijagonalama
    if row == col:
        for i in range(N):
            domain_copy[(i, i)].discard(value)
    if row + col == N - 1:
        for i in range(N):
            domain_copy[(i, N - 1 - i)].discard(value)

    return domain_copy

def is_valid(matrix):
    # Proveri redove
    for row in matrix:
        if sum(row) != SUM:
            return False

    # Proveri kolone
    for col in range(N):
        if sum(matrix[row][col] for row in range(N)) != SUM:
            return False

    # Proveri glavnu dijagonalu
    if sum(matrix[i][i] for i in range(N)) != SUM:
        return False

    # Proveri sporednu dijagonalu
    if sum(matrix[i][N - 1 - i] for i in range(N)) != SUM:
        return False

    return True

def is_over(matrix, row, col):
    # Proveri redove
    if sum(matrix[row]) > SUM:
        return False

    # Proveri kolone
    if sum(matrix[i][col] for i in range(N)) > SUM:
        return False

    # Proveri glavnu dijagonalu
    if row==col:
        if sum(matrix[i][i] for i in range(N)) > SUM:
            return False
    if row == N-1-col:
        if sum(matrix[i][N - 1 - i] for i in range(N)) > SUM:
            return False

    return True

def select_unassigned_variable(matrix, domain):
    min_options = math.inf
    best_cell = None

    for row, col in product(range(N), range(N)):
        if matrix[row][col] == 0:  # Nezauzeto polje
            options = domain[(row, col)]
            if len(options) < min_options:
                min_options = len(options)
                best_cell = (row, col)

    return best_cell

def backtracking(matrix, domain):
    # Ako je matrica popunjena, proveri validnost
    if all(matrix[row][col] != 0 for row, col in product(range(N), range(N))):
        return is_valid(matrix)

    # Izaberi sledeće polje pomoću MRV heuristike
    cell = select_unassigned_variable(matrix, domain)
    if not cell:
        return False

    row, col = cell

    # Isprobaj sve mogućnosti iz domena za dato polje
    for value in sorted(domain[(row, col)]):
        matrix[row][col] = value

        # Rekurzivno pokušaj da rešiš problem
        new_domain = forward_check(matrix, domain, row, col, value)
        if new_domain is not None:
            # Nastavi dalje samo ako je domen validan
            if backtracking(matrix, new_domain):
                return True

        # Povratak na prethodno stanje
        matrix[row][col] = 0

    return False

def solve_magic_square():
    matrix = [[0] * N for _ in range(N)]
    domain = {(row, col): set(range(1, N**2 + 1)) for row, col in product(range(N), range(N))}

    if backtracking(matrix, domain):
        return matrix
    else:
        return None

if __name__ == '__main__':
    solution = solve_magic_square()
    if solution:
        for row in solution:
            print(row)
    else:
        print("Rešenje nije pronađeno.")
