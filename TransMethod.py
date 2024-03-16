#Import a Library
import numpy as np
from pprint import pprint

MAX_INT = np.iinfo(np.intc).max

class TransportationProblem:
    """
    Represents a Transportation Problem solver using various approximation methods.
    """

    def __init__(self, supply: np.ndarray, demand: np.ndarray, costs: np.ndarray):
        """
        Initializes a TransportationProblem instance using input arrays.

        Args:
        - supply (np.ndarray[int]): Array representing the supply from each supplier.
        - demand (np.ndarray[int]): Array representing the demand from each consumer.
        - costs (np.ndarray[np.ndarray[int]]): 2D array representing the transportation costs.
        """
        self.supply = supply
        self.demand = demand
        self.costs = costs
        self.n = len(supply)
        self.m = len(demand)

        self.__check_input()

    def __check_input(self) -> None:
        """
        Checks the validity of the input arrays.
        """
        if self.n != self.supply.size or self.m != self.demand.size:
            raise ValueError("Invalid input: Dimensions of supply and demand do not match.")

        if sum(self.supply) != sum(self.demand):
            raise ValueError("Invalid input: Total supply does not equal total demand.")

    def solve_with_north_west_corner(self) -> np.ndarray:
        """
        Solves the Transportation Problem using the North-West Corner method and returns the solution.

        Returns:
        - np.ndarray: Solution matrix.
        """
        costs = np.zeros_like(self.costs)
        supply = self.supply.copy()
        demand = self.demand.copy()
        step_all=[]
        total_cost = 0
        i, j = 0, 0

        while i < self.n and j < self.m:
            allocation = min(supply[i], demand[j])
            costs[i, j] = allocation
            supply[i] -= allocation
            demand[j] -= allocation
            total_cost += allocation * self.costs[i, j]
            step_all.append(costs.copy())
            #print(total_cost)
            if supply[i] == 0:
                i += 1
            if demand[j] == 0:
                j += 1

        return step_all,  total_cost

    def __find_diff(self, costs: np.ndarray[np.ndarray[int]]):
        """
            Finds the difference between the two smallest and the two smallest values in each row and column.

            Args:
            - costs (np.ndarray[np.ndarray[int]]): Transportation costs matrix.

            Returns:
            - Tuple[np.ndarray[int], np.ndarray[int]]: Tuple containing row differences and column differences.
        """

        row_diff = np.array([])
        col_diff = np.array([])

        for i in range(self.n):
            arr = costs[i][:]
            arr = np.sort(arr)
            row_diff = np.append(row_diff, arr[1] - arr[0])
        col = 0

        while col < self.m:
            arr = np.array([])
            for i in range(self.n):
                arr = np.append(arr, costs[i][col])
            arr = np.sort(arr)
            col += 1
            col_diff = np.append(col_diff, arr[1] - arr[0])
        return row_diff, col_diff

    def get_total_cost(self, costs, ans):
      total_cost = 0
      for i, row in enumerate(costs):
          for j, cost in enumerate(row):
              total_cost += cost * ans[i][j]
      return total_cost

    def solve_with_vogel_approximation(self) -> np.ndarray[np.ndarray[int]]:
        """
            Solves the Transportation Problem using Vogel's Approximation method and returns the solution.

            Returns:
            - np.ndarray[np.ndarray[int]]: Solution matrix.
        """
        ans = np.zeros_like(self.costs)
        costs = self.costs.copy()
        supply = self.supply.copy()
        demand = self.demand.copy()
        step_all=[]

        while np.max(supply) != 0 or np.max(demand) != 0:
            row, col = self.__find_diff(costs)
            row_max = np.max(row)
            row_col = np.max(col)

            if row_max >= row_col:
                for row_index, row_value in enumerate(row):
                    if row_value == row_max:
                        row_min = np.min(costs[row_index])

                        for col_index, col_value in enumerate(costs[row_index]):
                            if col_value == row_min:
                                min_value = min(supply[row_index], demand[col_index])

                                ans[row_index][col_index] = min_value
                                step_all.append(ans.copy())  # Menggunakan copy() untuk mencegah referensi yang sama
                                supply[row_index] -= min_value
                                demand[col_index] -= min_value
                                if demand[col_index] == 0:
                                    for r in range(self.n):
                                        costs[r][col_index] = MAX_INT
                                else:
                                    costs[row_index] = [MAX_INT for _ in range(self.m)]
                                break
                        break
            else:
                for row_index, row_value in enumerate(col):
                    if row_value == row_col:
                        row_min = MAX_INT
                        for j in range(self.n):
                            row_min = min(row_min, costs[j][row_index])

                        for col_index in range(self.n):
                            col_value = costs[col_index][row_index]
                            if col_value == row_min:
                                min_value = min(supply[col_index], demand[row_index])
                                ans[col_index][row_index] = min_value
                                step_all.append(ans.copy())
                                supply[col_index] -= min_value
                                demand[row_index] -= min_value
                                if demand[row_index] == 0:
                                    for r in range(self.n):
                                        costs[r][row_index] = MAX_INT
                                else:
                                    costs[col_index] = [MAX_INT for _ in range(self.m)]
                                break
                        break
        tot_cost = self.get_total_cost(self.costs, ans)
        return step_all, tot_cost



    def get_balanced(self, supply, demand, costs, penalties = None):
        total_supply = sum(supply)
        total_demand = sum(demand)

        if total_supply < total_demand:
            if penalties is None:
                raise Exception('Supply less than demand, penalties required')
            new_supply = supply + [total_demand - total_supply]
            new_costs = costs + [penalties]
            return new_supply, demand, new_costs
        if total_supply > total_demand:
            new_demand = demand + [total_supply - total_demand]
            new_costs = costs + [[0 for _ in demand]]
            return supply, new_demand, new_costs
        return supply, demand, costs

    def monalisha(self, supply, demand,costs):
        supply_copy = supply.copy()
        demand_copy = demand.copy()
        step_all=[]
        m=len(supply)
        n=len(demand)
        i = 0
        j = 0
        bfs = []
        while len(bfs) < len(supply) + len(demand) - 1:
            s = supply_copy[i]
            d = demand_copy[j]
            v = min(s, d)
            supply_copy[i] -= v
            demand_copy[j] -= v
            bfs.append(((i, j), v))
            if supply_copy[i] == 0 and i < len(supply) - 1:
                i += 1
            elif demand_copy[j] == 0 and j < len(demand) - 1:
                j += 1
        cost=0
        bfs_arr = [[0 for i in range(n)] for j in range(m)]
        for item in bfs:
            bfs_arr[item[0][0]][item[0][1]]=item[1]
        #print('\n The initial bfs is:\n',bfs_arr)
        for item in bfs:
            cost=cost+costs[item[0][0]][item[0][1]]*item[1]
        #print('total bfs cost is: ',cost)
        return bfs

    def get_us_and_vs(self, bfs, costs):
        us = [None] * len(costs)
        vs = [None] * len(costs[0])
        us[0] = 0
        bfs_copy = bfs.copy()
        while len(bfs_copy) > 0:
            for index, bv in enumerate(bfs_copy):
                i, j = bv[0]
                if us[i] is None and vs[j] is None: continue

                cost = costs[i][j]
                if us[i] is None:
                    us[i] = cost - vs[j]
                else:
                    vs[j] = cost - us[i]
                bfs_copy.pop(index)
                break

        return us, vs

    def get_ws(self, bfs, costs, us, vs):
        ws = []
        for i, row in enumerate(costs):
            for j, cost in enumerate(row):
                non_basic = all([p[0] != i or p[1] != j for p, v in bfs])
                if non_basic:
                    ws.append(((i, j), us[i] + vs[j] - cost))

        return ws

    def can_be_improved(self, ws):
        for p, v in ws:
            if v > 0: return True
        return False

    def get_entering_variable_position(self, ws):
        ws_copy = ws.copy()
        ws_copy.sort(key=lambda w: w[1])
        return ws_copy[-1][0]

    def get_possible_next_nodes(self, loop, not_visited):
        last_node = loop[-1]
        nodes_in_row = [n for n in not_visited if n[0] == last_node[0]]
        nodes_in_column = [n for n in not_visited if n[1] == last_node[1]]
        if len(loop) < 2:
            return nodes_in_row + nodes_in_column
        else:
            prev_node = loop[-2]
            row_move = prev_node[0] == last_node[0]
            if row_move: return nodes_in_column
            return nodes_in_row

    def get_loop(self, bv_positions, ev_position):
        def inner(loop):
            if len(loop) > 3:
                can_be_closed = len(self.get_possible_next_nodes(loop, [ev_position])) == 1
                if can_be_closed: return loop

            not_visited = list(set(bv_positions) - set(loop))
            possible_next_nodes = self.get_possible_next_nodes(loop, not_visited)
            for next_node in possible_next_nodes:
                new_loop = inner(loop + [next_node])
                if new_loop: return new_loop

        return inner([ev_position])

    def loop_pivoting(self, bfs, loop):
        even_cells = loop[0::2]
        odd_cells = loop[1::2]
        get_bv = lambda pos: next(v for p, v in bfs if p == pos)
        leaving_position = sorted(odd_cells, key=get_bv)[0]
        leaving_value = get_bv(leaving_position)

        new_bfs = []
        for p, v in [bv for bv in bfs if bv[0] != leaving_position] + [(loop[0], 0)]:
            if p in even_cells:
                v += leaving_value
            elif p in odd_cells:
                v -= leaving_value
            new_bfs.append((p, v))

        return new_bfs

    def solve_with_monalisha(self, supply, demand, costs) -> np.ndarray:
        """
        Solves the Transportation Problem using the North-West Corner method and returns the solution.

        Returns:
        - np.ndarray: Solution matrix.
        """
        costs = np.zeros_like(self.costs)
        supply = supply.copy()
        demand = demand.copy()
        step_all=[]
        total_cost = 0
        i, j = 0, 0

        while i < self.n and j < self.m:
            allocation = min(supply[i], demand[j])
            costs[i, j] = allocation
            supply[i] -= allocation
            demand[j] -= allocation
            total_cost += allocation * self.costs[i, j]
            step_all.append(costs.copy())
            #print(total_cost)
            if supply[i] == 0:
                i += 1
            if demand[j] == 0:
                j += 1

        return step_all,  total_cost

    def monalisha_method(self) -> np.ndarray[np.ndarray[int]]:
         
        ans = np.zeros_like(self.costs)
        costs = self.costs.copy()
        supply = self.supply.copy()
        demand = self.demand.copy()
        penalties = None
        step_all=[]

        balanced_supply, balanced_demand, balanced_costs = self.get_balanced(
            supply, demand, costs
        )
        def inner(bfs):
            us, vs = self.get_us_and_vs(bfs, balanced_costs)
            ws = self.get_ws(bfs, balanced_costs, us, vs)
            if self.can_be_improved(ws):
                ev_position = self.get_entering_variable_position(ws)
                loop = self.get_loop([p for p, v in bfs], ev_position)
                return inner(self.loop_pivoting(bfs, loop))
            return bfs
        basic_variables = inner(self.monalisha(balanced_supply, balanced_demand,costs))
        basic_variables_v, _ = self.solve_with_monalisha(balanced_supply, balanced_demand,costs)
        ans = np.zeros((len(costs), len(costs[0])))
        for (i, j), v in basic_variables:
            ans[i][j] = int(v)
        basic_variables_v.append(ans.copy())
        tot_cost = self.get_total_cost(self.costs, ans)
        return basic_variables_v, tot_cost
    # Implement metode Vogel, Russell, dan metode MODI yang lainnya secara serupa seperti sebelumnya

    @staticmethod
    def __update_max_values(
            n: int,
            m: int,
            u: np.ndarray[int],
            v: np.ndarray[int],
            costs: np.ndarray[np.ndarray[int]],
            supply: np.ndarray[int],
            demand: np.ndarray[int],
    ) -> None:
        """
            Updates the maximum values for each row and column in the given arrays.

            Args:
            - n (int): Number of suppliers.
            - m (int): Number of consumers.
            - u (np.ndarray[int]): Array representing the dual variable for each supplier.
            - v (np.ndarray[int]): Array representing the dual variable for each consumer.
            - costs (np.ndarray[np.ndarray[int]]): Transportation costs matrix.
            - supply (np.ndarray[int]): Array representing the supply from each supplier.
            - demand (np.ndarray[int]): Array representing the demand from each consumer.
        """

        for i in range(n):
            u[i] = max(costs[i, :]) if supply[i] > 0 else u[i]
        for j in range(m):
            v[j] = max(costs[:, j]) if demand[j] > 0 else v[j]

    @staticmethod
    def __find_max_position(
            u: np.ndarray[int],
            v: np.ndarray[int],
            costs: np.ndarray[np.ndarray[int]],
            supply: np.ndarray[int],
            demand: np.ndarray[int],
    ) -> tuple[int, int]:
        """
            Finds the position with the maximum Russell value in the given arrays.

            Args:
            - u (np.ndarray[int]): Array representing the dual variable for each supplier.
            - v (np.ndarray[int]): Array representing the dual variable for each consumer.
            - costs (np.ndarray[np.ndarray[int]]): Transportation costs matrix.
            - supply (np.ndarray[int]): Array representing the supply from each supplier.
            - demand (np.ndarray[int]): Array representing the demand from each consumer.

            Returns:
            - Tuple[int, int]: Tuple containing the row and column indices of the maximum position.
        """
        max_value = -MAX_INT
        max_pos = -1, -1
        for i in range(len(u)):
            for j in range(len(v)):
                if supply[i] > 0 and demand[j] > 0:
                    russell_value = u[i] + v[j] - costs[i, j]
                    if russell_value > max_value:
                        max_value = russell_value
                        max_pos = i, j
        return max_pos

    @staticmethod
    def __allocate_at_max_position(
            ans: np.ndarray[np.ndarray[int]],
            max_pos: tuple[int, int],
            supply: np.ndarray[int],
            demand: np.ndarray[int],
    ) -> None:
        """
            Allocates transportation at the position with the maximum Russell value.

            Args:
            - ans (np.ndarray[np.ndarray[int]]): Solution matrix.
            - max_pos (Tuple[int, int]): Tuple containing the row and column indices of the maximum position.
            - supply (np.ndarray[int]): Array representing the supply from each supplier.
            - demand (np.ndarray[int]): Array representing the demand from each consumer.
        """
        allocation = min(supply[max_pos[0]], demand[max_pos[1]])
        ans[max_pos[0], max_pos[1]] = allocation
        supply[max_pos[0]] -= allocation
        demand[max_pos[1]] -= allocation

    def solve_with_russel_approximation(self):
        """
            Solves the Transportation Problem using Russell's Approximation method and returns the solution.

            Returns:
            - np.ndarray[np.ndarray[int]]: Solution matrix.
        """
        ans = np.zeros_like(self.costs)
        step_all = []
        u = np.full(self.n, -MAX_INT)
        v = np.full(self.m, -MAX_INT)

        supply = self.supply.copy()
        demand = self.demand.copy()
        costs = self.costs.copy()

        while supply.sum() > 0 and demand.sum() > 0:
            self.__update_max_values(self.n, self.m, u, v, costs, supply, demand)
            max_pos = self.__find_max_position(u, v, costs, supply, demand)
            self.__allocate_at_max_position(ans, max_pos, supply, demand)
            step_all.append(ans.copy())
        tot_cost = self.get_total_cost(self.costs, ans)
        return step_all, tot_cost


    # Implement Vogel's Approximation and Russell's Approximation methods similarly
