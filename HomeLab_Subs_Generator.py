import socket
import struct

JSON_IP = "192.168.30.48"
JSON_PORT = 1234

class Trigger(FirewallTrigger):

    def connectToPSM(self):
        self.psmSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.psmSock.connect((JSON_IP, JSON_PORT))

    def sendToPSM(self, data):
        try:
            if self.psmSock.send(data + "\n") <= 0:
                self.connectToPSM()
        except:
            self.connectToPSM()

    def __init__(self):
        #self.connectToPSM()
        FirewallTrigger.__init__(self)

    def trigger(self):
        localIP=str(self.client_ip)
        rawIP = socket.inet_aton(self.client_ip)
        fakeBillingId = struct.unpack("!L", rawIP)[0]



        if localIP.startswith("39.125.26."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f0000000000b","tier":"Gold","cellId":"enodeb107","apn":"unet","ggsn":"pgw1","device":"35344602"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)

        elif localIP.startswith("39.125.219."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020001","tier":"Silver","cellId":"nodeb73","apn":"unet","ggsn":"pgw1","tac":"35344602"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("219.254.136."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f0000000000b","tier":"Bronze","cellId":"enodeb119","apn":"unet","ggsn":"pgw1","tac":"35315102"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("116.122.73."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000009","tier":"Gold","cellId":"enodeb105","apn":"unet","ggsn":"pgw1","tac":"35344607"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.66."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010003","tier":"Silver","cellId":"cell15","apn":"unet","ggsn":"pgw1","tac":"35344605"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("10.10.10."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f0000003000b","tier":"Bronze","cellId":"nodeb95","apn":"unet","ggsn":"pgw1","tac":"35315101"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.84."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010008","tier":"Gold","cellId":"cell20","apn":"unet","ggsn":"pgw1","tac":"35344604"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.90."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000009","tier":"Silver","cellId":"enodeb141","apn":"unet","ggsn":"pgw1","tac":"35344668"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.181."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010001","tier":"Bronze","cellId":"nodeb61","apn":"unet","ggsn":"pgw1","tac":"35344657"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.179."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000009","tier":"Gold","cellId":"nodeb57","apn":"unet","ggsn":"pgw1","tac":"86367400"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.132."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030003","tier":"Silver","cellId":"nodeb87","apn":"unet","ggsn":"pgw1","tac":"10002"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.95."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f0000001000a","tier":"Bronze","cellId":"cell22","apn":"unet","ggsn":"pgw1","tac":"10003"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.70."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030003","tier":"Gold","cellId":"cell39","apn":"unet","ggsn":"pgw1","tac":"10004"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.236."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030004","tier":"Silver","cellId":"nodeb88","apn":"unet","ggsn":"pgw1","tac":"10007"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.118."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000004","tier":"Bronze","cellId":"enodeb124","apn":"unet","ggsn":"pgw1","tac":"10009"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.208."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000007","tier":"Gold","cellId":"enodeb115","apn":"unet","ggsn":"pgw1","tac":"35344645"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.232."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010007","tier":"Silver","cellId":"nodeb67","apn":"unet","ggsn":"pgw1","tac":"35344635"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.192."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000005","tier":"Bronze","cellId":"nodeb53","apn":"unet","ggsn":"pgw1","tac":"1161200"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.218."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020000","tier":"Gold","cellId":"nodeb72","apn":"unet","ggsn":"pgw1","tac":"35344634"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.233."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000007","tier":"Silver","cellId":"enodeb139","apn":"unet","ggsn":"pgw3","tac":"1194800"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.56."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000007","tier":"Bronze","cellId":"enodeb103","apn":"unet","ggsn":"pgw3","tac":"94000700"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.91."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000004","tier":"Gold","cellId":"enodeb100","apn":"unet","ggsn":"pgw3","tac":"35344625"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.237."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f0000001000b","tier":"Silver","cellId":"nodeb71","apn":"unet","ggsn":"pgw3","tac":"35344624"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.206."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030006","tier":"Bronze","cellId":"nodeb90","apn":"unet","ggsn":"pgw3","tac":"35318902"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.140."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000008","tier":"Gold","cellId":"enodeb140","apn":"unet","ggsn":"pgw3","tac":"35344692"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.78."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000008","tier":"Silver","cellId":"enodeb116","apn":"unet","ggsn":"pgw3","tac":"35344619"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.126."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000004","tier":"Bronze","cellId":"nodeb52","apn":"unet","ggsn":"pgw3","tac":"35344623"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.243."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000002","tier":"Gold","cellId":"nodeb50","apn":"unet","ggsn":"pgw3","tac":"35344611"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.65."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000003","tier":"Silver","cellId":"enodeb111","apn":"unet","ggsn":"pgw3","tac":"35344609"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.94."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010000","tier":"Bronze","cellId":"cell12","apn":"unet","ggsn":"pgw3","tac":"35344608"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("1.220.214."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030002","tier":"Gold","cellId":"nodeb86","apn":"unet","ggsn":"pgw3","tac":"35344612"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.57."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000009","tier":"Silver","cellId":"enodeb117","apn":"unet","ggsn":"pgw3","tac":"35344602"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.227."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000001","tier":"Bronze","cellId":"nodeb49","apn":"unet","ggsn":"pgw3","tac":"35315102"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.141."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020007","tier":"Gold","cellId":"cell31","apn":"unet","ggsn":"pgw3","tac":"35344607"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.235."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030004","tier":"Silver","cellId":"cell40","apn":"unet","ggsn":"pgw3","tac":"35344605"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.240."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000000","tier":"Bronze","cellId":"enodeb120","apn":"unet","ggsn":"pgw3","tac":"35315101"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.225."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020000","tier":"Gold","cellId":"cell24","apn":"unet","ggsn":"pgw3","tac":"35344604"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("1.250.179."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030006","tier":"Silver","cellId":"cell42","apn":"unet","ggsn":"pgw3","tac":"35344668"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.89."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010003","tier":"Bronze","cellId":"nodeb63","apn":"unet","ggsn":"pgw3","tac":"35344657"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.216."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000004","tier":"Gold","cellId":"cell04","apn":"unet","ggsn":"pgw3","tac":"86367400"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.79."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000002","tier":"Silver","cellId":"cell02","apn":"unet","ggsn":"pgw3","tac":"10002"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.133."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f0000000000b","tier":"Bronze","cellId":"nodeb59","apn":"unet","ggsn":"pgw3","tac":"10003"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.162."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000007","tier":"Gold","cellId":"nodeb55","apn":"unet","ggsn":"pgw3","tac":"10004"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.248."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020003","tier":"Silver","cellId":"cell27","apn":"unet","ggsn":"pgw2","tac":"10007"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.32."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000001","tier":"Bronze","cellId":"enodeb133","apn":"unet","ggsn":"pgw2","tac":"10009"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.92."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010000","tier":"Gold","cellId":"nodeb60","apn":"unet","ggsn":"pgw2","tac":"35344645"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.230."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f0000003000b","tier":"Silver","cellId":"cell47","apn":"unet","ggsn":"pgw2","tac":"35344635"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.210."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020009","tier":"Bronze","cellId":"nodeb81","apn":"unet","ggsn":"pgw2","tac":"1161200"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.224."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020008","tier":"Gold","cellId":"nodeb80","apn":"unet","ggsn":"pgw2","tac":"35344634"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.149."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020006","tier":"Silver","cellId":"nodeb78","apn":"unet","ggsn":"pgw2","tac":"1194800"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.226."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f0000000000a","tier":"Bronze","cellId":"enodeb142","apn":"unet","ggsn":"pgw2","tac":"94000700"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.242."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020006","tier":"Gold","cellId":"cell30","apn":"unet","ggsn":"pgw2","tac":"35344625"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.98."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000005","tier":"Silver","cellId":"enodeb101","apn":"unet","ggsn":"pgw2","tac":"35344624"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.20."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010005","tier":"Bronze","cellId":"cell17","apn":"unet","ggsn":"pgw2","tac":"35318902"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.169."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000006","tier":"Gold","cellId":"enodeb138","apn":"unet","ggsn":"pgw2","tac":"35344692"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.231."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000008","tier":"Silver","cellId":"nodeb56","apn":"unet","ggsn":"pgw2","tac":"35344619"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.163."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010008","tier":"Bronze","cellId":"nodeb68","apn":"unet","ggsn":"pgw2","tac":"35344623"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.7."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030001","tier":"Gold","cellId":"nodeb85","apn":"unet","ggsn":"pgw2","tac":"35344611"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.244."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f0000000000b","tier":"Silver","cellId":"enodeb131","apn":"unet","ggsn":"pgw2","tac":"35344609"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("221.141.195."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000008","tier":"Bronze","cellId":"enodeb128","apn":"unet","ggsn":"pgw2","tac":"35344608"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.180."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000006","tier":"Gold","cellId":"enodeb126","apn":"unet","ggsn":"pgw4","tac":"35344612"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.72."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020002","tier":"Silver","cellId":"nodeb74","apn":"unet","ggsn":"pgw4","tac":"35344602"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.147."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000000","tier":"Bronze","cellId":"enodeb108","apn":"unet","ggsn":"pgw4","tac":"35315102"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.25."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030002","tier":"Gold","cellId":"cell38","apn":"unet","ggsn":"pgw4","tac":"35344607"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.201."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f0000002000a","tier":"Silver","cellId":"cell34","apn":"unet","ggsn":"pgw4","tac":"35344605"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.239."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020004","tier":"Bronze","cellId":"nodeb76","apn":"unet","ggsn":"pgw4","tac":"35315101"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.93."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000003","tier":"Gold","cellId":"enodeb99","apn":"unet","ggsn":"pgw4","tac":"35344604"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.173."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000008","tier":"Silver","cellId":"cell08","apn":"unet","ggsn":"pgw4","tac":"35344668"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.96."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020007","tier":"Bronze","cellId":"nodeb79","apn":"unet","ggsn":"pgw4","tac":"35344657"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.136."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020004","tier":"Gold","cellId":"cell28","apn":"unet","ggsn":"pgw4","tac":"86367400"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("175.122.253."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f0000000000a","tier":"Silver","cellId":"enodeb130","apn":"unet","ggsn":"pgw4","tac":"10002"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.202."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030007","tier":"Bronze","cellId":"nodeb91","apn":"unet","ggsn":"pgw4","tac":"10003"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.183."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000002","tier":"Gold","cellId":"enodeb134","apn":"unet","ggsn":"pgw4","tac":"10004"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.160."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020002","tier":"Silver","cellId":"cell26","apn":"unet","ggsn":"pgw4","tac":"10007"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.36."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000002","tier":"Bronze","cellId":"enodeb98","apn":"unet","ggsn":"pgw4","tac":"10009"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.221."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f0000000000b","tier":"Gold","cellId":"enodeb143","apn":"unet","ggsn":"pgw4","tac":"35344645"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.117."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000005","tier":"Silver","cellId":"enodeb137","apn":"unet","ggsn":"pgw4","tac":"35344635"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.178."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030000","tier":"Bronze","cellId":"nodeb84","apn":"unet","ggsn":"pgw4","tac":"1161200"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.209."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010007","tier":"Gold","cellId":"cell19","apn":"unet","ggsn":"pgw4","tac":"35344634"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.234."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000005","tier":"Silver","cellId":"cell05","apn":"unet","ggsn":"pgw4","tac":"1194800"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.5."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000002","tier":"Bronze","cellId":"enodeb122","apn":"unet","ggsn":"pgw4","tac":"94000700"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.64."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000003","tier":"Gold","cellId":"enodeb123","apn":"unet","ggsn":"pgw4","tac":"35344625"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.76."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000003","tier":"Silver","cellId":"cell03","apn":"unet","ggsn":"pgw4","tac":"35344624"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.251."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"0025f00000000000","tier":"Bronze","cellId":"enodeb136","apn":"unet","ggsn":"pgw4","tac":"35318902"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.111."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"0025f00000030007","tier":"Gold","cellId":"enodeb132","apn":"unet","ggsn":"pgw4","tac":"35344692"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.54."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"0125f0000003000a","tier":"Silver","cellId":"enodeb118","apn":"unet","ggsn":"pgw4","tac":"35344619"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.254."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"0025f00000030008","tier":"Bronze","cellId":"enodeb106","apn":"unet","ggsn":"pgw4","tac":"35344623"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.223."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"8225f000000325f00000000004","tier":"Gold","cellId":"cell00","apn":"unet","ggsn":"pgw4","tac":"35344611"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.98.4"):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"8225f000000325f00000000000","tier":"Silver","cellId":"cell43","apn":"unet","ggsn":"pgw4","tac":"35344609"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.120."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"8225f000000125f0000000000a","tier":"Bronze","cellId":"nodeb94","apn":"unet","ggsn":"pgw4","tac":"35344608"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.10."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"8225f000000025f0000000000a","tier":"Gold","cellId":"cell44","apn":"unet","ggsn":"pgw4","tac":"35344612"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.187."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010006","tier":"Silver","cellId":"nodeb66","apn":"unet","ggsn":"pgw4","tac":"35344602"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.211."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000006","tier":"Bronze","cellId":"nodeb54","apn":"unet","ggsn":"pgw4","tac":"35315102"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.220."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030000","tier":"Gold","cellId":"cell36","apn":"unet","ggsn":"pgw4","tac":"35344607"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.39."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020008","tier":"Silver","cellId":"cell32","apn":"unet","ggsn":"pgw4","tac":"35344605"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.135."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020009","tier":"Bronze","cellId":"cell33","apn":"unet","ggsn":"pgw4","tac":"35315101"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.12."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f0000003000a","tier":"Gold","cellId":"cell46","apn":"unet","ggsn":"pgw4","tac":"35344604"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.219."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020001","tier":"Silver","cellId":"nodeb73","apn":"unet","ggsn":"pgw1","tac":"35344668"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("219.254.136."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f0000000000b","tier":"Bronze","cellId":"enodeb119","apn":"unet","ggsn":"pgw1","tac":"35344657"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("116.122.73."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000009","tier":"Gold","cellId":"enodeb105","apn":"unet","ggsn":"pgw1","tac":"86367400"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.66."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010003","tier":"Silver","cellId":"cell15","apn":"unet","ggsn":"pgw1","tac":"10002"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("10.10.10."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f0000003000b","tier":"Bronze","cellId":"nodeb95","apn":"unet","ggsn":"pgw1","tac":"10003"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.84."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010008","tier":"Gold","cellId":"cell20","apn":"unet","ggsn":"pgw1","tac":"10004"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.90."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000009","tier":"Silver","cellId":"enodeb141","apn":"unet","ggsn":"pgw1","tac":"10007"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.181."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010001","tier":"Bronze","cellId":"nodeb61","apn":"unet","ggsn":"pgw1","tac":"10009"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.179."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000009","tier":"Gold","cellId":"nodeb57","apn":"unet","ggsn":"pgw1","tac":"35344645"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.132."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030003","tier":"Silver","cellId":"nodeb87","apn":"unet","ggsn":"pgw1","tac":"35344635"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.95."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f0000001000a","tier":"Bronze","cellId":"cell22","apn":"unet","ggsn":"pgw1","tac":"1161200"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.70."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030003","tier":"Gold","cellId":"cell39","apn":"unet","ggsn":"pgw1","tac":"35344634"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.236."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030004","tier":"Silver","cellId":"nodeb88","apn":"unet","ggsn":"pgw1","tac":"1194800"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.118."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000004","tier":"Bronze","cellId":"enodeb124","apn":"unet","ggsn":"pgw1","tac":"94000700"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.208."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000007","tier":"Gold","cellId":"enodeb115","apn":"unet","ggsn":"pgw1","tac":"35344625"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.232."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010007","tier":"Silver","cellId":"nodeb67","apn":"unet","ggsn":"pgw1","tac":"35344624"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.192."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000005","tier":"Bronze","cellId":"nodeb53","apn":"unet","ggsn":"pgw1","tac":"35318902"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.218."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020000","tier":"Gold","cellId":"nodeb72","apn":"unet","ggsn":"pgw1","tac":"35344692"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.233."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000007","tier":"Silver","cellId":"enodeb139","apn":"unet","ggsn":"pgw3","tac":"35344619"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.56."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000007","tier":"Bronze","cellId":"enodeb103","apn":"unet","ggsn":"pgw3","tac":"35344623"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.91."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000004","tier":"Gold","cellId":"enodeb100","apn":"unet","ggsn":"pgw3","tac":"35344611"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.237."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f0000001000b","tier":"Silver","cellId":"nodeb71","apn":"unet","ggsn":"pgw3","tac":"35344609"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.206."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030006","tier":"Bronze","cellId":"nodeb90","apn":"unet","ggsn":"pgw3","tac":"35344608"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.140."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000008","tier":"Gold","cellId":"enodeb140","apn":"unet","ggsn":"pgw3","tac":"35344612"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.78."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000008","tier":"Silver","cellId":"enodeb116","apn":"unet","ggsn":"pgw3","tac":"35344602"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.126."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000004","tier":"Bronze","cellId":"nodeb52","apn":"unet","ggsn":"pgw3","tac":"35315102"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.243."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000002","tier":"Gold","cellId":"nodeb50","apn":"unet","ggsn":"pgw3","tac":"35344607"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.65."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000003","tier":"Silver","cellId":"enodeb111","apn":"unet","ggsn":"pgw3","tac":"35344605"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.94."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010000","tier":"Bronze","cellId":"cell12","apn":"unet","ggsn":"pgw3","tac":"35315101"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("1.220.214."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030002","tier":"Gold","cellId":"nodeb86","apn":"unet","ggsn":"pgw3","tac":"35344604"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.57."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000009","tier":"Silver","cellId":"enodeb117","apn":"unet","ggsn":"pgw3","tac":"35344668"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.227."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000001","tier":"Bronze","cellId":"nodeb49","apn":"unet","ggsn":"pgw3","tac":"35344657"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.141."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020007","tier":"Gold","cellId":"cell31","apn":"unet","ggsn":"pgw3","tac":"86367400"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.235."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030004","tier":"Silver","cellId":"cell40","apn":"unet","ggsn":"pgw3","tac":"10002"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.240."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000000","tier":"Bronze","cellId":"enodeb120","apn":"unet","ggsn":"pgw3","tac":"10003"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.225."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020000","tier":"Gold","cellId":"cell24","apn":"unet","ggsn":"pgw3","tac":"10004"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("1.250.179."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030006","tier":"Silver","cellId":"cell42","apn":"unet","ggsn":"pgw3","tac":"10007"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.89."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010003","tier":"Bronze","cellId":"nodeb63","apn":"unet","ggsn":"pgw3","tac":"10009"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.216."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000004","tier":"Gold","cellId":"cell04","apn":"unet","ggsn":"pgw3","tac":"35344645"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.79."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000002","tier":"Silver","cellId":"cell02","apn":"unet","ggsn":"pgw3","tac":"35344635"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.133."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f0000000000b","tier":"Bronze","cellId":"nodeb59","apn":"unet","ggsn":"pgw3","tac":"1161200"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.162."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000007","tier":"Gold","cellId":"nodeb55","apn":"unet","ggsn":"pgw3","tac":"35344634"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.248."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020003","tier":"Silver","cellId":"cell27","apn":"unet","ggsn":"pgw2","tac":"1194800"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.32."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000001","tier":"Bronze","cellId":"enodeb133","apn":"unet","ggsn":"pgw2","tac":"94000700"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.92."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010000","tier":"Gold","cellId":"nodeb60","apn":"unet","ggsn":"pgw2","tac":"35344625"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.230."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f0000003000b","tier":"Silver","cellId":"cell47","apn":"unet","ggsn":"pgw2","tac":"35344624"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.210."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020009","tier":"Bronze","cellId":"nodeb81","apn":"unet","ggsn":"pgw2","tac":"35318902"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.224."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020008","tier":"Gold","cellId":"nodeb80","apn":"unet","ggsn":"pgw2","tac":"35344692"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.149."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020006","tier":"Silver","cellId":"nodeb78","apn":"unet","ggsn":"pgw2","tac":"35344619"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.226."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f0000000000a","tier":"Bronze","cellId":"enodeb142","apn":"unet","ggsn":"pgw2","tac":"35344623"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.242."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020006","tier":"Gold","cellId":"cell30","apn":"unet","ggsn":"pgw2","tac":"35344611"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.98."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000005","tier":"Silver","cellId":"enodeb101","apn":"unet","ggsn":"pgw2","tac":"35344609"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.20."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010005","tier":"Bronze","cellId":"cell17","apn":"unet","ggsn":"pgw2","tac":"35344608"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.169."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000006","tier":"Gold","cellId":"enodeb138","apn":"unet","ggsn":"pgw2","tac":"35344612"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.231."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000008","tier":"Silver","cellId":"nodeb56","apn":"unet","ggsn":"pgw2","tac":"35344602"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.163."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010008","tier":"Bronze","cellId":"nodeb68","apn":"unet","ggsn":"pgw2","tac":"35315102"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.7."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030001","tier":"Gold","cellId":"nodeb85","apn":"unet","ggsn":"pgw2","tac":"35344607"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.244."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f0000000000b","tier":"Silver","cellId":"enodeb131","apn":"unet","ggsn":"pgw2","tac":"35344605"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("221.141.195."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000008","tier":"Bronze","cellId":"enodeb128","apn":"unet","ggsn":"pgw2","tac":"35315101"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.180."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000006","tier":"Gold","cellId":"enodeb126","apn":"unet","ggsn":"pgw4","tac":"35344604"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.72."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020002","tier":"Silver","cellId":"nodeb74","apn":"unet","ggsn":"pgw4","tac":"35344668"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.147."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000125f00000000000","tier":"Bronze","cellId":"enodeb108","apn":"unet","ggsn":"pgw4","tac":"35344657"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.25."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030002","tier":"Gold","cellId":"cell38","apn":"unet","ggsn":"pgw4","tac":"86367400"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.201."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f0000002000a","tier":"Silver","cellId":"cell34","apn":"unet","ggsn":"pgw4","tac":"10002"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.239."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020004","tier":"Bronze","cellId":"nodeb76","apn":"unet","ggsn":"pgw4","tac":"10003"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.93."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000003","tier":"Gold","cellId":"enodeb99","apn":"unet","ggsn":"pgw4","tac":"10004"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.173."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000008","tier":"Silver","cellId":"cell08","apn":"unet","ggsn":"pgw4","tac":"10007"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.96."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000020007","tier":"Bronze","cellId":"nodeb79","apn":"unet","ggsn":"pgw4","tac":"10009"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.136."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020004","tier":"Gold","cellId":"cell28","apn":"unet","ggsn":"pgw4","tac":"35344645"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("175.122.253."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f0000000000a","tier":"Silver","cellId":"enodeb130","apn":"unet","ggsn":"pgw4","tac":"35344635"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.202."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030007","tier":"Bronze","cellId":"nodeb91","apn":"unet","ggsn":"pgw4","tac":"1161200"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.183."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000002","tier":"Gold","cellId":"enodeb134","apn":"unet","ggsn":"pgw4","tac":"35344634"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.160."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020002","tier":"Silver","cellId":"cell26","apn":"unet","ggsn":"pgw4","tac":"1194800"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.36."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000025f00000000002","tier":"Bronze","cellId":"enodeb98","apn":"unet","ggsn":"pgw4","tac":"94000700"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.221."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f0000000000b","tier":"Gold","cellId":"enodeb143","apn":"unet","ggsn":"pgw4","tac":"35344625"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.117."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000325f00000000005","tier":"Silver","cellId":"enodeb137","apn":"unet","ggsn":"pgw4","tac":"35344624"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.178."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000030000","tier":"Bronze","cellId":"nodeb84","apn":"unet","ggsn":"pgw4","tac":"35318902"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.209."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000010007","tier":"Gold","cellId":"cell19","apn":"unet","ggsn":"pgw4","tac":"35344692"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.234."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000005","tier":"Silver","cellId":"cell05","apn":"unet","ggsn":"pgw4","tac":"35344619"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.5."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000002","tier":"Bronze","cellId":"enodeb122","apn":"unet","ggsn":"pgw4","tac":"35344623"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.64."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"8225f000000225f00000000003","tier":"Gold","cellId":"enodeb123","apn":"unet","ggsn":"pgw4","tac":"35344611"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.76."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000000003","tier":"Silver","cellId":"cell03","apn":"unet","ggsn":"pgw4","tac":"35344609"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.251."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"0025f00000000000","tier":"Bronze","cellId":"enodeb136","apn":"unet","ggsn":"pgw4","tac":"35344608"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.111."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"0025f00000030007","tier":"Gold","cellId":"enodeb132","apn":"unet","ggsn":"pgw4","tac":"35344612"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.54."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"0125f0000003000a","tier":"Silver","cellId":"enodeb118","apn":"unet","ggsn":"pgw4","tac":"35344602"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.254."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"4G","location":"0025f00000030008","tier":"Bronze","cellId":"enodeb106","apn":"unet","ggsn":"pgw4","tac":"35315102"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.223."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"8225f000000325f00000000004","tier":"Gold","cellId":"cell00","apn":"unet","ggsn":"pgw4","tac":"35344607"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.98.4"):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"8225f000000325f00000000000","tier":"Silver","cellId":"cell43","apn":"unet","ggsn":"pgw4","tac":"35344605"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.120."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"8225f000000125f0000000000a","tier":"Bronze","cellId":"nodeb94","apn":"unet","ggsn":"pgw4","tac":"35315101"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.10."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"8225f000000025f0000000000a","tier":"Gold","cellId":"cell44","apn":"unet","ggsn":"pgw4","tac":"35344604"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.187."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000010006","tier":"Silver","cellId":"nodeb66","apn":"unet","ggsn":"pgw4","tac":"35344668"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.211."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"3G","location":"0125f00000000006","tier":"Bronze","cellId":"nodeb54","apn":"unet","ggsn":"pgw4","tac":"35344657"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.220."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000030000","tier":"Gold","cellId":"cell36","apn":"unet","ggsn":"pgw4","tac":"86367400"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.39."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020008","tier":"Silver","cellId":"cell32","apn":"unet","ggsn":"pgw4","tac":"10002"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.135."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f00000020009","tier":"Bronze","cellId":"cell33","apn":"unet","ggsn":"pgw4","tac":"10003"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)
        elif localIP.startswith("39.125.12."):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"2G","location":"0025f0000003000a","tier":"Gold","cellId":"cell46","apn":"unet","ggsn":"pgw4","tac":"10004"}' % (fakeBillingId, self.client_ip) 
            self.sendToPSM(jsonData)




# Ungroup
        else:
            jsonData = '{"ip":"%s","networkGroup":"NotMyIP"}' % (fakeBillingId, self.client_ip)        
            
            
            
            
            
            
            
            