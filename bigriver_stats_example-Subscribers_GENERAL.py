#
# Example code to read stats for a specific subscriber (path "/Subscribers")
#

import packetlogic2

## Statistics server connection data
stats_server_ip_addr = "10.0.22.33"
stats_server_user = "admin"
stats_server_pass = "pldemo00"

## Subscriber data
start_date = "2015-07-16"
end_date = "2015-07-16"
subscriber_id = "311970100002848"

# Connects to statistics server and creates "Statistics" object to perform the query
pl_obj = packetlogic2.connect(stats_server_ip_addr, stats_server_user, stats_server_pass)
stats_obj = pl_obj.Statistics()

# Lists that will be used
full_volume_list = []
interesting_volume_list = []
graph_data_list =[]

# Gathers the subscriber data
try:
    ########## GATHERING VOLUME DATA

    # The line below collects volume data from a given statistics path
    full_volume_list=stats_obj.list(start_date, end_date, "/Subscribers?Statistics Object/All?NetObject/" + subscriber_id + "?NetObject", replymask = stats_obj.TOTALFIELD_BYTES_IN + stats_obj.TOTALFIELD_BYTES_OUT)

    for item in full_volume_list:
        if int(item['type']) == 517:
            # We're interested in items of type 517 (ServiceObjects), which are the service categories.
            # For the specific "Service" objects, the type is 518.
            interesting_volume_list.append(item)

    #
    # The resulting "interesting_volume_list" is a list containing items which the format is like the example below:
    #
    #   {'values': {'bytes out': 27475.0, 'bytes in': 24978.0}, 'type': 517, 'name': 'Entertainment', 'subitemcounts': {}, 'flags': 9}
    #
    # For the purpose of building a pie chart, the interesting data would be "values" and "name". Information can be accesses as
    # below:
    #
    #   Total Bytes IN: item['values']['bytes in']
    #   Total Bytes OUT: item['values']['bytes out']
    #   Category name: item['name']
    #
    print ""
    print "Subscriber data for " + subscriber_id + " (period from " + start_date + " to " + end_date + "):"
    print ""
    print "### CATEGORIES VOLUME DATA ###"
    print "Category;Total_Bytes"
    for item in interesting_volume_list:
        total_bytes = int(item['values']['bytes out']) + int(item['values']['bytes in'])
        print item['name'] + ";" + str(total_bytes)

    ########## GATHERING GRAPH DATA
    # Gathering graph data per service category is a little more complex, as we have to know all the paths in advance.
    # As we already collected volume information and we have the Category information in there, we can use that data to
    # build the paths dinamically.
    
    print ""
    print "### CATEGORIES THROUGHPUT DATA ###"
    for item in interesting_volume_list:
        service_category = item['name']
        # The line below collects volume data from a given statistics path.
        # The "num_graph_points" variable below controls how many data points will be returned. Example: 96 datapoints for
        # a day correspond to one datapoint per 15 minutes. Setting this to 24 will lead to 1 datapoint per hour.
        num_graph_points = 24
        category_graph_data = stats_obj.graph(start_date, end_date, "/Subscribers?Statistics Object/All?NetObject/" + subscriber_id + "?NetObject/" + service_category + "?ServiceObject", numvals = num_graph_points, mode = stats_obj.GRAPH_MODE_SPEED, replymask = stats_obj.GRAPHFIELD_BPS_IN + stats_obj.GRAPHFIELD_BPS_OUT)

        print "Graph data for Category: " + item['name']
        for graph_item in category_graph_data:
            # Caveats: 
            # - The throughput data is returned in "bits per second", despite the name of the fields say "bytes";
            # - Some graph data may return "-1.0". This means data is unavailable in that time, and can be deemed as zero;
            # - Timestamp is in local time, not Zulu time.
            print "UNIX Timestamp: " + str(graph_item['timestamp']) + "; bitsPerSecond_IN: " + str(graph_item['bytes in']) + "; bitsPerSecond_OUT: " + str(graph_item['bytes out'])

        print ""

except packetlogic2.exceptions.PLDBError as err:
    print err

## EOF
