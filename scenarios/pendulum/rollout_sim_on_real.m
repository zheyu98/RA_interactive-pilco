%% rollout.m
% *Summary:* Generate a state trajectory using an ODE solver (and any additional 
% dynamics) from a particular initial state by applying either a particular 
% policy or random actions.
%
%   function [x y L latent] = rollout(start, policy, H, plant, cost)
%
% *Input arguments:*
%   
%   start       vector containing initial states (without controls)   [nX  x  1]
%   policy      policy structure
%     .fcn        policy function
%     .p          parameter structure (if empty: use random actions)
%     .maxU       vector of control input saturation values           [nU  x  1]
%   H           rollout horizon in steps
%   plant       the dynamical system structure
%     .subplant   (opt) additional discrete-time dynamics
%     .augment    (opt) augment state using a known mapping
%     .constraint (opt) stop rollout if violated
%     .poli       indices for states passed to the policy
%     .dyno       indices for states passed to cost
%     .odei       indices for states passed to the ode solver
%     .subi       (opt) indices for states passed to subplant function
%     .augi       (opt) indices for states passed to augment function
%   cost    cost structure
%
% *Output arguments:*
%
%   x          matrix of observed states                           [H   x nX+nU]
%   y          matrix of corresponding observed successor states   [H   x   nX ]
%   L          cost incurred at each time step                     [ 1  x    H ]
%   latent     matrix of latent states                             [H+1 x   nX ]
%
%% High-Level Steps
%
% # Compute control signal $u$ from state $x$:
% either apply policy or random actions
% # Simulate the true dynamics for one time step using the current pair $(x,u)$
% # Check whether any constraints are violated (stop if true)
% # Apply random noise to the successor state
% # Compute cost (optional)
% # Repeat until end of horizon



function rollout_sim_on_real(policy, H, plant, cost)
%% Code

if isfield(plant,'augment'), augi = plant.augi;             % sort out indices!
else plant.augment = inline('[]'); augi = []; end
if isfield(plant,'subplant'), subi = plant.subi;
else plant.subplant = inline('[]',1); subi = []; end

fugiboard('CloseAll');
h=fugiboard('Open', 'mops1');
initial = fugiboard('Read', h);
xpos1_ = initial(3);
xpos2_ = initial(4);
pos = ConTheta(xpos1_);
pos_t = transform(pos);
vel = xpos2_;

odei = plant.odei; poli = plant.poli; dyno = plant.dyno; angi = plant.angi;
simi = sort([odei subi]);
nX = length(simi)+length(augi); nU = length(policy.maxU); nA = length(angi);
% initial states
% s_c = receive(sub);
% mu0 = [s_c.Speed s_c.Position0]';                  % initial state mean
mu0 = [vel pos_t]';
S0 = 0.01*eye(2);
start = gaussian(mu0, S0);

state(simi) = start; %state(augi) = plant.augment(state);      % initializations
x = zeros(1, nX+2*nA);
x(simi) = start' + randn(size(simi))*chol(plant.noise);
% x(augi) = plant.augment(x(:));
u = zeros(1, nU);
next = zeros(1,length(simi));

for i = 1:2*H % --------------------------------------------- generate trajectory
    s = x(dyno)'; sa = gTrig(s, zeros(length(s)), angi); s = [s; sa];
    x(end-2*nA+1:end) = s(end-2*nA+1:end);

    % 1. Apply policy ... or random actions --------------------------------------
    u(:) = policy.fcn(policy,s(poli),zeros(length(poli)));

    tic;

    fugiboard('Write', h, 0, 1, [u(:) 0.0]);
    pause(0.2);
    states = fugiboard('Read', h);
    xpos1_ = states(3);
    xpos2_ = states(4);
    pos = ConTheta(xpos1_);
    pos_t = transform(pos);
    vel = xpos2_;
    next(odei) = [vel pos_t]';
    next(subi) = plant.subplant(state, u(:));

    % 4. Augment state and randomize ---------------------------------------------
    state(simi) = next(simi); state(augi) = plant.augment(state);
    x(simi) = state(simi) + randn(size(simi))*chol(plant.noise);
%     x(augi) = plant.augment(x(:));
    
  toc;
end
end
%% coordinates transformation
function pos_t = transform(pos)
if pos < 0
    pos_t = -pi - pos;
else
    pos_t = pi - pos;
end
end