
function [Za] = minbregsol_idiv(Z,W,R,C,scheme,options);
%
%	Description
%	[R,C] = MINBREGSOL_IDIV(Z,W,R,C,SCHEME,OPTIONS)
%       Inputs: 
%       Z - m x n data matrix, 
%       W - m x n measure matrix, 
%       R - final row clustering , 
%       C - final column clusterin
%       SCHEME - co-clustering scheme (1-6)
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
Em = ones(m,1);
En = ones(n,1);
Gavg = (Em'*Y*En)/(Em'*W*En);
Ravg = ((Y*En)+Gavg*epsilon)./((W*En)+epsilon);
Cavg = ((Em'*Y)+Gavg*epsilon)./((Em'*W)+epsilon);
CoCavg = (R'*Y*C +Gavg*epsilon)./(R'*W*C +epsilon);
RCavg = (R'*Y*En +Gavg*epsilon)./(R'*W*En +epsilon);
CCavg = (Em'*Y*C +Gavg*epsilon)./(Em'*W*C +epsilon);
RC_Cavg =(R'*Y +Gavg*epsilon)./(R'*W +epsilon);
CC_Ravg =(Y*C +Gavg*epsilon)./(W*C +epsilon);

switch scheme
 case 1
   Za = ((Em*CCavg*C').*(R*RCavg*En'))./(Em*Gavg*En');
 case 2 
   Za = R*CoCavg*C'; 
 case 3
  Za = ((Ravg*En').*(R*CoCavg*C'))./(R*RCavg*En');
 case 4
  Za =((Em*Cavg).*(R*CoCavg*C'))./(Em*CCavg*C');	
 case 5
  Za = ((Ravg*En').*(Em*Cavg).*(R*CoCavg*C'))./((R*RCavg*En').*(Em*CCavg*C'));
 case 6 
  Za = ((CC_Ravg*C').*(R*RC_Cavg))./(R*CoCavg*C');
end






