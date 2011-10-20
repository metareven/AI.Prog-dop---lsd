Lyd = wavread('Training Data\left_0.wav');
Lydbuffer = buffer(Lyd, 10, 2);
Size = size(Lydbuffer);
Fouriertransformer = zeros(Size(1), Size(2));
disp(Size);
AverageAmps = zeros(10,1);
States = zeros(10,1);
for i = 1:Size(1),
    Fouriertransformer(i,:) = fft(Lydbuffer(i,:));
    Fouriertransformer(i,:) = Fouriertransformer(i,:).*conj(Fouriertransformer(i,:));
    [peaks, valleys] = peakdet(Fouriertransformer(i,:),0.5);
    for j = 1:length(peaks),
        AverageAmps(i) = AverageAmps(i) + (peaks(j,2));
        %disp(AverageAmps(i));
    end
end
normalizer = 0;
for i = 1:length(AverageAmps),
    if(AverageAmps(i) > normalizer),
        normalizer = AverageAmps(i);
    end
end
for i = 1:length(AverageAmps),
    AverageAmps(i) = AverageAmps(i) / normalizer;
    temp = AverageAmps(i);
    if(temp >= 0.9),
        States(i) = 1;
    elseif(temp >= 0.7),
        States(i) = 2;
    elseif(temp >= 0.5),
        States(i) = 3;
    elseif(temp >= 0.3),
        States(i) = 4;
    else,
        States(i) = 5
    end
end
%disp(AverageAmps);
disp(States);