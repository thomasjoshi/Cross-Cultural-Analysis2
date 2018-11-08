function [d] = idivdist2(W,Z,X,Y,options);

%       Description
%       [D] = IDIVDIST2(W,Z,X,Y)
%       Inputs:
%       W - m1 x n  matrix
%       Z - m1 x n  matrix 
%       X - m1 x n  matrix
%       Y - m2 x n  matrix 
%       OPTIONS(1) -precision of elements in the matrix: default 10^(-8)
%
%       Outputs:
%       D  - m1 * m2 matrix of idivergence comparison measure
%
%-------------------------------------------------------------------------------

if (options)
  epsilon = options(1);
else 
 epsilon = 10^(-8); 
end
 
% To prevent log of zero 
Y = Y + epsilon ;

d = (W.*X)*Y'-(W.*Z)*log(Y');


