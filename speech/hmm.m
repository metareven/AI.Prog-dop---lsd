function result = hmm(n, word)
hmm.prior = zeros(n,1);
hmm.messages = zeros(n,1);
hmm.norms = zeros(n,1);
hmm.sigma = zeros(n,1);
hmm.my = zeros(n,1);
    for i=1:length(hmm.prior)
        hmm.prior(i) = 1/n;
    end
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


result = hmm;

end

%metode som lager den dynamiske modellen
function dyn = createDynamicModel(n,word)
    dyn = zeros(n,n);
    counter = 0;
    %leser alle filene med training data fra ordet 'word' og sjekker hvor
    %ofte man g�r fra en gitt state til en annen
    for i=0:25
       temp = spectralRead(strcat('Training Data\',word,'_',num2str(i),'.','wav'),n);
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

function result = test(n)
obs = gaussmf(x,[1 n]);
dynamic = zeros(2,2);
dynamic(1,:) = [0.7 0.3];
dynamic(2,:) = [0.3 0.7];
pi = [0.5 0.5]';

end

%forward alogritmen, returnerer en liste med:
%l: summen av alle normaliseringskonstantene
%messages: en liste over alle framoverbeskjedene
%algoritmen legger ogs� til n-tall i model sin norms. Dette er
%normaliserings/skaleringsverdien som hvert steg deles med
function [l, messages] = forward(model,n)
    %initialisering
    l = 0;
    alpha = zeros(n,n);
    alpha(1,:) = model.observation(1,:,:) * model.prior;
    counter = 0;
    for i=1:length(alpha(1,:))
        counter = counter + alpha(1,i);
    end
    alpha(1,:) = alpha(1,:)/counter;
    model.norms(1,:) = counter;
    l = l + counter;
    
    %induksjon:
    for j=2:n
        alpha(j,:) = model.observation(j,:,:) * model.dynamic' * alpha(j-1,:);
        counter = 0;
        for i=1:length(alpha(j,:))
            counter = counter + alpha(j,i);
        end
        alpha(j,:) = alpha(j,:)/counter;
        model.norms(j,:) = counter;
        l = l + counter;
    end
    messages = alpha;
    l = log(l);
    
    
end

function messages = backward(model,n)
%initialisering
r = ones(n,1)';
r(n,:) = r/model.norms(n);

%induksjon

%dekrementerende for-l�kker er teite i matlab... funky syntaks
for i=n-1:-1:1
    r(i,:) = model.dynamic * model.observation(i+1,:,:) * r(i+1);
    r(i,:) = r(i,:) / model.norms(i);
end
messages = r;
    

end



function result = spectralRead(file,n)
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
end