function result = hmm(n, word)
% Starter med å initialisere og "gjette" verdier på de forskjellige
% modellene
hmm.prior = zeros(n,1); % Prior model
hmm.messages = zeros(n,1); % Forward messages
hmm.norms = zeros(n,1); % Normalized messages
hmm.sigma = zeros(n,1); % Sigma values used for the observation model
hmm.my = zeros(n,1); % Mu values used for the observation model
    for i=1:length(hmm.prior)
        hmm.prior(i) = 1/n;
    end
% Lager den initielle dynamiske modellen    
hmm.dynamic = createDynamicModel(n,word);
hmm.observation = zeros(n,n,n);

% Initialiserer my og sigmaverdiene
for i=1:n
    hmm.my(i,1) = i; % Mu(i) = i
    hmm.sigma(i,1) = 1; % Alle sigmaverdiene starter med å være lik 1
end

% Samler alle features fra rammene fra et ord i en stor tabell
feature_file = wavread(['Training Data\','',word,'','_0.wav']);
for i = 1:25,
    temp = feature_file.';
    new_feature = wavread(['Training Data\','',word,'','_','',num2str(i),'','.wav']);
    new_temp = new_feature.';
    feature_file = [temp new_temp].';
end

% Fyller inn verdier i observation model matrisene
for i = 1:n
    for j=1:Length(feature_file)
        hmm.observation(i,j,j) = normpdf(feature_file(j),i,1);
    end
end


% Beregner verdier for alle modellene ved hjelp av EM-algoritmen

% Starter med å sette noen verdier som brukes for å terminere loopen når
% man ser at log_likelihood som man får fra forward-algoritmen konvergerer.
prior_log = 999999999;
convergence = false;

while (convergence == false)
    % Starter med å gjøre Forward og backward med den nåværende modellen og
    % observasjonene O(1:T) for å få f(t) og r(t) for t = 1,...,T.
    [log, scaled_forward_messages] = forward(hmm,n);
    scaled_backward_messages = backward(hmm,n);
    % Finner så xi(t) og gamma(t) for alle t ved å bruke Rabiners likninger
    % 37 + 38 der alpha(t) og betha(t) byttes ut med f(t) og r(t).
    xi = zeros(Length(feature_file),n,n);
    gamma = zeros(Length(feature_file),n);
    % Regner ut gamma-verdier
    for t=1:Length(feature_file)
        sum = 0;
        for i=1:n
            sum = sum + (scaled_forward_messages(t,i) * scaled_backward_messages(t,i));
        end
        for i=1:n
            gamma(t,i) = (scaled_forward_messages(t,i) * scaled_backward_messages(t,i)) / sum;
        end
    end
    % Regner ut xi-verdier
    for t=1:Length(feature_file)
        divider_sum = 0;
        for k=1:n
            for l=1:n
                divider_sum = divider_sum + (scaled_forward_messages(t,k)*hmm.dynamic(k,l)*hmm.observation(l,t+1,t+1)*scaled_backward_messages(t+1,l));
            end
        end
        for i = 1:n
            for j = 1:n
                xi(t,i,j) = (scaled_forward_messages(t,i)*hmm.dynamic(i,j)*hmm.observation(j,t+1,t+1)*scaled_backward_messages(r+1,j)) / divider_sum
            end
        end
    end
    % Gjenestimerer prior distribution og transition model ved å bruke
    % Rabiners likninger 40a og 40b
    for i = 1:n
        hmm.prior(i) = gamma(1,i);
    end
    for i = 1:n
        for j = 1:n
            teller = 0;
            nevner = 0;
            for t=1:Length(feature_file)-1
                teller = teller + xi(t,i,j);
                nevner = nevner + gamma(t,i);
            end
            hmm.dynamic(i,j) = teller / nevner;
        end
    end
    % Oppdaterer verdier for my og zigma ved å bruke likninger 53 og 54
    for j = 1:n
        teller = 0;
        nevner = 0;
        for t = 1:Length(feature_file)
            teller = teller + (gamma(t,j) * feature_file(t));
            nevner = nevner + (gamma(t,j));
        end
        hmm.my(j) = teller / nevner;
    end
    for j = 1:n
        teller = 0;
        nevner = 0;
        for t = 1:Length(feature_file)
            teller = 0; % Skjønner ikke helt hva som skal stå her
            nevner = 0; % Skjønner ikke helt hva som skal stå her heller
        end
        hmm.sigma(j) = teller / nevner;
    end
    
    % !!! Her må hmm.observations oppdateres med de nye verdiene til hmm.my og
    % !!! hmm.sigma
    
    % Sjekker om log-likelihood konvergerer
    if (abs(prior_log - log) < 0.1)
        convergence = true;
    end
end

result = hmm;

end

%metode som lager den dynamiske modellen
function dyn = createDynamicModel(n,word)
    dyn = zeros(n,n);
    counter = 0;
    %leser alle filene med training data fra ordet 'word' og sjekker hvor
    %ofte man går fra en gitt state til en annen
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
%algoritmen legger også til n-tall i model sin norms. Dette er
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

%dekrementerende for-løkker er teite i matlab... funky syntaks
for i=n-1:-1:1
    r(i,:) = model.dynamic * model.observation(i+1,:,:) * r(i+1);
    r(i,:) = r(i,:) / model.norms(i);
end
messages = r;
    

end



function [result, features] = spectralRead(file,n)
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
    features = AverageAmps;
    for i=1:length(States)
        if States(i) == 0
            States(i) = n;
        end
    end
    result = States;
end
