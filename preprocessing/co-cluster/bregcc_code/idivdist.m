function [d] = idivdist(W,X,Y,options);

%
%       Description
%       [D] = IDIVDIST(X,Y,OPTIONS)
%       Inputs:
%       W - m1 x n  matrix
%       X - m1 x n  matrix 
%       Y - m2 x n  matrix 
%       OPTIONS(1) - precision of matrix elements: default 10 ^(-8)
% 
%       Outputs:
%       D  - m1 * m2 matrix of distances
%
%-------------------------------------------------------------------------------

if(size(W) ~=size(X) | size(X,2) ~=size(Y,2))
     disp('Error: dimensions of the weight and input matrices do not match');
end

m2 = size(Y,1);
m1 = size(X,1);
n  =  size(X,2);

% Check if non-negative
if (find(X <0)| find(Y<0)) 
     disp('Error: Input matrices  have negative entries');
     return; 
end

if (options)
  epsilon = options(1);
else 
  epsilon = 10^(-8);
end
  

% To prevent zero logs in X and Y
X = X + epsilon;
Y = Y + epsilon;

d =sum(W.*(X.*(log(X) -1)),2)*ones(1,m2) - (W.*X)*(log(Y))' -W*Y';










