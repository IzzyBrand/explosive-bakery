function MakeFakeCarlsonData(n)
%MAKEFAKECARLSONDATA Generate fake Carlson data
%   MAKEFAKECARLSONDATA(N) where N is the number of the log file to save
%
%14 August 2017, Benjamin Shanahan.

% flight params
recordDur  = 300;    % (s) Carlson total recording time
dt         = 0.01;   % (s) length of each time step recorded (on average)
offset     = 1;      % (s) time post-boot before recording starts
thrustG    = 16;     % (G) rocket max accel G-force
% thrustTime = 10;     % (s) how long is the rocket accelerating upwards?
apogeeTime = 11.5;   % (s) when do we reach apogee?
% gravity    = -9.81;  % (m/s^2) acceleration due to gravity
groundTemp = -2500;  % (?) MPU's temperature reading at ground level

% open text file for writing
if nargin == 0, n = 1; end
fid = fopen(sprintf('LOG_%02d.txt',n),'a');

% calculate some stuff
nTics = recordDur / dt;  % how many samples do we take overall?

% generate fake data
for t = 1:nTics
    
    % get timestamp and add some slop
    timestamp = (offset + dt*t + rand*dt*2-dt) * 1000;
    
    % TODO: make this simulate rocket thrusting with slight horizontal
    % deviations, but very minimal (maybe smooth them and add them in after
    % to simulate drift?)
    % NOTE: X and Z are swapped due to MPU orientation
    accel  = [rand*thrustG rand-.5 rand-.5];
    
    % TODO: add slight gyro drift, add gyro flip once apogee is reached
    % (thrust stops and fall starts)
    gyro = [rand-.5 rand-.5 rand-.5];
    
    % TODO: make temperature inversely dependent to altitude
    temperature = groundTemp + rand*10;
    
    % TODO: make microphone reading increase greatly during thrust,
    % decrease as rocket reaches apogee, and then increase again as rocket
    % begins fall descent
    microphone = rand*2;
    
    % have we reached apogee?
    if t > (apogeeTime / dt)
        flags = 1;  % bit field flag indicating manual deploy
    else
        flags = 0;  % chute not deployed
    end
    
    % write generated data at this time step to our log file
    fprintf(fid, '%.6f,\t', ...
        [timestamp accel gyro temperature microphone]);
    fprintf(fid, '%d\r\n', flags);
    
end

% clean up
fclose(fid);

end