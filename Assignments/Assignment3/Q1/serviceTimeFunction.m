% consider the case in which our servers are humans and by passing time
% they become tired and their servicetimes increases 
function serviceTime = serviceTimeFunction(arrivalTime)
    mean = 0;
    if arrivalTime < 100
        mean = 1;
    elseif arrivalTime >= 100 && arrivalTime < 200
        mean = 2;
    elseif arrivalTime >= 200 && arrivalTime < 300
        mean = 3;
    elseif arrivalTime >= 300 && arrivalTime < 400
        mean = 4;
    else
        mean = 5;
    end   
    serviceTime = -mean*log(1-rand());
    
