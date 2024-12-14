"""Testing for keyword module"""

from audio_case_grade import Case, count_keywords, get_keywords


def test_count_keywords():
    """Test count keywords function"""

    metrics = count_keywords(
        "This is a banana and apple test", ["banana", "apple", "kiwi"]
    )

    assert metrics is not None
    assert metrics.count == 2
    assert metrics.expected == 3
    assert metrics.sequence == {"banana": 11, "apple": 22, "kiwi": -1}
    assert metrics.used == ["banana", "apple"]


def test_get_keywords():
    """Test get keywords function"""

    text = "hello world chest pain two months fatigued ago"
    case = Case(
        code="I42.1",
        system="Cardiopulm",
        name="concentric left ventricular hypertrophy",
    )

    correct_soap, wrong_soap = get_keywords(text, case)

    assert correct_soap is not None
    assert correct_soap.totals.count == 3
    assert correct_soap.totals.expected == 52
    assert correct_soap.totals.word_count == 5

    assert wrong_soap is not None
    assert wrong_soap.totals.count == 0
    assert wrong_soap.totals.expected == 36
    assert wrong_soap.totals.word_count == 0
