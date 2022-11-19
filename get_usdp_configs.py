"""
Scan the chain for all events for configuration events from the USDP contract
"""

api_url = 'http://127.0.0.1:8545' #Address of your Ethereum node
start_block = 6294931 #The scanner scans the chain from start_block to the end of the chain (start_block is set to the block where the USDT contract was deployed)
contract_address = "0x8E870D67F660D95d5be530380D0eC0bd388289E1"
outfile = "data/usdp_configs.csv" #Where to save the data
scanned_events = ["OwnershipTransferProposed","OwnershipTransferDisregarded","OwnershipTransferred","Pause","Unpause","AddressFrozen","AddressUnfrozen","FrozenAddressWiped","AssetProtectionRoleSet","SupplyIncreased","SupplyDecreased","SupplyControllerSet","BetaDelegatedTransfer","BetaDelegateWhitelisterSet","BetaDelegateWhitelisted","BetaDelegateUnwhitelisted"]

from tools.get_contract_events import getContractEvents

getContractEvents(api_url,start_block,contract_address,outfile,scanned_events)

