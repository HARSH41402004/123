import pandas as pd
from openbb import obb
from typing import Optional

# --- Important Setup Note ---
# This script relies on the OpenBB SDK, which needs to be installed first.
# Installation: pip install openbb
# The OpenBB SDK handles the heavy lifting of finding and cleaning data from public sources.

def get_upcoming_ipos(limit: int = 10) -> pd.DataFrame:
    """
    Fetches a list of upcoming Initial Public Offerings (IPOs) from a free data provider
    via the OpenBB SDK.

    Args:
        limit: The maximum number of upcoming IPOs to retrieve.
    
    Returns:
        A pandas DataFrame containing IPO information, or an empty DataFrame on error.
    """
    print(f"--- Fetching the next {limit} Upcoming IPOs... ---")
    try:
        # obb.equity.calendar.upcoming_ipo is the command for Future IPOs (FIPO)
        ipo_data = obb.equity.calendar.upcoming_ipo(limit=limit)
        
        # Convert the result object into a pandas DataFrame for easy display
        df = ipo_data.to_dataframe()
        
        if df.empty:
            print("No upcoming IPOs found for the specified limit.")
            return df
            
        # Select and rename columns for clarity
        df = df[['name', 'expected_date', 'expected_shares_offered', 'price_low', 'price_high', 'exchange']]
        df.columns = ['Company Name', 'Expected Date', 'Shares Offered (M)', 'Price Low ($)', 'Price High ($)', 'Exchange']
        
        # Sort by expected date
        return df.sort_values(by='Expected Date').reset_index(drop=True)

    except Exception as e:
        print(f"ERROR: Could not fetch upcoming IPO data.")
        print(f"Please ensure the 'openbb' library is installed and initialized correctly. Details: {e}")
        return pd.DataFrame()

def get_past_ipos(limit: int = 10) -> pd.DataFrame:
    """
    Fetches a list of recent past Initial Public Offerings (IPOs) from a free data provider
    via the OpenBB SDK.

    Args:
        limit: The maximum number of past IPOs to retrieve.
    
    Returns:
        A pandas DataFrame containing IPO information, or an empty DataFrame on error.
    """
    print(f"\n--- Fetching the last {limit} Recent Past IPOs... ---")
    try:
        # obb.equity.calendar.historical_ipo is the command for Past IPOs (PIPO)
        ipo_data = obb.equity.calendar.historical_ipo(limit=limit)
        df = ipo_data.to_dataframe()
        
        if df.empty:
            print("No recent past IPOs found for the specified limit.")
            return df

        # Select and rename columns for clarity.
        df = df[['name', 'date', 'price', 'exchange']]
        df.columns = ['Company Name', 'IPO Date', 'IPO Price ($)', 'Exchange']
        
        # Sort by most recent IPO date
        return df.sort_values(by='IPO Date', ascending=False).reset_index(drop=True)
        
    except Exception as e:
        print(f"ERROR: Could not fetch past IPO data.")
        print(f"Please ensure the 'openbb' library is installed and initialized correctly. Details: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Initialize the OpenBB SDK (optional, but good practice)
    try:
        obb.system.log_system_info() # Logs system info, helps with debugging
    except Exception:
        # Ignore if initialization fails, the functions will catch missing lib later
        pass 
        
    # 1. Fetch Upcoming IPOs
    upcoming_df = get_upcoming_ipos(limit=10)
    
    # Display the upcoming IPO data
    if not upcoming_df.empty:
        print("\n" + "="*70)
        print("Upcoming IPOs:")
        print(upcoming_df.to_markdown(index=True))
        print("="*70)
    
    # 2. Fetch Past IPOs
    past_df = get_past_ipos(limit=10)
    
    # Display the past IPO data
    if not past_df.empty:
        print("\n" + "="*70)
        print("Recent Past IPOs:")
        print(past_df.to_markdown(index=True))
        print("="*70)

    print("\nScript Finished.")
