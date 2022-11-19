import pandas as pd

#CSV columns:
#event_name,block_number,txhash,log_index,timestamp,newAddress,amount,feeBasisPoints,maxFee,_user,_balance,_blackListedUser,contract_address
usdp_configs = pd.read_csv("../data/usdp_configs.csv")

print( usdp_configs.groupby(['event_name']).size() )

blacklists = usdp_configs.loc[usdp_configs.event_name=='AddedBlacklist']
unblacklists = usdp_configs.loc[usdp_configs.event_name=='RemovedBlacklist']

if 'msg.sender' in blacklists.columns:
	print( blacklists.groupby(['msg.sender']).size() )	
else:
	print( "The USDP events do *not* record the address that made the transaction." )
	print( "Run the script ../addSender.py and try again" )
