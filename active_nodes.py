def active_nodes(c,d):
   #find which nodes are active

    k_active = [];
    for n in  range(len(c)):
        k_active += [c[n][:d[n]]]; # go only till the depth for each cluster. and pick the unique nodes(objects), max no of clusters=objects
    				   #check [:d[n]] vs [:] 
    k_active = set(k_active);


