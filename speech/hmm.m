function result = hmm(n, word)
hmm.prior = zeros(n,1);
hmm.messages = zeros(n,1);
hmm.norms = zeros(n,1);
hmm.sigma = zeros(n,1);
hmm.my = zeros(n,1);
    for i=1:length(hmm.prior)
        hmm.prior(i) = 1/n;
    end
hmm.prior = hmm.prior';
%lager den initielle dynamiske modellen    
hmm.dynamic = createDynamicModel(n,word);
hmm.observation = zeros(n,n,n);

%initialiserer my og sigmaverdiene
for i=1:n
    hmm.my(i,1) = i;
    hmm.sigma(i,1) = 1;
end

for i = 1:n
    for j=1:n
        hmm.observation(i,j,j) = normpdf(j,i,1);
    end
end

eksempelTest(hmm);

result = hmm;

end

function res = eksempelTest(obj)
St = [1,2];
obj.prior = [0.5 0.5]';
obj.observation = [1.5,1,1.3];
obj.dynamic = [.7 .3; .3 .7];
[obj.norms, messages] = (forward(obj,2));
backward(obj,2);

end


%metode som lager den dynamiske modellen
function dyn = createDynamicModel(n,word)
    dyn = zeros(n,n);
    counter = 0;
    %leser alle filene med training data fra ordet 'word' og sjekker hvor
    %ofte man går fra en gitt state til en annen
    for i=0:25
       [temp amps] = spectralRead(strcat('Training Data\',word,'_',num2str(i),'.','wav'),n);
       for j=1:length(temp) -1
           from = temp(j);
           to = temp(j+1);
           dyn(from,to) = dyn(from,to)+1;
       end
    end
    %Deler alle elementene i tabellen med counter slik at summen av alle
    %tallene blir 1
    for x=1:n
        counter = 0;
        for y=1:n
            counter = counter + dyn(x,y);
        end
        if(counter > 0)
            for i=1:n
                dyn(x,i) = dyn(x,i)/counter;
            end
        end
    end
    
    
       
           
    
    

end

%forward alogritmen, returnerer en liste med:
%l: summen av alle normaliseringskonstantene
%messages: en liste over alle framoverbeskjedene
%algoritmen legger også til n-tall i model sin norms. Dette er
%normaliserings/skaleringsverdien som hvert steg deles med

function [l, messages] = forward(model,n)
l = zeros(length(model.observation),1);
f = zeros(n);
F = zeros(length(model.observation),n);

%regner ut observasjosverdiene for det første steget
for i=1:n
    f(i,i) = normpdf(model.observation(1),i,model.sigma(1));
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
        f(j,j) = normpdf(model.observation(i),j,model.sigma(j));
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

function messages = backward(model,n);
    %init
    r = ones(length(model.observation),n);
    B = zeros(n,n);
    r(length(r),:) = r(length(r),:)/model.norms(length(r));
    %induksjon
    for i=length(model.observation)-1:-1:1
        %regner ut observasjonsmatrisa for dette steget
        for j=1:n
            B(j,j) = normpdf(model.observation(i),j,model.sigma(j));
        end
        r(i,:) = model.dynamic * B * r(i+1,:)';
        r(i,:) = r(i,:) / model.norms(i);
    end
    messages = r;
    disp(r);
end


function [result amps] = spectralRead(file,n)
    Lyd = wavread(file);
    Lydbuffer = buffer(Lyd, 80);
    Size = size(Lydbuffer);
    Fouriertransformer = zeros(Size(1), Size(2));
    AverageAmps = zeros(Size(2),1);
    States = zeros(Size(2),1);
    for i = 1:Size(2)
        Fouriertransformer(:,i) = fft(Lydbuffer(:,i));
        Fouriertransformer(:,i) = Fouriertransformer(:,i).*conj(Fouriertransformer(:,i));
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
    for i=1:length(States)
        if States(i) == 0
            States(i) = n;
        end
    end
    result = States;
    amps = AverageAmps;
end
