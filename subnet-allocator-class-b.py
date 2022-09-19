from pprint import pprint as pp
import ipaddress as ip
import pandas as pd

'''
Subnet Allocator - Class B
- Consider only assigning of subnets, doesn't merge (if possible) on deassignment

'''

print('######### Subnet Allocator - Class B #########')

# ip.IPv4Network('128.1.1.0/24')
# a = ip.ip_address('128.0.0.0')

def insertrow(df, row, index):
    # Inserting a Row at a Specific Index
    df.loc[index-0.5] = row
    df.sort_index(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return 

def closestlarger_index(df,x):
    avail = df[df.used==False]
    largest = avail[avail.wildcard>x].loc[:,'wildcard'].idxmin()
    return largest

def dosub(df,x):
    f = closestlarger_index(df,x)
    df.loc[f,'wildcard'] -= 1
    i = df.loc[f,'wildcard']
    while i>x:
        insertrow(df,[i-1,False,None,None,None,None],f)
        i -=  1
    insertrow(df,[x,True,None,None,None,None],f)
    return f


def addsub(df, x):
    # df = pd.DataFrame(columns=['wildcard','used'])
    if x<2:
        print('Cannot subnet for /1')
        return -1
    eq = df[(df.wildcard==x) & (df.used==False)]
    if eq.empty:
        gt = df[(df.wildcard>x) & (df.used==False)]
        if gt.empty:
            #cannot assign
            print("Cannot assign subnet")
            index = -1
        else:
            #need to subnet further
            index = dosub(df,x)
    else:
        #assign first from eq
        index = eq.iloc[0].name
        df.loc[index,'used'] = True
    
    # pp(df)
    return index

def userinput():
    
    name = input('Enter customer name : ')

    while True:
        netnumstr = input('Enter the required network address as [128-191].[0-255].0.0 : ')
        netaddr = ip.IPv4Address(netnumstr)
        oct = netnumstr.split('.')
        octets = [int(x) for x in oct]
        if (not (128<=octets[0]<192)) or (octets[2]!=0) or (octets[3]!=0):
            print('Network number is not a Class B network, try again')
            continue
        else:
            break

    return name,netaddr

def main():
    db = pd.DataFrame(columns=['name','numhosts','network'])


if __name__=='__main__':
    #df is database for the network
    #Changes in columns here need approriate changes in dosub rows
    df = pd.DataFrame(columns=['wildcard','used','netaddr','avail','req','name'])

    # #Test1
    # data = [{'wildcard': 2, 'used': True},
    #         {'wildcard': 2, 'used': False},
    #         {'wildcard': 3, 'used': False},
    #         {'wildcard': 4, 'used': False},
    #         {'wildcard': 5, 'used': False},
    #         {'wildcard': 6, 'used': False},
    #         {'wildcard': 7, 'used': False}]

    # #Test2
    # data = [ [2,  True],
    #          [2,  False],
    #          [3,  False],
    #          [4,  False],
    #          [8,  True],
    #          [9,  False],
    #          [10,  False] ]
    # for item in data[::-1]:  #reversing the data for adding with preserving order
    #     insertrow(df,[item[0],item[1]],0)
    #     # print(df)
    # df.wildcard = df.wildcard+10
    # df = dosub(df,15)

    #Test3
    insertrow(df,[16,False,None,None,None,None],0)

    name,netaddr = userinput()
    while True:
        req = int(input('Enter number of hosts required in the network [> 0]: '))
        wildcard = (req+1).bit_length()
        #adding 2 to req hosts to satisfy net and bcast addresses, -1 because 2ⁿ gives n+1 bits
        mask = 32 - wildcard
        avail = 2**wildcard-2

        index = addsub(df,wildcard)
        if index>=0:
            if index>=1:
                subaddr = netaddr + df.loc[:index-1,'wildcard'].apply(lambda x:2**x).sum()
            else:
                subaddr = netaddr
            df.loc[index,['name','netaddr','req','avail']] = [name,subaddr,req,avail]
            pp(df)
        else:
            print('Unable to subnet')
