import requests
import json

class Request:
    def __init__(self):
        self.session = requests.Session()
        # We put this url to listen our requests
        self.url = "http://localhost:8080/"
        
    # Each method is a implementation of a HTTP method
    def get(self, path):
        self.data=json.loads(self.session.get(self.url + path).text)
        return(self.data)
    
    def post(self, path, data):
        #print("post :"+self.url + path)
        data=json.loads(self.session.post(self.url + path, data=data).text)
        return data
    
    def put(self, path, data):
        try:
            response=self.session.put(self.url + str(path), data=data)
            '''if response.status_code == 200:
                print("PUT request success")
            else:
                print("PUT request failed")'''
        except Exception as e:
            print(f"Error : {e}")
    
    def delete(self, path):
        #print("delete :"+self.url + path)
        return self.session.delete(self.url + path)
    
    def close(self):
        print("close")
        self.session.close()
    