"""Testing for keybank module"""

from pandas import DataFrame

from audio_case_grade import Case, get_keybank, get_keybank_csv


def test_keybank():
    """Test keybank function"""

    case = Case(
        code="I42.1",
        system="Cardiopulm",
        name="concentric left ventricular hypertrophy",
    )

    correct_keybank, wrong_keybank = get_keybank(case)

    assert correct_keybank is not None
    assert wrong_keybank is not None
    assert len(correct_keybank) == 15
    assert len(wrong_keybank) == 15


def test_get_keybank_for_abbreviations():
    """Test keybank for abbreviations"""

    case = Case(
        code="K80.00",
        system="GI",
        name="acute calculus cholecystitis",
    )

    correct_keybank, wrong_keybank = get_keybank(case)

    assert correct_keybank is not None
    assert wrong_keybank is not None
    assert correct_keybank.iloc[0] == ["abdominal pain"]
    assert "elevated white blood cells" in correct_keybank.iloc[7]
    assert wrong_keybank.iloc[0] == []


def test_get_keybank_for_contamination():
    """Test to ensure the wrong keybank doesn't contain the correct keywords"""

    case = Case(
        code="I25.2",
        system="Cardiopulm",
        name="ischemic cardiomyopathy",
    )

    correct_keybank, wrong_keybank = get_keybank(case)

    assert correct_keybank is not None
    assert wrong_keybank is not None
    assert sorted(correct_keybank.iloc[1]) == sorted(
        ["short breath", "six months", "physical activity"]
    )
    assert "nyha two" in wrong_keybank.iloc[9]
    assert "nyha four" not in wrong_keybank.iloc[9]
    assert "myocarditis dilated cardiomyopathy" in wrong_keybank.iloc[9]


def test_get_keybank_csv():
    """Test getting keybank csv"""

    csv = get_keybank_csv()

    assert csv is not None
    assert isinstance(csv, DataFrame)
