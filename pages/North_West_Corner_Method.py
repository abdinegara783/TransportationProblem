import streamlit as st
import numpy as np
from TransMethod import TransportationProblem

st.sidebar.title("Transportation Calculator Sidebar")
st.sidebar.markdown('---')
st.sidebar.subheader(' North West Corner')
st.sidebar.markdown('---')

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

    history = {
        'supply': matrix_supply,
        'demand': matrix_demand,
        'costs': input_table
    }

    if st.button("Hitung"):
        supply = np.array(matrix_supply)
        demand = np.array(matrix_demand)
        costs = np.array(input_table)
        solver = TransportationProblem(supply, demand, costs)
        num_all = solver.solve_with_north_west_corner()[0]
        total_cost = solver.solve_with_north_west_corner()[1]
        st.write("List Allocation Matrices:")
        for k, allocation in enumerate(num_all):
            allocation = np.array(allocation, dtype=np.str_)
            for i in range(len(input_table)):
                for j in range(len(input_table[0])):
                    allocation[i][j] = allocation[i][j] + " (" + str(input_table[i][j]) + ")"
            st.write("Langkah ke-"+str(k+1)+' :' )
            allocation_html = "<table>"
            for i in range(len(allocation)):
                allocation_html += "<tr>"
                for j in range(len(allocation[0])):
                    allocation_html += f"<td>{allocation[i][j]}</td>"
                allocation_html += "</tr>"
            allocation_html += "</table>"
            st.write(allocation_html, unsafe_allow_html=True)
        
        st.markdown(f" **Total Cost** : {total_cost}")

        # Tampilkan riwayat
        st.subheader("Riwayat")
        history_selection = st.selectbox("Pilih Riwayat Input:", list(range(1, len(history['supply'])+1)))
        st.write("Dimensi Supply:", history['supply'][history_selection-1])
        st.write("Dimensi Demand:", history['demand'][history_selection-1])
        st.write("Biaya:", history['costs'][history_selection-1])

if __name__ == "__main__":
    main()
