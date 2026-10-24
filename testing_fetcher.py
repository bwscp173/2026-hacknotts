from get_me_data import fetcher

fetcher.init_db()

# IBM                                       DONE
# Intel (-84%)                      - INTC  DONE
# Lucent Technologies (-99%)        - LU    DONE
# Qualcomm (-86%)                   - QCOM  DONE
# Pets.com (Bankrupt)               - IPET

symbols = ['IBM', 'INTC', 'LU', 'QCOM', 'AMZN', 'AAPL', 'NVDA', 'AMD', 'GOOGL']

start_year = 2005
start_month = 6

months_to_fetch = 5


for symbol in symbols:
    fetcher.fetch('AAPL')

    break

