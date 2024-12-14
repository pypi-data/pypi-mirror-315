import ctypes
from ctypes import c_char_p, c_int, c_uint8, c_uint16, c_uint32, POINTER
import os
import pickle
from threading import Lock
import time



current_folder = os.path.dirname(os.path.abspath(__file__))

class CONVERTER:
    def __init__(self) -> None:
        with open(os.path.join(current_folder,"datafile.pkl"), "rb") as file:  # rb: read binary
            self.datafile = pickle.load(file)

    def getId(self,itemName):
        return self.datafile["itemToId"].get(itemName,None)
    
    def getName(self,id):
        return self.datafile["idToItem"].get(id,None)

class DB:
    sell = 0
    buyOrder = 1

class SITE:
    youpin = 0
    buff163 = 1

class FAST_PRICE():
    def __init__(self,host="103.74.106.225",port=26251,api_key="") -> None:
        self.lock = Lock()
        self.host = host
        self.client_socket = None
        self.port = port
        self.api_key = api_key
        self.client = ctypes.CDLL(os.path.join(current_folder,'client.dll'))
        self.client.client_connect_and_auth.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
        self.client.client_connect_and_auth.restype = c_int

        self.client.get_data.argtypes = [c_uint8, c_uint16, c_uint8, POINTER(c_uint32)]
        self.client.get_data.restype = c_int

        self.client.close.argtypes = []
        self.client.close.restype = None
        # self.response_value = ctypes.c_uint32()
        self.conveter = CONVERTER()
        self.__connect()

    def __connect(self):
        auth_response = ctypes.create_string_buffer(256)  # Tạo buffer để nhận phản hồi xác thực
        result = self.client.client_connect_and_auth(self.host.encode('utf-8'), self.port, self.api_key.encode('utf-8'), auth_response, len(auth_response))

        if result == 0:
            print("Connected and authenticated successfully.")
            print("Auth Response:", auth_response.value.decode('utf-8'))
        else:
            raise "Failed to connect or authenticate."
            # print("Failed to connect or authenticate.")
        return result

    
    def __getByIndex(self,site:SITE,itemId:int,index:int):
        with self.lock: 
            response_value = c_uint32(0)  # Giá trị mặc định là 0
            result = self.client.get_data(site, itemId, index, ctypes.byref(response_value))

            if result == 0:
                print(f"Data retrieved successfully: {response_value.value}")
            else:
                print("Failed to retrieve data.")

            return response_value.value
        
    def get(self,site:SITE,itemId:int,index:DB=0):

        return self.__getByIndex(site,itemId,index)

    def getMoreBuyOrder(self,site:SITE,itemId:int):
        result = []
        for i in range(0, 18, 2):
            result.append({
                "price": self.__getByIndex(site,itemId,i+1),
                "itemLeft" : self.__getByIndex(site,itemId,i+2)
            })
        return result
    def liquidity(self,site:SITE,itemId:int):
         return self.__getByIndex(site,itemId,21)
    def __del__(self):
        if self.client_socket:
            self.client_socket.close()