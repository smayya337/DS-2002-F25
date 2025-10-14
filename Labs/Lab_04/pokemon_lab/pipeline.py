import update_portfolio
import generate_summary
import sys

def run_production_pipeline():
    print("--- Starting Production Pipeline ---", file=sys.stderr)

    print("Step 1: Updating portfolio data...", file=sys.stderr)
    update_portfolio.main()

    print("Step 2: Generating summary report...", file=sys.stderr)
    generate_summary.main()

    print("--- Production Pipeline Complete ---", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()
