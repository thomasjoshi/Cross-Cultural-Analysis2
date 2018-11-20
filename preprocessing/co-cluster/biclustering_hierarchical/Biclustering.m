function [row_clust_idx, col_clust_idx, y_index, x_index]=Biclustering(A, k_row, k_col)
% ===== INPUT =====
% A: MxN input data matrix, where M is the number of examples/voxels; N is
% the dimensionality of the feature
% k_row: the number of cluster in row
% k_col: the number of cluster in column
% ===== OUTPUT =====
% row_clust_idx: the cluster label given to each row of matrix A, thus, 
% the order is with respect to the original matrix A.
% col_clust_idx: the cluster label given to each col of matrix A, thus, 
% the order is with respect to the original matrix A.
% y_index: The row permutation matrix to convert the original space to the new 
% biclustering space. That is, A_row_rearranged = A(y_index,:). 
% x_index: The column permutation matrix to convert the original space to the new 
% biclustering space. That is, A_col_rearranged = A(:,x_index).
%
% Last updated: Thu, Nov 23, 2012
% =======================================
% Kittipat "Bot" Kampa
% kittipat@gmail.com
% Integrated Brain Imaging Center (IBIC)
% University of Washington
% =======================================
%%
[numRow,numCol] = size(A);
% row_name = 1:numRow; row_name = num2cell(row_name);
% col_name = 1:numCol; col_name = num2cell(col_name);


%% Hierarchical clustering along the column
method = 'average';
metric = 'euclidean';

% build hierarchical tree clustering row and column separately
tree_row = linkage(A,method,metric);
tree_col = linkage(A',method,metric);

% Group the row according to the desired number
figure; 
subplot(2,1,1);
[~,row_clust_idx,perm_row] = dendrogram(tree_row,k_row);
title('dendrogram of row');

% Group the col according to the desired number
subplot(2,1,2);
[~,col_clust_idx,perm_col] = dendrogram(tree_col,k_col);
title('dendrogram of column');

% Get the permutation vector
[y_index, y_label] = findPermutationIndex(1:numRow, row_clust_idx, perm_row );
[x_index, x_label] = findPermutationIndex(1:numCol, col_clust_idx, perm_col );

