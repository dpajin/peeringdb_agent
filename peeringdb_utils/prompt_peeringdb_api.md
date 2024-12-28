## PeeringDB overview
PeeringDB was set up to facilitate peering between networks and peering coordinators. The database is no longer just for peering and peering related information. It now includes all types of interconnection data for networks, clouds, services, and enterprise, as well as interconnection facilities that are developing at the edge of the Internet.
PeeringDB exists to facilitate the exchange of user-maintained interconnection related information. This information is presented in data relating to entities known as Organizations, Facilities, Internet Exchanges, and Networks in the Internet industry. Derived from that is data relating to where Networks and IXs are located, and to which IXs, Networks are connected to.

### Organizations 
Organization refers to the holding entity for any number of IXs, Facilities, and Networks. They are denoted by "org" data elements.

### Facilities 
Facility records data centers which are public centralized locations where computing and networking equipment of tenants are located, and may include one or more meet-me-rooms. A Facility may also simply be a public meet-me-room for interconnection. Facilities can house IXs and Networks, and these entities can establish interconnection. 
They are denoted by "fac" data elements and referenced in "ixfac" and "netfac" data elements. 
The major information among Facility records:
- org: The relevant Organization managing the Facility
- ixfac: IXs at the Facility
- netfac: Networks at the Facility

### Internet Exchanges 
Internet Exchange, also known as an Internet Exchange Point, refers to a network facility that enables the interconnection of more than two independent Autonomous Systems, primarily for the purpose of facilitating the exchange of Internet traffic. 
PeeringDB provides methods for both IXs and Networks to indicate the participation of a network at an IX. IXs may be present at one or more Facilities. 
IXs are denoted by "ix" data elements and referenced in "ixfac", "ixlan", "ixpfx", and "netixlan" data elements. 
The major information among IX records:
- org: The relevant Organization managing the IX.
- ixlan: Local Area Networks (LANs) (MTU and VLAN details) of IXs.
- ixpfix: LANs (IPv4 and IPv6 subnets) of IXs.
- netixlan: Networks at the IX and the specific IP addresses assigned to each participant.
- ixfac: Facilities the IX is present at.

### Networks
Entities with an Autonomous System Number (ASN) may be a Network in PeeringDB. 
They are denoted by "net" data elements and referenced in "as_set", "netfac", and "netixlan" data elements. 
The major information among Network records:
- org: The relevant Organization managing the Network
- poc: Contact Information
- netixlan: Connection detail at an IX
- netfac: Facilities the Network is present at

### Points of Contact 
Refers to a Network role along with optional name, email, and telephone information. 
They are denoted by "poc" data elements

### Public Peering Exchange Points 
A Network may have a list of Public Peering Exchange Points that it is connected to, along with IP address assignments, speed, and route server peer status. 
They are denoted by "netixlan" data elements. 

### Private Peering Facilities 
A Network may have a list of Private Peering Facilities it is present at. 
They are denoted by "netfac" data elements.

### LAN 
Each Internet Exchange has a LAN with a configuration for the name, MTU, whether IEEE 802.1Q is supported, and IX-F Member Import details. 
They are denoted by "ixlan" data elements.

### Prefixes
Each Internet Exchange has one or more Prefixes which represent an IPv4 or IPv6 subnet at the IX. 
They are denoted by "ixpfx" data elements.

### Local Facilities and Exchanges
Each Internet Exchange may have a list of Local Facilities it is present at, while each Facility may have a list of Internet Exchanges, or simply Exchanges, it hosts.
They are denoted by "ixfac" data elements.


## PeeringDB API information

### Requests
The URL base appended with `/api/`, append with object type and optionally object primary key
Object type is not case sensitive.
For example: `https://www.peeringdb.com/api/"OBJ"/"id"

### GET Operations

#### GET multiple objects
Used for list API endpoints to retrieve multiple or single objects
These API endpoints should be used for search for certain objects.
Since the resulting list can be quite large, it is necessary to use these endpoints to limit the output. 
Hence first use these endpoints with showing only "id" and "name" fields, to get the initial set of the results. With only these two fields, you can make queries with "limit" up to 1000 results. Once you are sure that the result scope of the objects is smaller and more narrow and you want to include more fields, you can use "limit" up to 100 results, with "depth" 1. If you want to use depth of 2, you must "limit" the result set to 20 objects, or retrieve details using single object endpoints. 
Once you detect the objects of interest, use this or "single object" endpoints to get all other required details about the object, once you are sure that the result scope is smaller. 

endpoint: GET `/api/OBJ`

optional URL parameters
- limit `int` limits rows in the result set
- skip `int` skips n rows in the result set
- depth `int` nested sets will be loaded (slow)
- fields `str` comma separated list of field names - only matching fields will be returned in the data
- since `int` retrieve all objects updated since specified time (unix timestamp, seconds)
- [field_name] `int|string` queries for fields with matching value

returns: array of objects

##### Nested data
Any field ending in the suffix `_set` (with the exception of `irr_as_set`) is a list of objects in a relationship with the parent object, you can expand those lists with the 'depth' parameter as explained below.
The naming schema of the field will always tell you which type of object the set is holding and will correspond with the object's endpoint on the API

```
<object_type>_set
```

So a set called 'net_set' will hold Network objects (API endpoint /net)
Unlike GET single, 'depth' here will **ONLY** expand sets, no single relationships will be expanded - this is by design
Possible `depth` values:
- 0: don't expand anything (default)
- 1: expand all first level sets to ids
- 2: expand all first level sets to objects

Query endpoint examples:

- using depth: `/api/OBJ?depth=2`
- exact match: `/api/OBJ?name=something`
- query modifier match: `/api/OBJ?name__contains=something`

##### Query modifiers
Query modifiers are used to advanced query of the fields. Different modifiers are allowed of different field types.
Based on the field type, you can determine which query modifiers are applicable for that field. 
Query modifiers are added on the field name to achieve required filtering.

For numeric fields (integer and date-time):
- `__lt`, less than
- `__lte`, less than equal
- `__gt`, greater than
- `__gte`, greater than equal
- `__in`, value inside set of values (comma separated)

For string fields:
- `__contains`, field value contains this value
- `__startswith`, field value starts with this value
- `__in`, value inside set of values (comma separated)

For Country filtering:
- Any country related field uses values which are two-letter country codes. Any country related field can be filtered the same way as strings. 

For Region or Continent filtering:
- for filtering by continent or region, use `region_continent` field where applicable, which can have the following possible values: North America, Asia Pacific, Europe, South America, Africa, Australia, Middle East

Examples:
- string filter: `/api/OBJ?name__contains=ams`
- string filter: `/api/OBJ?name__startswith=ams`
- integer filter: `/api/OBJ?id__in=12,345,5367`
- country filter: `/api/OBJ?country__in=US,NL,RS`

Since:
You can use the since argument with a unix timestamp (seconds) to retrieve all objects updated since then. Example: `/api/OBJ?since=1443414678`

#### GET: single object
For getting single object details using API, the endpoint must have `/id` after `/api/OBJ` part.
This is used to retrieve details of the single object, once object `id` is already known, after searching of the objects using multiple objects API endpoints.
When viewing a single object, generally it is not necessary to filter "fields" that should be shown over API, as the resulting data should be smaller.

endpoint: GET `/api/OBJ/id`

required URL parameters
1. id `int`

optional URL parameters
1. depth `int` defaults to 2 aka. nested sets and objects will be expanded
2. fields `str` comma separated list of field names - only matching fields will be returned in the data


## List of API endpoints 
The following is the list of API "OBJ" endpoints that can be used and their related fields for viewing and related fields that can be used for querying/filtering of the multiple objects API.

### fac
"fac" represents a Facility. Information such as the name, location, and website and org_id are contained within the "fac" data element.
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,org_id,org_name,org,campus_id,campus,name,aka,name_long,website,social_media,clli,rencode,npanxx,notes,net_count,ix_count,sales_email,sales_phone,tech_email,tech_phone,available_voltage_services,diverse_serving_substations,property,region_continent,status_dashboard,created,updated,status,address1,address2,city,country,state,zipcode,floor,suite,latitude,longitude

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
address1,string
address2,string
aka,string
available_voltage_services,string
campus,integer
campus__aka,string
campus__created,date-time
campus__id,integer
campus__name,string
campus__name_long,string
campus__notes,string
campus__status,string
campus__updated,date-time
campus__version,integer
campus__website,string
city,string
clli,string
country,string
created,date-time
depth,integer [ 0 .. 2 ]
diverse_serving_substations,boolean
floor,string
geocode_date,date-time
geocode_status,boolean
id,integer
ix_count,integer
latitude,number
limit,integer
longitude,number
name,string
name_long,string
net_count,integer
net_count,integer
notes,string
notified_for_geocoords,boolean
npanxx,string
org,integer
org__address1,string
org__address2,string
org__aka,string
org__city,string
org__country,string
org__created,date-time
org__email_domains,string
org__flagged,boolean
org__flagged_date,date-time
org__floor,string
org__geocode_date,date-time
org__geocode_status,boolean
org__id,integer
org__last_notified,date-time
org__name,string
org__name_long,string
org__notes,string
org__periodic_reauth,boolean
org__periodic_reauth_period,string
org__require_2fa,boolean
org__restrict_user_emails,boolean
org__state,string
org__status,string
org__suite,string
org__updated,date-time
org__version,integer
org__website,string
org__zipcode,string
page,integer
per_page,integer
property,string
region_continent,string
rencode,string
sales_email,string
sales_phone,string
since,integer
skip,integer
state,string
status,string
status_dashboard,string
suite,string
tech_email,string
tech_phone,string
updated,date-time
version,integer
website,string
zipcode,string
```

### carrier
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,org_id,org_name,org,name,aka,name_long,website,social_media,notes,carrierfac_set,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
aka,string
created,date-time
depth,integer [ 0 .. 2 ]
id,integer
limit,integer
name,string
name_long,string
notes,string
org,integer
org__address1,string
org__address2,string
org__aka,string
org__city,string
org__country,string
org__created,date-time
org__email_domains,string
org__flagged,boolean
org__flagged_date,date-time
org__floor,string
org__geocode_date,date-time
org__geocode_status,boolean
org__id,integer
org__last_notified,date-time
org__name,string
org__name_long,string
org__notes,string
org__periodic_reauth,boolean
org__periodic_reauth_period,string
org__require_2fa,boolean
org__restrict_user_emails,boolean
org__state,string
org__status,string
org__suite,string
org__updated,date-time
org__version,integer
org__website,string
org__zipcode,string
page,integer
per_page,integer
since,integer
skip,integer
status,string
updated,date-time
version,integer
website,string
```

### carrierfac
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,name,carrier_id,carrier,fac_id,fac,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
carrier,integer
carrier__aka,string
carrier__created,date-time
carrier__id,integer
carrier__name,string
carrier__name_long,string
carrier__notes,string
carrier__status,string
carrier__updated,date-time
carrier__version,integer
carrier__website,string
created,date-time
depth,integer [ 0 .. 2 ]
fac__address1,string
fac__address2,string
fac__aka,string
fac__available_voltage_services,string
fac__city,string
fac__clli,string
fac__country,string
fac__created,date-time
fac__diverse_serving_substations,boolean
fac__floor,string
fac__geocode_date,date-time
fac__geocode_status,boolean
fac__id,integer
fac__ix_count,integer
fac__latitude,number
fac__longitude,number
fac__name,string
fac__name_long,string
fac__net_count,integer
fac__notes,string
fac__notified_for_geocoords,boolean
fac__npanxx,string
fac__property,string
fac__region_continent,string
fac__rencode,string
fac__sales_email,string
fac__sales_phone,string
fac__state,string
fac__status,string
fac__status_dashboard,string
fac__suite,string
fac__tech_email,string
fac__tech_phone,string
fac__updated,date-time
fac__version,integer
fac__website,string
fac__zipcode,string
facility,integer
id,integer
limit,integer
page,integer
per_page,integer
since,integer
skip,integer
status,string
updated,date-time
version,integer
```


### ix
"ix" represents an Internet Exchange. Information such as the name, location, website, org_id and contact information are contained within the "ix" data element. 
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,org_id,org,name,aka,name_long,city,country,region_continent,media,notes,proto_unicast,proto_multicast,proto_ipv6,website,social_media,url_stats,tech_email,tech_phone,policy_email,policy_phone,sales_phone,sales_email,fac_set,ixlan_set,net_count,fac_count,ixf_net_count,ixf_last_import,ixf_import_request,ixf_import_request_status,service_level,terms,status_dashboard,created,updated,status,

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
aka,string
city,string
country,string
created,date-time
depth,integer [ 0 .. 2 ]
fac,number
fac_count,integer
id,integer
ixf_import_request,date-time
ixf_import_request_status,string
ixf_import_request_user,integer
ixf_import_request_user__created,date-time
ixf_import_request_user__date_joined,date-time
ixf_import_request_user__email,string
ixf_import_request_user__first_name,string
ixf_import_request_user__flagged_for_deletion,date-time
ixf_import_request_user__id,integer
ixf_import_request_user__is_active,boolean
ixf_import_request_user__is_staff,boolean
ixf_import_request_user__is_superuser,boolean
ixf_import_request_user__last_login,date-time
ixf_import_request_user__last_name,string
ixf_import_request_user__locale,string
ixf_import_request_user__never_flag_for_deletion,boolean
ixf_import_request_user__notified_for_deletion,date-time
ixf_import_request_user__password,string
ixf_import_request_user__primary_org,integer
ixf_import_request_user__status,string
ixf_import_request_user__updated,date-time
ixf_import_request_user__username,string
ixf_last_import,date-time
ixf_net_count,integer
ixfac,number
ixlan,number
limit,integer
media,string
name,string
name_long,string
net,number
net_count,integer
net_count,integer
notes,string
org,integer
org__address1,string
org__address2,string
org__aka,string
org__city,string
org__country,string
org__created,date-time
org__email_domains,string
org__flagged,boolean
org__flagged_date,date-time
org__floor,string
org__geocode_date,date-time
org__geocode_status,boolean
org__id,integer
org__last_notified,date-time
org__name,string
org__name_long,string
org__notes,string
org__periodic_reauth,booean
org__periodic_reauth_periold,string
org__require_2fa,boolean
org__restrict_user_emails,boolean
org__state,string
org__status,string
org__suite,string
org__updated,date-time
org__version,integer
org__website,string
org__zipcode,string
page,integer
per_page,integer
policy_email,string
policy_phone,string
proto_ipv6,boolean
proto_multicast,boolean
proto_unicast,boolean
region_continent,string
sales_email,string
sales_phone,string
service_level,string
since,integer
skip,integer
status,string
status_dashboard,string
tech_email,string
tech_phone,string
terms,string
updated,date-time
url_stats,string
version,integer
website,string
```


### ixfac
"ixfac" represents the presence of an Internet Exchange at a Facility. The "ixfac" data element includes an "ix_id", which points to an "ix" data element, which includes an "org_id".
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,name,city,country,ix_id,ix,fac_id,fac,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
created,date-time
depth,integer [ 0 .. 2 ]
fac__address1,string
fac__address2,string
fac__aka,string
fac__available_voltage_services,string
fac__city,string
fac__clli,string
fac__country,string
fac__created,date-time
fac__diverse_serving_substations,boolean
fac__floor,string
fac__geocode_date,date-time
fac__geocode_status,boolean
fac__id,integer
fac__ix_count,integer
fac__latitude,number
fac__longitude,number
fac__name,string
fac__name_long,string
fac__net_count,integer
fac__notes,string
fac__notified_for_geocoords,boolean
fac__npanxx,string
fac__property,string
fac__region_continent,string
fac__rencode,string
fac__sales_email,string
fac__sales_phone,string
fac__state,string
fac__status,string
fac__status_dashboard,string
fac__suite,string
fac__tech_email,string
fac__tech_phone,string
fac__updated,date-time
fac__version,integer
fac__website,string
fac__zipcode,string
facility,integer
id,integer
ix,integer
ix__aka,string
ix__city,string
ix__country,string
ix__created,date-time
ix__fac_count,integer
ix__id,integer
ix__ixf_import_request,date-time
ix__ixf_import_request_status,string
ix__ixf_last_import,date-time
ix__ixf_net_count,integer
ix__media,string
ix__name,string
ix__name_long,string
ix__net_count,integer
ix__notes,string
ix__policy_email,string
ix__policy_phone,string
ix__proto_ipv6,boolean
ix__proto_multicast,boolean
ix__proto_unicast,boolean
ix__region_continent,string
ix__sales_email,string
ix__sales_phone,string
ix__service_level,string
ix__status,string
ix__status_dashboard,string
ix__tech_email,string
ix__tech_phone,string
ix__terms,string
ix__updated,date-time
ix__url_stats,string
ix__version,integer
ix__website,string
limit,integer
page,integer
per_page,integer
since,integer
skip,integer
status,string
updated,date-time
version,integer
```

### ixlan
"ixlan" represents some aspects of an Internet Exchange LAN such as the name, MTU, whether IEEE 802.1Q is supported, and IX-F Member Import details. It also points to the "ix" data element.
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,ix_id,ix,name,descr,mtu,dot1q_support,rs_asn,arp_sponge,net_set,ixpfx_set,ixf_ixp_member_list_url,ixf_ixp_member_list_url_visible,ixf_ixp_import_enabled,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
arp_sponge,string
created,date-time
depth,integer [ 0 .. 2 ]
descr,string
dot1q_support,boolean
id,integer
ix,integer
ix__aka,string
ix__city,string
ix__country,string
ix__created,date-time
ix__fac_count,integer
ix__id,integer
ix__ixf_import_request,date-time
ix__ixf_import_request_status,string
ix__ixf_last_import,date-time
ix__ixf_net_count,integer
ix__media,string
ix__name,string
ix__name_long,string
ix__net_count,integer
ix__notes,string
ix__policy_email,string
ix__policy_phone,string
ix__proto_ipv6,boolean
ix__proto_multicast,boolean
ix__proto_unicast,boolean
ix__region_continent,string
ix__sales_email,string
ix__sales_phone,string
ix__service_level,string
ix__status,string
ix__status_dashboard,string
ix__tech_email,string
ix__tech_phone,string
ix__terms,string
ix__updated,date-time
ix__url_stats,string
ix__version,integer
ix__website,string
ixf_ixp_import_enabled,boolean
ixf_ixp_import_error,string
ixf_ixp_import_error_notified,date-time
ixf_ixp_import_protocol_conflict,integer
ixf_ixp_member_list_url,string
ixf_ixp_member_list_url_visible,string
limit,integer
mtu,integer
name,string
page,integer
per_page,integer
rs_asn,integer
since,integer
skip,integer
status,string
updated,date-time
version,integer
vlan,integer
```

### ixpfx
"ixpfx" represents the IP subnet of IP assignments on an Internet Exchange LAN. It also points to the associated "ixlan" data element. The "ixpfx" data element includes an "ixlan_id", which points to an "ixlan" data element, which includes an "ix_id", which points to an "ix" data element, which includes an "org_id".
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,ixlan,ixlan_id,protocol,prefix,in_dfz,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
created,date-time
depth,integer [ 0 .. 2 ]
id,integer
in_dfz,boolean
ix,number
ixlan,integer
ixlan__arp_sponge,string
ixlan__created,date-time
ixlan__dot1q_support,boolean
ixlan__id,integer
ixlan__ixf_ixp_import_enabled,boolean
ixlan__ixf_ixp_import_error,string
ixlan__ixf_ixp_import_error_notified,date-time
ixlan__ixf_ixp_import_protocol_conflict,integer
ixlan__ixf_ixp_member_list_url_visible,string
ixlan__mtu,integer
ixlan__name,string
ixlan__rs_asn,integer
ixlan__status,string
ixlan__updated,date-time
ixlan__version,integer
ixlan__vlan,integer
limit,integer
notes,string
page,integer
per_page,integer
prefix,string
protocol,string
since,integer
skip,integer
status,string
updated,date-time
version,integer
whereis,string
```

### net
"net" represents a Network. Information such as the name, website, ASN, as-set/route-set, prefix counts, type of network, tra?c ratios, policies, etc. are contained within the "net" data element. The "net" data element includes an "org_id".
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,org_id,org,name,aka,name_long,website,social_media,asn,looking_glass,route_server,irr_as_set,info_type,info_types,info_prefixes4,info_prefixes6,info_traffic,info_ratio,info_scope,info_unicast,info_multicast,info_ipv6,info_never_via_route_servers,ix_count,fac_count,notes,netixlan_updated,netfac_updated,poc_updated,policy_url,policy_general,policy_locations,policy_ratio,policy_contracts,netfac_set,netixlan_set,poc_set,allow_ixp_update,status_dashboard,rir_status,rir_status_updated,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
aka,string
allow_ixp_update,boolean
asn,integer
created,date-time
depth,integer [ 0 .. 2 ]
fac,number
fac_count,integer
id,integer
info_ipv6,boolean
info_multicast,boolean
info_never_via_route_servers,boolean
info_prefixes4,integer
info_prefixes6,integer
info_ratio,string
info_scope,string
info_traffic,string
info_types,string
info_unicast,boolean
irr_as_set,string
ix,number
ix_count,integer
ixlan,number
limit,integer
looking_glass,string
name,string
name_long,string
name_search,string
netfac,number
netfac_updated,date-time
netixlan,number
netixlan_updated,date-time
not_fac,number
not_ix,number
notes,string
notes_private,string
org,integer
org__address1,string
org__address2,string
org__aka,string
org__city,string
org__country,string
org__created,date-time
org__email_domains,string
org__flagged,boolean
org__flagged_date,date-time
org__floor,string
org__geocode_date,date-time
org__geocode_status,boolean
org__id,integer
org__last_notified,date-time
org__name,string
org__name_long,string
org__notes,string
org__periodic_reauth,boolean
org__periodic_reauth_period,string
org__require_2fa,boolean
org__restrict_user_emails,boolean
org__state,string
org__status,string
org__suite,string
org__updated,date-time
org__version,integer
org__website,string
org__zipcode,string
page,integer
per_page,integer
poc_updated,date-time
policy_contracts,string
policy_general,string
policy_locations,string
policy_ratio,boolean
policy_url,string
rir_status,string
rir_status_updated,date-time
route_server,string
since,integer
skip,integer
status,string
status_dashboard,string
updated,date-time
version,integer
website,string
```

### poc
"poc" represents a Point of Contact. The "poc" data element includes a "net_id", which points to an "net" data element, which includes an "org_id".
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,net_id,net,role,visible,name,phone,email,url,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
created,date-time
depth,integer [ 0 .. 2 ]
email,string
id,integer
limit,integer
name,string
net__aka,string
net__allow_ixp_update,boolean
net__asn,integer
net__created,date-time
net__fac_count,integer
net__id,integer
net__info_ipv6,boolean
net__info_multicast,boolean
net__info_never_via_route_servers,boolean
net__info_prefixes4,integer
net__info_prefixes6,integer
net__info_ratio,string
net__info_scope,string
net__info_traffic,string
net__info_types,string
net__info_unicast,boolean
net__irr_as_set,string
net__ix_count,integer
net__looking_glass,string
net__name,string
net__name_long,string
net__netfac_updated,date-time
net__netixlan_updated,date-time
net__notes,string
net__poc_updated,date-time
net__policy_contracts,string
net__policy_general,string
net__policy_locations,string
net__policy_ratio,boolean
net__policy_url,string
net__rir_status,string
net__rir_status_updated,date-time
net__route_server,string
net__status,string
net__status_dashboard,string
net__updated,date-time
net__version,integer
net__website,string
network,integer
page,integer
per_page,integer
phone,string
role,string
since,integer
skip,integer
status,string
updated,date-time
url,string
version,integer
visible,string
```

### netfac
"netfac" represents the presence of a Network at a Facility. This information can include the name of the Facility, the location, and the ASN employed by the Network at the location. The "netfac" data element includes a "net_id", which points to an "net" data element, which includes an "org_id".
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,name,city,country,net_id,net,fac_id,fac,local_asn,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
avail_atm,boolean
avail_ethernet,boolean
avail_sonet,boolean
city,string
country,string
created,date-time
depth,integer [ 0 .. 2 ]
fac__address1,string
fac__address2,string
fac__aka,string
fac__available_voltage_services,string
fac__city,string
fac__clli,string
fac__country,string
fac__created,date-time
fac__diverse_serving_substations,boolean
fac__floor,string
fac__geocode_date,date-time
fac__geocode_status,boolean
fac__id,integer
fac__ix_count,integer
fac__latitude,number
fac__longitude,number
fac__name,string
fac__name_long,string
fac__net_count,integer
fac__notes,string
fac__notified_for_geocoords,boolean
fac__npanxx,string
fac__property,string
fac__region_continent,string
fac__rencode,string
fac__sales_email,string
fac__sales_phone,string
fac__state,string
fac__status,string
fac__status_dashboard,string
fac__suite,string
fac__tech_email,string
fac__tech_phone,string
fac__updated,date-time
fac__version,integer
fac__website,string
fac__zipcode,string
facility,integer
id,integer
limit,integer
local_asn,integer
name,string
net__aka,string
net__allow_ixp_update,boolean
net__asn,integer
net__created,date-time
net__fac_count,integer
net__id,integer
net__info_ipv6,boolean
net__info_multicast,boolean
net__info_never_via_route_servers,boolean
net__info_prefixes4,integer
net__info_prefixes6,integer
net__info_ratio,string
net__info_scope,string
net__info_traffic,string
net__info_types,string
net__info_unicast,boolean
net__irr_as_set,string
net__ix_count,integer
net__looking_glass,string
net__name,string
net__name_long,string
net__netfac_updated,date-time
net__netixlan_updated,date-time
net__notes,string
net__poc_updated,date-time
net__policy_contracts,string
net__policy_general,string
net__policy_locations,string
net__policy_ratio,boolean
net__policy_url,string
net__rir_status,string
net__rir_status_updated,date-time
net__route_server,string
net__status,string
net__status_dashboard,string
net__updated,date-time
net__version,integer
net__website,string
network,integer
page,integer
per_page,integer
since,integer
skip,integer
status,string
updated,date-time
version,integer
```

### netixlan
"netixlan" represents the connection of a Network to an Internet Exchange, including the IP address assignments. The "netixlan" data element includes a "net_id", which points to an "net" data element, which includes an "org_id".
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,net_id,net,ix_id,name,ixlan_id,ixlan,notes,speed,asn,ipaddr4,ipaddr6,is_rs_peer,bfd_support,operational,net_side_id,ix_side_id,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
asn,integer
bfd_support,boolean
created,date-time
depth,integer [ 0 .. 2 ]
id,integer
ipaddr4,string
ipaddr6,string
is_rs_peer,boolean
ix_side,integer
ix_side__address1,string
ix_side__address2,string
ix_side__aka,string
ix_side__available_voltage_services,string
ix_side__city,string
ix_side__clli,string
ix_side__country,string
ix_side__created,date-time
ix_side__diverse_serving_substations,boolean
ix_side__floor,string
ix_side__geocode_date,date-time
ix_side__geocode_status,boolean
ix_side__id,integer
ix_side__ix_count,integer
ix_side__latitude,number
ix_side__longitude,number
ix_side__name,string
ix_side__name_long,string
ix_side__net_count,integer
ix_side__notes,string
ix_side__notified_for_geocoords,boolean
ix_side__npanxx,string
ix_side__property,string
ix_side__region_continent,string
ix_side__rencode,string
ix_side__sales_email,string
ix_side__sales_phone,string
ix_side__state,string
ix_side__status,string
ix_side__status_dashboard,string
ix_side__suite,string
ix_side__tech_email,string
ix_side__tech_phone,string
ix_side__updated,date-time
ix_side__version,integer
ix_side__website,string
ix_side__zipcode,string
ixlan,integer
ixlan__arp_sponge,string
ixlan__created,date-time
ixlan__dot1q_support,boolean
ixlan__id,integer
ixlan__ixf_ixp_import_enabled,boolean
ixlan__ixf_ixp_import_error,string
ixlan__ixf_ixp_import_error_notified,date-time
ixlan__ixf_ixp_import_protocol_conflict,integer
ixlan__ixf_ixp_member_list_url_visible,string
ixlan__mtu,integer
ixlan__name,string
ixlan__rs_asn,integer
ixlan__status,string
ixlan__updated,date-time
ixlan__version,integer
ixlan__vlan,integer
limit,integer
name,string
net__aka,string
net__allow_ixp_update,boolean
net__asn,integer
net__created,date-time
net__fac_count,integer
net__id,integer
net__info_ipv6,boolean
net__info_multicast,boolean
net__info_never_via_route_servers,boolean
net__info_prefixes4,integer
net__info_prefixes6,integer
net__info_ratio,string
net__info_scope,string
net__info_traffic,string
net__info_types,string
net__info_unicast,boolean
net__irr_as_set,string
net__ix_count,integer
net__looking_glass,string
net__name,string
net__name_long,string
net__netfac_updated,date-time
net__netixlan_updated,date-time
net__notes,string
net__poc_updated,date-time
net__policy_contracts,string
net__policy_general,string
net__policy_locations,string
net__policy_ratio,boolean
net__policy_url,string
net__rir_status,string
net__rir_status_updated,date-time
net__route_server,string
net__status,string
net__status_dashboard,string
net__updated,date-time
net__version,integer
net__website,string
net_side,integer
net_side__address1,string
net_side__address2,string
net_side__aka,string
net_side__available_voltage_services,string
net_side__city,string
net_side__clli,string
net_side__country,string
net_side__created,date-time
net_side__diverse_serving_substations,boolean
net_side__floor,string
net_side__geocode_date,date-time
net_side__geocode_status,boolean
net_side__id,integer
net_side__ix_count,integer
net_side__latitude,number
net_side__longitude,number
net_side__name,string
net_side__name_long,string
net_side__net_count,integer
net_side__notes,string
net_side__notified_for_geocoords,boolean
net_side__npanxx,string
net_side__property,string
net_side__region_continent,string
net_side__rencode,string
net_side__sales_email,string
net_side__sales_phone,string
net_side__state,string
net_side__status,string
net_side__status_dashboard,string
net_side__suite,string
net_side__tech_email,string
net_side__tech_phone,string
net_side__updated,date-time
net_side__version,integer
net_side__website,string
net_side__zipcode,string
network,integer
notes,string
operational,boolean
page,integer
per_page,integer
since,integer
skip,integer
speed,integer
status,string
updated,date-time
version,integer
```

### org
"org" represents an Organization. Information such as the name, website, and address are contained within the "org" data element.
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,name,aka,name_long,website,social_media,notes,require_2fa,net_set,fac_set,ix_set,carrier_set,campus_set,address1,address2,city,country,state,zipcode,floor,suite,latitude,longitude,created,updated,status

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
address1,string
address2,string
aka,string
asn,number
city,string
country,string
created,date-time
depth,integer [ 0 .. 2 ]
email_domains,string
flagged,boolean
flagged_date,date-time
floor,string
geocode_date,date-time
geocode_status,boolean
id,integer
last_notified,date-time
latitude,number
limit,integer
longitude,number
name,string
name_long,string
notes,string
page,integer
per_page,integer
periodic_reauth,boolean
periodic_reauth_period,string
require_2fa,boolean
restrict_user_emails,boolean
since,integer
skip,integer
state,string
status,string
suite,string
updated,date-time
version,integer
website,string
zipcode,string
```

### campus
List of fields applicable to view with this API OBJ, with multiple and single objects GET operations:
id,org_id,org_name,org,status,created,updated,name,name_long,notes,aka,website,social_media,fac_set,country,city,zipcode,state

CSV with query fields applicable for filtering with this API OBJ:
```csv
field,type
aka,string
created,date-time
depth,integer [ 0 .. 2 ]
id,integer
limit,integer
name,string
name_long,string
notes,string
org,integer
org__address1,string
org__address2,string
org__aka,string
org__city,string
org__country,string
org__created,date-time
org__email_domains,string
org__flagged,boolean
org__flagged_date,date-time
org__floor,string
org__geocode_date,date-time
org__geocode_status,boolean
org__id,integer
org__last_notified,date-time
org__name,string
org__name_long,string
org__notes,string
org__periodic_reauth,boolean
org__periodic_reauth_period,string
org__require_2fa,boolean
org__restrict_user_emails,boolean
org__state,string
org__status,string
org__suite,string
org__updated,date-time
org__version,integer
org__website,string
org__zipcode,string
page,integer
per_page,integer
since,integer
skip,integer
status,string
updated,date-time
version,integer
website,string
```

### as_set
"as_set" represents Internet Routing Registry (IRR) as-set/route-set from "net" data element.
This API OBJ returns the list of all available AS numbers and as-set names in case of getting multiple objects API.
For retrieveing only one AS number as-set name, use get single object API endpoint where id is AS number. 
