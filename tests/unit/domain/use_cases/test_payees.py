from ynab_cli.adapters.ynab import models
from ynab_cli.domain.use_cases import payees as use_cases


def test_should_skip_payee() -> None:
    assert use_cases.should_skip_payee(payee=models.Payee(id="", name="Payee", deleted=False)) is False
    assert use_cases.should_skip_payee(payee=models.Payee(id="", name="Payee", deleted=True)) is True

    assert use_cases.should_skip_payee(payee=models.Payee(id="", name="Transfer : Savings", deleted=False)) is True
    assert use_cases.should_skip_payee(payee=models.Payee(id="", name="Transfer : Savings", deleted=True)) is True

    assert use_cases.should_skip_payee(payee=models.Payee(id="", name="Starting Balance", deleted=False)) is True
    assert use_cases.should_skip_payee(payee=models.Payee(id="", name="Starting Balance", deleted=True)) is True

    assert use_cases.should_skip_payee(payee=models.Payee(id="", name="My Starting Balance", deleted=False)) is False
    assert use_cases.should_skip_payee(payee=models.Payee(id="", name="My Starting Balance", deleted=True)) is True


def test_normalize_name() -> None:
    assert use_cases.normalize_name("payee") == "Payee"
    assert use_cases.normalize_name("payee ") == "Payee"
    assert use_cases.normalize_name(" payee") == "Payee"
    assert use_cases.normalize_name(" payee ") == "Payee"
    assert use_cases.normalize_name("PAYEE.COM") == "Payee.com"
    assert use_cases.normalize_name("PAYEE.CA") == "Payee.ca"
    assert use_cases.normalize_name("PAyee's RestAurAnt") == "Payee's Restaurant"
    assert use_cases.normalize_name("Payee's \t Restaurant\t\t\n\rand Grill") == "Payee's Restaurant And Grill"
