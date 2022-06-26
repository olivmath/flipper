from ape.contracts.base import ContractInstance, ContractEvent
from ape_test import TestAccount


def test_flipper_is_contract(flipper: ContractInstance):
    assert flipper.is_contract == True

def test_flipper_initial(flipper: ContractInstance):
    assert flipper.flip() == True

def test_change_flip(flipper: ContractInstance, another: TestAccount):
    flipper.flipping(sender=another)
    assert flipper.flip() == False

def test_get_fliped_event(flipper: ContractInstance, another: TestAccount):
    def get_event(event: ContractEvent) -> dict:
        return list(
            tx.decode_logs(event)
        )[0].event_arguments

    tx = flipper.flipping(sender=another)
    assert {
        'state': False
    } == get_event(flipper.Fliped)
