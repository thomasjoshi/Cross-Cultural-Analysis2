function AkrpB = krp(A,B);

[I F] = size(A);
[J F1] = size(B);

if (F1 ~= F)
 disp('krp.m: column dimensions do not match!!! - exiting matlab');
 exit;
end

AkrpB = [];
for f=1:F,
 AkrpB = [AkrpB kron(A(:,f),B(:,f))];
end