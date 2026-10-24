from get_me_data import fetcher

fetcher.init_db()

# IBM                                       DONE
# Intel (-84%)                      - INTC  DONE
# Lucent Technologies (-99%)        - LU    DONE
# Qualcomm (-86%)                   - QCOM  DONE
# Pets.com (Bankrupt)               - IPET

symbols = ["IPET"]

for symbol in symbols:
    fetcher.fetch(symbol, 2000, 3)
    fetcher.fetch(symbol, 2000, 4)
    fetcher.fetch(symbol, 2000, 5)
    fetcher.fetch(symbol, 2000, 6)
    fetcher.fetch(symbol, 2000, 7)
