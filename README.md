                                        Web-based cryptocurrency trading system
                                       ------------------------------------------

Accessing Docker Image from Docker Hub:
---------------------------------------
  


The program functionalities:
----------------------------
This is a web-based trading system that take orders to buy or sell cryptocurrency based on user selection. Users can see the current bid or ask price of the selected currency, generate chart and graphics to see market status with 100 day trading history and get statistics for 24 hour trading data. User can see his/her own previous trading activities (blotter) and the trade status of specific currencies, inventory/position, profit or loss by selecting appropriate tools.

The scope, limitations and assumptions:
----------------------------------------
The project is limited to the USDT market in the BITTREX exchange for currency and price information. The historical data is collected from cryptocompare.com through their API. crytocompare.com was selected since it collects information from several exchanges and was assumed to provide a better insight of a currency's trading information and market status.

USDT was selected as the base price. The difference between USDT and true USD was ignored and no conversion was made. In this project USDT was assumed to be exactly equal to USD and all the values were treated that way. 

The application uses mongoDB to store and retrieve all trading information. This mongoDB is hosted in the cloud (mongoDB Atlas ).
NOTE:  for this project no effort was made to hide the connection string
  
Initial screen:
---------------
At the start of the program the user is greeted with a welcome screen with some project information. it displays buttons with link to specific functionalities of the system. These buttons are common in all the pages that help users to navigate to any specfic page or functionality from any other page. Clicking the “Trade” button takes a user to the trading page (trade.html), similarly “View Blotter” and “View P/L” takes a user to the ‘blotter’ or ‘pl’ page to see the BLOTTER or P/L screen. Two other buttons - "Reset Account" and "Return to Main" are also available. The "Reset Account" button resets the available cash to $1000,000 and deletes all the trading history. The "Return to Main" takes users back to the main initial page. Followig image shows part of the initial view:

![image](https://user-images.githubusercontent.com/25092754/38469833-066039da-3b29-11e8-9494-22b7f97f97aa.png)

How to:
-------
    1. Trade:
    ----------
User lands on the trade page once the  “Trade” button is clicked. It provides the user with am interface to select a currency, a trading option and a button to see the current market price:

![image](https://user-images.githubusercontent.com/25092754/38469886-aa36c56a-3b29-11e8-8e49-19115dcd1f30.png)

Once the "View Market Status" is clicked with appropriate inputs the program provides current price information and a graphical view of 100 day history and the trade statistics of 24 hour period:

![image](https://user-images.githubusercontent.com/25092754/38469938-65a416f4-3b2a-11e8-800f-96fda41724d2.png)

Once the user decides to execute the trade, he and she can enter the quantity and click the ‘Execute Trade’ button to complete the trade.  Appropriate messages are shown if the trade is successful or if an error is occurred.

    NOTE: a. Once the first characters are typed into the symbol input it does an auto-search to 
             list appropriate currencies.
          b. User need scroll the page to see all the graphics depending on the size of their window.
 --  
    
    2. View Blotter:
    -------------------
User clicks on “View Blotter” button to go to the blotter page. The screen display the trading history or blotter of the transactions:

![image](https://user-images.githubusercontent.com/25092754/38469997-01f390a2-3b2b-11e8-949e-a014a70a6972.png)

     
    3. View P/L:
    --------------
User clicks “View P/L” button to go to the P/L page. The programs display the profit/loss (P/L) of the currencies that were traded: 
        Note: If a trading attempt is made (by clicking on Execute trade) and the trading fails for any reason, 
        the P/L view will still include the symbol to capture the user's interest on that currency and will act as
        a reminder for the user to trade the currency in the future.  
        
![image](https://user-images.githubusercontent.com/25092754/38470015-39ed5902-3b2b-11e8-9890-1edc73aba7b4.png)


The Functions:
---------------
Following are a description of the functions used in the system:

    1.@app.route("/")
      show_main_page():
Shows the main page
  
    2.@app.route("/reset")
      reset_account()
calls reset_account() function, which connects to mongoDB and deletes all the trading history and profit/loss information and finally sets the initial cash account to its original value of $1000,000 and takes the user to the initial screen.

    
    3.@app.route("/trade")
      show_trade_screen()
Route to url of trade.html, which contains the main functionalities of the site.

    4.@app.route("/submitTrade",methods=['POST'])
      execute_trade2():
execute_trade2 function is triggered to show the price, market status and statistics or execute the trade from inside the trade.html.  Other functions are called such as get_Markets() to get the market and currency information, find_price_crypto() to get the price information, plotdata() to create the chart and graphics, get_twentyfourhr_stat() to get 24 hours statistics of the selected currency. At the end, the output of all these functions are sent as variables to be rendered in the html

     5.@app.route("/blotter")
       show_blotter():
show_blotter() function is called when routed to the url for blotter page. This function calls get_BlotterData() to get trading information in a dataframe which is passed as a variable to be rendered in the html page as a table.

    6.@app.route("/pl")
      execute_pl():
execute_pl() function is called when routed to the url for PL page. This function calls updateUpl()  to get PL information in a dataframe which is passed as a variable to be rendered in the html page as a table.


    7.	do_transaction(side,qty,price,ticker):
The function takes four parameters: the type of trade, the quantity, trading price and the symbol information. This function does all the actions relevant to trading i.e. updates inventory and cash values, updates RPL if the trading option is a sell, retrieve and store all data into  mongoDB and finally returns all the transaction information as a DICT object. It calls get_statusDF() function that returns a dataframe with the current trading status of a currency. Information are checked and updated based on the current status

    8.	updateWap(oldwap,oldqty,price,newqty,stock):
The function takes five parameters: previous wap, previous quantity, trading price, current quantity and the trading currency. It does an arithmetic operation to calculate the WAP after the current buy of the selected currency and update the WAP information in the database.

    9.	updateUpl():
The function calls get_statusDF() and find_price_crypto() function to get the most recent trading price, current WAP and inventory information, estimate UPL values of the currencies and update UPL column of statusDF dataframe with updated UPL values. Since this information is dynamic and recalculated every time the function is called, this function does not store any value in the database. It returns all these information in dataframe to be viewed in the P/L screen.

    10.	find_price_crypto(name,opt): 
The function takes two parameters: the ticker and the trading option. The function uses Bitterex API to retrieve cryptocurrency price based on the trading option (ask for buy and bid for sell) from the BITTEREX exchange. This function collects data only from currencies in USDT market. If for any reason the price information is not available it show a message asking to try trading later. After retrieving the price information it converts the price into float. It finally returns the price value (price = 0 if no valid price is found) along with a message string as a dict object.

    11.	get_Markets():
The function finds the market information and returns only the USDT market in a dataframe. It uses API provided by BITTEREX

    12.	get_marketHistory(name):
The function uses cryptocompare.com is used to get the historical information of a given currency through API provided by cryptocompare.com the crytocompare.com was selected since it collects information from several exchanges and provides better insights of a currency's trading information and market status. The function returns 100 day historical data.

    13.	get_twentyfourhr_stat(ticker):
The function collects 24 hours trading information of a given currency through API provided by cryptocompare.com. The function returns statistical information of the data in a dataframe.

    14.	moving_average(data, days):
The function takes two parameters- a pandas Series with 100 day price information and a number (for number of days) and uses numpy's convolve method to create moving average price for the given number of days.

    15.	plotdata(currency):
The function takes the selected currency as its parameter and calls get_marketHistory() function to get the 100 day market history. It also calls moving_average() function for moving average data and uses matplotlib library to plot all those data. The resulting plot is saved in .png format and returned as Base64 encoded string.

    16.	write_Blotter_ToMongo(blotterData):
The function connects to mongoDB in the cloud and save information of each transaction.

    17.	get_BlotterData():
The function connects to mongoDB in the cloud, retrieve transaction data and return them as a dataframe.

    18.	get_currentBalance():
The function connects to mongoDB in the cloud, retrieve the available fund data and return the fund/cash information.

    19.	write_StatusDF(name, selloption):
The function takes the currency name and trading option (sell or buy) as its parameter, connects to mongoDB in the cloud and creates a record if the currency is being traded for the first time.

    20.	get_statusDF():
The function connects to mongoDB in the cloud, retrieve trading information for each individual currency and return information as a dataframe.

    21.	execute_BuySell(tradeoption,name,qty):
The execute_BuySell function takes three parameters - the symbol of a currency and trade option i.e. buy or sell and the quantity. The function calls other functions (find_price_crypto and do_transaction) to retrieve the latest price information and to complete the requested transaction. It looks at the previous position/inventory, and WAP information and update WAP if the trading option is a buy. Finally the function saves transaction info in the database and returns a message with success or error information.

    22 db_reset():
The function connects to mongoDB and deletes all the trading history and profit/loss information and finally sets the initial cash account to its original value of $1000,000 and takes the user to the initial screen.   

