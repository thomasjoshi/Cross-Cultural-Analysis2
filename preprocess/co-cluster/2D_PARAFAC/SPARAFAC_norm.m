function [A,B,C,rho_vec,iterations]=SPARAFAC_norm(X,F,lambA,lambB,lambC,SMALLNUMBER)
%Evangelos E. Papalexakis, Nicholas D. Sidiropoulos, Rasmus Bro
%Sparse PARAFAC with imbalanced penalties and non-negative factors
%as introduced in: From K-means to higher-way co-clustering: multilinear decomposition with sparse latent factors
%IEEE Transactions on Signal Processing, 2013

if nargin==5
   SMALLNUMBER=10^-8;
end
MAXNUMITER = 10000;
quiet=1;
[I J K]=size(X);
A=zeros(I,F);B=zeros(J,F);C=zeros(K,F);
rho_vec=zeros(1,F);
iterations = zeros(1,F);
% allcosts=zeros(F,MAXNUMITER);
%One component at a time

for f = 1:F

    [a b c rho it cost] = SPARAFAC_norm_rank_one(X,lambA,lambB,lambC,SMALLNUMBER);
    f
    iterations(f) = it;
    rho_vec(f)=rho;
    folded=rho*krp(a,b)*c';
    unfolded=zeros(size(X));
    for ii=1:I
        unfolded(ii,:,:)=folded((ii-1)*J+1:ii*J,:);       
    end   
    A(:,f)=a;B(:,f)=b;C(:,f)=c;   
    X = X - unfolded;
    disp(sprintf('Calculated component %d, iterations: %d, fit=%12.10f, ',f,it,cost))
end
end

function [a b c rho it cost] = SPARAFAC_norm_rank_one(X,lambA,lambB,lambC,SMALLNUMBER)
    model=zeros(size(X));
    quiet=1;
    MAXNUMITER = 10000;
    [I J K]=size(X);
  % Used in the A-update step:
    UA = zeros(K*J,I);
    for j=1:J,
      UA((j-1)*K+1:j*K,:) = squeeze(X(:,j,:)).';
    end

    % Used in the B-update step:
    UB = zeros(I*K,J);
    for k=1:K,
      UB((k-1)*I+1:k*I,:) = squeeze(X(:,:,k));
    end

    % Used in the C-update step:
    UC = zeros(J*I,K);
    for i=1:I,
      UC((i-1)*J+1:i*J,:) = squeeze(X(i,:,:));
    end
    
    % initial estimates: 
    Options(2)=1;Options(5)=NaN;
    factors=parafac(X,1,Options,[2 2 2]);
    a=factors{1};b=factors{2};c=factors{3};

    a_s=(max(a));a=a/a_s;
    b_s=(max(b));b=b/b_s;
    c_s=(max(c));c=c/c_s;
   
    rho = a_s*b_s*c_s;
    rho_bound = max(max(max(X)));
    
    %now begin the ALS iteration
    cost = norm(UC - rho*krp(a,b)*c' ,'fro')^2 + lambA*sum(sum(abs(a))) + lambB*sum(sum(abs(b))) + lambC*sum(sum(abs(c)));
    costold = 2*cost;
    it = 0;
    while abs((cost-costold)/costold) > SMALLNUMBER && it < MAXNUMITER && cost > 10^1*eps
        it=it+1;
        costold=cost;
       
        %re-estimate A:
        a = SMR_01(UA,rho*krp(b,c),a,lambA);
        %update rho
        rho = min(rho_bound, scalar_nnls(UA,krp(b,c)*a'));
        % re-estimate B:
        b = SMR_01(UB,rho*krp(c,a),b,lambB);
        %update rho
        rho = min(rho_bound,scalar_nnls(UB,krp(c,a)*b'));
        % re-estimate C:
        c = SMR_01(UC,rho*krp(a,b),c,lambC);
        %update rho
        rho = min(rho_bound, scalar_nnls(UC,krp(a,b)*c'));
        
        
        cost = 0;
        for k=1:K,
            model(:,:,k) = rho*a*diag(c(k,:))*b.';
            cost = cost + norm(squeeze(X(:,:,k))-squeeze(model(:,:,k)),'fro')^2;
        end
        % add sparse regularization part of the cost:
        cost = cost + lambA*(sum(abs(a))) + lambB*(sum(abs(b))) + lambC*(sum(abs(c)));
%         allcosts(f,it) = cost;

             
%         fprintf('iteration: %d cost: %12.10f diff: %.12f\n',it,cost,abs((cost-costold)/costold));
        if costold < cost
            disp(['*** bummer! *** ',num2str(costold-cost)])
        end
    end

end

function s = scalar_nnls(X,A)
x = X(:);
a = A(:);
s = x'*a/(a.'*a);
if s < 0
    s = 0;
end
% s
end

function B = SMR_01(X,A,B,lambda)

[I,J]=size(X);
[I,F]=size(A);
maxit=10000;
convcrit = 1e-9;
it=0;
Oldfit=1e100;
Diff=1e100;

while Diff>convcrit && it<maxit
    it=it+1;
    for j=1:J,
        for f=1:F,
%             data = X(:,j);
            data = X(:,j) - A*B(j,:).' + A(:,f)*B(j,f);           
            alpha = A(:,f);

            diff= alpha'*data - lambda/2;
            if ( diff < 0)
                B(j,f) = 0;
            elseif ( diff > (alpha.'*alpha))
                B(j,f) = 1;
            else
                B(j,f)=diff/(alpha.'*alpha);
            end
            
        end
    end

    fit= norm(X-A*B.','fro')^2+ lambda*sum(sum(abs(B)));
    Diff=abs(Oldfit-fit);
%     sprintf('iter %d, %.10f',it, Diff)
    Oldfit=fit;

end
end

