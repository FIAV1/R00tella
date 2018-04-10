# R00tella

:books: Reti Peer To Peer - Università degli Studi di Ferrara :books:

A peer-to-peer server based on Gnutella's approach:

> ### Query flooding
> **Fully distributed**
>   * No central server
>   * Peers contact a few nodes to become neighbours
>   * Search: peers ask neighbors, who ask their neighbors
>   * Peers get files directly from other nodes
>
> ### Advantages
>   * Fully decentralized
>   * Search cost distributed
>   * Processing per node permits powerful search semantics
>
> ### Disadvantages
>   * Search scope may be quite large
>   * Search time may be quite long
>   * High overhead, and nodes come and go often

## Usage
```shell
python3 R00tella.py
```

Files to be shared must be put in the 'shared' folder. Files must be present at app's startup, otherwise they won't be managed.

**_Note:_** Python 3.6 or above is required

### Peer's supported commands:
[xxxB] = the parameter length in bytes
 
```shell
# Search a File
QUER[4B].Packet_Id[16B].IP_Peer[55B].Port_Peer[5B].TTL[2B].Research[20B]
# Server response will be
AQUE[4B].Packet_Id[16B].IP_Peer_j[55B].Port_Peer_j[5B].Filemd5[32B].Filename[100B]

# Search Neighbour
NEAR[4B].Packet_Id[16B].IP_Peer[55B].Port_Peer[5B].TTL[2B]
# Server response will be
ANEA[4B].Packet_Id[16B].IP_Peer_j[55B].Port_Peer_j[5B]

# Download a File
RETR[4B].Filemd5[32B]
# Server response will be
ARET[4B].\#chunk[3B].{Lenchunk_i[5B].data[LB]}(i=1..#chunk)
```

## Authors :rocket:
* [Federico Frigo](https://github.com/xBlue0)
* [Niccolò Fontana](https://github.com/NicFontana)
* [Giovanni Fiorini](https://github.com/GiovanniFiorini)
* [Marco Rambaldi](https://github.com/jhonrambo93)

Enjoy :sunglasses:
