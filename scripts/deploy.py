def main():
    from ape import project, accounts

    owner = accounts.load("my_wallet")
    owner.deploy(project.Flipper)