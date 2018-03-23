# R00tella

:books: Reti Peer To Peer - Università degli Studi di Ferrara :books:

A peer-to-peer server based on Gnutella's approach

## Usage
```shell
python3 R00tella.py
```
**_Note:_** Python 3.6 or above is required

### Client's supported commands:
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

## To-Do
- [ ] Directory Server implementation
- [ ] Peer implementation

## Authors :rocket:
* [Federico Frigo](https://github.com/xBlue0)
* [Niccolò Fontana](https://github.com/NicFontana)
* [Giovanni Fiorini](https://github.com/GiovanniFiorini)
* [Marco Rambaldi](https://github.com/jhonrambo93)

Enjoy :sunglasses:
