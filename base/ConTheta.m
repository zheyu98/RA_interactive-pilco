function [theta] = ConTheta(theta)
%CONTHETA Summary of this function goes here
%   Detailed explanation goes here
    theta(abs(theta) >= 2*pi)=sign(theta(abs(theta) >= 2*pi)).*mod(abs(theta(abs(theta) >= 2*pi)),2*pi);
    mask=theta >= 0;
    theta(mask)=theta(mask)-pi;
    theta(~mask)=theta(~mask)+pi;
end

