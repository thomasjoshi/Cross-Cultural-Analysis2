%Calculate purity
function [purity] = cal_purity_parafac_soft_tri_weight(XX, ori_A, ori_B, ori_C)



A = ori_A;
B = ori_B;
C = ori_C;


A_index = A(:,1);
for i = 2 : size(A, 2)
	A_index = A_index + A(:,i);
end
B_index = B(:,1);
for j = 2: size(B, 2)
	B_index = B_index + B(:,j);
end
C_index = C(:,1);
for k = 2: size(C, 2)
	C_index = C_index + C(:,k);
end
A_index = find(A_index>0);
whos A_index
B_index = find(B_index>0);
whos B_index
C_index = find(C_index>0);
whos C_index
pause
num_group = size(A,2); %number of groups
for g = 1 : num_group
	base = 0;
	up = 0;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	temp_a_index = find(A(:,g) > 0);
	temp_b_index = find(B(:,g) > 0);
	temp_c_index = find(C(:,g) > 0);

	inter_a_b = sum(sum(sum(XX(temp_a_index, temp_b_index, :))));
	inter_a_c = sum(sum(sum(XX(temp_a_index, :, temp_c_index))));
	inter_b_c = sum(sum(sum(XX(:,temp_b_index, temp_c_index))));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% out index

	all_a_b = sum(sum(sum(XX(A_index, B_index, :))));
	
	all_a_c = sum(sum(sum(XX(A_index, :, C_index))));
	all_b_c = sum(sum(sum(XX(:,B_index, C_index))));


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%pause
	base = all_a_b + all_a_c + all_b_c;
	up = inter_a_b + inter_a_c + inter_b_c;



	up/base


end

