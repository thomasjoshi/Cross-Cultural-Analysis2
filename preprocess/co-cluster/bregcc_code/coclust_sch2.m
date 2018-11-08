function [R,C] = coclust_sch2(Z,W,k,l, bregdist, options)
%
%	Description
%	[R,C] = COCLUST_SCH2(Z,K,L,OPTIONS)
%       Inputs: 
%       Z - m x n data matrix, 
%       W - m x n measure matrix, 
%       k - num row clusters,
%       l - num col clusters
%       bregdist - Bregman divergence
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
Gavg = (ones(1,m)*Y*ones(n,1))/(ones(1,m)*W*ones(n,1));




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

% obtain co-cluster averages
CoCavg = ((R'*Y*C) +Gavg*epsilon)./ ((R'*W*C) +epsilon);
%SM: might be more efficient to use CC_Ravg and RC_Cavg for large m, n
%CC_Ravg = (Y*C+Gavg*epsilon)./(W*C+epsilon); 
%RC_Cavg = (R'*Y+Gavg*epsilon)./(R'*W+epsilon); 


% Calculate distance based on row approximation
%d2=feval(bregdist, W*C,CC_Ravg, CoCavg,[])
d2 = feval(bregdist, W, Z, CoCavg*C',[]);



% Assign to best row cluster
[minvals, index] = min(d2', [], 1);
R = idk(index,:);

  
% Calculate distance based on column approximation
%d2 = feval(bregdist, (R'*W)', RC_Cavg', CoCavg',[]);
d2 = feval(bregdist, W', Z', (R*CoCavg)',[]);


% Assign to best column cluster
[minvals, index] = min(d2', [], 1);
C = idl(index,:);


% Error values 
old_e = e;
e = sum(minvals);
s = s+1;
end           % Loop s


Rfinalobj(r) = e ;
RR{r} = R;
RC{r} = C;

end           % Loop r

[val,ind] = min(Rfinalobj);
R=  RR{ind};
C=  RC{ind};

