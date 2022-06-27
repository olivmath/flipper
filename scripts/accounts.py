# todo: get a private key by cli args
def main():
    from eth_account.signers.local import LocalAccount
    from eth_account import Account

    random_wallet: LocalAccount = Account.create()

    print("✅ New random wallet created!")
    print(f"🔑 Private key: {random_wallet.privateKey.hex()}")
    print(f"📭 Address: {random_wallet.address}")