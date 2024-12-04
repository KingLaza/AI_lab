from itertools import product

def create_magic_square(size):
    target_sum = size * (size**2 + 1) // 2  # Ciljni zbir

    # Generiši prioritet dijagonalnih polja
    priority_cells = [
        (i, i) for i in range(size)
    ] + [
        (i, size - 1 - i) for i in range(size) if i != size - 1 - i
    ] + [
        (r, c) for r, c in product(range(size), range(size))
        if (r, c) not in {(i, i) for i in range(size)} and (r, c) not in {(i, size - 1 - i) for i in range(size)}
    ]

    # Ažuriraj zbir redova, kolona i dijagonala
    def update_sums(matrix):
        row_sums = [sum(matrix[row]) for row in range(size)]
        col_sums = [sum(matrix[row][col] for row in range(size)) for col in range(size)]
        diag1_sum = sum(matrix[i][i] for i in range(size))
        diag2_sum = sum(matrix[i][size - 1 - i] for i in range(size))
        return row_sums, col_sums, diag1_sum, diag2_sum

    # Provera validnosti trenutne matrice
    def is_valid_partial(matrix, row_sums, col_sums, diag1_sum, diag2_sum):
        for s in row_sums + col_sums:
            if s > target_sum:
                return False
        if diag1_sum > target_sum or diag2_sum > target_sum:
            return False
        return True

    # Backtracking pretraga sa MRV heuristikom
    def backtracking(matrix, domain, index, row_sums, col_sums, diag1_sum, diag2_sum):
        if index == size**2:
            return all(s == target_sum for s in row_sums + col_sums) and diag1_sum == target_sum and diag2_sum == target_sum

        # Pronađi čvor sa najmanjim domenom (MRV heuristika)
        unfilled_cells = [(r, c) for r, c in priority_cells if matrix[r][c] == 0]
        next_cell = min(unfilled_cells, key=lambda cell: len(domain[cell]), default=None)
        if not next_cell:
            return False

        row, col = next_cell

        for value in sorted(domain[(row, col)]):
            matrix[row][col] = value

            # Ažuriraj zbirove
            row_sums[row] += value
            col_sums[col] += value
            if row == col:
                diag1_sum += value
            if row + col == size - 1:
                diag2_sum += value

            if is_valid_partial(matrix, row_sums, col_sums, diag1_sum, diag2_sum):
                new_domain = {k: set(v) for k, v in domain.items()}

                # Ažuriraj domen za susedna polja
                for i in range(size):
                    new_domain[(row, i)].discard(value)
                    new_domain[(i, col)].discard(value)
                if row == col:
                    for i in range(size):
                        new_domain[(i, i)].discard(value)
                if row + col == size - 1:
                    for i in range(size):
                        new_domain[(i, size - 1 - i)].discard(value)

                if backtracking(matrix, new_domain, index + 1, row_sums, col_sums, diag1_sum, diag2_sum):
                    return True

            # Resetuj vrednosti
            matrix[row][col] = 0
            row_sums[row] -= value
            col_sums[col] -= value
            if row == col:
                diag1_sum -= value
            if row + col == size - 1:
                diag2_sum -= value

        return False

    # Rešavanje magičnog kvadrata
    def solve_magic_square():
        matrix = [[0] * size for _ in range(size)]
        domain = {(row, col): set(range(1, size**2 + 1)) for row, col in product(range(size), range(size))}
        row_sums, col_sums, diag1_sum, diag2_sum = [0] * size, [0] * size, 0, 0

        if backtracking(matrix, domain, 0, row_sums, col_sums, diag1_sum, diag2_sum):
            return matrix
        else:
            return None

    return solve_magic_square()

# Pokreni rešavanje za zadatu veličinu matrice
matrix_size = 3 #4
#matrix_size = 4
solution = create_magic_square(matrix_size)
if solution:
    print("Rešenje magičnog kvadrata:")
    for row in solution:
        print(row)
else:
    print("Rešenje nije pronađeno.")
