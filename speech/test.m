Lyd = wavread('D:\NTNU\kunstig intelligens programmering\Speach Recognition\sound_files\wav\Left_0.wav');
Lydbuffer = buffer(Lyd, 10, 2);
Size = size(Lydbuffer);
Fouriertransformer = zeros(Size(1), Size(2));
disp(Size);
for i = 1:Size(1),
    Fouriertransformer(i,:) = fft(Lydbuffer(1,:));
end
disp(length(Fouriertransformer));
for i = 1:length(Fouriertransformer),
    %disp(Fouriertransformer(i,:));
end
