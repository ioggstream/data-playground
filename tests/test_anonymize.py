import re
from pathlib import Path

import pytest
from anonymization import (
    Anonymization,
    AnonymizerChain,
    EmailAnonymizer,
    NamedEntitiesAnonymizer,
    SimpleNamespace,
)
from faker.providers import BaseProvider

DATADIR = Path(__file__).parent / "data"


class ConstantProvider(BaseProvider):
    """A fake provider always returning the same CIE number."""

    def cie_provider(self):
        return "CA 00000 AB"


class CieAnonymizer:
    """
    Redact Identity card numbers using a constant value.
    """

    def __init__(self, anonymization: Anonymization) -> None:
        self.anonymization = anonymization
        self.anonymization.add_provider(ConstantProvider)
        self.id_regex = r"\b(CA\s*[0-9]{5}\s*[A-Z]{2})\b"

    def anonymize(self, text: str) -> str:
        return self.anonymization.regex_anonymizer(text, self.id_regex, "cie_provider")


class IbanAnonymizer:
    """
    Replace all credit card numbers
    """

    def __init__(self, anonymization: Anonymization):
        self.anonymization = anonymization
        # matches an IBAN with optional spaces
        self.iban_regex = r"([A-Z]{2}[0-9]{2}[A-Z0-9]{11,23})"

    def anonymize(self, text: str) -> str:
        return self.anonymization.regex_anonymizer(text, self.iban_regex, "iban")

    def evaluate(self, text: str) -> str:
        matchs = re.finditer(self.iban_regex, text)
        ents = [
            SimpleNamespace(
                start=m.start(), end=m.end(), entity_type="IBAN_CODE", score=1
            )
            for m in matchs
        ]
        return ents


def ensure_utf8(fpath: Path):
    try:
        text = fpath.read_text()
    except UnicodeDecodeError:
        text = fpath.read_text(encoding="utf-16")
        fpath.write_text(text, encoding="utf-8")




@pytest.mark.parametrize(
    "name,fpath,needles",
    [[f.name, f, ("IT12A3456789012345678901234",)] for f in DATADIR.glob("**/*.txt")],
)
def test_iban(
    name,
    fpath,
    needles,
):
    anonymized_text = harn_anonymizer(name, fpath, IbanAnonymizer)
    assert all(name not in anonymized_text for name in needles)


@pytest.mark.parametrize(
    "name,fpath,needles", [[f.name, f, ("CA12345BB",)] for f in DATADIR.glob("**/*.txt")]
)
def test_cie(
    name,
    fpath,
    needles,
):
    anonymized_text = harn_anonymizer(name, fpath, CieAnonymizer)
    assert all(name not in anonymized_text for name in needles)


@pytest.mark.parametrize(
    "name,fpath,needles",
    [[f.name, f, ("luca.bianchi@example.com",)] for f in DATADIR.glob("**/*.txt")],
)
def test_email(
    name,
    fpath,
    needles,
):
    anonymized_text = harn_anonymizer(name, fpath, EmailAnonymizer)
    assert all(name not in anonymized_text for name in needles)


@pytest.mark.parametrize(
    "name,fpath,needles",
    [[f.name, f, ("Rossi", "Luca", "Bianchi")] for f in DATADIR.glob("**/*.txt")],
)
def test_name(name, fpath, needles):
    anonymized_text = harn_anonymizer(
        name, fpath, NamedEntitiesAnonymizer("en_core_web_lg")
    )
    assert all(name not in anonymized_text for name in needles)


def harn_anonymizer(name, fpath, addon):
    ensure_utf8(fpath)
    anon = AnonymizerChain(Anonymization("it_IT"))
    anon.add_anonymizers(addon)

    text = fpath.read_text()
    # When I anonymize the text
    anonymized_text = anon.anonymize(text)

    # Then the text is different from the original
    assert anonymized_text != text
    return anonymized_text

@pytest.mark.parametrize("name,fpath", [[f.name, f] for f in DATADIR.glob("**/*.txt")])
def test_chain(name, fpath):
    ensure_utf8(fpath)
    anon = AnonymizerChain(Anonymization("it_IT"))

    chain = (
        IbanAnonymizer,
        EmailAnonymizer,
        NamedEntitiesAnonymizer("en_core_web_lg"),
    )
    anon.add_anonymizers(chain)
    raise NotImplementedError
