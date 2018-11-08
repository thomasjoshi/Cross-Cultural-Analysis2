

function [X_1, X_2, X_3 ] = optimize_parameter(X, I, J, N)

X_1=[];
for t = 1:J
	temp = X(:,t,:);
	temp = squeeze(temp);
	temp = temp';
	X_1 = [X_1;temp];
end

X_2=[];
for t = 1:N
	temp = X(:,:,t);
	temp = squeeze(temp);
	X_2 = [X_2;temp];
end

X_3=[];
for t = 1:I
	temp = X(t,:,:);
	temp = squeeze(temp);
	X_3 = [X_3;temp];
end
