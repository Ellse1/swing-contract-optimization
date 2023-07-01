class SwingContractPurchaser:

    # load profile in step k of M(T) (24 hours -> 24 steps k) = 4 MW
    # load_profile_mw_in_step_k = []

    def __init__(self, load_profile_mw_in_every_step_k, number_of_steps_k, name):
        self.load_profile_mw_in_step_k = []
        self.name = name

        for k in range(number_of_steps_k):
            # load profile in step k of M(T) (24 hours -> 24 steps k) = 4 MW 
            # this swing contract purchaser has a load profile of x (paramenter) MW in every step k of M(T)
            self.load_profile_mw_in_step_k.append(load_profile_mw_in_every_step_k)
