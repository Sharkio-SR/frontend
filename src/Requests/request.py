import requests
import json

class Request:
    def __init__(self):
        self.session = requests.Session()
        # We put this url to listen our requests
        self.url = "http://sharkio.istic.univ-rennes1.fr:8080/"
        
    # Each method is a implementation of a HTTP method
    def get(self, path):
        #print("get :"+self.url + path)
        self.data=json.loads(self.session.get(self.url + path).text)
        return(self.data)
    
    def post(self, path, data):
        print("post :"+self.url + path)
        return self.session.post(self.url + path, data=data)
    
    def put(self, path, data):
        print("put :"+self.url + str(path))
        return self.session.put(self.url + str(path), data=data)
    
    def delete(self, path):
        print("delete :"+self.url + path)
        return self.session.delete(self.url + path)
    
    def close(self):
        print("close")
        self.session.close()
    