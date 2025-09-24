import math
import matlab


try:
    import matlab.engine  
except Exception:  
    _matlab_engine = None
else:
    _matlab_engine = matlab.engine


def _start_engine():
    """Start and return a MATLAB engine session."""
    if _matlab_engine is None:
        raise ImportError(
            "MATLAB Engine for Python not found. "
            "Install it per MathWorks instructions before running."
        )
    return _matlab_engine.start_matlab()


def play_tone_matlab(
    freq: float = 440.0,
    duration: float = 0.5,
    fs: int = 8000,
    *,
    eng=None,
    play: bool = True,
):
  
    if duration <= 0:
        raise ValueError("duration must be positive")
    if fs <= 0:
        raise ValueError("fs must be positive")
    if freq <= 0:
        raise ValueError("freq must be positive")

    engine = eng or _start_engine()
    n_samples = int(round(duration * fs))

    if play:
        # Do the entire operation in MATLAB for simplicity.
        engine.eval(
            f"fs={fs}; f={freq}; dur={duration}; "
            "t = linspace(0, dur, round(fs*dur)); "
            "y = sin(2*pi*f*t); "
            "soundsc(y, fs);",
            nargout=0,
        )

    return {"samples": n_samples, "fs": fs