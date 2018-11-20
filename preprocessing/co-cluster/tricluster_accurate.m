function [result] = tricluster_accurate(X,k)

addpath('NWAY')
addpath('2D_PARAFAC')
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

%[A,B,rho_vec,iterations]=bi_PARAFAC_norm(X,k,5,5);
[A,B,C,rho_vec,iterations]=SPARAFAC_norm(X,k,5,10,2);

%load ground truth
[gt_filename] = textread('cluster_name.txt', '%s');

for i = 1:k
load(gt_filename{2*(i-1)+1});
load(gt_filename{2*(i-1)+2});
tag_truth(:,i) = c_tag';
meme_truth(:,i) = c_meme';
end

%PARAFAC
P_cocluster_size = 0;
for c = 1:k
   P_cocluster_size(c) = size(find(A(:,c)>0),1)+size(find(B(:,c)>0),1);
end
[temp,P_order] = sort(P_cocluster_size);
compared = zeros(k,1);
ave_acc = 0;
th = 0.25;
for i = 1:k
    target_id = P_order(k-i+1);
    this_R = A(:,target_id);
    %this_R(this_R<th) = 0;
    this_C = B(:,target_id);
    %this_C(this_C<th) = 0;
    if (size(find(this_R>0),1) + size(find(this_C>0),1) == 0)
        continue;
    end
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





