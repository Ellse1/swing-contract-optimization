class SwingContractGenerator:

# OFFER PRICE
    # the price for clearing this contract
    # offer_price_dlar = 0


    # COLLECTION OF POSSIBLE EXERCISE TIMES 
    # negligible becaus this is a swing contract in firm form (only one exercise time that coincides with the close of the market M(T) )


    # SET OF POSSIBLE POWER PATHS
    # deliery location of the contract (From A to Z)
    # delivery_location = ""

    # start time of the contract 
    # neglibible because only one market is taken into account M(T) 

    # minium down / up time 
    # neglibible because there are no constraints taken into account referring to the minimum up / down time of the generator

    # minimum power, a generator can generate, maximum power, a generator can generate
    # powermin_mw = 0
    # powermax_mw = 0

    # ramping condition: maximum change in power between two time steps
    # ramping_max_mw_up_per_k = 0
    # ramping_max_mw_down_per_k = 0

    # duration limits
    # neglibible because there are no constraints taken into account referring to the duration of the duration limits 


    # PERFORMANCE PAYMENT METHOD
    # cost function of the generator: Linear cost function. 
    # The cost function is a function which gives the price for generating a certain amount of power between the minimum and maximum power.
    # costfunction should be a linear cost function for the power delivered;
    # price_per_mw_h_dlar = 0

    # cost function: number of discretization steps
    # costfunction_discretization_steps = 10
    # neglibible because the cost fucntion is linear and therefore no discretization is needed


    
    
    # variables that are normaly not needed for generator / swing_contract but are needed for the optimization
    # is this contract cleared from the market?
    #is_cleared = False

    # the power in step k of M(T) (24 hours -> 24 steps k)
    # power_mw_in_step_k = []
            
            
            
            
            
            



    def __init__(self, offer_price_dlar, delivery_location, powermin_mw, powermax_mw, ramping_max_mw_up_per_k, ramping_max_mw_down_per_k, price_per_mw_h_dlar):
        
        #declare variables here, because then they are instance variables and not class variables
        self.is_cleared = False
        self.power_mw_in_step_k = []
            
        self.offer_price_dlar = offer_price_dlar
        self.delivery_location = delivery_location
        self.powermin_mw = powermin_mw
        self.powermax_mw = powermax_mw
        self.ramping_max_mw_up_per_k = ramping_max_mw_up_per_k
        self.ramping_max_mw_down_per_k = ramping_max_mw_down_per_k
        self.price_per_mw_h_dlar = price_per_mw_h_dlar
