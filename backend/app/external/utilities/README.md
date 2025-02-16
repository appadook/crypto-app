# Thesis Table generation

## Arbitrage seeker in different case scenarios

### 1. Same currency, same crypto, all exchanges
- exchange_spread.py -> This class is used to track the highest and lowest prices of all our cryptocurrencies across different exchanges.
returns a dictionary of the highest and lowest prices for each crypto and fiat pair, or displaying
the spread between the highest and lowest prices.
- The table generated will have the following columns:
    - Crypto/fiat
    - Timestamp
    - [A column for each exchange price for that cryto/fiat pair]
    - strategy
    - arbitrage


### 2. Different fiat currency, same crypto, same exchange
- exchange_arbitrage.py -> this module is used to calculate the arbitrage within a singular exchange and their different fiat currencies, providing us
with the best arbitrage opportunity within a single exchnage and given exchage rates and fiat prices for a cryptocurrency.
- The table generated will have the following columns:
    - Crypto/exchange pair
    - Timestamp
    - [A column for each crypto/exchange prices in fiat currency]
    - strategy
    - arbitrage


### 3. Different fiat, same crypto, different platforms
- cross_exchange_fiat_arbitrage -> This module contains functions to find the lowest and highest price of a cryptocurrency across all different exchanges and fiat currencies.
The output indicates the user where the lowest nominal price is and where the highest nominal price is, so
that the user can take advantage of arbitrage opportunities by buying in one exchange in one fiat currency and selling
on another exchange in another fiat currency.
- The table generated will have the following columns:
    - crypto
    - Timestamp	
    - [A column for each exchange/fiat pairing]	 
    - strategy	
    - Arbitrage 
Note: Both the strategy and arbitrage column include the fees


### *UI data for front-end



## fee_calc.py
- This module calculates the fees for buying and selling cryptocurrencies on different exchanges.
Fees included are trading fees, spread fees, payment fees, network fees, blockchain fees, and withdrawal fees.
It allows us to calculate the total fees for a given transaction along with the price arbitrage between the biggest spread.

