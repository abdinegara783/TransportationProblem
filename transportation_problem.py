# -*- coding: utf-8 -*-
"""Transportation_problem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JcjaS3ycjg03pnYmr5OT6S6VtNvccPh9
"""

def vam_method(matrix_supply, matrix_demand, costs):
    num_all = []  # List untuk menyimpan semua alokasi
    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    # Menginisialisasi variabel yang diperlukan untuk VAM
    supply_remaining = supply.copy()
    demand_remaining = demand.copy()
    penalties = np.zeros((m, n))

    while True:
        # Menentukan sel dengan biaya terendah (dalam matriks biaya + penalti)
        min_cost_cell = np.argmin(costs + penalties)
        i, j = divmod(min_cost_cell, n)

        # Mengalokasikan sebanyak mungkin dari sumber ke tujuan
        allocation_amount = min(supply_remaining[i], demand_remaining[j])
        allocation[i][j] = allocation_amount

        # Mengurangi sisa persediaan dan permintaan
        supply_remaining[i] -= allocation_amount
        demand_remaining[j] -= allocation_amount

        # Menambahkan alokasi ke dalam list num_all
        num_all.append(allocation.copy())  # Menggunakan copy() untuk mencegah referensi yang sama
        # Memperbarui penalti
        penalties[i][j] = np.inf  # Menandai sel yang sudah dialokasikan dengan nilai tak terhingga
        for k in range(m):
            for l in range(n):
                if penalties[k][l] != np.inf:  # Hanya sel yang belum dialokasikan yang diperbarui
                    penalties[k][l] = costs[k][l] - np.min([costs[k][j] + penalties[i][l], costs[i][l] + penalties[k][j]])

        # Menghentikan iterasi jika semua persediaan dan permintaan telah terpenuhi
        if np.all(supply_remaining == 0) and np.all(demand_remaining == 0):
            break

    # Menghitung total biaya alokasi
    total_cost = np.sum(allocation * costs)

    return num_all, total_cost

# Contoh penggunaan:
matrix_supply = [20, 30, 50]
matrix_demand = [30, 40, 30]
costs = [[8, 6, 10],
         [9, 7, 4],
         [3, 5, 12]]

allocation, total_cost = vam_method(matrix_supply, matrix_demand, costs)
print("\nAllocation Matrix:")
print(allocation)
print("Total Cost:", total_cost)

import numpy as np

def monalisha_method(matrix_supply, matrix_demand, costs):
    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    # Metode Northwest Corner untuk mendapatkan solusi awal
    row, col = 0, 0
    while row < m and col < n:
        if supply[row] > 0 and demand[col] > 0:
            quantity = min(supply[row], demand[col])
            allocation[row, col] = quantity
            supply[row] -= quantity
            demand[col] -= quantity
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1
        else:
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1

    # Perbaikan menggunakan pendekatan Metode VAM
    while np.any(supply > 0) and np.any(demand > 0):
        u, v = [False] * m, [False] * n
        costs_copy = np.copy(costs)

        # Menghitung selisih biaya terbesar dan kedua terbesar
        for i in range(m):
            for j in range(n):
                if allocation[i, j] == 0:
                    costs_copy[i, j] -= min(costs_copy[i])
                    costs_copy[i, j] -= min(costs_copy[:, j])

        # Menandai baris dan kolom dengan selisih biaya terbesar
        for i in range(m):
            if np.count_nonzero(costs_copy[i] == 0) == 1:
                u[i] = True
        for j in range(n):
            if np.count_nonzero(costs_copy[:, j] == 0) == 1:
                v[j] = True

        # Memilih sel untuk dialokasikan
        row_index = np.where(u)[0][0]
        col_index = np.where(v)[0][0]

        quantity = min(supply[row_index], demand[col_index])
        allocation[row_index, col_index] = quantity
        supply[row_index] -= quantity
        demand[col_index] -= quantity

    total_cost = np.sum(allocation * costs)

    return allocation, total_cost

# Contoh penggunaan
matrix_supply = [100, 150, 200]
matrix_demand = [120, 100, 180]
costs = [[6, 8, 10],
         [9, 7, 4],
         [3, 2, 8]]

allocation, total_cost = monalisha_method(matrix_supply, matrix_demand, costs)
print("Allocation:")
print(allocation)
print("Total Cost:", total_cost)

import numpy as np

def north_west_corner(matrix_supply, matrix_demand, costs):
    num_all=[]
    num =0
    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    row, col = 0, 0
    total_cost = 0  # Inisialisasi total biaya

    print("Iterasi | Allocation Matrix")
    print("-----------------------------")
    while row < m and col < n:
        if supply[row] > 0 and demand[col] > 0:
            quantity = min(supply[row], demand[col])
            allocation[row, col] = quantity
            supply[row] -= quantity
            demand[col] -= quantity
            total_cost += quantity * costs[row, col]  # Menghitung total biaya
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1

            print(f"   {row+1},{col+1}   | {allocation}")
            num_all.append[num]=allocation
            num = num+1
        else:
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1

    print("-----------------------------")

    return allocation, total_cost

# Contoh penggunaan:
matrix_supply = [20, 30, 50]
matrix_demand = [30, 40, 30]
costs = [[8, 6, 10],
         [9, 7, 4],
         [3, 5, 12]]

allocation, total_cost = north_west_corner(matrix_supply, matrix_demand, costs)
print("\nAllocation Matrix:")
print(allocation)
print("Total Cost:", total_cost)

import numpy as np

def north_west_corner(matrix_supply, matrix_demand, costs):
    num_all = []  # List untuk menyimpan semua alokasi

    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    row, col = 0, 0
    total_cost = 0  # Inisialisasi total biaya

    print("Iterasi | Allocation Matrix")
    print("-----------------------------")
    while row < m and col < n:
        if supply[row] > 0 and demand[col] > 0:
            quantity = min(supply[row], demand[col])
            allocation[row, col] = quantity
            supply[row] -= quantity
            demand[col] -= quantity
            total_cost += quantity * costs[row, col]  # Menghitung total biaya
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1

            print(f"   {row+1},{col+1}   | {allocation}")

            # Menambahkan alokasi ke dalam list num_all
            num_all.append(allocation.copy())  # Menggunakan copy() untuk mencegah referensi yang sama
        else:
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1

    print("-----------------------------")

    return num_all, total_cost

# Contoh penggunaan:
matrix_supply = [20, 30, 50]
matrix_demand = [30, 40, 30]
costs = [[8, 6, 10],
         [9, 7, 4],
         [3, 5, 12]]

num_all, total_cost = north_west_corner(matrix_supply, matrix_demand, costs)
print("\nList of Allocation Matrices:")
for i, allocation in enumerate(num_all):
    print(f"Allocation Matrix {i+1}:")
    print(allocation)
print("Total Cost:", total_cost)

matrix_list[0]

import numpy as np

def monalisa(matrix_supply, matrix_demand, costs):
    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        min_cost = np.inf
        min_row = -1
        min_col = -1

        for i in range(m):
            for j in range(n):
                if supply[i] > 0 and demand[j] > 0:
                    cost = costs[i, j]
                    if cost < min_cost:
                        min_cost = cost
                        min_row = i
                        min_col = j

        quantity = min(supply[min_row], demand[min_col])
        allocation[min_row, min_col] = quantity
        supply[min_row] -= quantity
        demand[min_col] -= quantity

    total_cost = np.sum(allocation * costs)

    return allocation, total_cost

# Contoh penggunaan:
matrix_supply = [20, 30, 50]
matrix_demand = [30, 40, 30]
costs = [[8, 6, 10],
         [9, 7, 4],
         [3, 5, 12]]

allocation, total_cost = monalisa(matrix_supply, matrix_demand, costs)
print("Allocation Matrix:")
print(allocation)
print("Total Cost:", total_cost)

import numpy as np
def monalisa(matrix_supply, matrix_demand, costs):
    num_all = []  # List untuk menyimpan semua alokasi
    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    print("Iterasi | Allocation Matrix")
    print("-----------------------------")

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        min_cost = np.inf
        min_row = -1
        min_col = -1

        for i in range(m):
            for j in range(n):
                if supply[i] > 0 and demand[j] > 0:
                    cost = costs[i, j]
                    if cost < min_cost:
                        min_cost = cost
                        min_row = i
                        min_col = j

        quantity = min(supply[min_row], demand[min_col])
        allocation[min_row, min_col] = quantity
        supply[min_row] -= quantity
        demand[min_col] -= quantity

        #print(f"   {min_row+1},{min_col+1}   | {allocation}")
        # Menambahkan alokasi ke dalam list num_all
        num_all.append(allocation.copy())  # Menggunakan copy() untuk mencegah referensi yang sama

    #print("-----------------------------")

    total_cost = np.sum(allocation * costs)

    return num_all, total_cost

# Contoh penggunaan:
matrix_supply = [20, 30, 50]
matrix_demand = [30, 40, 30]
costs = [[8, 6, 10],
         [9, 7, 4],
         [3, 5, 12]]

num_all, total_cost = monalisa(matrix_supply, matrix_demand, costs)
print("Allocation Matrix:")
print(num_all[len(num_all)-1])
print("Total Cost:", total_cost)

import numpy as np

def monalisa(matrix_supply, matrix_demand, costs):
    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    print("Iterasi | Allocation Matrix")
    print("-----------------------------")

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        min_cost = np.inf
        min_row = -1
        min_col = -1

        for i in range(m):
            for j in range(n):
                if supply[i] > 0 and demand[j] > 0:
                    cost = costs[i, j]
                    if cost < min_cost:
                        min_cost = cost
                        min_row = i
                        min_col = j

        quantity = min(supply[min_row], demand[min_col])
        allocation[min_row, min_col] = quantity
        supply[min_row] -= quantity
        demand[min_col] -= quantity

        print(f"   {min_row+1},{min_col+1}   | {allocation}")


    print("-----------------------------")

    total_cost = np.sum(allocation * costs)

    return allocation, total_cost

# Contoh penggunaan:
matrix_supply = [20, 30, 50]
matrix_demand = [30, 40, 30]
costs = [[8, 6, 10],
         [9, 7, 4],
         [3, 5, 12]]

allocation, total_cost = monalisa(matrix_supply, matrix_demand, costs)
print("Allocation Matrix:")
print(allocation)
print("Total Cost:", total_cost)

import numpy as np

def north_west_corner(matrix_supply, matrix_demand, costs):
    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    row, col = 0, 0
    total_cost = 0

    print("Initial Allocation Matrix (NWC):")
    print("---------------------------------")
    while row < m and col < n:
        if supply[row] > 0 and demand[col] > 0:
            quantity = min(supply[row], demand[col])
            allocation[row, col] = quantity
            supply[row] -= quantity
            demand[col] -= quantity
            total_cost += quantity * costs[row, col]
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1
            print(f"   {row+1},{col+1}   | {allocation}")
        else:
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1
    print("---------------------------------")

    return allocation, total_cost

def get_unoccupied_cells(allocation):
    return [(i, j) for i in range(allocation.shape[0]) for j in range(allocation.shape[1]) if allocation[i, j] == 0]

def compute_potential(costs, allocation):
    row_potential = np.zeros(costs.shape[0])
    col_potential = np.zeros(costs.shape[1])
    unoccupied_cells = get_unoccupied_cells(allocation)

    for i, j in unoccupied_cells:
        if allocation[i, :].sum() == 0:
            col_potential[j] = costs[i, j] - row_potential[i]
        elif allocation[:, j].sum() == 0:
            row_potential[i] = costs[i, j] - col_potential[j]

    return row_potential, col_potential

def modi_method(matrix_supply, matrix_demand, costs):
    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    allocation, total_cost = north_west_corner(matrix_supply, matrix_demand, costs)
    print("\nInitial Allocation Matrix (NWC):")
    print(allocation)
    print("Total Cost (NWC):", total_cost)

    row_potential, col_potential = compute_potential(costs, allocation)
    print("\nInitial Row Potentials:")
    print(row_potential)
    print("Initial Column Potentials:")
    print(col_potential)

    while True:
        u, v = np.array(row_potential), np.array(col_potential)
        unoccupied_cells = get_unoccupied_cells(allocation)
        for i, j in unoccupied_cells:
            if allocation[i, :].sum() == 0:
                v[j] = costs[i, j] - u[i]
            elif allocation[:, j].sum() == 0:
                u[i] = costs[i, j] - v[j]

        reduced_costs = np.zeros_like(costs)
        for i in range(costs.shape[0]):
            for j in range(costs.shape[1]):
                reduced_costs[i, j] = costs[i, j] - (u[i] + v[j])

        min_cost_cell = np.unravel_index(np.argmin(reduced_costs), reduced_costs.shape)
        if reduced_costs[min_cost_cell] >= 0:
            break

        entering_cell = min_cost_cell
        path = [entering_cell]
        visited = set()
        visited.add(entering_cell)

        while True:
            i, j = path[-1]
            if (i, j[0]) not in visited:
                visited.add((i, j[0]))
                path.append((i, j[0]))
            elif (j[0], i) not in visited:
                visited.add((j[0], i))
                path.append((j[0], i))
            else:
                break

        min_allocation = min(allocation[i, j[0]], allocation[j[0], i])
        for idx, cell in enumerate(path):
            if idx % 2 == 0:
                allocation[cell[0], cell[1][0]] += min_allocation
            else:
                allocation[cell[1][0], cell[0]] -= min_allocation

        row_potential, col_potential = compute_potential(costs, allocation)

    total_cost = np.sum(allocation * costs)
    return allocation, total_cost

# Contoh penggunaan:
matrix_supply = [20, 30, 50]
matrix_demand = [30, 40, 30]
costs = [[8, 6, 10],
         [9, 7, 4],
         [3, 5, 12]]

allocation, total_cost = modi_method(matrix_supply, matrix_demand, costs)
print("\nFinal Allocation Matrix (MODI):")
print(allocation)
print("Total Cost (MODI):", total_cost)

import numpy as np

# Contoh data untuk initial row dan column potentials
row_potential = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]]
allocation_col = np.array(row_potential, dtype=np.str_).flatten(order='F')  # Flattened horizontally
allocation_col = allocation_col.reshape((1, -1))  # Reshape to a horizontal matrix
print(allocation_col)

import numpy as np

def vam_method(matrix_supply, matrix_demand, costs):
    supply = np.array(matrix_supply)
    demand = np.array(matrix_demand)
    costs = np.array(costs)

    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))

    # Menginisialisasi variabel yang diperlukan untuk VAM
    supply_remaining = supply.copy()
    demand_remaining = demand.copy()
    penalties = np.zeros((m, n))

    while True:
        # Menentukan sel dengan biaya terendah (dalam matriks biaya + penalti)
        min_cost_cell = np.argmin(costs + penalties)
        i, j = divmod(min_cost_cell, n)

        # Mengalokasikan sebanyak mungkin dari sumber ke tujuan
        allocation_amount = min(supply_remaining[i], demand_remaining[j])
        allocation[i][j] = allocation_amount

        # Mengurangi sisa persediaan dan permintaan
        supply_remaining[i] -= allocation_amount
        demand_remaining[j] -= allocation_amount

        # Memperbarui penalti
        penalties[i][j] = np.inf  # Menandai sel yang sudah dialokasikan dengan nilai tak terhingga
        for k in range(m):
            for l in range(n):
                if penalties[k][l] != np.inf:  # Hanya sel yang belum dialokasikan yang diperbarui
                    penalties[k][l] = costs[k][l] - np.min([costs[k][j] + penalties[i][l], costs[i][l] + penalties[k][j]])

        # Menghentikan iterasi jika semua persediaan dan permintaan telah terpenuhi
        if np.all(supply_remaining == 0) and np.all(demand_remaining == 0):
            break

    # Menghitung total biaya alokasi
    total_cost = np.sum(allocation * costs)

    return allocation, total_cost

# Contoh penggunaan:
matrix_supply = [20, 30, 50]
matrix_demand = [30, 40, 30]
costs = [[8, 6, 10],
         [9, 7, 4],
         [3, 5, 12]]

allocation, total_cost = vam_method(matrix_supply, matrix_demand, costs)
print("\nFinal Allocation Matrix (VAM):")
print(allocation)
print("Total Cost (VAM):", total_cost)

