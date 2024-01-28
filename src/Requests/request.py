import requests

class Request:
    def __init__(self):
        self.session = requests.Session()
        # We put this url to listen our requests
        self.url = "https://eoqleo2r6vceqqa.m.pipedream.net?"
        
    # Each method is a implementation of a HTTP method
    def get(self, path):
        print("get :"+self.url + path)
        return self.session.get(self.url + path)
    
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
    