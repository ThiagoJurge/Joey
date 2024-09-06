from pyzabbix import ZabbixAPI

results = []


def get_bgp_items_by_asn(asn):

    host_list = [10706, 10530, 10532, 10528]
    keys_to_search = [
        "net.bgp.peer.status",
        "net.bgp.peer.prefixes.ipv4.received",
        "net.bgp.peer.prefixes.ipv4.advertised",
    ]

    # Connect to Zabbix API
    zabbix_server = "http://187.16.255.201/zabbix/"
    zapi = ZabbixAPI(
        zabbix_server,
        user="thiago.jurge@altarede.com.br",
        password="Ac82338a",
    )

    for host_id in host_list:
        # Loop over the keys and search items
        for key in keys_to_search:
            items = zapi.item.get(
                hostids=host_id,
                output="extend",
                search={"key_": key},
            )

            # Append retrieved items to the result list if ASN is in key
            for item in items:
                if asn in item["key_"]:  # Check if the ASN is in the key
                    result = (
                        f"Item ID: {item['itemid']}, Name: {item['name']}, "
                        f"Key: {item['key_']}, Value: {item['lastvalue']}"
                    )
                    results.append(result)

    # Logout from the API
    zapi._logout()

    return results


asn = "262739"  # Pass the ASN as a string

# Get BGP items filtered by ASN
bgp_items = get_bgp_items_by_asn(asn)

# Print the results
for item in bgp_items:
    print(item)
