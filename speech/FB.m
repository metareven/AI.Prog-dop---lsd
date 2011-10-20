% Solution for Exercise 2 in TDT4171 Methods in AI
% Helge Langseth, 31-01-08

% function FB - Entrypoint for running the whole thing
function FB

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Define the model                                                      %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The HMM is defined by a transformation matrix and an observation model. 
% let the state variable have S states, and the observations have R states.
% The ...
% - The Transfomation matrix is S \times S, entry <ij> giving probability
% of moving from state i to state j within a time step.
% - The observation matrix is actually a set of R matrixes, each of size 
% S \times S. Fr a given observation, the S times S matrix is diagonal,
% element <i,i> tells the probability of observing exactly that evidence
% (out of the possible R) for the different states, i.e., diag(P(e|x_t))
% The structure also has a prior vector, size S \times 1, giving the a
% priori distribution over the possible states.

% Define model
hmm.prior = [.5;.5];
hmm.dynamics = [.7 .3;.3 .7];
hmm.observations = zeros(2,2,2);
hmm.observations(:,:,1)=[.9 0;0 .2];
hmm.observations(:,:,2)=[.1 0;0 .8];
clc; % Clear output


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Code for solving part B of the assignment                             %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Run -- Debug with 2 observations
disp(' ---- DOING DEBUG RUN FOR FILTERING ----- ');
e = [1 1];
fwd_messages = filtering(hmm, e);
disp(['Probability distribution for Rain given two observations of umbrella is ' mat2str(normalize(fwd_messages(:,2)), 3) ')']);

% Run -- Test with the five observations
disp(' ---- DOING FILTERING OF FIVE OBSERVATIONS ----- ');
e = [1 1 2 1 1];
fwd_messages = filtering(hmm, e);
disp(['Probability distribution for Rain given observations is ' mat2str(normalize(fwd_messages(:,length(e))), 3) ')']);
disp('Forward messages:');
for i=1:size(fwd_messages,2)
	disp(['Time ' num2str(i) ': Forward message = ' mat2str(normalize(fwd_messages(:,i)), 3) ')']);
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Code for solving part C of the assignment                             %
% ... when we are here we already have the forward messages             %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Run -- Debug smoothing with 2 observations
disp(' ---- DOING DEBUG RUN FOR SMOOTHING ----- ');
e = [1 1];
fwd_messages = filtering(hmm, e);
smoothed = smooth(hmm, e, fwd_messages, 1);
disp(['Probability distribution for Rain_1 given 2 umbrella-observations is ' mat2str(smoothed, 3) ')']);


disp(' ---- DOING SMOOTHING OF FIVE OBSERVATIONS ----- ');
e = [1 1 2 1 1];
fwd_messages = filtering(hmm, e);
[smoothed backward_msg] = smooth(hmm, e, fwd_messages, 1);
disp(['Probability distribution for Rain_1 given the 5 observations is ' mat2str(normalize(smoothed), 3) ')']);
disp('Backward messages:');
for k=size(fwd_messages,2):-1:1
	disp(['b_{' num2str(k+1) ':' num2str(size(fwd_messages,2)) '} = ' mat2str(backward_msg(:,k), 3) ')']);
end

end





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% THE FUNCTIONS DOING THE JOB FOLLOWS %%%%%%%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%% SMOOTHING
% function SMOOTH does the smootihing procedure, i.e. does the backward
% recursion a number of times. 

% Input: 
%
% hmm: A MATLAB structure containing the prior, the observation models (O), and the dynamic
%		model. Both are coded as matrixes
% evidence: A vector of the observations we have (the boldface e). Length equals <t>
% forwards: Forward messages
% k: The value for which we will backtrack, i.e., calculate P(X_k|e_{1:t}), k < t
% 
% Output: 
%     The smooothed probability

function [smooted_value backwards_msg] = smooth(hmm, evidence, forward, k)
t = length(evidence);
backwards_msg = zeros(length(hmm.prior), t);
backwards_msg(:, t) = ones(size(hmm.prior)); % First backward message is simply a vector of ones. 

for  i = t:-1:k+1
	% Do recursive step
	backwards_msg(:, i-1)= backwards(backwards_msg(:,i), hmm.observations(:,:,evidence(i)), hmm.dynamics);
end

smooted_value = normalize(backwards_msg(:, k) .* forward(:,k));

end





%%% FILTERING
% function FILTERING does the filtering procedure, i.e. does th forward
% recursion a number of times. 

% Input: 
%
% hmm: A MATLAB structure containing the prior, the observation models (O), and the dynamic
%		model. Both are coded as matrixes
% evidence: A vector of the observations we have (the boldface e). Length equals <t>
% 
% Output: 
%     A dynarray of filter-messages

function fwd_messages = filtering(hmm, evidence)
t = length(evidence);
fwd_messages = zeros(length(hmm.prior), t);
for  i = 1:t
	% Unfortulately vectors in matlab cannot start with index 0 so have to
	% take care of this separately
	if(i==1), pass_on = hmm.prior; else pass_on = fwd_messages(:,i-1); end
	
	% Do recursive step
	fwd_messages(:, i) = forward(pass_on, hmm.observations(:,:,evidence(i)), hmm.dynamics);
end

end




%%% NORMALIZE
% function normalize normalizes a vector to make sure it sums to onetates.
% Input: vector: An unnormalized distribution (all elements >=0, though)
% Output: Normalized vector (i.e., a vector that can be seen as a
% aprobability distribution

function distr = normalize(vector)
assert(isempty(vector(vector<0)));
distr = vector ./ (eps + sum(vector));
end




%%% FORWARD MESSAGES
% function forward makes the forward recursion of the HMM algorithm, by
% implementing Eqn 15.10 in the book.
%
% The HMM is defined by a transofrmation matrix and an observation models. 
% let the state variable have S states, and the observations have R states.
% 
% Input to the function doing forward recursion: 
%
% - old_message: The OLD message (normalized or not, does not matter)
% - observation: The observation matrix. It is a diagonal matrix (only 
%        nonzero elements are on the diagonal). The size is S \times  S,
%        and elementy (i,i) is given as 
%		 P(seing the observation we actually got|State is no. i) 
% - dynamics: The dynamic model, descriobed as an S \times S matrix.
%		 Element (i,j) is the probability of moving from state i to state 
%        j within one time step
%
% Output:
%
% message = the new forward message
function message = forward(old_message, observation, dynamics)
	message = observation * dynamics' * old_message;
end
	
%%% BACKWARD MESSAGES
% function backward makes the backwards recursion of the HMM algorithm, by
% implementing Eqn 15.11 in the book.
%
% 
% Input to the function doing forward recursion: 
%
% - old_message: The OLD message (normalized or not, does not matter)
% - observation: The observation matrix. It is a diagonal matrix (only 
%        nonzero elements are on the diagonal). The size is S \times  S,
%        and elementy (i,i) is given as 
%		 P(seing the observation we actually got|State is no. i) 
% - dynamics: The dynamic model, descriobed as an S \times S matrix.
%		 Element (i,j) is the probability of moving from state i to state 
%        j within one time step
%
% Output:
%
% message = the new backward message
function message = backwards(old_message, observation, dynamics)
	message = dynamics * observation * old_message;
end
	

	
	
