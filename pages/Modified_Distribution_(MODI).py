import streamlit as st
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

    # print("Iterasi | Allocation Matrix")
    # print("-----------------------------")
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
    # print("-----------------------------")
    return num_all, total_cost


def north_west_corner(matrix_supply, matrix_demand, costs):
    num_all = []
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
            # Menambahkan alokasi ke dalam list num_all
            num_all.append(allocation.copy())  # Menggunakan copy() untuk mencegah referensi yang sama
        else:
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1

    return num_all, total_cost

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

    num_all, total_cost = north_west_corner(matrix_supply, matrix_demand, costs)
    allocation = num_all[len(num_all)-1]
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
    return num_all, allocation, total_cost, row_potential, col_potential

# # Contoh penggunaan:
# matrix_supply = [20, 30, 50]
# matrix_demand = [30, 40, 30]
# costs = [[8, 6, 10],
#          [9, 7, 4],
#          [3, 5, 12]]

# allocation, total_cost, row_potential, col_potential = modi_method(matrix_supply, matrix_demand, costs)
# print("\nFinal Allocation Matrix (MODI):")
# print(allocation)
# print("Total Cost (MODI):", total_cost)


def main():
    st.title("Menggunakan Metode North West Corner")
    st.subheader("Created by Ahmad Hanafi Prasetyo")

    st.markdown("**Masukan Dimensi Supply dan Demand**")
    m = st.number_input("Jumlah Baris (Supply): ", min_value=1, step=1)
    n = st.number_input("Jumlah Kolom (Demand): ", min_value=1, step=1)

    matrix_supply = []
    matrix_demand = []
    costs = []

    st.markdown("**Masukan Nilai Supply**")
    for i in range(m):
        matrix_supply.append(st.number_input(f"Supply pada Baris {i+1}: ", min_value=0, step=1))

    st.markdown("**Masukan Nilai Demand**")
    for i in range(n):
        matrix_demand.append(st.number_input(f"Demand pada Kolom {i+1}: ", min_value=0, step=1))

    st.markdown("**Masukan Biaya:**")
    input_table = []
    for i in range(m):
        cost_row = st.text_input(f"Biaya untuk Baris {i+1} (Dipisahkan dengan spasi): ")
        cost_row = cost_row.split()  # Split string menjadi list angka
        cost_row = [int(x) for x in cost_row]  # Konversi angka dari string ke integer
        input_table.append(cost_row)

    if st.button("Hitung"):
        num_all, allocations, total_cost, row_potential, col_potential = modi_method(matrix_supply, matrix_demand, input_table)
        st.write("List Allocation Matrices:")
        for k, allocation in enumerate(num_all):
            allocation = np.array(allocation, dtype=np.str_)
            for i in range(len(input_table)):
                for j in range(len(input_table[0])):
                    allocation[i][j] = allocation[i][j] + " (" + str(input_table[i][j]) + ")"
            st.write("Allocation Matrix "+str(k+1)+' :' )
            allocation_html = "<table>"
            for i in range(len(allocation)):
                allocation_html += "<tr>"
                for j in range(len(allocation[0])):
                    allocation_html += f"<td>{allocation[i][j]}</td>"
                allocation_html += "</tr>"
            allocation_html += "</table>"
            st.write(allocation_html, unsafe_allow_html=True)

        st.markdown(" **Initial Row Potentials** :")
        allocation = np.array(row_potential, dtype=np.str_)
        allocation_html = "<table>"
        for i in range(len(allocation)):
            allocation_html += "<tr>"
            for j in range(len(allocation[0])):
                allocation_html += f"<td>{allocation[i][j]}</td>"
            allocation_html += "</tr>"
        allocation_html += "</table>"
        st.write(allocation_html, unsafe_allow_html=True)
        st.markdown(" **Initial Col Potentials** :")
        allocation = np.array(col_potential, dtype=np.str_)
        allocation_html = "<table>"
        for i in range(len(allocation)):
            allocation_html += "<tr>"
            for j in range(len(allocation[0])):
                allocation_html += f"<td>{allocation[i][j]}</td>"
            allocation_html += "</tr>"
        allocation_html += "</table>"
        st.write(allocation_html, unsafe_allow_html=True)
        allocation = allocations
        allocation = np.array(allocation, dtype=np.str_)
        for i in range(len(input_table)):
            for j in range(len(input_table[0])):
                allocation[i][j] = allocation[i][j] + " (" + str(input_table[i][j]) + ")"
        st.write(" **Matrix Alocation after (MODI)** : " )
        allocation_html = "<table>"
        for i in range(len(allocation)):
            allocation_html += "<tr>"
            for j in range(len(allocation[0])):
                allocation_html += f"<td>{allocation[i][j]}</td>"
            allocation_html += "</tr>"
        allocation_html += "</table>"
        st.write(allocation_html, unsafe_allow_html=True)
        st.markdown(f" **Total Cost** : {total_cost}")

if __name__ == "__main__":
    main()
