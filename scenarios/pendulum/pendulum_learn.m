%% pendulum_learn.m
% *Summary:* Script to learn a controller for the pendulum swingup
%
% Copyright (C) 2008-2013 by
% Marc Deisenroth, Andrew McHutchon, Joe Hall, and Carl Edward Rasmussen.
%
% Last modified: 2013-03-27
%
%% High-Level Steps
% # Load parameters
% # Create J initial trajectories by applying random controls
% # Controlled learning (train dynamics model, policy learning, policy
% application)
%% clear
clear;
clc;
%% Code

% 1. Initialization
clear all; close all;
settings_pendulum;            % load scenario-specific settings
basename = 'pendulum_';       % filename used for saving data

% 2. Initial J random rollouts
for jj = 1:J
  [xx, yy, realCost{jj}, latent{jj}] = ...
    rollout_real(struct('maxU',policy.maxU), H, plant, cost);
  x = [x; xx]; y = [y; yy];       % augment training sets for dynamics model
%   if plotting.verbosity > 0;      % visualization of trajectory
%     if ~ishandle(1); figure(1); else set(0,'CurrentFigure',1); end; clf(1);
%     draw_rollout_pendulum;
%   end
end

mu0Sim(odei,:) = mu0; S0Sim(odei,odei) = S0;
mu0Sim = mu0Sim(dyno); S0Sim = S0Sim(dyno,dyno);

% 3. Controlled learning (N iterations)
for j = 1:N
%   if j == 1
%     tr = 1;
%   else
%     tr = 0;
%   end
  trainDynModel;   % train (GP) dynamics model
  learnPolicy;     % learn policy
  applyController_new; % apply controller to system
  disp(['controlled trial # ' num2str(j)]);
%   if plotting.verbosity > 0;      % visualization of trajectory
%     if ~ishandle(1); figure(1); else set(0,'CurrentFigure',1); end; clf(1);
%     draw_rollout_pendulum;
%   end
end