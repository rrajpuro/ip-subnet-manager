# ***IP Subnet Manager***
Python program to assign first available IPv4 subnets given a network address and number of hosts

Designed for Class B network subnetting
# Requirements

  * Python 3.7
  * Pandas 1.1


# Sample Execution & Output

Run using command prompt,

```
python ./subnet-allocator-class-b.py
```
Prompting user input
```
######### Subnet Allocator - Class B #########
Enter customer name : NC State
Enter the required network address as [128-191].[0-255].0.0 : 152.1.0.0
Enter number of hosts required in the network [> 0]: 4095
```

output *simliar* to

```
   wildcard   used    netaddr avail   req      name
0        13   True  152.1.0.0  8190  4095  NC State
1        13  False       None  None  None      None
2        14  False       None  None  None      None
3        15  False       None  None  None      None
```
1. `wildcard` column is the number of bits used for the network assignment
2. `used` column indicates if the subnet is assigned or available
3. `netaddr` column is the network address for a particular subnet
4. `avail` column is the total number of IPv4 addresses available
5. `req` column is the number of IPv4 addresses required
6. `name` column is the identifier used for a specific customer  

<br/>

> ***Note:** Subnet mask, usable address range, broadcast address and other trivial details have been ommited for concision.*  

<br/>

# Example
Continuing from the initial sample the program recursively asks for required hosts on next input as follows,
```
Enter number of hosts required in the network [> 0]: 16382
```
Output is as follows,
```
   wildcard   used     netaddr  avail    req      name
0        13   True   152.1.0.0   8190   4095  NC State
1        13  False        None   None   None      None
2        14   True  152.1.64.0  16382  16382  NC State
3        15  False        None   None   None      None
```
Next iteration,
```
Enter number of hosts required in the network [> 0]: 2000 
   wildcard   used     netaddr  avail    req      name
0        13   True   152.1.0.0   8190   4095  NC State
1        11   True  152.1.32.0   2046   2000  NC State
2        11  False        None   None   None      None
3        12  False        None   None   None      None
4        14   True  152.1.64.0  16382  16382  NC State
5        15  False        None   None   None      None
```
Further,
```
Enter number of hosts required in the network [> 0]: 4000
   wildcard   used     netaddr  avail    req      name
0        13   True   152.1.0.0   8190   4095  NC State
1        11   True  152.1.32.0   2046   2000  NC State
2        11  False        None   None   None      None
3        12   True  152.1.48.0   4094   4000  NC State
4        14   True  152.1.64.0  16382  16382  NC State
5        15  False        None   None   None      None
```
```
Enter number of hosts required in the network [> 0]: 2022
   wildcard   used     netaddr  avail    req      name
0        13   True   152.1.0.0   8190   4095  NC State
1        11   True  152.1.32.0   2046   2000  NC State
2        11   True  152.1.40.0   2046   2022  NC State
3        12   True  152.1.48.0   4094   4000  NC State
4        14   True  152.1.64.0  16382  16382  NC State
5        15  False        None   None   None      None
```
# Error handling
Case 1: Network address is not in Class B
```
######### Subnet Allocator - Class B #########
Enter customer name : NC State
Enter the required network address as [128-191].[0-255].0.0 : 192.168.0.0
Network number is not a Class B network, try again
```
Case 2: Cannot satisfy host requirements for subnets
```
######### Subnet Allocator - Class B #########
Enter customer name : NCSU 
Enter the required network address as [128-191].[0-255].0.0 : 128.0.0.0
Enter number of hosts required in the network [> 0]: 30000
   wildcard   used    netaddr  avail    req  name
0        15   True  128.0.0.0  32766  30000  NCSU
1        15  False       None   None   None  None
Enter number of hosts required in the network [> 0]: 40000
Cannot assign subnet
Unable to subnet
```
