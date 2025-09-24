import pytest
import math
import matlab
import numpy 
import pylab

class FakeEngine:
    """Tiny fake for matlab.engine.MatlabEngine that captures eval calls."""
    def __init__(self):
        self.eval_calls = []

    def eval(self, code, nargout=0):
        self.eval_calls.append((code, nargout))


def test_calls_matlab_soundsc_when_play_true():
    eng = FakeEngine()
    res = play_tone_matlab(freq=1000.0, duration=0.01, fs=8000, eng=eng, play=True)

    assert res["fs"] == 8000
    assert res["samples"] == 80  # round(0.01 * 8000)

    # Ensure we asked MATLAB to generate and play the tone.
    assert len(eng.eval_calls) == 1
    code, nargout = eng.eval_calls[0]
    assert "linspace" in code and "sin" in code and "soundsc" in code
    assert "fs=8000" in code and "f=1000.0" in code
    assert nargout == 0


def test_skips_matlab_when_play_false():
    eng = FakeEngine()
    res = play_tone_matlab(freq=440.0, duration=0.02, fs=8000, eng=eng, play=False)

    assert res["samples"] == 160
    assert eng.eval_calls == []  # no MATLAB call when play=False


@pytest.mark.parametrize(
    "freq,duration,fs",
    [
        (440.0, 0.5, 8000),
        (523.25, 0.1, 44100),
        (880.0, 0.005, 16000),
    ],
)
def test_sample_count_rounding(freq, duration, fs):
    eng = FakeEngine()
    res = play_tone_matlab(freq=freq, duration=duration, fs=fs, eng=eng, play=False)
    assert res["samples"] == int(round(duration * fs))


@pytest.mark.parametrize(
    "freq,duration,fs,err",
    [
        (0, 0.5, 8000, ValueError),
        (440, 0, 8000, ValueError),
        (440, 0.5, 0, ValueError),
        (-440, 0.5, 8000, ValueError),
    ],
)
def test_input_validation(freq, duration, fs, err):
    with pytest.raises(err):
        play_tone_matlab(freq=freq, duration=duration, fs=fs, eng=FakeEngine(), play=False)

#used to debug engine error
@pytest.mark.skipif(
    pytest.importorskip("matlab.engine", reason="MATLAB not available") is None,
    reason="MATLAB not available",
)  
def test_integration_matlab_engine_smoke():

    res = play_tone_matlab(freq=440.0, duration=0.01, fs=8000, eng=None, play=False)
    assert res["samples"] == 80