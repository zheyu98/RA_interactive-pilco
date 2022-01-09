function dz = dynamics_pendulum_real(t,z,u)

J = 0.000189238; % Pendulum inertia
m = 0.0563641; % Pendulum mass
g = 9.81; % acceleration due to gravity
l = 0.0437891; % Pendulum length
b0 = 0.000142205; % Viscous damping
K = 0.0502769; % Torque constant
R = 9.83536; % Rotor resistance
c = 1.49553; % Standard deviation of Gaussian that is added to b around 0
a = 0.00183742; % Amplitude of Gaussian that is added to b around 0

b = b0 + a * exp(- z(1) * z(1) / (c * c));

tau_gravity = -m * g * l * sin(z(2));
tau_damping = (b + K * K / R) * z(1);
tau_motor = (K / R) * u(t);

dz = zeros(2,1);
dz(2)= z(1); 
dz(1) = (tau_gravity - tau_damping + tau_motor) / J;