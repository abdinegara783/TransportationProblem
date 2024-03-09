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

            #print(f"   {row+1},{col+1}   | {allocation}")

            # Menambahkan alokasi ke dalam list num_all
            num_all.append(allocation.copy())  # Menggunakan copy() untuk mencegah referensi yang sama
        else:
            if supply[row] == 0:
                row += 1
            if demand[col] == 0:
                col += 1
    # print("-----------------------------")
    return num_all, total_cost

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

def main():
    st.title("Menggunakan Metode Vogel Approximation Method (VAM) ")
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
        #allocation, total_cost = north_west_corner(matrix_supply, matrix_demand, input_table)
        num_all, total_cost = vam_method(matrix_supply, matrix_demand, input_table)
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
        
        st.markdown(f" **Total Cost** : {total_cost}")

if __name__ == "__main__":
    main()
