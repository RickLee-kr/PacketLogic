def parse(name):
    out = {}
    name = name.strip().split('_-_')
    rctime = name[1].split('.')
    timeprivext = name[2].split('.')
    out['node_id'] = name[0]
    out['rc'] = rctime[0]
    out['time'] = (rctime[1] + timeprivext[0])[:-5]
    out['timezone'] = (rctime[1] + timeprivext[0])[-5:]
    out['private'] = timeprivext[1]
    out['extension'] = timeprivext[2]
    return out

if __name__ == '__main__':
    list = file('cdrs').readlines()
    for name in list:
        print parse(name)
