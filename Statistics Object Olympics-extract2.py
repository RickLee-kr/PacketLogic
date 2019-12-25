import packetlogic2
import datetime

HOST = '1.235.126.132' # The address of the PacketLogic
USER = 'pl'
PASSWORD = 'pl'
TIMEOUT = 900

# The path is the same as you would see in the statistics view of the client,
# excluding some parameters used exclusively for display settings. In this
# case, the Statistics Object Olympics has a single subpath called Server 
# Hostname which is a Property of the connection. Under the Server Hostname
# path you will find the individual hostnames, and under those, you will find
# the NetObjects representing the individual subscribers.
PATH = '/Subscribers?Statistics Object/?splittype'
HOURS = 24

def get_interval(end_time, n):
    """ Returns a time interval ending at the last full hour before and
    including end_time and starting at the last full hour - n hours before and
    including end_time.

    """

    start_time = end_time - datetime.timedelta(hours=n)
    start_time = start_time.strftime("%Y-%m-%d %H:00:00")
    end_time = end_time.strftime("%Y-%m-%d %H:00:00")
    return start_time, end_time

def extract(stats, path, start_time, end_time):
    """ Returns a condensed representation of a listing of a Property node in
    the statistics tree.

    The returned value is a list of dictionaries with the keys "host",
    "subscribers" and "megabytes"
    """

    # This is documented at http://python.proceranetworks.com/current/statistics.html#module-packetlogic2.pldb.statistics-Statistics-list
    # In short, the returned data is a list of dictionaries, each enty
    # representing a sub-path of the path we are listing
    subpaths = stats.list(start_time, end_time, PATH)

    # Rearrange and condense the data into something that is meaningful in
    # this use case
    return [
        {
            # In this case, the subpath name is the hostname of one of the
            # services included in the statistics
            'host': subpath['name'],

            # subitemcounts is a dictionary where each key represents a type
            # of object that exists in the subpaths. The associated value of
            # each of these keys is the total count of objects of that type
            # that exist in under this node. In this case, we want to count
            # subitems of the NetObject type, of which each represents a
            # subscriber
            'subscribers': int(subpath['subitemcounts'].get('NetObject', 0)),

            # values is a dictionary of statistical values for the subpath.
            # Depending on how the associated statistics object is configured,
            # it will contain different values. In this case, we have
            # configured the object to track traffic, and we extract
            # "bytes_total" to derive the usage in megabytes
            'megabytes': subpath['values']['bytes total'] / (1024 ** 2)
        }
        for subpath in subpaths
    ]

if __name__ == '__main__':
    import json

    # Create a PacketLogic connection object.
    pl = packetlogic2.connect(HOST, USER, PASSWORD, timeout=TIMEOUT)

    # Get the statistics object of that connection
    stats = pl.Statistics()

    # Set the timeout on the stats object as well, to avoid a know bug causing
    # the connection object timeout not to apply
    stats.timeout = TIMEOUT

    # Get the appropriate time interval; in this case HOURS hours before now
    start_time, end_time = get_interval(datetime.datetime.now(), HOURS)

    # Extract the data we need
    data = extract(stats, PATH, start_time, end_time)

    # Close the connection using the statistics object (the statistics instance
    # is what actually maintains the connection, not the connection object)
    stats.close()

    # Pretty print the extracted data
    print json.dumps(data, indent=2)
