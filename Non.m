clear all

% set syns variable

syms P0 P1 P2 a b alfa beta;
probility = [P0 P1 P2];
%[alfa, beta]= getConditionalProb([1,20,5], [1,15,3]);
% secomd solve

matrix = [0                  a*P0             0;
          beta * b*P1        0               alfa*a*P1;
          0                  b*P2            0];

count = size(matrix, 1);
eql = zeros(count, 'sym');

for j = 1:count
    eql(j) = sum(matrix(j,:)) == sum(matrix(:,j));
end

eql(count+1) = sum(probility) == 1;
sol2 = solve(eql, probility);


% funNormal = @(x, sigma, mu)exp(-((x- mu).^2)/(2*sigma.^2)) / (sigma*sqrt(2*pi));
% 
% funNormal2 = @(x, sko2, mu2)exp(-((x- mu).^2)/(2*sko.^2)) / (sko*sqrt(2*pi));
% 
% 
% 
% w = integral(@(x)funNormal2(x, sko2, mu2), 0, Inf)

ass = ['экспонта', 'гамма', 'нормальное', 'равномерно', 'релея'];













function [alfa, beta]= getConditionalProb(firstLaw, secondLaw)
    syms x
    %get probability density function
    pdfValue = pdf('Normal', x, firstLaw(2), firstLaw(3));
    
    %get cumulative distribution function
    cdfValue = cdf('Normal', x, secondLaw(2), secondLaw(3));
    
    %set formule conditional probability
    formuleCondProb = (1 - cdfValue)*pdfValue;
    
    %get alfa and beta
    alfa = vpaintegral(formuleCondProb, x, [-inf,inf]);
    beta = 1 - alfa;
end