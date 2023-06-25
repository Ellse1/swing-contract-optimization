class Generator:

    
    # minimum power, a generator can generate
    powermin = 0

    # maximum power, a generator can generate
    powermax = 0

    # cost function of the generator. 
    # The cost function is a function which gives the price for generating a certain amount of power between the minimum and maximum power.
    # costfunction = 0;

    # cost function: number of discretization steps
    costfunction_discretization_steps = 10






    def __init__(self, costfunction_discretization_steps):
        self.costfunction_discretization_steps = costfunction_discretization_steps

        
