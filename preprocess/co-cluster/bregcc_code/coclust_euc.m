function [R,C] = coclust_euc(Z,W,k,l,scheme, options);
%
%	Description
%	[R,C] = COCLUST_SCH2(Z,K,L,OPTIONS)
%       Inputs: 
%       Z - m x n data matrix, 
%       W - m x n measure matrix, 
%       k - num row clusters,
%       l - num col clusters
%       scheme - co-clustering scheme (1-6)
%       OPTIONS(1) - precision of obj fun for convergence; default 1e-3.
%       OPTIONS(2) - max iterations; default 20
%       OPTIONS(3) - max runs; default 5
%       OPTIONS(4) - precision of matrix elements: default 10^(-8)
%
%       Outputs:
%       R - final row clustering , 
%       C - final column clustering
% 
%------------------------------------------------------------------------------


% Sort out the options
noptions =size(options,1);

if (noptions < 1)
  errobj = 0.0001;
else 
  errobj = options(1)
end

if (noptions < 2)
    niters = 20; 
 else  
    niters = options(2);  
 end

if (noptions < 3)
    nruns = 5 ; 
 else  
    nruns = options(3);  
 end

if (noptions < 4)
    epsilon =10^(-8);
 else  
    epsilon = options(4);  
 end

 
% get data matrix size
[m, n] = size(Z); 
Y =W.*Z;
Em = ones(m,1);
En = ones(n,1);
Gavg = (Em'*Y*En)/(Em'*W*En);
Ravg = ((Y*En)+Gavg*epsilon)./((W*En)+epsilon);
Cavg = ((Em'*Y)+Gavg*epsilon)./((Em'*W)+epsilon);


%------------------------------------------------------------------------------
% Loop over the runs

for r =1:nruns 

% Randomly initialize row and column clusterings
idk = eye(k);
idl = eye(l);
pr(:,1)= randperm(m)';
for g=1:k
pr(((g-1)*floor(m/k) +1) : g*floor(m/k), 2) = g;
end
pr(k*floor(m/k):m,2) = k;
pr = sortrows(pr,[1]);
R =idk(pr(:,2),:);
pc(:,1)= randperm(n)';
for h=1:l
pc( ((h-1)*floor(n/l) +1):h*floor(n/l),2) = h;
end
pc(l*floor(n/l):n,2) = l;
pc = sortrows(pc,[1]);
C =idl(pc(:,2),:);




% Main loop of algorithm
e = 2*errobj;
old_e = 0;
s = 1; 
while ( (abs(e-old_e) > errobj) & (s <= niters) )  

% Obtain all the averages
CoCavg = (R'*Y*C +Gavg*epsilon)./(R'*W*C +epsilon);
RCavg = (R'*Y*En +Gavg*epsilon)./(R'*W*En +epsilon);
CCavg = (Em'*Y*C +Gavg*epsilon)./(Em'*W*C +epsilon);
RC_Cavg =(R'*Y +Gavg*epsilon)./(R'*W +epsilon);
CC_Ravg =(Y*C +Gavg*epsilon)./(W*C +epsilon);



% Pick Zrowv and Zrowc based on the scheme
switch scheme
 case 1
   Zrowc = Em*CCavg*C'-Em*Gavg*En';
   Zrowv = RCavg*En';
 case 2 
   Zrowc = zeros(m,n);
   Zrowv = CoCavg*C';
 case 3
  Zrowc = Ravg*En';
  Zrowv = CoCavg*C' - RCavg*En';
 case 4
   Zrowc = Em*Cavg -Em*CCavg*C';
   Zrowv = CoCavg*C';
 case 5
  Zrowc = Ravg*En' +Em*Cavg -Em*CCavg*C';
  Zrowv = CoCavg*C' - RCavg*En';
 case 6 
  Zrowc = CC_Ravg*C';
  Zrowv = RC_Cavg- CoCavg*C';
end


% Calculate distance based on row approximation
d2 = eucdist(W, (Z- Zrowc), Zrowv,[]);

% Assign to best row cluster
[minvals, index] = min(d2', [], 1);
R = idk(index,:);

% Pick Zcolv and Zcolc based on the scheme
switch scheme
 case 1
  Zcolc = R*RCavg*En' -Em*Gavg*En';
  Zcolv = Em*CCavg;
 case 2  
  Zcolc = zeros(m,n);
  Zcolv = R*CoCavg;  
 case 3
  Zcolc = Ravg*En' - R*RCavg*En';
  Zcolv = R*CoCavg; 
 case 4
  Zcolc = Em*Cavg ;
  Zcolv = R*CoCavg -Em*CCavg;
 case 5
  Zcolc = Ravg*En' +Em*Cavg - R*RCavg*En';
  Zcolv = R*CoCavg -Em*CCavg;
 case 6 
  Zcolc = R*RC_Cavg;
  Zcolv = CC_Ravg -R*CoCavg;
end

  
% Calculate distance based on column approximation
d2 = eucdist(W', (Z- Zcolc)', Zcolv',[]);

% Assign to best column cluster
[minvals, index] = min(d2', [], 1);
C = idl(index,:);


% Error value 
old_e = e;
e = sum(minvals.^2);
s = s+1;
end           % Loop s


Rfinalobj(r) = e ;
RR{r} = R;
RC{r} = C;


end           % Loop r

[val,ind] = min(Rfinalobj);
R=  RR{ind};
C=  RC{ind};

