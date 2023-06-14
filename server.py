import socket
import random


class Server:
  def __init__(self):
    pass

  def run(self):

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("localhost",9999))

    server.listen()
    
    while True:
      print("running")
      client,add = server.accept()
      print("Connected to :",add)
      data = client.recv(1024)
      
      newData = []
      with open(".\\dataset\\TextData.txt","r") as file:
        fdata = file.read()
        fdata = fdata.split(" ")
        for word in fdata:
          if "\n" in word:
            fdata.pop()
        for word in fdata:
            if word not in newData and word not in data.decode():
                newData.append(word)
        
      data = random.choices(newData,k=10)

      client.send(",".join(data).encode())
      
      client.close()



if __name__  == "__main__":
  
  s = Server()
  s.run()