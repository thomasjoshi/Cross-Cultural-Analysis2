function [result] = cocluster_accurate(X,k)

addpath('NWAY')
addpath('bregcc_code')
addpath('2D_PARAFAC')
addpath('KDD2001')
addpath('biclustering_hierarchical')
[v_name v_index] = textread('video_index', '%s %d');
[m_name m_index] = textread('visual_meme_index', '%s %d');
[t_name t_index] = textread('tag_index', '%s %d');


video = cell(size(v_index));
for i = 1 : size(v_index)
    video(v_index(i)+1) = v_name(i);
end

visualmeme = cell(size(m_index));
for i = 1 : size(m_index)
    visualmeme(m_index(i)+1) = m_name(i);
end
visualmeme

tag = cell(size(t_index));
for i = 1 : size(t_index)
    tag(t_index(i)+1) = t_name(i);
end 
tag

W = ones(size(X));
[IT_R,IT_C] = coclust_euc(X,W,k,k,1,0.0001);
[A,B,rho_vec,iterations]=bi_PARAFAC_norm(X,k,5,5);
%[Ad,Bd,rho_vecd,iterationsd]=bi_dPARAFAC_norm(X,k,5,5);

[row_clust_idx, col_clust_idx,y_index,x_index]=SpectralCoClustering(X,k);
[H_row_clust_idx, H_col_clust_idx, H_y_index, H_x_index]=Biclustering(X, k, k);

%load ground truth
[gt_filename] = textread('cluster_name.txt', '%s');

for i = 1:k
load(gt_filename{2*(i-1)+1});
load(gt_filename{2*(i-1)+2});
tag_truth(:,i) = c_tag';
meme_truth(:,i) = c_meme';
end
%IT
IT_cocluster_size = 0;
for c = 1:k
   IT_cocluster_size(c) = size(find(IT_R(:,c)>0),1)+size(find(IT_C(:,c)>0),1);
end
[temp,IT_order] = sort(IT_cocluster_size);
compared = zeros(k,1);
ave_acc = 0;
for i = 1:k
    target_id = IT_order(i);
    this_R = IT_R(:,target_id);
    this_C = IT_C(:,target_id);
    max_acc = 0;
    match_clust = 0;
    P = 0;
    R = 0;
    for j = 1:k
	if compared(j) == 1
	    continue;
	end
        test_meme = this_R & meme_truth(:,j);
	test_tag = this_C & tag_truth(:,j);
        neg_test_meme = (~this_R) & (~meme_truth(:,j));
	neg_test_tag = (~this_C) & (~tag_truth(:,j));

	num_match = size(find(test_meme)>0,1) + size(find(test_tag)>0,1);  % intersection
	outer_num_match = size(find(neg_test_meme)>0,1) + size(find(neg_test_tag)>0,1); 
 	gbase = size(this_R,1) + size(this_C,1);
	acc_RI = (num_match + outer_num_match) / gbase;

 	num_test_set = size(find(meme_truth(:,j)>0),1) + size(find(tag_truth(:,j)>0),1);
	num_detect_set = size(find(this_R>0),1) + size(find(this_C>0),1);
% Jaccurd	acc = num_match / (num_test_set + num_detect_set - num_match);

	precision = num_match / num_detect_set;
	recall = num_match / num_test_set;
	acc_f = (2*precision*recall) / (precision+recall); 
	if acc_f >= max_acc
		max_acc = acc_f;
		match_clust = j;
		P = precision;
		R = recall;
	end 
    end
    compared(match_clust) = 1;
    ave_acc = ave_acc + max_acc;
    all_acc(i) = max_acc;
end
ave_acc = ave_acc / k
all_acc
pause

%PARAFAC
P_cocluster_size = 0;
for c = 1:k
   P_cocluster_size(c) = size(find(A(:,c)>0),1)+size(find(B(:,c)>0),1);
end
[temp,P_order] = sort(P_cocluster_size);
compared = zeros(k,1);
ave_acc = 0;
th = 0.001;
for i = 1:k
    target_id = P_order(i);
    this_R = A(:,target_id);
    %this_R(this_R<th) = 0;
    this_C = B(:,target_id);
    %this_C(this_C<th) = 0;
    max_acc = 0;
    match_clust = 0;
    P = 0;
    R = 0;
    for j = 1:k
	if compared(j) == 1
	    continue;
	end
        test_meme = this_R & meme_truth(:,j);
	test_tag = this_C & tag_truth(:,j);
        neg_test_meme = (~this_R) & (~meme_truth(:,j));
	neg_test_tag = (~this_C) & (~tag_truth(:,j));

	num_match = size(find(test_meme)>0,1) + size(find(test_tag)>0,1);  % intersection
	outer_num_match = size(find(neg_test_meme)>0,1) + size(find(neg_test_tag)>0,1); 
 	gbase = size(this_R,1) + size(this_C,1);
	acc_RI = (num_match + outer_num_match) / gbase;

 	num_test_set = size(find(meme_truth(:,j)>0),1) + size(find(tag_truth(:,j)>0),1)
	num_detect_set = size(find(this_R>0),1) + size(find(this_C>0),1)
% Jaccurd	acc = num_match / (num_test_set + num_detect_set - num_match);

	precision = num_match / num_detect_set;
	recall = num_match / num_test_set;
	acc_f = (2*precision*recall) / (precision+recall); 
	if acc_f >= max_acc
		max_acc = acc_f;
		match_clust = j;
		P = precision;
		R = recall;
	end 
    end
    compared(match_clust) = 1;
    ave_acc = ave_acc + max_acc;
    all_acc(i) = max_acc;
end
ave_acc = ave_acc / k
all_acc
pause




%SPECTRAL
S_cocluster_size = 0;
for c = 1:k
   S_cocluster_size(c) = size(find(row_clust_idx==c),1)+size(find(col_clust_idx==c),1);
end
[temp,S_order] = sort(S_cocluster_size);
compared = zeros(k,1);
ave_acc = 0;
group = 0;
for i = 1:k
    target_id = S_order(i);
    this_R = zeros(size(row_clust_idx)); 
    this_R(find(row_clust_idx==target_id)) = 1;
    this_C = zeros(size(col_clust_idx)); 
    this_C(find(col_clust_idx==target_id)) = 1;
    max_acc = 0;
    match_clust = 0;
    P = 0;
    R = 0;
    for j = 1:k
	if compared(j) == 1
	    continue;
	end
        test_meme = this_R & meme_truth(:,j);
	test_tag = this_C & tag_truth(:,j);
        neg_test_meme = (~this_R) & (~meme_truth(:,j));
	neg_test_tag = (~this_C) & (~tag_truth(:,j));

	num_match = size(find(test_meme)>0,1) + size(find(test_tag)>0,1)  % intersection
	%if num_match == 0
	%    continue;
        %end
	outer_num_match = size(find(neg_test_meme)>0,1) + size(find(neg_test_tag)>0,1); 
 	gbase = size(this_R,1) + size(this_C,1);
	acc_RI = (num_match + outer_num_match) / gbase;

 	num_test_set = size(find(meme_truth(:,j)>0),1) + size(find(tag_truth(:,j)>0),1);
	num_detect_set = size(find(this_R>0),1) + size(find(this_C>0),1);
% Jaccurd	acc = num_match / (num_test_set + num_detect_set - num_match);

	precision = num_match / num_detect_set;
	recall = num_match / num_test_set;
	acc_f = (2*precision*recall) / (precision+recall); 
	if acc_f >= max_acc
		max_acc = acc_f;
		match_clust = j;
		P = precision;
		R = recall;
	end 
    end
    %i 
    %match_clust
    max_acc
    if match_clust > 1
        compared(match_clust) = 1;
    end
    %if max_acc ~= 0
%	group = group +1;
 %   end
    ave_acc = ave_acc + max_acc;
    all_acc(i) = max_acc;
end
ave_acc = ave_acc / k
all_acc
pause

%H
H_cocluster_size = 0;
for c = 1:k
   H_cocluster_size(c) = size(find(H_row_clust_idx==c),1)+size(find(H_col_clust_idx==c),1);
end
[temp,H_order] = sort(H_cocluster_size);
compared = zeros(k,1);
ave_acc = 0;
group = 0;
for i = 1:k
    target_id = H_order(i);
    this_R = zeros(size(H_row_clust_idx)); 
    this_R(find(H_row_clust_idx==target_id)) = 1;
    this_C = zeros(size(H_col_clust_idx)); 
    this_C(find(H_col_clust_idx==target_id)) = 1;
    max_acc = 0;
    match_clust = 0;
    P = 0;
    R = 0;
    for j = 1:k
	if compared(j) == 1
	    continue;
	end
        test_meme = this_R & meme_truth(:,j);
	test_tag = this_C & tag_truth(:,j);
        neg_test_meme = (~this_R) & (~meme_truth(:,j));
	neg_test_tag = (~this_C) & (~tag_truth(:,j));

	num_match = size(find(test_meme)>0,1) + size(find(test_tag)>0,1)  % intersection
	%if num_match == 0
	%    continue;
        %end
	outer_num_match = size(find(neg_test_meme)>0,1) + size(find(neg_test_tag)>0,1); 
 	gbase = size(this_R,1) + size(this_C,1);
	acc_RI = (num_match + outer_num_match) / gbase;

 	num_test_set = size(find(meme_truth(:,j)>0),1) + size(find(tag_truth(:,j)>0),1);
	num_detect_set = size(find(this_R>0),1) + size(find(this_C>0),1);
% Jaccurd	acc = num_match / (num_test_set + num_detect_set - num_match);

	precision = num_match / num_detect_set;
	recall = num_match / num_test_set;
	acc_f = (2*precision*recall) / (precision+recall); 
	if acc_f >= max_acc
		max_acc = acc_f;
		match_clust = j;
		P = precision;
		R = recall;
	end 
    end
    %i 
    %match_clust
    max_acc
    if match_clust > 1
        compared(match_clust) = 1;
    end
    if max_acc ~= 0
	group = group +1;
    end
    ave_acc = ave_acc + max_acc;
    all_acc(i) = max_acc;
end
ave_acc = ave_acc / group
all_acc
pause

