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

feature_file = spectralReadFromTable(feature_file,n);
feature_file = abs(feature_file);

T = length(feature_file);

hmm.observation = zeros(T,n,n);

% eksempelTest(hmm);
% disp('Success');

% Fyller inn verdier i observation model matrisene
for t = 1:T % Time slots
    for j= 1:n % States
        hmm.observation(t,j,j) = normpdf(feature_file(t),hmm.my(j),hmm.sigma(j));
    end
end


% Beregner verdier for alle modellene ved hjelp av EM-algoritmen
% START EM

% Starter med å sette noen verdier som brukes for å terminere loopen når
% man ser at log_likelihood som man får fra forward-algoritmen konvergerer.
prior_log = 999999999;
convergence = false;

counter = 0;
while (convergence == false)
    disp(counter);
    counter = counter + 1;
    % Starter med å gjøre Forward og backward med den nåværende modellen og
    % observasjonene O(1:T) for å få f(t) og r(t) for t = 1,...,T.
    [norms, scaled_forward_messages] = forward(hmm,n);
    norms = abs(norms);
    hmm.norms = norms;
    %disp(norms);
    scaled_backward_messages = backward(hmm,n);
    log_lik = 0;
    for i = 1:length(norms)
        log_lik = log_lik + log(norms(i));
    end
    % Finner så xi(t) og gamma(t) for alle t ved å bruke Rabiners likninger
    % 37 + 38 der alpha(t) og betha(t) byttes ut med f(t) og r(t).
    xi = zeros(T,n,n);
    gamma = zeros(T,n);
    % Regner ut gamma-verdier
    for t=1:T
        divider_sum = 0;
        for i=1:n
            divider_sum = divider_sum + (scaled_forward_messages(t,i) * scaled_backward_messages(t,i));
        end
        for j=1:n
            gamma(t,j) = (scaled_forward_messages(t,j) * scaled_backward_messages(t,j)) / divider_sum;
        end
    end
    % Regner ut xi-verdier
    for t=1:T-1
        divider_sum = 0;
        for k=1:n
            for l=1:n
                divider_sum = divider_sum + (scaled_forward_messages(t,k)*hmm.dynamic(k,l)*hmm.observation(t+1,l,l)*scaled_backward_messages(t+1,l));
            end
        end
        for i = 1:n
            for j = 1:n
                xi(t,i,j) = (scaled_forward_messages(t,i)*hmm.dynamic(i,j)*hmm.observation(t+1,j,j)*scaled_backward_messages(t+1,j)) / divider_sum;
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
            for t=1:T-1
                teller = teller + xi(t,i,j);
                nevner = nevner + gamma(t,i);
            end
            hmm.dynamic(i,j) = teller / nevner;
        end
    end
    % Oppdaterer verdier for my og sigma ved å bruke likninger 53 og 54
    for j = 1:n
        teller = 0;
        nevner = 0;
        for t = 1:T
            teller = teller + (gamma(t,j) * feature_file(t)); % Litt usikker på om det er selve feature_file(t) som skal brukes her eller observasjonsmodellen
            nevner = nevner + (gamma(t,j));
        end
        hmm.my(j) = teller / nevner;
    end
    for j = 1:n
        teller = 0;
        nevner = 0;
        for t = 1:T
            teller = teller + (gamma(t,j) * (feature_file(t) - hmm.my(j)) * (feature_file(t) - hmm.my(j))); % Tror ikke dette stemmer, men...
            nevner = nevner + gamma(t,j);
        end
        hmm.sigma(j) = teller / nevner;
    end
    
    % Oppdaterer hmm.observations
    for t = 1:T
        for j = 1:n
            hmm.observation(t,j,j) = normpdf(feature_file(t),hmm.my(j),hmm.sigma(j));
        end
    end
    
    % Sjekker om log-likelihood konvergerer
    disp(log_lik);
    if (abs(prior_log - log_lik) < 1)
        convergence = true;
    end
    prior_log = log_lik;
end
% END EM

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

function res = eksempelTest(obj)
St = [1,2];
obj.prior = [0.5 0.5]';
obj.observation = [1.5,1,1.3];
obj.dynamic = [.7 .3; .3 .7];
obj.my = [1,2];
[obj.norms, messages] = (forward(obj,2));
disp(messages);
backward(obj,2);

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
    if (l(i) ~= 0)
        f = f/l(i);
    end
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
            B(j,j) = normpdf(model.observation(i),model.my(j),model.sigma(j));
        end
        r(i,:) = model.dynamic * B * r(i+1,:)';
        r(i,:) = r(i,:) / model.norms(i);
    end
    messages = r;
    % disp(r);
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

function feature_list = spectralReadFromTable(feature_file,n)
    feature_buffer = buffer(feature_file,80);
    feature_size = size(feature_buffer);
    fouriertransformer = zeros(feature_size(1), feature_size(2));
    AverageAmps = zeros(feature_size(2), 1);
    for i = 1:feature_size(2);
        fouriertransformer(:,i) = fft(feature_buffer(:,i));
        fouriertransformer(:,i) = fouriertransformer(:,i).*conj(fouriertransformer(:,i));
        [peaks, valleys] = peakdet(fouriertransformer(:,i),0.1);
        for j = 1:(size(peaks))(1)
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
    for i = 1:feature_size(2)
        AverageAmps(i) = AverageAmps(i) / normalizer;
        temp = AverageAmps(i);
        for j=n:-1:1
            if(temp > 1 - (1/j))
                States(i)=j;
                break
            end
        end
    end
    feature_list = AverageAmps;

end
