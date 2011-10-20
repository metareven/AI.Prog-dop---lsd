Fs = 1000; % Sampling frequency
T = 1/Fs; % Sample time
L = 250; % Length of signal
t = (0:L-1)*T; % Time vector
% Sum of a 50 Hz sinusoid and a 120 Hz sinusoid + noise
y = 0.7*sin(2*pi*50*t)+sin(2*pi*120*t)+randn(size(t));
plot(Fs*t,y);
title('Signal Corrupted with Zero-Mean Random Noise');
NFFT = 2^nextpow2(L); % Next power of 2 from length of y
Y = fft(y,NFFT)/L; % Y = FFT of original data
f = Fs/2*linspace(0,1,NFFT/2+1); % Frequencies used by FFT
% Generate and plot single-sided amplitude spectrum.
amplitudes = 2*abs(Y(1:NFFT/2+1));
plot(f,amplitudes);
title('Single-Sided Amplitude Spectrum of y(t)');