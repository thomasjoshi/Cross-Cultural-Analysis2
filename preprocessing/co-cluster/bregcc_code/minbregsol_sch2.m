
function [Za] = minbregsol_sch2(Z,W,R,C,options);
%
%	Description
%	[R,C] = MINBREGSOL_SCH2(Z,W,R,C,OPTIONS)
%       Inputs: 
%       Z - m x n data matrix, 
%       W - m x n measure matrix, 
%       R - final row clustering , 
%       C - final column clustering
%       OPTIONS(4) - precision of matrix elements: default 10^(-8)
%
%       Outputs: 
%       Za - minimum Bregman information matrix
% 
%------------------------------------------------------------------------------


if (options)
   epsilon = options(1); 
else 
   epsilon = 10^(-8);
end


[m,n] = size(Z);
Y =W.*Z;
Gavg = (ones(1,m)*Y*ones(n,1))/(ones(1,m)*W*ones(n,1)); 
CoCavg = ((R'*Y*C) +Gavg*epsilon)./ ((R'*W*C) +epsilon);
Za = R*CoCavg*C'; 

