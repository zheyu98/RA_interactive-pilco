% 1. Initialization
clear all; close all;
settings_pendulum_sim;            % load scenario-specific settings
basename = 'pendulum_';       % filename used for saving data

load('controller_real2.mat','policy');

% 3. Control
if isfield(plant,'constraint'), HH = maxH; else HH = H; end
rollout_sim_on_real(policy, HH, plant, cost);