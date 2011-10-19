function result = hmm(n, word)
hmm.prior = zeros(n,1);
    for i=1:length(hmm.prior)
        hmm.prior(i) = 1/n;
    end
hmm.dynamic = createDynamicModel(n,word);

result = hmm;

end

%metode som lager den dynamiske modellen
function dyn = createDynamicModel(n,word)
    dyn = zeros(n,n);
    counter = 0;
    %leser alle filene med training data fra ordet 'word' og sjekker hvor
    %ofte man g�r fra en gitt state til en annen
    for i=0:25
       temp = spectralRead(strcat('Training Data\',word,'_',num2str(i),'.','wav'));
       for j=1:length(temp) -1
           from = temp(j);
           to = temp(j+1);
           dyn(from,to) = dyn(from,to)+1;
           %counter = counter +1;
       end
    end
    %Deler alle elementene i tabellen med counter slik at summen av alle
    %tallene blir 1
    for x=1:n
        counter = 0;
        for y=1:n
            counter = counter + dyn(x,y);
            %dyn(x,y) = dyn(x,y)/counter;
        end
        if(counter > 0)
            for i=1:n
                dyn(x,i) = dyn(x,i)/counter;
            end
        end
    end
    
    
       
           
    
    

end

function result = spectralRead(file)
    Lyd = wavread(file);
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
        else
            States(i) = 5;
        end
    end
    result = States;
end
