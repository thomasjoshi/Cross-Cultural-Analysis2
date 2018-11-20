
load bi_relation_mat.mat
[new_mat, col, row] = FilterSparseData(bi_relation_mat, 3);
whos new_mat
save('new_mat.mat','new_mat')
[row_clust_ids, col_clust_ids,y_index,x_index]=PlotCoClustering(new_mat, 10);

