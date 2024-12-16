import math

#region LibInfo
__lib__ = "libfilter"
__lib_creator__ = "radio95"
__lib_version__ = 1.0
__version__ = __lib_version__
#endregion LibInfo

#region Base classes
class StereoFilter:
    # 2 channels -> 2 channels
    def process(self, left: float, right: float) -> tuple:
        return left, right

class MonoFilter:
    # 1 channel -> 1 channel
    def process(self, audio: float) -> float:
        return audio

class SemiStereoFilter:
    # 2 channels -> 1 channel
    def process(self, left: float, right: float) -> float:
        return left

class SemiMonoFilter:
    # 1 channel -> 2 channels
    def process(self, audio: float) -> tuple:
        return audio, audio

class StereoOutput:
    # 0 channels -> 2 channels
    def process(self) -> tuple:
        return 0.0, 0.0

class MonoOutput:
    # 0 channels -> 1 channels
    def process(self) -> float:
        return 0.0

class Oscillator(MonoOutput):
    frequency = -1
    sample_rate = -1

class Modulator:
    def modulate(self, signal):
        return signal

class Demodulator:
    def demodulate(self, signal):
        return signal

class Encoder:
    def encode(self, signal):
        return -int(signal)

class Decoder:
    def decode(self, signal):
        return -int(signal)
#endregion Base classes

#region Audio Filters

#region Clippers
class MonoClipper(MonoFilter):
    """
    Limits incoming audio to -1.0 or 1.0
    """
    def process(self, audio: float):
        return (max(min(audio,1.0),-1.0))
class StereoClipper(StereoFilter):
    """
    Does the same thing as the mono version but stereo
    """
    def process(self, left: float, right: float):
        return (max(min(left,1.0),-1.0)), (max(min(right,1.0),-1.0)) 
class MonoDeclipper:
    """
    This does linear interpolation
    
    Can't do well Real-Time without some buffering
    """
    def __init__(self, threshold: float=1.0) -> None:
        self.threshold = threshold
    def process(self, prev_audio: float, current_audio: float, future_audio: float):
        if current_audio > self.threshold or current_audio < -self.threshold:
            # If the audio is clipped, restore it by linear interpolation
            return (prev_audio + future_audio) / 2
        else:
            # Limit the audio to the range [-1.0, 1.0]
            return max(min(current_audio, 1.0), -1.0)
class StereoDeclipper:
    """
    Stereo version of the mono one
    """
    def __init__(self, threshold: float=1.0) -> None:
        self.declipper_l = MonoDeclipper(threshold)
        self.declipper_r = MonoDeclipper(threshold)
    def process(self, prev_audio_l: float, prev_audio_r: float, current_audio_l: float, current_audio_r: float, future_audio_l: float, future_audio_r: float) -> tuple:
        return self.declipper_l.process(prev_audio_l, current_audio_l, future_audio_l), self.declipper_r.process(prev_audio_r, current_audio_r, future_audio_r)
#endregion Clippers

class StereoToMono(SemiStereoFilter):
    """
    Converts 2 channels into one using averaging ([a+b]/2)
    """
    def process(self, left: float, right: float):
        return ((left + right) / 2)

class MonoFadeOut(MonoFilter):
    """
    Makes a linear fade out
    """
    def __init__(self, duration: float, sample_rate: float, allow_negative_amplitude:bool=False):
        self.duration = duration
        self.sr = sample_rate
        self.decrement = None
        self.amplitude = 1.0
        self.reset()
        self.allow_negative_amplitude = allow_negative_amplitude
    def reset(self):
        self.decrement = 1/(self.sr*self.duration)
        self.amplitude = 1.0
    def process(self, audio: float) -> float:
        if not self.allow_negative_amplitude:
            self.amplitude = max(0.0, self.amplitude)
        sample = audio * self.amplitude
        self.amplitude -= self.decrement
        return sample
class StereoFadeOut(StereoFilter):
    def __init__(self, duration: float, sample_rate: float, allow_negative_amplitude:bool=True):
        self.fo_l = MonoFadeOut(duration, sample_rate, allow_negative_amplitude)
        self.fo_r = MonoFadeOut(duration, sample_rate, allow_negative_amplitude)
    def reset(self):
        self.fo_l.reset()
        self.fo_r.reset()
    def process(self, left:float, right: float) -> tuple[float,float]:
        return self.fo_l.process(left), self.fo_r.process(right)
class MonoFadeIn(MonoFilter):
    """
    Makes a linear fade in
    """
    def __init__(self, duration: float, sample_rate: float):
        self.duration = duration
        self.sr = sample_rate
        self.decrement = None
        self.amplitude = 0.0
        self.reset()
    def reset(self):
        self.decrement = 1/(self.sr*self.duration)
        self.amplitude = 0.0
    def process(self, audio: float) -> float:
        self.amplitude = min(1.0, self.amplitude)
        sample = audio * self.amplitude
        self.amplitude += self.decrement
        return sample
class StereoFadeIn(StereoFilter):
    def __init__(self, duration: float, sample_rate: float, dont_inverse:bool=True):
        self.fi_l = MonoFadeIn(duration, sample_rate, dont_inverse)
        self.fi_r = MonoFadeIn(duration, sample_rate, dont_inverse)
    def reset(self):
        self.fi_l.reset()
        self.fi_r.reset()
    def process(self, left:float, right: float) -> tuple[float,float]:
        return self.fi_l.process(left), self.fi_r.process(right)

#region Compressors
class StereoRpitxCompressor(StereoFilter):
    """
    This is the broadcast compressor that can be found in pifmrds
    """
    def __init__(self, attack: float, decay: float, mgr:float=0.01) -> None:
        self.lmax = 0.0
        self.rmax = 0.0
        self.attack = attack
        self.decay = decay
        self.mgr = mgr
    def process(self, left: float, right: float):
        l_abs = abs(left)
        if l_abs > self.lmax:
            self.lmax += (l_abs - self.lmax)*self.attack
        else:
            self.lmax *= self.decay
        r_abs = abs(right)
        if r_abs > self.rmax:
            self.rmax += (r_abs - self.rmax)*self.attack
        else:
            self.rmax *= self.decay
        if self.lmax > self.rmax: self.rmax = self.lmax
        elif self.rmax > self.lmax: self.lmax = self.rmax
        return left/(self.lmax+self.mgr), right/(self.rmax+self.mgr)
class MonoRpitxCompressor(MonoFilter):
    """
    This is the broadcast compressor that can be found in pifmrds but mono
    """
    def __init__(self, attack: float, decay: float, mgr:float=0.01) -> None:
        self.max = 0.0
        self.attack = attack
        self.decay = decay
        self.mgr = mgr
    def process(self, audio: float):
        a_abs = abs(audio)
        if a_abs > self.max:
            self.max += (a_abs - self.max)*self.attack
        else:
            self.max *= self.decay
        return audio/(self.max+self.mgr)
#endregion Compressors

#region Frequency Filters
class MonoExponentialLPF(MonoFilter):
    """
    A simple low-pass filter using exponential smoothing.
    
    Args:
        cutoff_frequency (float): The cutoff frequency in Hz.
        sampling_rate (float): The sampling rate in Hz.
    """
    def __init__(self, cutoff_frequency: float, sampling_rate: float):
        if cutoff_frequency <= 0 or sampling_rate <= 0:
            raise ValueError("cutoff_frequency and sampling_rate must be positive.")
        if cutoff_frequency >= sampling_rate / 2:
            raise ValueError("cutoff_frequency must be less than half the sampling rate (Nyquist limit).")
        self.cutoff_frequency = cutoff_frequency
        self.sampling_rate = sampling_rate
        # Calculate the smoothing factor (alpha)
        rc = 1 / (2 * math.pi * cutoff_frequency)  # Time constant (RC)
        self.alpha = sampling_rate / (sampling_rate + rc)  # Adjust for discrete sampling
        self.previous_output = None
    def process(self, audio: float):
        """
        Applies the low-pass filter to a single input sample.
        
        Args:
            audio (float): The input audio sample.
        
        Returns:
            float: The filtered output sample.
        """
        if self.previous_output is None:
            self.previous_output = audio  # Initialize with the first sample
        # Calculate the filtered output
        output_sample = self.alpha * audio + (1 - self.alpha) * self.previous_output
        self.previous_output = output_sample
        return output_sample
class StereoExponentialLPF(StereoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float) -> None:
        self.lpf_l = MonoExponentialLPF(cutoff_frequency, sampling_rate)
        self.lpf_r = MonoExponentialLPF(cutoff_frequency, sampling_rate)
    def process(self, left: float, right: float) -> tuple:
        return self.lpf_l.process(left), self.lpf_r.process(right)
class MonoExponentialHPF(MonoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float):
        if cutoff_frequency <= 0 or sampling_rate <= 0:
            raise ValueError("cutoff_frequency and sampling_rate must be positive.")
        if cutoff_frequency >= sampling_rate / 2:
            raise ValueError("cutoff_frequency must be less than half the sampling rate (Nyquist limit).")
            
        self.cutoff_frequency = cutoff_frequency
        self.sampling_rate = sampling_rate
        
        # Calculate the smoothing factor (alpha)
        rc = 1 / (2 * math.pi * cutoff_frequency)
        self.alpha = rc / (rc + 1/sampling_rate)
        
        self.previous_input = None
        self.previous_output = None

    def process(self, audio: float):
        if self.previous_input is None:
            self.previous_input = audio
            self.previous_output = 0
            return 0
        output_sample = self.alpha * (self.previous_output + audio - self.previous_input)
        
        self.previous_input = audio
        self.previous_output = output_sample
        
        return output_sample
class StereoExponentialHPF(StereoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float) -> None:
        self.hpf_l = MonoExponentialHPF(cutoff_frequency, sampling_rate)
        self.hpf_r = MonoExponentialHPF(cutoff_frequency, sampling_rate)
    def process(self, left: float, right: float) -> tuple:
        return self.hpf_l.process(left), self.hpf_r.process(right)
class MonoButterworthLPF(MonoFilter):
    def __init__(self, cutoff_freq: float, sample_rate: float, order: int = 2):
        super().__init__()
        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate
        self.order = order
        
        # Intermediate calculation values
        f = math.tan(math.pi * cutoff_freq / sample_rate)
        self.a = [0.0] * (order + 1)  # denominator coefficients
        self.b = [0.0] * (order + 1)  # numerator coefficients
        
        # Calculate coefficients for 2nd order sections
        if order == 2:
            # Prototype Butterworth polynomials for 2nd order
            q = math.sqrt(2.0)  # Q factor for Butterworth response
            
            # Bilinear transform coefficients
            ff = f * f
            self.b[0] = ff
            self.b[1] = 2.0 * ff
            self.b[2] = ff
            self.a[0] = 1.0 + (2.0 * f / q) + ff
            self.a[1] = 2.0 * (ff - 1.0)
            self.a[2] = 1.0 - (2.0 * f / q) + ff
            
            # Normalize coefficients
            for i in range(3):
                self.b[i] /= self.a[0]
            self.a[1] /= self.a[0]
            self.a[2] /= self.a[0]
            self.a[0] = 1.0
        
        # Initialize state variables for the filter
        self.x = [0.0] * (order + 1)  # input history
        self.y = [0.0] * (order + 1)  # output history
    
    def process(self, audio: float) -> float:
        # Shift the previous values
        for i in range(self.order, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        # Add new input
        self.x[0] = audio
        
        # Calculate new output
        self.y[0] = self.b[0] * self.x[0]
        for i in range(1, self.order + 1):
            self.y[0] += self.b[i] * self.x[i] - self.a[i] * self.y[i]
        
        return self.y[0]
    
    def reset(self):
        self.x = [0.0] * (self.order + 1)
        self.y = [0.0] * (self.order + 1)
class StereoButterworthLPF(StereoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float, order: int=2) -> None:
        self.lpf_l = MonoButterworthLPF(cutoff_frequency, sampling_rate, order)
        self.lpf_r = MonoButterworthLPF(cutoff_frequency, sampling_rate, order)
    def process(self, left: float, right: float) -> tuple:
        return self.lpf_l.process(left), self.lpf_r.process(right)
class MonoButterworthHPF(MonoFilter):
    def __init__(self, cutoff_freq: float, sample_rate: float, order: int = 2):
        super().__init__()
        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate
        self.order = order
        
        # Intermediate calculation values
        f = math.tan(math.pi * cutoff_freq / sample_rate)
        self.a = [0.0] * (order + 1)  # denominator coefficients
        self.b = [0.0] * (order + 1)  # numerator coefficients
        
        # Calculate coefficients for 2nd order sections
        if order == 2:
            # Prototype Butterworth polynomials for 2nd order
            q = math.sqrt(2.0)  # Q factor for Butterworth response
            
            # Bilinear transform coefficients
            ff = f * f
            self.b[0] = 1.0
            self.b[1] = -2.0
            self.b[2] = 1.0
            self.a[0] = 1.0 + (2.0 * f / q) + ff
            self.a[1] = 2.0 * (ff - 1.0)
            self.a[2] = 1.0 - (2.0 * f / q) + ff
            
            # Normalize coefficients
            for i in range(3):
                self.b[i] /= self.a[0]
            self.a[1] /= self.a[0]
            self.a[2] /= self.a[0]
            self.a[0] = 1.0
        
        # Initialize state variables for the filter
        self.x = [0.0] * (order + 1)  # input history
        self.y = [0.0] * (order + 1)  # output history
    
    def process(self, audio: float) -> float:
        # Shift the previous values
        for i in range(self.order, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        # Add new input
        self.x[0] = audio
        
        # Calculate new output
        self.y[0] = self.b[0] * self.x[0]
        for i in range(1, self.order + 1):
            self.y[0] += self.b[i] * self.x[i] - self.a[i] * self.y[i]
        
        return self.y[0]
    
    def reset(self):
        self.x = [0.0] * (self.order + 1)
        self.y = [0.0] * (self.order + 1)
class StereoButterworthHPF(StereoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float, order: int=2) -> None:
        self.hpf_l = MonoButterworthHPF(cutoff_frequency, sampling_rate, order)
        self.hpf_r = MonoButterworthHPF(cutoff_frequency, sampling_rate, order)
    def process(self, left: float, right: float) -> tuple:
        return self.hpf_l.process(left), self.hpf_r.process(right)
#endregion Frequency Filters

#region Emphasis
class MonoPreemphasis(MonoFilter):
    def __init__(self, microsecond_tau: float, sample_rate: float) -> None:
        tau_seconds = microsecond_tau / 1_000_000
        self.alpha = math.exp(-1 / (tau_seconds * sample_rate))
        self.prevsample = None
    def process(self, audio: float) -> float:
        if self.prevsample is None:
            self.prevsample = audio
            return audio
        sample = audio - self.alpha * self.prevsample
        self.prevsample = sample
        return sample
class StereoPreemphasis(StereoFilter):
    def __init__(self, microsecond_tau: float, sample_rate: float) -> None:
        self.filter_l = MonoPreemphasis(microsecond_tau, sample_rate)
        self.filter_r = MonoPreemphasis(microsecond_tau, sample_rate)
    def process(self, left: float, right: float) -> tuple:
        return self.filter_l.process(left), self.filter_r.process(right)
class MonoDeemphasis(MonoFilter):
    def __init__(self, microsecond_tau: float, sample_rate: float) -> None:
        tau_seconds = microsecond_tau / 1_000_000
        self.alpha = math.exp(-1 / (tau_seconds * sample_rate))
        self.prevsample = None
    def process(self, audio: float) -> float:
        if self.prevsample is None:
            self.prevsample = audio
            return audio
        sample = audio + self.alpha * self.prevsample
        self.prevsample = sample
        return sample
class StereoDeemphasis(StereoFilter):
    def __init__(self, microsecond_tau: float, sample_rate: float) -> None:
        self.filter_l = MonoDeemphasis(microsecond_tau, sample_rate)
        self.filter_r = MonoDeemphasis(microsecond_tau, sample_rate)
    def process(self, left: float, right: float) -> tuple:
        return self.filter_l.process(left), self.filter_r.process(right)
#endregion Emphasis
#endregion Audio Filters

#region Oscilators
class Sine(Oscillator):
    """
    Generates a sine wave of a selected frequency and sample rate, allowing dynamic frequency changes.
    """
    def __init__(self, frequency: float, sampling_rate: float) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate

    def process(self, phase_offset: float = 0.0) -> float:
        # Compute the sample
        sample = math.sin(self._phase + phase_offset)
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        return sample
class MultiSine(Oscillator):
    """
    Generates a sine wave of a selected frequency and sample rate, allowing dynamic frequency changes. Also returns harmonics
    """
    def __init__(self, frequency: float, sampling_rate: float, harmonics: int) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        self.harmonics = harmonics

    def process(self, phase_offset: float = 0.0) -> float:
        out = []
        # Compute the sample(s)
        for i in range(self.harmonics+1):
            out.append(math.sin((self._phase*(i+1)) + phase_offset))
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        return out
class SquareOscillator(Oscillator):
    """
    Generates a square wave of a selected frequency and sample rate, allowing dynamic frequency changes.
    """
    def __init__(self, frequency: float, sampling_rate: float) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate

    def process(self, phase_offset: float = 0.0) -> float:
        # Compute the sample
        sample = math.sin(self._phase + phase_offset)
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        # Convert sine wave into square wave
        sample = 1.0 if sample >= 0 else -1.0
        return sample
class MultiSquareOscillator(Oscillator):
    """
    Generates a square wave of a selected frequency and sample rate, allowing dynamic frequency changes. Also returns harmonics
    """
    def __init__(self, frequency: float, sampling_rate: float, harmonics: int) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        self.harmonics = harmonics

    def process(self, phase_offset: float = 0.0) -> float:
        out = []
        # Compute the sample(s)
        for i in range(self.harmonics+1):
            out.append(math.sin((self._phase*(i+1)) + phase_offset))
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        # Convert sine wave into square wave
        out = [1.0 if i >= 0 else -1.0 for i in out]
        return out
class Triangle(Oscillator):
    """
    Generates a triangle wave of a selected frequency and sample rate, allowing dynamic frequency changes.
    """
    def __init__(self, frequency: float, sampling_rate: float) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate

    def process(self, phase_offset: float = 0.0) -> float:
        # Compute the sample
        sample = math.sin(self._phase + phase_offset)
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        # Convert sine wave into triangle wave
        sample = (2 / math.pi) * math.asin(sample)
        return sample
class MultiTriangle(Oscillator):
    """
    Generates a triangle wave of a selected frequency and sample rate, allowing dynamic frequency changes. Also returns harmonics
    """
    def __init__(self, frequency: float, sampling_rate: float, harmonics: int) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        self.harmonics = harmonics

    def process(self, phase_offset: float = 0.0) -> float:
        out = []
        # Compute the sample(s)
        for i in range(self.harmonics+1):
            out.append(math.sin((self._phase*(i+1)) + phase_offset))
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        # Convert sine wave into triangle wave
        out = [(2 / math.pi) * math.asin(i) for i in out]
        return out
#endregion Oscilators

#region Modulators
class DSBSCModulator(Modulator):
    """
    DSB-SC modulator, in order to modulate DSB-SC you multiply the signal by the carrier, so c*s, i like to think of moving the center frequency, like you know the negative tones? yeah that becomes the lsb part
    """
    def __init__(self, frequency: float, sample_rate: float):
        self.osc = Sine(frequency, sample_rate)
    def modulate(self, signal: float) -> float:
        return self.osc.process()*signal
class AMModulator(Modulator):
    """
    AM modulator based on the DSB-SC modulator (only diffrence is that you have to add the carrier amplitude to your signal)
    """
    def __init__(self, carrier_wave_amplitude:float, frequency: float, sample_rate: float):
        if carrier_wave_amplitude < 0:
            raise ValueError("Carrier wave amplitude must be non-negative.")
        self.cwa = carrier_wave_amplitude
        self.dsbscmod = DSBSCModulator(frequency, sample_rate)
    def modulate(self, signal: float) -> float:
        return self.dsbscmod.modulate(self.cwa+signal)
class FMModulator(Modulator):
    """
    Simple FM Modulator
    """
    def __init__(self, frequency: float, deviation: float, sample_rate: float, deviation_limiter:int=None):
        self.frequency = frequency # Transmission frequency, like where to tune in
        self.deviation = deviation
        self.osc = Sine(frequency, sample_rate) # This is the osciilator we're gonna use, since FM is just a single sine wave but it's freqeuency is changed very fast
        self.deviation_limit = deviation_limiter
    def modulate(self, signal: float) -> float:
        inst_freq = self.frequency + (self.deviation*signal) # Calculate the instantaneous frequency based on the carrier frequency, frequency deviation, and input signal
        # Potentially limit the frequency
        if self.deviation_limit is not None: # Make sure it's on
            if abs(inst_freq-self.frequency) > self.deviation_limit:
                inst_freq = self.frequency + (self.deviation_limit if inst_freq > self.frequency else -self.deviation_limit)
        self.osc.frequency = inst_freq
        return self.osc.process()
class BPSKModulator(Modulator):
    """
    Simple BPSK modulator
    positive phase is phase when its 1 and negative is when its 0
    
    takes phase in radians
    """
    def __init__(self, frequency: float, sample_rate: float, positive_phase: float=math.pi, negetive_phase: float=0.0):
        self.osc = Sine(frequency, sample_rate)
        self.positive_phase = positive_phase
        self.negative_phase = negetive_phase
    def modulate(self, signal: bool):
        return self.osc.process(self.positive_phase if bool(signal) else self.negative_phase) # process takes a phase offset in radians
class QPSKModulator(Modulator):
    """
    Simple QPSK modulator
    00: phase0
    01: phase1
    10: phase2
    11: phase3
    
    takes phase in radians
    """
    def __init__(self, frequency: float, sample_rate: float, phase0: float=0, phase1:float=(math.pi/2), phase2:float = math.pi, phase3:float=(2*math.pi)):
        self.osc = Sine(frequency, sample_rate)
        self.phase0 = phase0
        self.phase1 = phase1
        self.phase2 = phase2
        self.phase3 = phase3
    def modulate(self, signal: bool, signal2: bool):
        signal = bool(signal)
        signal2 = bool(signal2)
        if signal and signal2: phase = self.phase3
        elif signal: phase = self.phase2
        elif signal2: phase = self.phase1
        else: phase = self.phase0
        return self.osc.process(phase) # process takes a phase offset in radians
class FSKModulator(Modulator):
    """
    Simple FSK modulator, works a little bit like the FM modulator
    """
    def __init__(self, frequency0: float, frequency1: float, sample_rate: float):
        if frequency0 == frequency1:
            raise Warning("[FSK] Same frequencies?")
        self.freq0 = frequency0
        self.freq1 = frequency1
        self.osc = Sine(frequency0, sample_rate)
    def modulate(self, signal: bool):
        self.osc.frequency = self.freq1 if signal else self.freq0
        return self.osc.process()
class FourFSKModulator(Modulator):
    """
    Simple 4-FSK modulator, works a little bit like the FM modulator
    
    freq0 = 00
    freq1 = 01
    freq2 = 10
    freq3 = 11
    """
    def __init__(self, frequency0: float, frequency1: float, frequency2: float, frequency3: float, sample_rate: float):
        if frequency0 == frequency1:
            raise Warning("[FSK] Same frequencies?")
        self.freq0 = frequency0
        self.freq1 = frequency1
        self.freq2 = frequency2
        self.freq3 = frequency3
        self.osc = Sine(frequency0, sample_rate)
    def modulate(self, signal: bool, signal2: bool):
        if signal and signal2: freq = self.freq3
        elif signal: freq = self.freq2
        elif signal2: freq = self.freq1
        else: freq = self.freq0
        self.osc.frequency = freq
        return self.osc.process()
#endregion Modulators

#region Encoders
class FMStereoEncoder(Encoder):
    def __init__(self, sample_rate:float, output_57k: bool=False, volumes: list=[0.7, 0.1, 0.3, 1]):
        """
        volumes is a list with the volumes of each signals in this order: mono, pilot, stereo, mpx
        """
        if sample_rate < (53000*2):
            raise Exception("Sample rate too small to stereo encode")
        self.osc = MultiSine(19000, sample_rate, 2) # Multisine generates a number of harmonics of a signal, which are perfectly is phase and thus great for this purpose
        self.stm = StereoToMono()
        self.lpf = StereoButterworthLPF(15000, sample_rate)
        self.mono_vol, self.pilot_vol, self.stereo_vol, self.mpx_vol = volumes
        self.output_57k = output_57k
    def encode(self, left: float, right: float, mpx:float=0.0):
        left,right = self.lpf.process(left, right)
        
        pilot, stereo_carrier, rds_carrier = self.osc.process()
        
        mono = self.stm.process(left, right)
        stereo = (left-right)
        modulated_stereo = stereo*stereo_carrier # Can't use the DSB-SC mod object because it generates it's own sine wave
        
        out = 0.0
        out += (mono*self.mono_vol)
        out += (pilot*self.pilot_vol)
        out += (modulated_stereo*self.stereo_vol)
        out += (mpx*self.mpx_vol)
        
        if self.output_57k:
            return out, rds_carrier
        else:
            return out
#endregion Encoders

#region Other
class Buffer:
    def __init__(self, buffer_size: int):
        self.size = buffer_size
        self.buffer = []
    def process(self, sample):
        self.buffer.append(sample)
        if len(self.buffer) >= self.size:
            b = self.buffer
            self.buffer.clear()
            return b
class Decimator:
    def __init__(self, ratio: int, sample_rate: float):
        self.sr = sample_rate
        self.nsr = sample_rate/ratio
        self.ratio = ratio
        self.lpf = MonoButterworthLPF(self.nsr, sample_rate)
    def process(self, audio: list) -> list:
        return [self.lpf.process(i) for i in audio][::self.ratio]
class Interpolator:
    def __init__(self, ratio: int, sample_rate: int):
        self.sr = sample_rate
        self.nsr = sample_rate*ratio
        self.ratio = ratio
    def process(self, audio: list) -> list:
        out = []
        padded_audio = [audio[0]] + audio + [audio[-1]]
        for past, now, future in zip(padded_audio, padded_audio[1:], padded_audio[2:]):
            out.append(now)
            for i in range(1, self.ratio):
                t = i / self.ratio  # Interpolation factor between 0 and 1
                interpolated = now * (1 - t) + future * t
                out.append(interpolated)
        return out
        
class DiscreteFourierTransform:
    def __init__(self, sample_rate: float):
        self.sr = sample_rate
    def process(self, signal: list) -> list:
        """
        Compute the frequencies that make up a signal using DFT and return strongest frequency in Hz.

        Parameters:
        - signal: List of signal amplitudes (time domain).

        Returns:
        - strongest_frequency: The frequency in Hz with the highest magnitude.
        - magnitudes: Magnitudes of the frequencies in the signal.
        """
        N = len(signal)
        frequencies = [(self.sr * k) / N for k in range(N)]
        magnitudes = []
        
        for k in range(N):  # For each frequency bin
            real_part = 0
            imag_part = 0
            for n in range(N):  # Sum over all time domain samples
                angle = 2 * math.pi * k * n / N
                real_part += signal[n] * math.cos(angle)
                imag_part -= signal[n] * math.sin(angle)
            # Magnitude of the k-th frequency component
            magnitude = math.sqrt(real_part**2 + imag_part**2) / N
            magnitudes.append(magnitude)
        
        half_N = N // 2
        magnitudes = magnitudes[:half_N]
        frequencies = frequencies[:half_N]
        
        max_index = magnitudes.index(max(magnitudes))
        strongest_frequency = frequencies[max_index]
        
        return strongest_frequency, frequencies, magnitudes
class FastFourierTransform:
    def __init__(self, sample_rate: float):
        self.sr = sample_rate

    def fft(self, signal):
        N = len(signal)
        if N & (N - 1) != 0:
            raise ValueError("Signal length must be a power of 2.")

        signal = list(signal)  # Ensure mutable
        indices = self._bit_reversal_indices(N)
        signal = [signal[i] for i in indices]

        for step in range(1, int(math.log2(N)) + 1):
            M = 2 ** step
            half_M = M // 2
            twiddle_factors = [
                math.e**(-2j * math.pi * k / M) for k in range(half_M)
            ]
            for start in range(0, N, M):
                for k in range(half_M):
                    even = signal[start + k]
                    odd = twiddle_factors[k] * signal[start + k + half_M]
                    signal[start + k] = even + odd
                    signal[start + k + half_M] = even - odd

        return signal

    def _bit_reversal_indices(self, N):
        bits = int(math.log2(N))
        return [int(bin(i)[2:].zfill(bits)[::-1], 2) for i in range(N)]

    def process(self, signal):
        N = len(signal)
        if N & (N - 1) != 0:
            raise ValueError("Signal length must be a power of 2.")

        frequencies = [(self.sr * k) / N for k in range(N // 2)]
        transformed = self.fft(signal)
        magnitudes = [abs(transformed[k]) / N for k in range(N // 2)]

        max_index = magnitudes.index(max(magnitudes))
        strongest_frequency = frequencies[max_index]

        return strongest_frequency, frequencies, magnitudes
#endregion Other

#region Data encoders
def convert_to_s8(audio_samples):
    """
    Convert a list of 2V peak-to-peak audio samples (float in range -1.0 to 1.0)
    to signed 8-bit little-endian format.

    :param audio_samples: List of audio samples in range -1.0 to 1.0
    :return: bytearray containing the audio samples in s16le format
    """
    s8_samples = bytearray()

    for sample in audio_samples:
        if not -1.0 <= sample <= 1.0:
            print(sample)
            raise ValueError("Audio sample must be in the range of -1.0 to 1.0")

        # Convert to signed 16-bit integer
        int_sample = int(sample * 127)

        # Pack into little-endian format
        s8_samples.append(int_sample)

    return s8_samples
def convert_from_s8(s8le_data):
    """
    Convert signed 8-bit little-endian audio data to a list of float audio samples
    in the range -1.0 to 1.0.

    :param s8le_data: bytearray containing audio samples in s16le format
    :return: List of audio samples in range -1.0 to 1.0
    """
    if len(s8le_data) % 1 != 0:
        raise ValueError("The length of the s16le data must be odd (2 bytes per sample).")

    audio_samples = []

    for i in range(0, len(s8le_data), 1):
        # Combine two bytes (little-endian) to form a signed 16-bit integer
        int_sample = s8le_data[i]

        # Handle negative values for 8-bit signed integers
        if int_sample >= 127:
            int_sample -= 255

        # Convert back to the range -1.0 to 1.0
        float_sample = int_sample / 127.0

        # Append the float sample to the list
        audio_samples.append(float_sample)

    return audio_samples
def convert_to_s16le(audio_samples):
    """
    Convert a list of 2V peak-to-peak audio samples (float in range -1.0 to 1.0)
    to signed 16-bit little-endian format.

    :param audio_samples: List of audio samples in range -1.0 to 1.0
    :return: bytearray containing the audio samples in s16le format
    """
    s16le_samples = bytearray()

    for sample in audio_samples:
        # Scale from -1.0 to 1.0 to -32768 to +32767
        if not -1.0 <= sample <= 1.0:
            print(audio_samples.index(sample), sample)
            raise ValueError("Audio sample must be in the range of -1.0 to 1.0")

        # Convert to signed 16-bit integer
        int_sample = int(sample * 32767)

        # Pack into little-endian format
        s16le_samples.append(int_sample & 0xFF)          # Low byte
        s16le_samples.append((int_sample >> 8) & 0xFF)  # High byte

    return s16le_samples
def convert_from_s16le(s16le_data):
    """
    Convert signed 16-bit little-endian audio data to a list of float audio samples
    in the range -1.0 to 1.0.

    :param s16le_data: bytearray containing audio samples in s16le format
    :return: List of audio samples in range -1.0 to 1.0
    """
    if len(s16le_data) % 2 != 0:
        raise ValueError("The length of the s16le data must be even (2 bytes per sample).")

    audio_samples = []

    for i in range(0, len(s16le_data), 2):
        # Combine two bytes (little-endian) to form a signed 16-bit integer
        int_sample = s16le_data[i] | (s16le_data[i + 1] << 8)

        # Handle negative values for 16-bit signed integers
        if int_sample >= 0x8000:
            int_sample -= 0x10000

        # Convert back to the range -1.0 to 1.0
        float_sample = int_sample / 32767.0

        # Append the float sample to the list
        audio_samples.append(float_sample)

    return audio_samples
def convert_to_s24le(audio_samples):
    """
    Convert a list of 2V peak-to-peak audio samples (float in range -1.0 to 1.0)
    to signed 24-bit little-endian format.

    :param audio_samples: List of audio samples in range -1.0 to 1.0
    :return: bytearray containing the audio samples in s24le format
    """
    s24le_samples = bytearray()

    for sample in audio_samples:
        # Scale from -1.0 to 1.0 to -32768 to +32767
        if not -1.0 <= sample <= 1.0:
            print(sample)
            raise ValueError("Audio sample must be in the range of -1.0 to 1.0")

        # Convert to signed 16-bit integer
        int_sample = int(sample * 524287)

        # Pack into little-endian format
        s24le_samples.append(int_sample & 0xFF)
        s24le_samples.append((int_sample >> 8) & 0xFF)
        s24le_samples.append((int_sample >> 16) & 0xFF)

    return s24le_samples
def convert_from_s24le(s24le_data):
    """
    Convert signed 16-bit little-endian audio data to a list of float audio samples
    in the range -1.0 to 1.0.

    :param s24le_data: bytearray containing audio samples in s16le format
    :return: List of audio samples in range -1.0 to 1.0
    """
    if len(s24le_data) % 3 != 0:
        raise ValueError("The length of the s24le data must be odd (3 bytes per sample).")

    audio_samples = []

    for i in range(0, len(s24le_data), 3):
        # Combine two bytes (little-endian) to form a signed 24-bit integer
        int_sample = s24le_data[i] | (s24le_data[i + 1] << 8) | (s24le_data[i + 2] << 16)

        # Handle negative values for 16-bit signed integers
        if int_sample >= 524288:
            int_sample -= 1048575

        # Convert back to the range -1.0 to 1.0
        float_sample = int_sample / 524287.0

        # Append the float sample to the list
        audio_samples.append(float_sample)

    return audio_samples
#endregion Data encoders