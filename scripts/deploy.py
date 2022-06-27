def main():
    from ape.cli import get_user_selected_account
    from ape import project

    account = get_user_selected_account()
    account.deploy(project.Flipper)