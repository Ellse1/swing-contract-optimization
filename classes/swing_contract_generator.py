class SwingContractGenerator:
    
    # the price for clearing this contract
    offer_price_dollar = 0

    # minimum power, a generator can generate
    powermin_mw = 0

    # maximum power, a generator can generate
    powermax_mw = 0

    # ramping condition: maximum change in power between two time steps
    ramping_max_mw_up_per_k = 0
    ramping_max_mw_down_per_k = 0

    # cost function of the generator: Linear cost function. 
    # The cost function is a function which gives the price for generating a certain amount of power between the minimum and maximum power.
    # costfunction = 0;

    # cost function: number of discretization steps
    costfunction_discretization_steps = 10


    
    
    # variables that are normaly not needed for generator but are needed for the optimization
    
    # is this contract cleared from the market?
    is_cleared = False
