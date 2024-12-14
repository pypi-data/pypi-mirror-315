"""Testing for core module"""

from audio_case_grade import Case, Transcriber, Transcript, clean, get_score, hello


def test_hello():
    """Test hello function"""

    result = hello()

    assert result == "Welcome to audio-case-grade!"


def test_score_no_density():
    """Test score function with no lexical density"""

    raw_text = "this is text"
    mock_clean_text = raw_text
    transcript = Transcript(
        type=Transcriber.DEEPGRAM, raw=raw_text, clean=mock_clean_text
    )

    case = Case(
        code="I42.1",
        system="Cardiopulm",
        name="concentric left ventricular hypertrophy",
    )
    expected_lexical_density = 0.0

    actual_score = get_score(transcript, case)

    assert actual_score.lexical_density == expected_lexical_density


def test_score_with_density():
    """Test score function with an easy to calculate lexical density"""

    raw_text = "hello world chest pain two months fatigued ago"
    mock_clean_text = raw_text
    transcript = Transcript(
        type=Transcriber.DEEPGRAM,
        raw=raw_text,
        clean=mock_clean_text,
    )
    case = Case(
        code="I42.1",
        system="Cardiopulm",
        name="concentric left ventricular hypertrophy",
    )
    expected_lexical_density = 62.5

    actual_score = get_score(transcript, case)

    assert actual_score.lexical_density == expected_lexical_density


def test_score_with_clean():
    """Test score function"""

    raw_text = "hello world chest pain two months fatigued ago"
    transcript = Transcript(type=Transcriber.DEEPGRAM, raw=raw_text)
    transcript = clean(transcript)
    case = Case(
        code="I42.1",
        system="Cardiopulm",
        name="concentric left ventricular hypertrophy",
    )
    expected_lexical_density = 62.5

    actual_score = get_score(transcript, case)

    assert actual_score.lexical_density == expected_lexical_density
