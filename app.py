
from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.contract import ContractDetails
from ibapi.utils import Decimal
from ibapi.wrapper import EWrapper
from threading import Thread
import time
from lightweight_charts import Chart
from ibapi.client import Contract, Order
from ibapi.tag_value import TagValue
import random


# this is a new class for the connection for IB idk how it works


class NewConnectionClient(EWrapper,EClient):
    
    def __init__(self,host,port, client_id):
        print(f"I'm client{client_id}")
        EClient.__init__(self,self)
        
        self.connect(host,port,client_id)
        thread = Thread(target = self.run)
        thread.start()
        
        
        
    def returnmessages(self, req_id,code,msg,misc): 
        if code in [2104,2106,2158]:
            print(msg)
        else:
            print("Error {}: {}".format(code,msg))
    def historicalData(self, reqId: int, bar: BarData):
        print(bar)
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print (f"end of data{start}{end}")
    def reqScannerParameters(self):
        return super().reqScannerParameters()
    
    def reqPositions(self):
        return super().reqPositions()
    
    def scannerParameters(self,xml):
        dir = "/Users/bryanlin/Stock_Manager/ScannerParameters.xml"
        open(dir,"w").write(xml)
        print("Params received")
    def scannerData(self, reqId: int, rank: int, contractDetails: ContractDetails, distance: str, benchmark: str, projection: str, legsStr: str):
        print(f"reqId:{reqId}, rank: {rank}, contractDetails: {contractDetails}, distance: {distance}, benchmark: {benchmark}, projection: {projection}, legsStr: {legsStr}")
    def scannerDataEnd(self, reqId: int):
        print('Scanner data ended')
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)       
        self.order_id = orderId
        print(f"next valid id is {self.order_id}")
    def position(self, account: str, contract: Contract, position: Decimal, avgCost: float):
        super().position(account, contract, position, avgCost)  
        print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:",
        contract.secType, "Currency:", contract.currency,
        "Position:", position, "Avg cost:", avgCost)
 
    def reqMatchingSymbols(self, reqId: int, pattern: str):
        return super().reqMatchingSymbols(reqId, pattern)
        
        
    def symbolSamples(self, reqId: int, contractDescriptions: list):
        
        
        try: 
            contractDescription = contractDescriptions[0]
            derivetype = ""
            for sectype in contractDescription.derivativeSecTypes:
                derivetype += " "
                derivetype += sectype
            my_dict = {"name":contractDescription.contract.description,
                "symbol":contractDescription.contract.symbol,
                    "secType":contractDescription.contract.secType,
                    "exchange":contractDescription.contract.primaryExchange,
                    "currency":contractDescription.contract.currency}
            dir = "/Users/bryanlin/Stock_Manager/Contracts.txt"
            f = open(dir,"w")
            f.write(str(my_dict))
            f.write('\n')
            f.close()
            print(f'scan finished for {contractDescription.contract.description}')
            
            
            return super().symbolSamples(reqId, contractDescriptions)
            
            
            
            
        except:
            if len(contractDescriptions) == 0:
                print("No results")
            else:
                print("ERROR IDK WHATS GOING ON")
        
    def orderStatus(self, order_id, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"order status {order_id} {status} {filled} {remaining} {avgFillPrice}")  
    def disconnect(self):
        print(f"{self} Disconnected")
        return super().disconnect() 
    def reqAccountSummary(self, reqId: int, groupName: str, tags: str):
        return super().reqAccountSummary(reqId, groupName, tags) 
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                        currency: str):
         super().accountSummary(reqId, account, tag, value, currency)
         print("AccountSummary. ReqId:", reqId, "Account:", account,
               "Tag: ", tag, "Value:", value, "Currency:", currency)
    
def create_Contract(client, company):
    contract = Contract()
    client.reqMatchingSymbols(random.randint(1,20),company)
    dir = "/Users/bryanlin/Stock_Manager/Contracts.txt"
    time.sleep(0.5)
    f = open(dir,"r")
    info = eval(f.readline())
    contract.symbol = info['symbol']
    contract.exchange = info['exchange']
    contract.secType = info['secType']
    contract.currency = info['currency']
    return contract

def Buy_stock_LMT(company,amount):
    #get contract
    contract = create_Contract(client1, company)

    
    order = Order()
    order.totalQuantity = amount
    order.orderType = "MKT"

    
    #get next order id
    client1.reqIds(-1)

    order.action = "BUY"
    if client1.order_id:
        print("We in the clear to buy")
        client1.placeOrder(client1.order_id,contract,order)
def Sell_stock_LMT(company,amount):
    contract = create_Contract(client1,company)
    
    order = Order()
    order.totalQuantity = amount
    order.orderType = "MKT"

   
    #get next order id
    client1.reqIds(-1)

    order.action = "SELL"
    if client1.order_id:
        print("We in the clear to sell")
        client1.placeOrder(client1.order_id,contract,order)






# called when we want to render scan results

if __name__ == '__main__':
    client1 = NewConnectionClient("127.0.0.1",7497,1) 
    time.sleep(1)
    
    client1.reqAccountSummary(909,'All',"$LEDGER")
    time.sleep(2)
    Buy_stock_LMT('NVDIA',5)
    Sell_stock_LMT('Lockheed',2)
    
    time.sleep(3)
    client1.disconnect()
