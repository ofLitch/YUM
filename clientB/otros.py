
# Maniobrar Msg
def encryptMsg(self, msg):
    return rsa.encrypt(msg.encode(), self.priKey)

def decryptMsg(self, data):
    return rsa.decrypt(data, self.pubKey).decode()

# For keys
def generateKeys(self):
    private_key, public_key = rsa.newkeys(512)
    file_pri = open('clientA/privKeyUserA.txt', 'wb')
    pickle.dump(private_key, file_pri)
    file_pri.close()

    file_pub = open('clientA/pubKeyUserA.txt', 'wb')
    pickle.dump(public_key, file_pub)
    file_pub.close()
    
def readKeys(self):
    file_pri_c = open('clientA/privKeyUserA.txt', 'rb')
    self.priKey = pickle.load(file_pri_c)
    file_pri_c.close()
    
    file_pub_c = open('clientA/pubKeyUserA.txt', 'rb')
    self.pubKey = pickle.load(file_pub_c)
    file_pub_c.close()
    
    file_pub_c_B = open('clientB/pubKeyUserB.txt', 'rb')
    self.pubKeyB = pickle.load(file_pub_c_B)
    file_pub_c_B.close()
        
def saveKeyFromUser(public_key):
    file_pub = open('clientA/pubKeyUserB.txt', 'wb')
    pickle.dump(public_key, file_pub)
    file_pub.close()

def readKeyFromUser():
    file_pub = open('clientA/pubKeyUserB.txt', 'rb')
    key = pickle.load(file_pub)
    file_pub.close()
    return key
