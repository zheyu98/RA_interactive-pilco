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



function [x y L latent] = rollout_real(policy, H, plant, cost)
%% Code

if isfield(plant,'augment'), augi = plant.augi;             % sort out indices!
else plant.augment = inline('[]'); augi = []; end
if isfield(plant,'subplant'), subi = plant.subi;
else plant.subplant = inline('[]',1); subi = []; end

% % ROS subscribe to the states
% addpath('/home/zheyu/Desktop/real_pend/src/matlab_msg_gen_ros1/glnxa64/install/m');
% sub = rossubscriber('/mops/read',"DataFormat","struct");
% pause(1);
% 
% % ROS service client
% actionclient = rossvcclient("/mops/write","DataFormat","struct");
% reqMsg = rosmessage(actionclient);
% reqMsg.Actuators.DigitalOutputs = uint8(1);
% reqMsg.Actuators.Voltage0 = 0.0;
% reqMsg.Actuators.Voltage1 = 0.0;
% reqMsg.Actuators.Timeout = 0.5;
% % if(isServerAvailable(actionclient))
% %     [~,~] = waitForServer(actionclient);
% % end

fugiboard('CloseAll');
h=fugiboard('Open', 'mops1');
initial = fugiboard('Read', h);
xpos1_ = initial(3);
xpos2_ = initial(4);
pos = ConTheta(xpos1_);
vel = xpos2_;

odei = plant.odei; poli = plant.poli; dyno = plant.dyno; angi = plant.angi;
simi = sort([odei subi]);
nX = length(simi)+length(augi); nU = length(policy.maxU); nA = length(angi);
% initial states
% s_c = receive(sub);
% mu0 = [s_c.Speed s_c.Position0]';                  % initial state mean
mu0 = [vel pos]';
S0 = 0.01*eye(2);
start = gaussian(mu0, S0);

state(simi) = start; state(augi) = plant.augment(state);      % initializations
x = zeros(H+1, nX+2*nA);
x(1,simi) = start' + randn(size(simi))*chol(plant.noise);
x(1,augi) = plant.augment(x(1,:));
u = zeros(H, nU); latent = zeros(H+1, size(state,2)+nU);
y = zeros(H, nX); L = zeros(1, H); next = zeros(1,length(simi));

r = rateControl(20);
for i = 1:H % --------------------------------------------- generate trajectory
  s = x(i,dyno)'; sa = gTrig(s, zeros(length(s)), angi); s = [s; sa];
  x(i,end-2*nA+1:end) = s(end-2*nA+1:end);
  
  
  % 1. Apply policy ... or random actions --------------------------------------
  if isfield(policy, 'fcn')
    u(i,:) = policy.fcn(policy,s(poli),zeros(length(poli)));
  else
    u(i,:) = policy.maxU.*(2*rand(1,nU)-1);
  end
  latent(i,:) = [state u(i,:)]; % latent state

  % 2. Simulate dynamics -------------------------------------------------------
%   next(odei) = simulate(state(odei), u(i,:), plant); 
%   reqMsg.Actuators.Voltage0 = u(i,:);
%   resp = call(actionclient, reqMsg);
%   pause(0.1)
%   s_c = receive(sub);
%   next(odei) = [s_c.Speed s_c.Position0]';
%   reset(r);
  tic;

  fugiboard('Write', h, 0, 1, [u(i,:) 0.0]);
  pause(0.05);
  states = fugiboard('Read', h);
  xpos1_ = states(3);
  xpos2_ = states(4);
  pos = ConTheta(xpos1_);
  vel = xpos2_;
  next(odei) = [vel pos]';
  am = [vel pos]';
  next(subi) = plant.subplant(state, u(i,:));
%   disp(['The result is: [' num2str(am(:).') ']']) ;
%       waitfor(r);

  toc;
  
  % 3. Stop rollout if constraints violated ------------------------------------
%   if isfield(plant,'constraint') && plant.constraint(next(odei))
%     H = i-1;
%     fprintf('state constraints violated...\n');
%     break;
%   end

  % 4. Augment state and randomize ---------------------------------------------
    state(simi) = next(simi); state(augi) = plant.augment(state);
    x(i+1,simi) = state(simi) + randn(size(simi))*chol(plant.noise);
    x(i+1,augi) = plant.augment(x(i+1,:));
    
  
  
  % 5. Compute Cost ------------------------------------------------------------
%   if nargout > 2
%     L(i) = cost.fcn(cost,state(dyno)',zeros(length(dyno)));
%   end
end

y = x(2:H+1,1:nX); x = [x(1:H,:) u(1:H,:)]; 
latent(H+1, 1:nX) = state; latent = latent(1:H+1,:); L=0; %L = L(1,1:H);