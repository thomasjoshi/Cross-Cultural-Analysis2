%Calculate purity
function [purity] = cal_purity_parafac_soft_weight(XX, ori_A, ori_B)



A = ori_A;
B = ori_B;


A_index = A(:,1);
for i = 2 : size(A, 2)
	A_index = A_index + A(:,i);
end
B_index = B(:,1);
for j = 2: size(B, 2)
	B_index = B_index + B(:,j);
end

A_index = find(A_index>0);
whos A_index
B_index = find(B_index>0);
whos B_index

pause
num_group = size(A,2); %number of groups
for g = 1 : num_group
	base = 0;
	up = 0;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	temp_a_index = find(A(:,g) > 0);
	temp_b_index = find(B(:,g) > 0);
	
	this_a = sum(sum(XX(temp_a_index, B_index,1)));
	this_b = sum(sum(XX(A_index, temp_b_index,1)));
	this_small = sum(sum(XX(temp_a_index, temp_b_index,1)));

	%pause
	base = base + this_a + this_b - this_small;
	up = up + this_small;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



	purity(g) = up/base;


end


