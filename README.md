# PyBittrex
Some functional scripts to get data from Bittrex.

Note: If you store the market history in a database remember to program a routine in your db to eliminate periodically duplicated records.

# Summary of functions

Market History: Get the historical market of any currency in bittrex.

Volume: Get the quantity of coins sold "SELL" and bought "BUY" from the last 100 orders of the market history.

Price: Get the movement of the price of a coin and shows it graphically.

Filtrar_market_precio: Filter the operations performed for a specific price.

Orderbook: Get the order book of any currency in bittrex.

Order: shows all orders in the order book filtered by price, highlighting orders with a big quantity.

Spread: calculates the spread of the order book among the first 10 orders of each book

Buscar_ordenes: Shows orders of the order book filtered for a specific price.


# This project was carried out in 2018, so now I know more efficient ways to do it
