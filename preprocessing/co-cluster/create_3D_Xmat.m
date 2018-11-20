function X = create_3D_Xmat()


folder = 'timeline_matrix/';

timeline = 19;
for i = 1:timeline
    s = num2str(i-1,'v_t_%d.mat');
    temp = strcat(folder,s);
    load(temp);
    X(:,:,i) = v_t;
end

%smooth alongtime
%matsize = size(X);
%for i = 1 : matsize(1)
%    for j = 1 : matsize(2)
%        for k = 3 : matsize(3)-2
%	    X(i,j,k-2) = X(i,j,k-2) + X(i,j,k)*0.2;
%	    X(i,j,k-1) = X(i,j,k-1) + X(i,j,k)*0.5;
%	    X(i,j,k+1) = X(i,j,k+1) + X(i,j,k)*0.5;
%	    X(i,j,k+2) = X(i,j,k+2) + X(i,j,k)*0.2;
%	end
%   end
%end
