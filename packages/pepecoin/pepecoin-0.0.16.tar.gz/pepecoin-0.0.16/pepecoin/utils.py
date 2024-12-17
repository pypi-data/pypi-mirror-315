
# import os
# import sys
# import time
# from pepecoin import Pepecoin
import logging

# Configure logging to display info messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def bring_account_from_address(pepecoin_node,address):
        try:
            addr_account = pepecoin_node.rpc_connection.getaccount(address)
            logger.info(f"getaccount('{address}') returned: {addr_account}")
            return addr_account
        except Exception as e:
            logger.error(f"Error calling getaccount('{address}'): {e}")

def bring_address_info(pepecoin_node, address):
        try:
            addr_info = pepecoin_node.rpc_connection.getaddressinfo(address)
            logger.info(f"getaddressinfo('{address}') returned: {addr_info}")
        except Exception as e:
            logger.warning("getaddressinfo RPC might not be supported. Error: %s", e)  




def bring_addresses_by_account(pepecoin_node, account_name) :
       

        try:
            source_acc_addresses = pepecoin_node.rpc_connection.getaddressesbyaccount(account_name)
            if account_name== "":
                logger.info(f"getaddressesbyaccount('{account_name}' -no name-) returned: {source_acc_addresses}")
            else:
           
                logger.info(f"getaddressesbyaccount('{account_name}') returned: {source_acc_addresses}")
            return source_acc_addresses

        except Exception as e:
            logger.error(f"Error calling getaddressesbyaccount('{account_name}'): {e}")


def get_all_addresses(pepecoin_node):
    """
    Retrieve all addresses known by the node and their total amount received.
    This includes addresses with zero balance, if any.
    Mark the first address for easy access later.
    """
    try:
        # listreceivedbyaddress( minconf, include_empty ) 
        # minconf=0: include all transactions, even unconfirmed
        # include_empty=True: include addresses that haven't received any payments
        addresses_info = pepecoin_node.rpc_connection.listreceivedbyaddress(0, True)
        logger.info(f"Total existing addresses result: {len(addresses_info)}")
        

        # addresses_grouped = pepecoin_node.rpc_connection.listaddressgroupings()
        # logger.info(f"listaddressgroupings result: {addresses_grouped}")
        
        
        all_addresses = {}
        first_address = None
        
        for i, info in enumerate(addresses_info):
            address = info['address']
            amount = float(info['amount'])
            
            try:
                account_name = pepecoin_node.rpc_connection.getaccount(address)
            except Exception as e:
                # If getaccount is not supported or fails, set None or a default
                account_name = None
                logger.warning(f"Error calling getaccount({address}): {e}")

            all_addresses[address] = amount
            
            logger.info(f"   Address {i}: {address} , Account {account_name} ,  Balance: {amount} $PEP")
            
            

        return all_addresses
    except Exception as e:
        logger.error(f"Failed to retrieve addresses: {e}")
        return {}