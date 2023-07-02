import gurobipy as gp
from gurobipy import GRB
from classes.generator.swing_contract_generator import SwingContractGenerator
from classes.load_serving_entity.swing_contract_puchaser import SwingContractPurchaser


class MarketOptimizer:

    # This example formulates and solves the model for the RTO-ISO market optimization problem:
    # In the very first attemp, a swing contract market should be designed for a Market M(T)  with T  having 24 k in K (24 hours for day T)
    # Price swing for the reserve offers should be included (price dependent on dispatch point), for 10 different dispatch points (each power step of same width) a price is beeing set
    # No price dependent reserve bids should be included first

    # power_mw_in_step_k = [][]: added as a variable to the swing contract generator class and as a decision variable to the optimization problem
    number_of_swing_contract_offers = 0
    number_of_time_steps_k_in_market = 24

    # swing contract generator powerprice_curve discretzation in 10 steps
    # if a more granular discretization is needed, the number of steps can be increased but then also the creation of the swing contract generator powerprice_curve needs to be changed
    number_of_powerprice_steps = 10

    # cost for PowerImbalance for each time step k in K
    power_imb_cost_dlar_per_mwh_pos = 1000
    power_imb_cost_dlar_per_mwh_neg = 1000

    
    def optimize(self):
        print("Start optimization")

        # This example formulates and solves a simple MIP model:
        try:
            # Create a new model
            gurobi_model = gp.Model("sc_optimization_1")
            
            # Create random swing contracts
            print("Create random swing contracts")
            self.add_random_swing_contract_offers()

            # Create random load profiles
            print("Create random load profiles")
            self.add_random_swing_contract_purchaser()

            # Create variables for the optimization problem
            print("Creating Gurobi variables")
            self.create_gurobi_variables(gurobi_model)
            
            # Add constraints
            print("Adding constraints")
            self.add_gurobi_constraints(gurobi_model)
                   
            # Set objective function
            print("Setting objective function")
            self.set_gurobi_objective_function(gurobi_model)

            # Optimize model
            gurobi_model.optimize()

            # Print solution of variabels
            print('Objective value: %g' % gurobi_model.ObjVal)

            # Print solution of variables
            for v in gurobi_model.getVars():
                print('%s %g' % (v.VarName, v.X))

            gurobi_model.dispose()
            gp.disposeDefaultEnv()

        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ': ' + str(e))

        except AttributeError:
            print('Encountered an attribute error')
        
        return 0
    

    # Create variables for the optimization problem
    def create_gurobi_variables(self, gurobi_model):
        # is a swing contract cleared
        self.keys_is_cleared = gurobi_model.addVars(self.number_of_swing_contract_offers, vtype=GRB.BINARY, name="is_cleared")
        # the (to select) power of a generator in a time step k
        self.keys_power_mw_in_step_k = gurobi_model.addVars(self.number_of_swing_contract_offers, self.number_of_time_steps_k_in_market, lb=0, vtype=GRB.CONTINUOUS, name="power_mw_in_step_k")

        # the power price steps that are used from a generator in a time step k for each swing contract
        # for example a generator could use 2 MW of the 10 MW power it can to generate.
        # Then the variable would look like [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]  
        self.keys_powerprice_steps_used_in_step_k = gurobi_model.addVars(self.number_of_swing_contract_offers, self.number_of_time_steps_k_in_market, self.number_of_powerprice_steps, lb=0, ub=1, vtype=GRB.CONTINUOUS, name="powerprice_steps_used_in_step_k")

        # the power imbalance (pos and neg) in a time step k
        self.keys_power_imb_mw_pos = gurobi_model.addVars(self.number_of_time_steps_k_in_market, lb=0, vtype=GRB.CONTINUOUS, name="keys_power_imb_mw_pos")
        self.keys_power_imb_mw_neg = gurobi_model.addVars(self.number_of_time_steps_k_in_market, lb=0, vtype=GRB.CONTINUOUS, name="keys_power_imb_mw_neg")




    # Add constraints for the optimization problem
    def add_gurobi_constraints(self, gurobi_model):    
        # Set the power_mw_in_step_k in the model to smaller or equal to powermax_mw from the swing contract offers
        gurobi_model.addConstrs(self.keys_power_mw_in_step_k[i, k] <= self.swing_contract_offers[i].powermax_mw for i in range(self.number_of_swing_contract_offers) for k in range(self.number_of_time_steps_k_in_market))

        # Choose correct positive and negative power imbalance
        # positive power imbalance is: (power of step k) - (load profile of step k) ; lower_bound = 0
        gurobi_model.addConstrs( self.keys_power_imb_mw_pos[k] >= sum((self.keys_power_mw_in_step_k[i, k] * self.keys_is_cleared[i]) for i in range(self.number_of_swing_contract_offers)) - sum((self.swing_contract_purchaser[i].load_profile_mw_in_step_k[k]) for i in range(len(self.swing_contract_purchaser))) for k in range(self.number_of_time_steps_k_in_market))
        # negative power imbalance is: (load profile of step k) - (power of step k) ; lower_bound = 0
        gurobi_model.addConstrs( self.keys_power_imb_mw_neg[k] >= sum((self.swing_contract_purchaser[i].load_profile_mw_in_step_k[k]) for i in range(len(self.swing_contract_purchaser))) - sum((self.keys_power_mw_in_step_k[i, k] * self.keys_is_cleared[i]) for i in range(self.number_of_swing_contract_offers)) for k in range(self.number_of_time_steps_k_in_market))

        # make sure, that for each swing contract the choosen powerprice_steps_used_in_step_k are enough to cover the power_mw_in_step_k
        #                                                                           how much of this power price step is taken (betw. 0 and 1)     *          power increase of one discrete power step
        gurobi_model.addConstrs( self.keys_power_mw_in_step_k[i, k]   <=      sum(self.keys_powerprice_steps_used_in_step_k[i, k, j] * (self.swing_contract_offers[i].powermax_mw / self.number_of_powerprice_steps) for j in range(self.number_of_powerprice_steps) )  for i in range(self.number_of_swing_contract_offers) for k in range(self.number_of_time_steps_k_in_market) )
        # make sure, that the first powerprice_step_used_in_step_k are used first (e.g. when the next powerprice steps is not zero, than this needs to be one -> no two steps not one after another)
        # the j+1 step is not zero => the j step is one
        # not the j step is one =>  the j+1 step is zero

        gurobi_model.addConstrs(self.keys_powerprice_steps_used_in_step_k[i, k, j+1] <= self.keys_powerprice_steps_used_in_step_k[i, k, j] for i in range(self.number_of_swing_contract_offers) for k in range(self.number_of_time_steps_k_in_market) for j in range(self.number_of_powerprice_steps - 1))



    # Set objective function for the optimization problem
    def set_gurobi_objective_function(self, gurobi_model):
        # Set the objective function:
        # Minimize the following:
        # sum over all offer_price_dlar of cleared swing contracts
        obj_fun_sum_over_offer_prices = sum(self.swing_contract_offers[i].offer_price_dlar * self.keys_is_cleared[i] for i in range(self.number_of_swing_contract_offers))
        
        # sum over all (power_mw_in_step_k * price_per_mw_h_dlar (because one time step is one hour) of cleared swing contracts)) 
        # sum_over_power_costs = sum(self.swing_contract_offers[i].price_per_mw_h_dlar * self.keys_power_mw_in_step_k[i, k] for i in range(self.number_of_swing_contract_offers) for k in range(self.number_of_time_steps_k_in_market))
                                        # is he using this part of energy? (1 /0)    *   price for this part of energy (€ / mwh)                    * power increase of one discrete power step for this sc
        sum_over_power_costs = sum((self.keys_powerprice_steps_used_in_step_k[i, k, j] * self.swing_contract_offers[i].power_price_curve[j] * (self.swing_contract_offers[i].powermax_mw / self.number_of_powerprice_steps)) for i in range(self.number_of_swing_contract_offers) for k in range(self.number_of_time_steps_k_in_market) for j in range(self.number_of_powerprice_steps) )



        # Set the correct imbalance values for each timestep k
        sum_over_pos_imb_costs = sum(self.keys_power_imb_mw_pos[k] * self.power_imb_cost_dlar_per_mwh_pos for k in range(self.number_of_time_steps_k_in_market))
        sum_over_neg_imb_costs = sum(self.keys_power_imb_mw_neg[k] * self.power_imb_cost_dlar_per_mwh_neg for k in range(self.number_of_time_steps_k_in_market))

        # set objective function together
        obj_fun_complete = obj_fun_sum_over_offer_prices + sum_over_power_costs + sum_over_pos_imb_costs + sum_over_neg_imb_costs
        gurobi_model.setObjective(obj_fun_complete, GRB.MINIMIZE)



    def add_random_swing_contract_offers(self):
        # Create three sample swing contracts 
        # This is a list of SwingContractGenerator objects
        self.swing_contract_offers = []
        swing_contract_offer1 = SwingContractGenerator(offer_price_dlar=100, delivery_location="A", powermin_mw=0, powermax_mw=10, ramping_max_mw_up_per_k=10, ramping_max_mw_down_per_k=10, power_price_c=[80, 80.5, 81, 82, 83, 84, 85, 86, 87, 130])
        swing_contract_offer2 = SwingContractGenerator(offer_price_dlar=100, delivery_location="A", powermin_mw=0, powermax_mw=10, ramping_max_mw_up_per_k=10, ramping_max_mw_down_per_k=10, power_price_c=[80, 80.5, 81.5, 82, 83, 84, 85, 86, 87, 130])
        swing_contract_offer3 = SwingContractGenerator(offer_price_dlar=100, delivery_location="A", powermin_mw=0, powermax_mw=15, ramping_max_mw_up_per_k=10, ramping_max_mw_down_per_k=10, power_price_c=[100, 101, 102, 103, 104, 105, 106, 107, 108, 130])

        # add swing contracts to the list of swing contract offers
        self.swing_contract_offers.append(swing_contract_offer1)
        self.swing_contract_offers.append(swing_contract_offer2)
        self.swing_contract_offers.append(swing_contract_offer3)
        self.number_of_swing_contract_offers = len(self.swing_contract_offers)

    def add_random_swing_contract_purchaser(self):
        # Create three sample swing contracts for LoadServingEntities (want to buy electricity for their customers)
        # This is a list of SwingContractPurchaser objects
        self.swing_contract_purchaser = []

        swing_contract_purchaser1 = SwingContractPurchaser(load_profile_mw_in_every_step_k = 4, number_of_steps_k = self.number_of_time_steps_k_in_market, name="SW 1")
        swing_contract_purchaser2 = SwingContractPurchaser(load_profile_mw_in_every_step_k = 8, number_of_steps_k = self.number_of_time_steps_k_in_market, name = "SW 2")
        # swing_contract_purchaser3 = SwingContractPurchaser(load_profile_mw_in_every_step_k = 4, number_of_steps_k = self.number_of_time_steps_k_in_market, name = "SW 3")

        # swing_contract_purchaser3.set_load_profile_mw_for_each_k([3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])

        self.swing_contract_purchaser.append(swing_contract_purchaser1)
        self.swing_contract_purchaser.append(swing_contract_purchaser2)
        # self.swing_contract_purchaser.append(swing_contract_purchaser3)



