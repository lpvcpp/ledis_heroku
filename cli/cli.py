import cmd
import requests
import json
import urllib.request


class HelloWorld(cmd.Cmd):

    def sendPostRequest(self, url, body):
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        response = urllib.request.urlopen(req, jsondataasbytes) 
        return response
        
    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print

################   STRING ######################
    def do_SET(self, text):
        """SET key value """
        words = text.split()
        if len(words) == 2:
            body = {"key":words[0], "value":words[1]}  
            url = "http://localhost:5000/SET"
            response = self.sendPostRequest(url, body)
            print (response.read())

          #  r = requests.post("http://localhost:5000/SET", data={words[0]: words[1]})
          #  print(r.text)
        else :
            print ("wrong parameter")


    def do_GET(self, text):
        """GET key"""
        words = text.split()
        if len(words) > 1:
            print ("wrong parameter")
        else:
            body = {"key":words[0]}
            url = "http://localhost:5000/GET"
            response = self.sendPostRequest(url, body)
            print(response.read())

################   LIST ######################
    def do_LLEN(self, text):
        """GET LENGTH OF LIST"""
        words = text.split()
        if len(words) == 1 :
            body = {"key":words[0]}
            url = "http://localhost:5000/LLEN"
            response = self.sendPostRequest(url, body)
            print(response.read())

        else :
            print ("Wrong parameter")

    def do_RPUSH(self, text):
        """PUSH TO LIST"""
        words = text.split()
        if len(words) < 2:            
            print ("Wrong parameter")
        else :
            list_value = ' '.join(words[1:])
            body = {"key":words[0], "value" :list_value}
            url = "http://localhost:5000/RPUSH"
            response = self.sendPostRequest(url, body)
            print(response.read())

    def do_LPOP(self, text):
        """POP LIST """
        words = text.split()
        if len(words) == 1:
            body = {"key":words[0]}
            url = "http://localhost:5000/LPOP"
            response = self.sendPostRequest(url, body)
            print(response.read())
        else:
            print ("Wrong parameter")

    def do_RPOP(self, text):
        """RPOP LIST """
        words = text.split()
        if len(words) == 1:
            body = {"key":words[0]}
            url = "http://localhost:5000/RPOP"
            response = self.sendPostRequest(url, body)
            print(response.read())
        else:
            print ("Wrong parameter")

    def do_LRANGE(self, text):
        """PRINT A RANGE OF LIST"""
        words = text.split()
        if len(words) == 3:
            body = {"key": words[0], "value": ' '.join(words[1:])}
            url = "http://localhost:5000/LRANGE"
            response = self.sendPostRequest(url, body)
            print(response.read())

        else:
            print ("Wrong parameter")

################   SET ######################

    def do_SADD(self, text):
        """ADD A SET"""
        words = text.split()
        if len(words) < 2:
            print ("Wrong parameter")
        else:
            body = {"key": words[0], "value": ' '.join(words[1:])}
            url = "http://localhost:5000/SADD"
            response = self.sendPostRequest(url, body)
            print(response.read())

    def do_SCARD(self, text):
        """COUNT TOTAL NUMBER OF SET"""
        words = text.split()
        if len(words) > 1:
            print ("Wrong parameter")
        else:
            body = {"key": words[0]}
            url = "http://localhost:5000/SCARD"
            response = self.sendPostRequest(url, body)
            print(response.read())

    def do_SMEMBERS(self, text):
        """PRINT MEMBER OF SET"""
        words = text.split()
        if len(words) > 1:
            print ("Wrong parameter")
        else:
            body = {"key": words[0]}
            url = "http://localhost:5000/SMEMBERS"
            response = self.sendPostRequest(url, body)
            print(response.read())

    def do_SREM(self, text):
        """REMOVE VALUE IN SET """
        words = text.split()
        if len(words) < 2:
            print ("Wrong parameter")
        else:
            body = {"key": words[0], "value": ' '.join(words[1:]) }
            url = "http://localhost:5000/SREM"
            response = self.sendPostRequest(url, body)
            print(response.read())

    def do_SINTER(self, text):
        """INTER OF SET"""
        words = text.split()
        if len(words) < 2:
            print ("Wrong parameter")
        else:
            body = {"listKey": ' '.join(words)}
            url = "http://localhost:5000/SINTER"
            response = self.sendPostRequest(url, body)
            print(response.read())

################ EXPIRATION ##################

    def do_KEYS(self, text):
        """ LIST ALL KEY"""
        r = requests.post("http://localhost:5000/KEYS")
        print(r.text)

    def do_DEL(self, text):
        """ DEL A KEY"""
        words = text.split()
        if len(words) != 1:
            print ("Wrong parameter")
        else:
            body = {"key": words[0]}
            url = "http://localhost:5000/DEL"
            response = self.sendPostRequest(url, body)
            print(response.read())

    def do_FLUSHDB(self, text):
        """ 'DELETE ALL KEY"""
        r = requests.post("http://localhost:5000/FLUSHDB")
        print(r.text)

    def do_EXPIRE(self, text):
        """ SET TIMEOUT FOR KEY"""
        words = text.split()
        if len(words) != 2:
            print ("Wrong parameter")
        else:
            body = {"key": words[0], "timeout": words[1]}
            url = "http://localhost:5000/EXPIRE"
            response = self.sendPostRequest(url, body)
            print(response.read())

    def do_TTL(self, text):
        """ GET TTL"""
        words = text.split()
        if len(words) != 1:
            print ("Wrong parameter")
        else:
            body = {"key": words[0]}
            url = "http://localhost:5000/TTL"
            response = self.sendPostRequest(url, body)
            print(response.read())

    def do_SAVE(self, text):
        """ SAVE CURRENT STATE"""
        r = requests.post("http://localhost:5000/SAVE")
        print(r.text)


    def do_RESTORE(self, text):
        """ RESTORE CURRENT STATE"""
        r = requests.post("http://localhost:5000/RESTORE")
        print(r.text)

if __name__ == '__main__':
    HelloWorld().cmdloop()