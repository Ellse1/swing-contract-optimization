import sys
sys.path.insert(0,"..")
from classes.rto_iso_market_optimizer import MarketOptimizer

def main():
    
    market_optimizer = MarketOptimizer()
    market_optimizer.optimize()

    # END
    print("I am a Python app and finished with optimization!")
    



# Start the main app
if __name__ == "__main__":
    main()
