from get_me_data import fetcher

fetcher.init_db()

# IBM                                       DONE
# Intel (-84%)                      - INTC  DONE
# Lucent Technologies (-99%)        - LU    DONE
# Qualcomm (-86%)                   - QCOM  DONE
# Pets.com (Bankrupt)               - IPET

symbols = ["IPET"]

year = 2000
month = 3

months_to_fetch = 5


for symbol in symbols:
    for i in range(months_to_fetch):
        fetcher.fetch(symbol, year, month)
        month += 1

        if month > 12:
            month = 1
            year += 1
