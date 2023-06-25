import gurobipy as gp
from gurobipy import GRB
from classes.swing_contract_generator import SwingContractGenerator

class MarketOptimizer:

    # Get all the Swing Contract Offers from the generators (do it directly here)
    # This is a list of SwingContractGenerator objects
    swing_contract_offers = []
    swing_contract_offer1 = SwingContractGenerator()
    swing_contract_offer1.offer_price_dollar = 10	
    swing_contract_offer1.powermin_mw = 0
    swing_contract_offer1.powermax_mw = 100

    # add first swing contract to the list of swing contract offers
    swing_contract_offers.append(swing_contract_offer1)

    # put the first swing contract into the optimization problem


    # This example formulates and solves the model for the RTO-ISO market optimization problem:
    # In the very first attemp, a swing contract market should be designed for a Market M(T)  with T  having 24 k in K (24 hours for day T)
    # Price swing for the reserve offers should be included (price dependent on dispatch point) but the price function should be linear first. 
    # No price dependent reserve bids should be included first

    def optimize(self):

        # This example formulates and solves a simple MIP model:
        try:
            # Create a new model
            gurobi_model = gp.Model("sc_optimization_1")

            # Create variables for the optimization problem
            self.create_gurobi_variables(gurobi_model)

            # Set objective function
            self.set_objective_function(gurobi_model)

            # Add constraints
            self.add_constraints(gurobi_model)

            # Optimize model
            gurobi_model.optimize()

            # Print solution of variabels
            for v in gurobi_model.getVars():
                print('%s %g' % (v.VarName, v.X))

            # Print solution of objective function (optimal values of the variables)
            print('Objective value: %g' % gurobi_model.ObjVal)

        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ': ' + str(e))

        except AttributeError:
            print('Encountered an attribute error')




        return 0
    

    # Create variables for the optimization problem
    def create_gurobi_variables(self, gurobi_model):
        # Create variables
        self.x = gurobi_model.addVar(vtype=GRB.BINARY, name="x")
        self.y = gurobi_model.addVar(vtype=GRB.BINARY, name="y")
        self.z = gurobi_model.addVar(vtype=GRB.BINARY, name="z")

    # Set objective function for the optimization problem
    def set_objective_function(self, gurobi_model):
        # Set objective
        gurobi_model.setObjective(self.x + self.y + 2 * self.z, GRB.MAXIMIZE)


    # Add constraints for the optimization problem
    def add_constraints(self, gurobi_model):
        # Add constraint: x + 2 y + 3 z <= 4
        gurobi_model.addConstr(self.x + 2 * self.y + 3 * self.z <= 4, "c0")

        # Add constraint: x + y >= 1
        gurobi_model.addConstr(self.x + self.y >= 1, "c1")