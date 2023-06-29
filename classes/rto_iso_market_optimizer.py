import gurobipy as gp
from gurobipy import GRB
from classes.swing_contract_generator import SwingContractGenerator

class MarketOptimizer:

    # This example formulates and solves the model for the RTO-ISO market optimization problem:
    # In the very first attemp, a swing contract market should be designed for a Market M(T)  with T  having 24 k in K (24 hours for day T)
    # Price swing for the reserve offers should be included (price dependent on dispatch point) but the price function should be linear first. 
    # No price dependent reserve bids should be included first

    # The Nodes that should be included in the Flow Model
    nodes = ['A', 'B', 'C']
    # In arcs a set of the arcs is defined ({('A', 'B'), ('A', 'C'), ('B', 'C')}). In capacity the capacity of the arcs is defined
    arcs, capacity = gp.multidict({
    ('A', 'B'):   100,
    ('A', 'C'):  80,
    ('B', 'C'):  120
    })


    # Each variable in one array (this is better for including it into gurobi)
    offer_price_dollar = []
    power_min_mw = []
    power_max_mw = []
    ramping_max_mw_up_per_k = []
    ramping_max_mw_down_per_k = []
    price_per_mw_h_dollar = []
    is_cleared = []
    # power_mw_in_step_k = [][]
    number_of_swing_contract_offers = 0
    number_of_time_steps_k_in_market = 24


    def optimize(self):
        print("Start optimization")

        # This example formulates and solves a simple MIP model:
        try:
            # Create a new model
            gurobi_model = gp.Model("sc_optimization_1")
            
            # Create random swing contracts
            print("Create random swing contracts")
            self.add_random_swing_contract_offers()
            # Prepare arrays (all variables of one type in one array, e.g. all prices are in one array)
            print("Prepare arrays")
            self.prepare_arrays()

            # Create variables for the optimization problem
            print("Creating Gurobi variables")
            self.create_gurobi_variables(gurobi_model)
            
            # Add constraints
            # self.add_constraints(gurobi_model)
            # print("finisehd with adding constraints")

            '''        
            # Set objective function
            # self.set_objective_function(gurobi_model)
            # print("finisehd with seting objective function")

            # Optimize model
            gurobi_model.optimize()

            # Print solution of variabels
            for v in gurobi_model.getVars():
                print('%s %g' % (v.VarName, v.X))

            # Print solution of objective function (optimal values of the variables)
            print('Objective value: %g' % gurobi_model.ObjVal)

            '''
        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ': ' + str(e))

        except AttributeError:
            print('Encountered an attribute error')
        
            


        return 0
    

    # Create variables for the optimization problem
    def create_gurobi_variables(self, gurobi_model):
        # offer_price
        self.keys_offer_price_dollar = gurobi_model.addVars(self.number_of_swing_contract_offers, lb=0, vtype=GRB.CONTINUOUS, name="offer_price_dollar")
        # power_min_mw of a generator, power_max_mw of a generator
        self.keys_power_min_mw = gurobi_model.addVars(self.number_of_swing_contract_offers, lb=0, vtype=GRB.CONTINUOUS, name="power_min_mw")
        self.keys_power_max_mw = gurobi_model.addVars(self.number_of_swing_contract_offers, lb=0, vtype=GRB.CONTINUOUS, name="power_max_mw")
        # max_ramping_up in mw and max_ramping_down in mw of a generator
        self.keys_ramping_max_mw_up_per_k = gurobi_model.addVars(self.number_of_swing_contract_offers, lb=0, vtype=GRB.CONTINUOUS, name="ramping_max_mw_up_per_k")
        self.keys_ramping_max_mw_down_per_k = gurobi_model.addVars(self.number_of_swing_contract_offers, lb=0, vtype=GRB.CONTINUOUS, name="ramping_max_mw_down_per_k")
        # price_per_mw_h_dollar of a generator
        self.keys_price_per_mw_h_dollar = gurobi_model.addVars(self.number_of_swing_contract_offers, lb=0, vtype=GRB.CONTINUOUS, name="price_per_mw_h_dollar")
        # is a swing contract cleared
        self.keys_is_cleared = gurobi_model.addVars(self.number_of_swing_contract_offers, vtype=GRB.BINARY, name="is_cleared")
        # the (to select) power of a generator in a time step k
        self.keys_power_mw_in_step_k = gurobi_model.addVars(self.number_of_swing_contract_offers, self.number_of_time_steps_k_in_market, lb=0, vtype=GRB.CONTINUOUS, name="power_mw_in_step_k")

        
    # Set objective function for the optimization problem
    def set_objective_function(self, gurobi_model):
        print("Set the objective function")

    # Add constraints for the optimization problem
    def add_constraints(self, gurobi_model):
        # Set the offer prices in the model to the correct offer prices from the swing contract offers
        gurobi_model.addConstrs(((self.keys_offer_price_dollar[i] == self.swing_contract_offers[i].offer_price_dollar) for i in range(self.number_of_swing_contract_offers) ), name="c1" )


    def add_random_swing_contract_offers(self):
        # Create three sample swing contracts 
        # This is a list of SwingContractGenerator objects
        self.swing_contract_offers = []
        swing_contract_offer1 = SwingContractGenerator(offer_price_dollar=1, delivery_location="A", powermin_mw=0, powermax_mw=100, ramping_max_mw_up_per_k=10, ramping_max_mw_down_per_k=10, price_per_mw_h_dollar=100)
        swing_contract_offer2 = SwingContractGenerator(offer_price_dollar=3, delivery_location="A", powermin_mw=0, powermax_mw=100, ramping_max_mw_up_per_k=10, ramping_max_mw_down_per_k=10, price_per_mw_h_dollar=100)
        swing_contract_offer3 = SwingContractGenerator(offer_price_dollar=3, delivery_location="A", powermin_mw=0, powermax_mw=100, ramping_max_mw_up_per_k=10, ramping_max_mw_down_per_k=10, price_per_mw_h_dollar=100)
       
        # add swing contracts to the list of swing contract offers
        self.swing_contract_offers.append(swing_contract_offer1)
        self.swing_contract_offers.append(swing_contract_offer2)
        self.swing_contract_offers.append(swing_contract_offer3)

    def prepare_arrays(self):
        for sc in self.swing_contract_offers: 
            self.offer_price_dollar.append(sc.offer_price_dollar)  
            self.power_min_mw.append(sc.powermin_mw)
            self.power_max_mw.append(sc.powermax_mw)
            self.ramping_max_mw_up_per_k.append(sc.ramping_max_mw_up_per_k)
            self.ramping_max_mw_down_per_k.append(sc.ramping_max_mw_down_per_k)
            self.price_per_mw_h_dollar.append(sc.price_per_mw_h_dollar)
            self.number_of_swing_contract_offers += 1