import streamlit as st
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

def main():
    st.title("Menggunakan Metode Monalisha")
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
        num_all, total_cost = monalisa(matrix_supply, matrix_demand, input_table)
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
