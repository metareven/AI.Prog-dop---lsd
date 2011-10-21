Lyd = wavread('C:\Documents and Settings\Lars\Mine dokumenter\workspace\AI.Prog-dop---lsd\speech\Training Data\Left_0.wav');
Lydbuffer = buffer(Lyd, 10, 2)';
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
