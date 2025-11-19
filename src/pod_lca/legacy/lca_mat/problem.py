from lca_mat.processess import ProcessessMatrix
from lca_mat.linear_algebra import LinearAlgebra

from numpy import zeros, ones, matmul
from scipy.linalg import inv, det
from scipy.sparse import csr_matrix

import os
import shutil
import time

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# =================================
# PROBLEM CLASS
# =================================


class Problem(object):

    def __init__(self):
        self.database = None
        self.process_matrix = None
        self.demand = None
        self.product_process_matrix = None
        self.process_exchange_matrix = None
        self.problem_settings = None

    # =================================
    # Setters / Getters
    # =================================

    def set_database(self, database):
        """Sets database for the problem.

        Inputs:
        ------
            database    : LCIDatabase obj.

        """
        self.database = database
        database.load_impacts()

    def set_process_matrix(self, process_matrix):
        """Sets process matrix for the problem.

        Inputs:
        ------
            process_matrix    : dict.

        """
        self.process_matrix = process_matrix

    def set_product_process_matrix(self, product_process_matrix):
        """Sets selection matrix for the problem.

        Inputs:
        ------
            selection_matrix    : array.

        """
        self.product_process_matrix = product_process_matrix

    def set_process_exchange_matrix(self, proces_exchange_matrix):
        """Sets selection matrix for the problem.

        Inputs:
        ------
            selection_matrix    : array.

        """
        self.process_exchange_matrix = proces_exchange_matrix

    def set_demand(self, row, val):

        if self.get_demand() is None:
            print("No inventory to set demand. Create process matrix before setting demand.")
        else:
            self.demand[row] = val

    def get_database(self):
        """Gets database for the problem."""
        return self.database

    def get_process_matrix(self):
        """Gets process matrix for the problem."""
        return self.process_matrix

    def get_product_process_matrix(self):
        """Gets selection matrix for the problem."""
        return self.product_process_matrix

    def get_process_exchange_matrix(self):

        return self.process_exchange_matrix

    def get_demand(self):

        return self.demand

    def get_impacts(self):

        return self.get_database().get_impacts()

    # =================================
    # Printer Methods
    # =================================

    def print_process(self, col_no=None, process_id=None):

        if col_no:
            process_id = self.get_process_matrix().cols[col_no]

        if process_id:
            print(self.get_database().get_unit_processess()[process_id])

    def print_inventory_item(self, row):

        inventory_item = self.get_process_matrix().get_basis().get_inventory_dict()[row]
        print(inventory_item)

    def print_unit_processes(self, n=50):

        terminal_size = shutil.get_terminal_size()
        lines_per_page = terminal_size.lines - 2
        os.system("cls" if os.name == "nt" else "clear")

        P = self.get_process_matrix()

        if P is not None:
            ids = P.get_process_ids()
            unitProcesss = self.get_database().get_unit_processess()
            print("col. no | process ID | process name")
            ctr = 0
            for id in ids.keys():
                print(str(ids[id]) + " | " + id + " | " + unitProcesss[id].get_name()[:n] + "...")

                if ctr > lines_per_page:
                    input("\nPress Enter to continue...")
                    os.system("cls" if os.name == "nt" else "clear")
                    print("col. no | process ID | process name")
                    ctr = 0
                else:
                    ctr += 1
        else:
            print("Create process matrix to load unit processess.")

    def print_inventory(self, n=100, print_nnz=False, tol=0.01):

        terminal_size = shutil.get_terminal_size()
        lines_per_page = terminal_size.lines - 2
        os.system("cls" if os.name == "nt" else "clear")

        P = self.get_process_matrix()
        if P is not None:
            inventory = P.get_basis().get_inventory_dict()
            if print_nnz:
                print("row. no | exchange name | location | unit process id | qty ")
            else:
                print("row. no | exchange name | location | unit process id")
            ctr = 0
            for id in inventory.keys():
                prt_str = str(inventory[id].get_row_num()) + " | " + inventory[id].get_name()[:n]
                if len(inventory[id].get_name()) > n:
                    prt_str += "..."
                prt_str += (
                    (" | " + inventory[id].get_location()) if inventory[id].get_location() is not None else " | --- "
                )
                prt_str += (
                    (" | " + inventory[id].get_unit_process_id())
                    if inventory[id].get_unit_process_id() is not None
                    else " | --- "
                )

                if print_nnz:
                    qty = inventory[id].get_qty()
                    unit = inventory[id].get_unit()
                    if abs(qty) > tol:
                        prt_str += " | " + "{:.2f}".format(qty) + " " + unit
                        print(prt_str)
                        ctr += 1
                else:
                    print(prt_str)
                    ctr += 1

                if ctr > lines_per_page:
                    input("\nPress Enter to continue...")
                    os.system("cls" if os.name == "nt" else "clear")
                    print("row. no | exchange name | location | unit process id")
                    ctr = 0

        else:
            print("Create process matrix to load unit processess.")

    def print_impacts(self):

        impacts = self.get_impacts()

        if impacts:
            print("impact name | qty ")
            for impact in impacts:
                prt_str = impacts[impact].get_name()
                prt_str += " | " + "{:.2f}".format(impacts[impact].get_qty())
                prt_str += " " + impacts[impact].get_unit()
                print(prt_str)
        else:
            print("Load database to print impacts.")

    # =================================
    # User Methods
    # =================================

    def create_process_matrix(self, process_id=None):
        """Creates the full process matrix.

        Inputs:
        ------


        Returns:
        -------

        """

        P = ProcessessMatrix()
        inventory_vector = P.get_basis()
        database = self.get_database()
        unit_processes = database.get_unit_processess(process_id)
        for unit_process in unit_processes.keys():
            inventory_ids, exchange_qtys = inventory_vector.add_inventory_items(
                unit_processes[unit_process].get_exchanges()
            )
            P.add_process(unit_processes[unit_process].get_process_id(), inventory_ids, exchange_qtys)

        self.set_process_matrix(P)

        self._generate_product_process_matrix()
        self._generate_process_exchange_matrix()

        # create demand matrix with all zeros
        rows = self.get_process_matrix().get_no_rows()
        self.demand = zeros(rows)

    def solve(self):
        """Solves the LCI problem.

        Inputs:
        ------


        Returns:
        -------

        """

        _, cols, product_rows = self._partition_process_matrix()

        P = LinearAlgebra.mat_data_to_np_mat(self.get_process_matrix().get_mat_data())
        d = self.get_demand()
        f = d[product_rows]

        A = P[product_rows, :][:, cols]
        if len(product_rows) == len(cols):
            s = matmul(inv(A), f)
        else:
            print("Product matrix is not square. Pseudo-inverse is considered.")
            pass

        # mask = ones(P.shape[0], dtype=bool)
        # mask[product_rows] = False
        # B = P[mask, :][:, cols]

        # g =  matmul(B, s)
        # d[mask] = g

        d = matmul(P[:, cols], s)

        inventory = self.get_process_matrix().get_basis()
        inventory_dict = inventory.get_inventory_dict()
        for i in range(inventory.get_inventory_size()):
            inventory_dict[i].set_qty(d[i])

        self._set_impacts()

        # TODO: Update process qtys

    # =================================
    # Private Methods
    # =================================

    def _generate_product_process_matrix(self):

        rows = self.get_process_matrix().get_no_rows()
        cols = self.get_process_matrix().get_no_cols()

        inventory_dict = self.get_process_matrix().get_basis().get_inventory_dict()
        process_ids = self.get_process_matrix().get_process_ids()

        data = []
        row_indices = []
        col_indices = []

        for item in inventory_dict.keys():
            if inventory_dict[item].unit_process_id is not None:
                process_id = inventory_dict[item].unit_process_id
                row = inventory_dict[item].get_row_num()
                col = process_ids[process_id]

                row_indices.append(row)
                col_indices.append(col)
                data.append(True)
            # else:
            #     if not inventory_dict[item].is_elementary_flow:
            #         raise NotImplementedError

        product_process_matrix = csr_matrix((data, (row_indices, col_indices)), shape=(rows, cols))

        self.set_product_process_matrix(product_process_matrix)

    def _generate_process_exchange_matrix(self):

        rows = self.get_process_matrix().get_no_rows()
        cols = self.get_process_matrix().get_no_cols()

        process_mat_data = self.get_process_matrix().get_mat_data()

        data = []
        row_indices = []
        col_indices = []

        for col in range(cols):
            for row in process_mat_data[col].keys():
                row_indices.append(row)
                col_indices.append(col)
                data.append(True)

        process_exchange_matrix = csr_matrix((data, (row_indices, col_indices)), shape=(rows, cols))

        self.set_process_exchange_matrix(process_exchange_matrix)

    def _partition_process_matrix(self, tol=0.001):

        PP = self.get_product_process_matrix()
        PE = self.get_process_exchange_matrix()

        rows = []
        cols = []

        d = self.get_demand()
        for row in range(len(d)):
            if d[row] > tol:
                rows.extend([row])

        no_rows, no_cols = len(rows), len(cols)
        update = True
        while update:

            cols.extend(PP[rows, :].nonzero()[1].tolist())
            rows.extend(PE[:, cols].nonzero()[0].tolist())

            cols = list(set(cols))
            rows = list(set(rows))

            if (no_rows == len(rows)) and (no_cols == len(cols)):
                update = False
            else:
                no_rows, no_cols = len(rows), len(cols)

        product_rows = PP[:, cols].nonzero()[0].tolist()

        return list(set(rows)), list(set(cols)), product_rows

    def _set_impacts(self):

        inventory = self.get_process_matrix().get_basis()
        inventory_dict = inventory.get_inventory_dict()
        inventory_flows = inventory.get_flow_ids()

        impacts = self.get_impacts()

        for impact in impacts.keys():
            flows = impacts[impact].get_flows()
            for flow in flows.keys():
                rows = inventory_flows[flow]
                unit_impact = flows[flow]
                for row in rows:
                    if inventory_dict[row].is_elementary_flow:
                        qty = inventory_dict[row].get_qty()
                        # TODO: check unit consistency
                        # flow_unit = inventory_dict[row].get_unit()
                        # impact_per_unit_ = impacts[impact]   (??)
                        impacts[impact].add_qty(unit_impact * qty)


if __name__ == "__main__":

    from lca_mat import HOME
    from lca_mat.ecoinvent_database import EcoinventDatabase

    from numpy import sum as npsum

    test_problem = Problem()

    process_database_path = HOME + "\Archive\ecoinvent_391_en15804gd_upr_n2_20230629"
    impact_database_path = HOME + "\Archive\ecoinvent_3_9_1_LCIA_Methods_openLCA_2_(1)"

    database = EcoinventDatabase(process_file_path=process_database_path, impact_file_path=impact_database_path)

    test_problem.set_database(database)
    test_problem.create_process_matrix()

    # processess
    # p1 = 'cement production, Portland | cement, Portland | EN15804, U - United States'
    # p2 = 'market for tap water | tap water | EN15804, U - Rest-of-World'
    # p3 = 'sand quarry operation, extraction from river bed | sand | EN15804, U - Rest-of-World'
    # p4 = 'gravel production, crushed | gravel, crushed | EN15804, U - Rest-of-World'

    # process ids
    # p1 = 'b6d92fa7-13c9-448b-9231-4736c9c4005a'
    # p2 = '3919839c-646f-422b-9cef-95879b14c52c'
    # p3 = 'efc81209-41ba-4abb-a293-a01f4489cf0a'
    # p4 = 'c8671c12-d160-44e7-9d93-e99d373cbd4a'

    # product ids
    # p1 = 'c5299a8e-d4b4-409c-9826-e8ae9e37c03d'
    # p2 = 'c5adb1fb-872e-4446-a3bb-c4b61aa4bd45'
    # p3 = 'f51d7ccf-0bee-430d-98a3-8334adbe39fc'
    # p4 = '37eceabd-b33f-4757-a4b9-5c51dee1710d'

    # product row
    # p1 = 13339
    # p2 = 411
    # p3 = 364
    # p4 = 3477

    # test_problem.print_unit_processes()
    # test_problem.print_inventory()

    # test_problem.print_process(col_no=10)
    test_problem.print_inventory_item(row=13339)

    test_problem.set_demand(13339, val=367.41)
    test_problem.set_demand(411, val=972.05)
    test_problem.set_demand(364, val=754.32)
    test_problem.set_demand(3477, val=18.14)

    test_problem.solve()

    test_problem.print_impacts()

    test_problem.print_inventory(print_nnz=True)

    # can 's' have negative values? negative amount of a process
    # can impact be negative
