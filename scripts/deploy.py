from os import O_WRONLY


def main():
    from ape import project, accounts

    owner = accounts.load("g")
    owner.deploy(project.Flipper)