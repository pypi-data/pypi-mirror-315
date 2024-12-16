import requests

class RPC:
  def __init__(self, rpc_url: str, auth = False, legacy = False):
    self.rpc_url = rpc_url
    self.auth = auth
    #if legacy is true, use 'pending' instead of receivable
    self.legacy = legacy
  #send rpc calls
  def call(self, payload):
    headers = {}
    #add auth header, if exists
    if self.auth:
      headers['Authorization'] = self.auth
    resp = requests.post(self.rpc_url, json=payload, headers=headers)
    #40x or 50x error codes returned, then there is a failure
    if resp.status_code >= 400:
      raise Exception("Request failed with status code "+str(resp.status_code))
    resp = resp.json()
    if "error" in resp:
      raise Exception("Node response: "+resp["error"])
    return resp
  """Network Informational RPC calls"""
  def get_block_count(self):
    return self.call({"action": "block_count"})
  def get_block_info(self, block: str):
    return self.call({"action": "block_info", "hash": block, "json_block": "true"})
  def get_blocks(self, blocks): #blocks: list[str]
    return self.call({"action": "blocks", "hashes": blocks, "json_block": "true"})
  def get_blocks_info(self, blocks): #blocks: list[str]
    return self.call({"action": "blocks_info", "hashes": blocks, "json_block": "true"})
  def get_representatives(self):
    return self.call({"action": "representatives"})
  def get_representatives_online(self):
    return self.call({"action": "representatives_online"})
  """Account Informational RPC calls"""
  def get_account_history(self, account: str, count: int = -1, head: str = None, account_filter = None, raw: bool = None, reverse: bool = None): #account_filter: list[str] = None
    payload = {
      "action": "account_history",
      "account": account,
      "count": str(count)
    }
    if head:
      payload["head"] = head
    if account_filter:
      payload["account_filter"] = account_filter
    if raw:
      payload["raw"] = raw
    if reverse:
      payload["reverse"] = reverse
    return self.call(payload)
  def get_account_info(self, account: str):
    return self.call({"action": "account_info", "account": account, "representative": "true"})
  def get_account_balance(self, account: str):
    return self.call({"action": "account_balance", "account": account})
  def get_account_representative(self, account: str):
    return self.call({"action": "account_representative", "account": account})
  def get_accounts_representatives(self, accounts): #accounts: list[str]
    return self.call({"action": "account_representatives", "accounts": accounts})
  def get_account_weight(self, account: str):
    return self.call({"action": "account_weight", "account": account})
  def get_receivable(self, account: str, count: int = 20, threshold = None):
    action_name = "receivable"
    if self.legacy:
      action_name = "pending"
    if threshold:
      return self.call({"action": action_name, "account": account, "count": str(count), "threshold": str(threshold)})
    else:
      return self.call({"action": action_name, "account": account, "count": str(count)})
  #todo: delegators, delegators_count, accounts_frontiers, account_block_count
  """Action RPC calls are provided by Wallet class in wallet.py, not here"""
