% Starter med å konkatenere alle signalene for et ord til en stor tabell
feature_file = wavread('Training Data\Left_0.wav');
for i = 1:25,
    temp = feature_file.';
    new_feature = wavread(['Training Data\Left_','',num2str(i),'','.wav']);
    new_temp = new_feature.';
    feature_file = [temp new_temp].';
end

% Henter så ut features fra den store tabellen


% Velger parametere i HMM for å maksimere sansynligheten av å observere
% observasjonene i feature_file. Dette gjøres ved hjelp av EM algoritmen.

% Starter med å gjette verdien for alle parametere.

pi = [0.2, 0.2, 0.2, 0.2, 0.2]; % Transition model
A = [pi; pi; pi; pi; pi];
sigma = 1;
mu = 1;