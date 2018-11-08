function [d] = eucdist(W,X,Y,options);
%
%       Description
%       [D] = EUCDIST(W,X,Y)
%       Inputs:
%       W - m1 x n matrix
%       X - m1 x n  matrix 
%       Y - m2 x n  matrix 
%       OPTIONS - in case we need to pass some extra arguments
%
%       Outputs:
%       D  - m1 * m2 matrix of distances
%
%-------------------------------------------------------------------------------
if(size(W) ~=size(X) | size(X,2) ~=size(Y,2))
     disp('Error: dimensions of the weight and input matrices do not match');
     return;
end

m2 = size(Y,1);
m1 = size(X,1);

for i=1:m2
d(:,i) = sum(W.*(X- ones(m1,1)*Y(i,:)).^2,2);
end





%d = (dist(X,Y')).^2;









