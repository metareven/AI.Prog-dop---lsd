function Classifier(n)
Left = hmm(n,'Left');
Right = hmm(n,'Right');
Start = hmm(n,'Go');
Stop = hmm(n,'Stop');

%1: Left
%2:Right
%3:Start
%4:Stop
correct = [4,1,2,3,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2];
%correct = ['Stop','Left', 'Right','Start','Start','Stop','Left','Right','Start','Stop','Left','Right','Start','Stop','Left','Right','Start','Stop''Left','Right','Start','Stop','Left','Right','Start','Stop','Left','Right','Start','Stop','Left','Right','Start','Stop','Left','Right'];

models = [Left, Right, Start,Stop];
names = [1,2,3,4];
%names = ['Left','Right','Stop','Start'];
probs = [0,0,0,0];

results = zeros(35,1);

for i=1:35
    probs = [0,0,0,0];
    [obs trash] = spectralRead(strcat(['TestData\query_',int2str(i),'.wav']),n);
    for j=1:length(models)
        models(j).observation = obs;
        norms = forward(models(j),n);
        for k=1:length(norms)
            probs(j) = probs(j) + norms(k);
        end
    end
    %disp(probs);
    results(i) = calculateWord(names,probs);
end

accuracy = 0;
for i=1:35
    if results(i) == correct(i)
        accuracy = accuracy + (1/35);
    end
end
%disp(correct);
%disp(results);
disp(accuracy);



end

function winner = calculateWord(names,probs);
highest = probs(1);
winner = 1;
for i=2:length(probs)
    if probs(i) > highest
        highest = probs(i);
        winner = names(i);
    end
end


end

function [l, messages] = forward(model,n)
l = zeros(length(model.observation),1);
f = zeros(n);
F = zeros(length(model.observation),n);

%regner ut observasjosverdiene for det første steget
for i=1:n
    f(i,i) = normpdf(model.observation(1),model.my(i),model.sigma(1));
end
f = f * model.prior;

for i=1:length(f)
    l(1) = l(1)+ f(i);
end
%normaliserer
f = f/l(1);
f = f';
F(1,:) = f;

%induksjonsteget
for i =2:length(model.observation)
    %regner ut observasjonsmatrisa for dette steget
    f = zeros(n);
    for j=1:n
        f(j,j) = normpdf(model.observation(i),model.my(j),model.sigma(j));
    end

    %fortsetter med formelen
    f = f * model.dynamic';
    f = f * F(i-1,:)';
        %normaliserer
    for j=1:length(f)
        l(i) = l(i)+ f(j);
    end
    f = f/l(i);
    F(i,:) = f;
end

messages = F;


end

function [result, features] = spectralRead(file,n)
    Lyd = wavread(file);
    Lydbuffer = buffer(Lyd, 80);
    Size = size(Lydbuffer);
    Fouriertransformer = zeros(Size(1), Size(2));
    AverageAmps = zeros(Size(2),1);
    States = zeros(Size(2),1);
    for i = 1:Size(2)
        %Fouriertransformer(:,i) = fft(Lydbuffer(:,i));
        %Fouriertransformer(:,i) = Fouriertransformer(:,i).*conj(Fouriertransformer(:,i));
        Fouriertransformer(:,i) = cceps(Lydbuffer(:,i));
        [peaks, valleys] = peakdet(Fouriertransformer(:,i),0.1);
        for j = 1:(size(peaks))(1);
            AverageAmps(i) = AverageAmps(i) + (peaks(j,2));
        end
        
    end
    normalizer = 0;
    for i = 1:length(AverageAmps),
        if(AverageAmps(i) > normalizer),
            normalizer = AverageAmps(i);
        end
    end
    %States = zeros(size(peaks));
    for i = 1:Size(2)
        AverageAmps(i) = AverageAmps(i) / normalizer;
        temp = AverageAmps(i);
        for j=n:-1:1
            if(temp > 1 - (1/j))
                States(i)=j;
                break
            end
        end
    end
    features = AverageAmps;
    for i=1:length(States)
        if States(i) == 0
            States(i) = n;
        end
    end
    result = States;
end

