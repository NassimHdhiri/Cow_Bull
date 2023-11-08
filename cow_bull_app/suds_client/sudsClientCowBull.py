from suds.client import Client 

#Create new instance of client 
soap_client =Client("http://127.0.0.1:8000/cb_game/?wsdl")

#call first service 
print(soap_client.service.AboutGame())