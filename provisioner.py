import csv
import os
import packetlogic2
import threading
import random
from plhost2 import PLHost2


class StaticProvisioner(object):
    def __init__(self, target, fixture_path, subscribers_file='subscribers.csv', base_netobject='/NetObjects/PSM'):
        self.devices = []
        self.cells = []
        self.subscribers = []
        self.target = target
        self.fixture = {}
        self.connection = packetlogic2.connect(target.ip, "admin", "pldemo00")
        self.rs = self.connection.Ruleset()

        self.fixture_path = fixture_path
        self.subscribers_file = subscribers_file

        self.base_netobject = base_netobject

        self.netobject_paths = self.getNetObjectPaths()

    def setFixturePath(self, fixture_path):
        self.fixture_path = fixture_path

    def setSubsribersFile(self, subscribers_file):
        self.subscribers_file = subscribers_file

    def setBaseNetObject(self, base_netobject):
        self.base_netobject = base_netobject

    def getNetObjectPaths(self):
        paths = {}
        paths['device'] = self.base_netobject + '/Mobile/By Device'
        paths['location'] = self.base_netobject + '/Mobile/By Location'
        paths['subscriber_id'] = self.base_netobject + '/Subscribers'
        paths['subscriber_tier_name'] = self.base_netobject + '/By Tier'
        paths['cell_id'] = self.base_netobject + '/Mobile/By Cell ID'
        paths['cmts_name'] = self.base_netobject + '/Fixed/By CMTS'
        paths['device_imei'] = self.base_netobject + '/Mobile/By IMEI'
        paths['device_tac'] = self.base_netobject + '/Mobile/By TAC'
        return paths

    def loadFixture(self, fixture_file):
        with open(os.path.join(self.fixture_path, fixture_file)) as finput:
            csv_reader = csv.DictReader(finput)
            for row in csv_reader:
                self.fixture[row['subscriber_id']] = row

    def loadSubscribers(self):
        with open(os.path.join(self.subscribers_file)) as finput:
            csv_reader = csv.DictReader(finput)
            for row in csv_reader:
                if 'subscriber_id' in row.keys():
                    self.subscribers.append((row['ip_address'], row['subscriber_id']))

    def createDynItems(self):
        rt = self.connection.Realtime()
        path_ids = {}
        base_no_id = self.getBaseNetObject().id
        for key in self.netobject_paths.keys():
            path_ids[key] = self.addNetObject(self.netobject_paths[key]).id
        self.rs.commit()
        for ip_address, subscriber_id in self.subscribers:
            dyn_items = []
            if subscriber_id in self.fixture.keys():
                row = self.fixture[subscriber_id]
                for name, value in row.items():
                    if name in path_ids.keys():
                        dyn_items.append((path_ids[name], {rt.dyn.SUBSCRIBER_NAME: value, rt.dyn.IS_SUBSCRIBER: True}))
            rt.dyn.set(base_no_id, ip_address, dyn_items)

    def addNetObject(self, netobject_path):
        netobject = self.rs.object_find(netobject_path)
        if not netobject:
            netobject = self.rs.object_add(netobject_path)
        return netobject

    def getBaseNetObject(self):
        base_netobject = self.addNetObject(self.base_netobject)
        base_netobject.set_visible(True)
        self.addNetObject(self.base_netobject + '/Mobile')
        self.addNetObject(self.base_netobject + '/Fixed')
        return base_netobject


class SCWorker(threading.Thread):
    
    def __init__(self, target):
        super(SCWorker, self).__init__()
        self.connect(target.ip)
        self.sc = self.connection._SessionContext()
        self.rt = self.connection.Realtime()
        self.sublist = []
        self.sc_sch_handle = None

    def run(self):
        self.register_schema(self.sc)
        self.update()

    def update(self):
        vb = self.rt.get_view_builder()
        vb.filter_out("Session Context", "TestSchema/provisioned=true")
        vb.distribution("Local Host")
        self.rt.add_aggr_view_callback(vb, self.cb)
        self.rt.update_forever()

    def cb(self, node):
        for c in node.children:
            if c.name not in self.sublist:
                self.register_subscriber(c.name)
                self.sublist.append(c.name)
        self.sublist = sorted(self.sublist)

    def register_subscriber(self, ip):
        if ':' in ip:
            subnet = '128'
        else:
            subnet = '32'
        self.sc_sch_handle.create(
            ip="{}/{}".format(ip, subnet),
            subscriber="{}".format(ip),
            provisioned=1,
            service_plan=random.choice(xrange(4))
            )

    def connect(self, ip):
        self.connection = packetlogic2.connect(ip, "admin", "pldemo00")

    def register_schema(self, sc):
        schema = sc.Schema(
            id=2,
            name='TestSchema',
            timeout=5,
            columns=[
                sc.Column(name='ip',
                               type=sc.IP_PREFIX,
                               is_sticky=1,
                               content_type='ip',
                               keytype=sc.LOCALIP),
                sc.Column(name='subscriber',
                               type=sc.OCTETS,
                               is_sticky=0,
                               content_type='',
                               keytype=sc.NOT_IN_KEY),
                sc.Column(name='provisioned',
                               type=sc.INT16,
                               is_sticky=0,
                               content_type='application/x-boolean',
                               keytype=sc.NOT_IN_KEY),
                sc.Column(name='service_plan',
                               type=sc.INT16,
                               is_sticky=0,
                               content_type='enum:0=Unknown,1=Gold,2=Silver,3=Bronze',
                               keytype=sc.NOT_IN_KEY)])
        self.sc_sch_handle = sc.register(schema)


def test_dynamic_sc(ip):
    pl = PLHost2(ip, '')
    scw = SCWorker(pl)
    scw.run()
