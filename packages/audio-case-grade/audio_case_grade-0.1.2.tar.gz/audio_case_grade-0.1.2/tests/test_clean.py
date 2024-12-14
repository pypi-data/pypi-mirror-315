"""Tests for the clean module."""

from pandas import DataFrame

from audio_case_grade import Transcriber, Transcript, clean, get_abbreviations_csv


def test_clean():
    """Test clean function"""

    text = "This is the raw transcript"
    transcript = Transcript(type=Transcriber.DEEPGRAM, raw=text)
    expected_cleaned_text = "This raw transcript"

    cleaned_transcript = clean(transcript)

    assert cleaned_transcript.clean == expected_cleaned_text


def test_get_abbreviations_csv():
    """Test getting abbreviations csv"""

    csv = get_abbreviations_csv()

    assert csv is not None
    assert isinstance(csv, DataFrame)
