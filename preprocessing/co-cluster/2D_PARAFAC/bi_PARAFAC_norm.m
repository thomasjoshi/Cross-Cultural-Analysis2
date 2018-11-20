function [A,B,rho_vec,iterations]=bi_SPARAFAC_norm(X,F,lambA,lambB,SMALLNUMBER)
if nargin==4
   SMALLNUMBER=10^-8;
end
MAXNUMITER = 10000;
quiet=1;
% F is # of co-clusters
[I J]=size(X);
A=zeros(I,F);B=zeros(J,F);
rho_vec=zeros(1,F);
iterations = zeros(1,F);
% allcosts=zeros(F,MAXNUMITER);
%One component at a time

for f = 1:F

    [a b rho it cost] = SPARAFAC_norm_rank_one(X,lambA,lambB,SMALLNUMBER);
    iterations(f) = it;
    rho_vec(f)=rho;
    unfolded= rho*a * b';
    %pause;
    A(:,f)=a;B(:,f)=b; 
    X = X - unfolded;
    %pause
    disp(sprintf('Calculated component %d, iterations: %d, fit=%12.10f, ',f,it,cost))
end
end

function [a b rho it cost] = SPARAFAC_norm_rank_one(X,lambA,lambB,SMALLNUMBER)
    model=zeros(size(X));
    quiet=1;
    MAXNUMITER = 10000;
    [I J]=size(X);
    % Used in the A-update step:
    UA = X';   % J by I

    % Used in the B-update step:
    UB = X ;   % I by J
    % [W,H] = nnmf(A,k) factors the nonnegative n-by-m matrix A into nonnegative factors W (n-by-k) and H (k-by-m). The factorization is not exact; W*H is a lower-rank approximation to A. The factors W and H are chosen to minimize the root-mean-squared residual D between A and W*H:

    [a, b] = nnmf(X,1)  % [W,H] = nnmf(A,k)
    b = b';  % J-by-1
    a_s=(max(a));a=a/a_s;
    b_s=(max(b));b=b/b_s;
   
    rho = a_s*b_s;
    rho_bound = max(max(X));
    
    %now begin the ALS iteration
    cost = norm(X - a*b' ,'fro')^2 + lambA*sum(sum(abs(a))) + lambB*sum(sum(abs(b)));
    costold = 2*cost;
    it = 0;
    while abs((cost-costold)/costold) > SMALLNUMBER && it < MAXNUMITER && cost > 10^5*eps
        it=it+1;
        costold=cost;
       
        %re-estimate A:
        a = SMR_01(UA,b ,a,lambA);
        %update rho
        rho = min(rho_bound, scalar_nnls(UA, b*a'));
        % re-estimate B:
        b = SMR_01(UB,a ,b,lambB);
        %update rho
        rho = min(rho_bound,scalar_nnls(UB, a*b'));
        
        
        cost = 0;
        cost = cost + norm(X-a*b','fro')^2;
        % add sparse regularization part of the cost:
        cost = cost + lambA*(sum(abs(a))) + lambB*(sum(abs(b)));
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


