# Python scripts for analyzing USDP on Ethereum

## USDP

USDP is a fiat-backed stablecoin issued by Paxos.  You can read about the off-chain reserves backing USDP at Paxos's [transparency](https://paxos.com/regulation-and-transparency/) page.
USDP is a token on the Ethereum blockchain, implemented as an ERC-20 contract, but USDP has significant additional functionality beyond the minimum specified by the [ERC-20 standard](https://ethereum.org/en/developers/docs/standards/tokens/erc-20/).

Paxos provides the [source code for the USDP contracts on github](https://github.com/paxosglobal/usdp-contracts).

This repository is provided to aid in analysis of the on-chain use of USDP.  
If you are considering *using* USDP, please read the [terms of service](https://paxos.com/stablecoin-terms-and-conditions/).

## Contract overview

The USDP contract is deployed at [0x8e870d67f660d95d5be530380d0ec0bd388289e1](https://etherscan.io/address/0x8e870d67f660d95d5be530380d0ec0bd388289e1)

The USDP contract is a "proxy" contract following the [OpenZeppelin proxy standard](https://docs.openzeppelin.com/contracts/4.x/api/proxy), this means that the 
functionality of the contract can be changed arbitrarily by the "owner".

The Owner is [0x0644Bd0248d5F89e4F6E845a91D15c23591e5D33](https://etherscan.io/address/0x0644Bd0248d5F89e4F6E845a91D15c23591e5D33).  
The Owner is itself a contract, in particular, the Owner is a [3](https://etherscan.io/address/0x0644Bd0248d5F89e4F6E845a91D15c23591e5D33#readContract#F1)-out-of-7 [Simple Multisig](https://github.com/christianlundkvist/simple-multisig) 
contract.

* [0x3eDD0d6562e9321Fb4a95e52576eE7f0b5Aa017e](https://etherscan.io/address/0x3eDD0d6562e9321Fb4a95e52576eE7f0b5Aa017e)
* [0x5d21C8C9dD0692bdEb7AC1A3fB24DFC3500E4c3e](https://etherscan.io/address/0x5d21C8C9dD0692bdEb7AC1A3fB24DFC3500E4c3e)
* [0x61efB23a6868a74A8DFE32651361a6165F6f173E](https://etherscan.io/address/0x61efB23a6868a74A8DFE32651361a6165F6f173E)
* [0x6dC212f6610a34cDb4099e6E50B3178F0C7c980a](https://etherscan.io/address/0x6dC212f6610a34cDb4099e6E50B3178F0C7c980a)
* [0x868FB9D7618ab17ec5D023A8300031ac534ECF3a](https://etherscan.io/address/0x868FB9D7618ab17ec5D023A8300031ac534ECF3a)
* [0x9fCE35e475Fdd84DB06eEc4cbE65028d6F9C9d01](https://etherscan.io/address/0x9fCE35e475Fdd84DB06eEc4cbE65028d6F9C9d01)
* [0xb08B382f09029AB7cE3CD486540aed0ed62680E3](https://etherscan.io/address/0xb08B382f09029AB7cE3CD486540aed0ed62680E3)

The contract owners have changed [3 times](https://bloxy.info/txs/calls_sc/0x0644bd0248d5f89e4f6e845a91d15c23591e5d33?signature_id=1494288).
The current owners were [set in February 2022](https://etherscan.io/tx/0xb84579abb8df34672e5d1fcd57da30fec4fcf6900f63ce80ddd976c57e1d69f6), and since that time, they have *never* 
interacted with the contract.

The USDP contract is also "[Pausable](https://docs.openzeppelin.com/contracts/4.x/api/security#Pausable)", meaning that the owner can pause the contract at will.  In the context of 
USDP, pausing the contract prevents all transfers (including mints and burns).

## Tools

[get_usdp_configs.py](get_usdp_configs.py) Will scrape all "configuration" events from the USDP contract.  Specifically, it scans the Ethereum blockchain for the following events, 
and records them to [data/usdp_configs.csv](data/usdp_configs.csv).

The events emitted by the USDP contract (e.g. AddressFrozen, OwnershipTransferred etc) do *not* record the caller's address.  So we have to get that separately.
The script [add_sender.py](add_sender.py) adds a new column ("msg.sender") to [data/usdp_configs.csv](data/usdp_configs.csv).

The file [analysis/usdp_analysis.py](analysis/usdp_analysis.py) does some basic analytics, e.g. counting the number of mints and burns by minter address.

The file [analysis/usdp_frozen_funds.py](analysis/usdp_frozen_funds.py) looks at all the frozen addresses, and gets their USDP balance at the time of their freeze.

## Who's in charge?

There are three key roles that control all aspects of USDP.

* **[Owner](https://etherscan.io/address/0x0644Bd0248d5F89e4F6E845a91D15c23591e5D33)** - The owner can [pause](https://github.com/paxosglobal/usdp-contracts/blob/master/contracts/USDPImplementationV3.sol#L346) the contract, 
[change the AssetProtectionRole](https://github.com/paxosglobal/usdp-contracts/blob/master/contracts/USDPImplementationV3.sol#L368) and [change the SupplyController role](https://github.com/paxosglobal/usdp-contracts/blob/master/contracts/USDPImplementationV3.sol#L429).
* **[AssetProtectionRole](https://etherscan.io/address/0x0644Bd0248d5F89e4F6E845a91D15c23591e5D33)** - The AssetProtectionRole can [freeze](https://github.com/paxosglobal/usdp-contracts/blob/master/contracts/USDPImplementationV3.sol#L429) and [unfreeze](https://github.com/paxosglobal/usdp-contracts/blob/master/contracts/USDPImplementationV3.sol#L392)
addresses.
* **[SupplyController](https://etherscan.io/address/0xE25a329d385f77df5D4eD56265babe2b99A5436e)** - The SupplyController is in charge of [minting](https://github.com/paxosglobal/usdp-contracts/blob/master/contracts/USDPImplementationV3.sol#L445) and [burning](https://github.com/paxosglobal/usdp-contracts/blob/master/contracts/USDPImplementationV3.sol#L458) 
tokens.

This separation of roles is good security practice, and it is odd that competing stablecoins like USDC and USDT do not separate roles as cleanly.

### Minting

USDP calls the process of "minting" new tokens "increaseSupply."
Issuing new USDP is controlled by the "SupplyController" [0xE25a329d385f77df5D4eD56265babe2b99A5436e](https://etherscan.io/address/0xE25a329d385f77df5D4eD56265babe2b99A5436e).

The SupplyController is a contract (rather than an Externally Owned Account), but the source code for the contract has not been supplied to Etherscan, 
so we can only guess as to how it functions.

### Freezing

AssetProtectionRole [0x0644Bd0248d5F89e4F6E845a91D15c23591e5D33](https://etherscan.io/address/0x0644Bd0248d5F89e4F6E845a91D15c23591e5D33).  
Like the "owner" the AssetProtectionRole is a Simple Multisig contract.  In this case, however, it is a 3-out-of-9 multisig
controlled by the following addresses

* [0x3eDD0d6562e9321Fb4a95e52576eE7f0b5Aa017e](https://etherscan.io/address/0x3eDD0d6562e9321Fb4a95e52576eE7f0b5Aa017e)
* [0x5d21C8C9dD0692bdEb7AC1A3fB24DFC3500E4c3e](https://etherscan.io/address/0x5d21C8C9dD0692bdEb7AC1A3fB24DFC3500E4c3e)
* [0x3eDD0d6562e9321Fb4a95e52576eE7f0b5Aa017e](https://etherscan.io/address/0x3eDD0d6562e9321Fb4a95e52576eE7f0b5Aa017e)
* [0x61efB23a6868a74A8DFE32651361a6165F6f173E](https://etherscan.io/address/0x61efB23a6868a74A8DFE32651361a6165F6f173E)
* [0x3eDD0d6562e9321Fb4a95e52576eE7f0b5Aa017e](https://etherscan.io/address/0x3eDD0d6562e9321Fb4a95e52576eE7f0b5Aa017e)
* [0x6dC212f6610a34cDb4099e6E50B3178F0C7c980a](https://etherscan.io/address/0x6dC212f6610a34cDb4099e6E50B3178F0C7c980a)
* [0x868FB9D7618ab17ec5D023A8300031ac534ECF3a](https://etherscan.io/address/0x868FB9D7618ab17ec5D023A8300031ac534ECF3a)
* [0x9fCE35e475Fdd84DB06eEc4cbE65028d6F9C9d01](https://etherscan.io/address/0x9fCE35e475Fdd84DB06eEc4cbE65028d6F9C9d01)
* [0xb08B382f09029AB7cE3CD486540aed0ed62680E3](https://etherscan.io/address/0xb08B382f09029AB7cE3CD486540aed0ed62680E3)

To date, [2 accounts have been frozen](https://bloxy.info/txs/events_sc/0x8e870d67f660d95d5be530380d0ec0bd388289e1?signature_id=406756)

### Clawbacks

USDP implements "clawbacks" through the "[wipeFrozenAddress](https://github.com/paxosglobal/usdp-contracts/blob/master/contracts/USDPImplementationV3.sol#L403)" function.
As the name implies, Paxos only has the ability to remove funds from users that were previously frozen.  Thus a clawback is a two-step process, first the address 
must be frozen, and only then can the funds be removed.  This is not much of a barrier to clawbacks since both steps of the process are controlled by the same address (the AssetProtectionRole)
and both steps can be incorporated into a single transaction.
