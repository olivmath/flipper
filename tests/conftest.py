from ape.managers.project.manager import ProjectManager
from ape_test import TestAccount
from pytest import fixture

@fixture
def owner(accounts: TestAccount):
    return accounts[0]

@fixture
def another(accounts: TestAccount):
    return accounts[1]

@fixture
def flipper(project: ProjectManager, owner: TestAccount):
    return owner.deploy(project.Flipper)
