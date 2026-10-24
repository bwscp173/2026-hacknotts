from get_me_data import fetcher

fetcher.init_db()

# IBM                                       DONE
# Intel (-84%)                      - INTC  DONE
# Lucent Technologies (-99%)        - LU    DONE
# Qualcomm (-86%)                   - QCOM  DONE
# Pets.com (Bankrupt)               - IPET

#symbols = ['IBM', 'INTC', 'LU', 'QCOM', 'AMZN'] # ['IBM', 'INTC', 'LU', 'QCOM', 'AMZN', 'AAPL', 'NVDA', 'AMD', 'GOOGL']
symbols = ['AAPL', 'NVDA', 'AMD', 'GOOGL']

start_year = 2001
start_month = 6

months_to_fetch = 5


for symbol in symbols:
    year = start_year
    month = start_month

    for i in range(months_to_fetch):
        fetcher.fetch(symbol, year, month)
        month += 1

        if month > 12:
            month = 1
            year += 1
