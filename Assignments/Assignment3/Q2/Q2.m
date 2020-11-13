% p2.slx must be run first to gain simulation results (utilizations)
n = 5;

util1 = mean(utilizationSimulated1.Data);
util2 = mean(utilizationSimulated2.Data);
util3 = mean(utilizationSimulated3.Data);
util4 = mean(utilizationSimulated4.Data);
util5 = mean(utilizationSimulated5.Data);

lambda = 2; % interarrival ~ exp(2)
mu = 3; % serviceTime ~ N(3, 0.04)

util = min(1, (1 / lambda) ^ 3 * (mu ^ 2));

utils = [util1, util2, util3, util4, util5];
evalUtilMean = mean(utils);

evalUtilVar = var(utils);

pivotal = abs(evalUtilMean - util) / (sqrt(evalUtilVar) / sqrt(n));

pValue = 1 - tcdf(pivotal, n - 1);

confidenceLevel = 0.05;
display(pValue);
display(confidenceLevel);

if pValue < confidenceLevel
    display("We reject H0 therefore the model stated is not validated!");
else 
    display("We can not reject H0 therefore the model stated is validated by this test!");
end







