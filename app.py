import gurobipy as gp
from gurobipy import GRB

def main():
    # This example formulates and solves a simple MIP model:
    try:
        # Create a new model
        m = gp.Model("mip1")

        # Create variables
        x = m.addVar(vtype=GRB.BINARY, name="x")
        y = m.addVar(vtype=GRB.BINARY, name="y")
        z = m.addVar(vtype=GRB.BINARY, name="z")

        # Set objective
        m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

        # Add constraint: x + 2 y + 3 z <= 4
        m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

        # Add constraint: x + y >= 1
        m.addConstr(x + y >= 1, "c1")

        # Optimize model
        m.optimize()

        for v in m.getVars():
            print('%s %g' % (v.VarName, v.X))

        print('Obj: %g' % m.ObjVal)

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')


    # END
    print("I am a Python app!")
    



# Start the main app
if __name__ == "__main__":
    main()
