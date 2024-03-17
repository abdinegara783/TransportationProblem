import streamlit as st
import numpy as np
from TransMethod import TransportationProblem

def isDegenerate(m, n, l):
  if m+n-1 == l:
    # Not degenrate
    return False
  else:
    # Degenerate
    return True

def get_uv(bfs, cost_matrix, default):
  u = [None] * len(cost_matrix)
  v = [None] * len(cost_matrix[0])

  u[default] = 0
  bfs_copy = bfs.copy()

  while len(bfs_copy)>0:
    for index, bv in enumerate(bfs_copy):
      i, j = bv[2]

      if u[i] is None and v[j] is None:
        continue

      c_ij = cost_matrix[i][j]
      if u[i] is None:
        u[i] = c_ij - v[j]
      if v[j] is None:
        v[j] = c_ij - u[i]

      bfs_copy.pop(index)
      break

  return u, v

def get_d(bfs, cost_matrix, u, v):
  d = []
  allocated_cells = [bfs[i][2] for i in range(len(bfs))]

  for i in range(len(cost_matrix)):
    for j in range(len(cost_matrix[0])):
      if (i,j) not in allocated_cells:
        c_ij = cost_matrix[i][j]
        d_ij = c_ij - u[i] - v[j]
        d.append([d_ij,(i,j)])

  return d

def get_min_index(d):
  min_index = 0
  min_val = d[0][0]
  for i in range(len(d)):
    if d[i][0] < min_val:
      min_val = d[i][0]
      min_index = i
  return min_index

def get_loop(bfs, p_row, p_col):

  loop_indices = [(p_row, p_col)]
  assigned = [i[2] for i in bfs]
  # ic(assigned)

  same_row_assignments = []
  same_col_assignments = []

  for assignment in assigned:
    if assignment[0] == p_row:
      same_row_assignments.append(assignment)
    if assignment[1] == p_col:
      same_col_assignments.append(assignment)

  # ic(same_row_assignments)
  # ic(same_col_assignments)

  for i in same_row_assignments:
    fl = 0
    for j in same_col_assignments:
      if (j[0],i[1]) in assigned:
        # ic(j[0],i[1])
        loop_indices.append(i)
        loop_indices.append(j)
        loop_indices.append((j[0],i[1]))
        fl = 1
        break
    if fl==1:
      return loop_indices

  return None


def improve(cost_matrix, bfs, d):
  min_index = get_min_index(d)
  # ic(min_index)

  p_row,p_col = d[min_index][1]

  loop_indices = get_loop(bfs, p_row, p_col)
  if loop_indices == None:
    return None

  # ic(loop_indices)

  bfs_dict = {}
  for i in bfs:
    bfs_dict[i[2]] = [i[0], i[1]]
  # ic(bfs_dict)

  # min_alloc = float("Inf")
  min_alloc = min(bfs_dict[loop_indices[1]][0],
                  bfs_dict[loop_indices[2]][0])

  # ic(min_alloc)

  bfs_dict[loop_indices[0]] = [min_alloc, cost_matrix[loop_indices[0][0]][loop_indices[0][1]]]
  bfs_dict[loop_indices[1]][0] -= min_alloc
  bfs_dict[loop_indices[2]][0] -= min_alloc
  bfs_dict[loop_indices[3]][0] += min_alloc

  # ic(bfs_dict)

  new_bfs = []
  for key, val in bfs_dict.items():
    if val[0] != 0:
      new_bfs.append([val[0], val[1], key])

  # ic(new_bfs)
  return new_bfs

def MODI(supply, demand, cost_matrix, bfs):

  default = 0
  # for i in range(2):
  while True:
    u,v = get_uv(bfs, cost_matrix, default)
    # ic(u)
    # ic(v)
    d = get_d(bfs, cost_matrix, u, v)
    # ic(d)
    if not any(i[0]<0 for i in d):
      # ic("OPT", bfs)
      return bfs

    temp_bfs = improve(cost_matrix, bfs, d)
    if temp_bfs == None:
      default = default + 1
      if default == len(u):
        # print("*Complex closed path")
        return None
    else:
      bfs = temp_bfs

def calculate_cost(fs):
  cost = 0
  for i in fs:
    cost += i[0]*i[1]
  return cost

def non_zero_elements(matrix, costs):
    result = []
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val != 0:
                result.append((val, costs[i,j], (i, j)))
    return result


st.sidebar.title("Transportation Calculator Sidebar")
st.sidebar.markdown('---')
st.sidebar.subheader('Modification Method (MODI)')
st.sidebar.markdown('---')

def main():
    st.title("Menggunakan Metode Modification Method (MODI)")
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
    
    Metode = st.selectbox("Pilih Metode yang Diingingkan sebagai nilai awal",
                                ['North West Corner','Vogel Approximation','Monalisha Approximation'])

    if st.button("Hitung"):
        supply = np.array(matrix_supply)
        demand = np.array(matrix_demand)
        costs = np.array(input_table)
        answer = np.zeros_like(costs)
        solver = TransportationProblem(supply, demand, costs)
        if Metode == 'North West Corner':
          num_all = solver.solve_with_north_west_corner()[0]
          total_cost = solver.solve_with_north_west_corner()[1]
        elif Metode == 'Vogel Approximation':
          num_all = solver.solve_with_vogel_approximation()[0]
          total_cost = solver.solve_with_vogel_approximation()[1]
        else:
          num_all = solver.monalisha_method()[0]
          total_cost = solver.monalisha_method()[1]              
        ans = non_zero_elements(num_all[-1], costs)
        ops = MODI(supply, demand, costs, ans)
        total_cost_MODI = calculate_cost(ops)
        for a, b, (i,j) in ops:
           answer[i][j] = int(a)
        num_all.append(answer.copy())
        st.write("List Allocation Matrices:")
        for k, allocation in enumerate(num_all):
            allocation = np.array(allocation, dtype=np.str_)
            for i in range(len(input_table)):
                for j in range(len(input_table[0])):
                    allocation[i][j] = allocation[i][j] + " (" + str(input_table[i][j]) + ")"
            if k == len(num_all)-2:
              st.write("\n **Nilai Awal Adalah** : " )
              allocation_html = "<table>"
              for i in range(len(allocation)):
                  allocation_html += "<tr>"
                  for j in range(len(allocation[0])):
                      allocation_html += f"<td>{allocation[i][j]}</td>"
                  allocation_html += "</tr>"
              allocation_html += "</table>"
              st.write(allocation_html, unsafe_allow_html=True)
              st.markdown(f" **Total Cost** : {total_cost}")
            if k == len(num_all)-1:
              st.write("\n **Hasil Setelah Modi** : " )
              allocation_html = "<table>"
              for i in range(len(allocation)):
                  allocation_html += "<tr>"
                  for j in range(len(allocation[0])):
                      allocation_html += f"<td>{allocation[i][j]}</td>"
                  allocation_html += "</tr>"
              allocation_html += "</table>"
              st.write(allocation_html, unsafe_allow_html=True)
              st.markdown(f" **Total Cost Setelah MODI** : {total_cost_MODI}")
            else:
              st.write("Langkah ke-"+str(k+1)+' :' )
              allocation_html = "<table>"
              for i in range(len(allocation)):
                  allocation_html += "<tr>"
                  for j in range(len(allocation[0])):
                      allocation_html += f"<td>{allocation[i][j]}</td>"
                  allocation_html += "</tr>"
              allocation_html += "</table>"
              st.write(allocation_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
