function [l_v l_s l_t] = select_parameter(X, mean_v, mean_s, mean_t)

%select l_v
max_norm = 0; 
for i = 1 : size(X,1)
	thisnorm = norm(squeeze(X(i,:,:)));
	if thisnorm > max_norm
		max_norm = thisnorm;
	end
end
l_v = 0.0001*mean_s*mean_t*max_norm;

%select l_s
max_norm = 0; 
for j = 1 : size(X,2)
	thisnorm = norm(squeeze(X(:,j,:)));
	if thisnorm > max_norm
		max_norm = thisnorm;
	end
end
l_s = 0.0001*mean_v*mean_t*max_norm;

%select l_t
max_norm = 0; 
for k = 1 : size(X,3)
	thisnorm = norm(squeeze(X(:,:,k)));
	if thisnorm > max_norm
		max_norm = thisnorm;
	end
end
l_t = 0.0001*mean_s*mean_v*max_norm;
