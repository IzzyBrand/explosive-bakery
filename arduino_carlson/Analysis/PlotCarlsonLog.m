function PlotCarlsonLog(n)
%PLOTCARLSONLOG Plot Carlson log file
%   PLOTCARLSONLOG(N) where N is the number of the log file to load
%
%   NOTE: see subsections below for generating analysis plots
%
%14 August 2017, Benjamin Shanahan.

filename = sprintf('LOG_%02d.txt',n);
data     = csvread(filename);    % load data

% extract all data
startIdx = 3000;  % define this in post
timestamp   = data(startIdx:end,1);
accel       = data(startIdx:end,[2 3 4]);  % switch X and Z values
gyro        = data(startIdx:end,[5 6 7]);  % switch X and Z values
temperature = data(startIdx:end,8);
microphone  = data(startIdx:end,9);
flags       = data(startIdx:end,10);

% plotting data
h = figure;
lbls = {};
hold on;
window = 100;  % smoothing Gaussian window size

%% Plot Acceleration (accelerometer)
% Raw
if true
%     plot(timestamp, accel(:,1));  lbls = [lbls; 'Accel X (G)'];
%     plot(timestamp, accel(:,2));  lbls = [lbls; 'Accel Y (G)'];
    plot(timestamp, accel(:,3));  lbls = [lbls; 'Accel Z (G)'];
end
% Smoothed
if false
    plot(timestamp, smsig(accel(:,1),window));  lbls = [lbls; 'Smoothed Accel X (G)'];
    plot(timestamp, smsig(accel(:,2),window));  lbls = [lbls; 'Smoothed Accel Y (G)'];
    plot(timestamp, smsig(accel(:,3),window));  lbls = [lbls; 'Smoothed Accel Z (G)'];
end

%% Plot Angular Acceleration (gyroscope)
% Raw
if false
    plot(timestamp, gyro(:,1));  lbls = [lbls; 'Gyro X (deg/s^2)'];
    plot(timestamp, gyro(:,2));  lbls = [lbls; 'Gyro Y (deg/s^2)'];
    plot(timestamp, gyro(:,3));  lbls = [lbls; 'Gyro Z (deg/s^2)'];
end
% Smoothed
if false
    plot(timestamp, smsig(gyro(:,1),window));  lbls = [lbls; 'Gyro X (deg/s^2)'];
    plot(timestamp, smsig(gyro(:,2),window));  lbls = [lbls; 'Gyro Y (deg/s^2)'];
    plot(timestamp, smsig(gyro(:,3),window));  lbls = [lbls; 'Gyro Z (deg/s^2)'];
end

%% Plot Other Readings (temperature, microphone, chute status)
% Raw
if true
%     plot(timestamp, temperature); lbls = [lbls; 'Temperature (?)'];
%     plot(timestamp, microphone);  lbls = [lbls; 'Microphone (Volts)'];
    plot(timestamp, flags);       lbls = [lbls; 'Flags'];
end
% Smoothed
if false
    plot(timestamp, smsig(temperature,window)); lbls = [lbls; 'Temperature'];
    plot(timestamp, smsig(microphone,window));  lbls = [lbls; 'Microphone'];
    plot(timestamp, smsig(flags,window));       lbls = [lbls; 'Flags'];
end

%% continue
hold off;
legend(lbls);
xlim([timestamp(1) timestamp(end)]);
xlabel('Time (s)');

    function sm = smsig(data,windowSize)
        %SMSIG Smooth data using Gaussian window
        %   SMSIG(DATA,WINDOWSIZE) Smooth inputted data via a Gaussian
        %   window function.
        %
        %21 April 2015, Benjamin Shanahan.
        
        if mod(windowSize, 2) ~= 0
            error('windowSize must be an even number.');
        end
        
        half = windowSize / 2;
        filt = gausswin(windowSize); % create filter
        filt = filt / sum(filt); % normalize
        sm_pre = conv(data, filt); % convolve w filter
        
        sm = sm_pre(half : (end - half)); % return 
    end

end