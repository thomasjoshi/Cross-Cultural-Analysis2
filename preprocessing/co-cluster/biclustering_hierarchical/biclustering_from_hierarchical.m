%% Biclustering
% The program shows how to make biclustering algorithm based on the
% hierarchical clustering algorithm. This can be done by first clustering
% along row, then column, or vice versa. However, this method does NOT
% provide the subspace of the data. So, it's awkward to call this simple
% method "subspace clustering". Nevertheless, the advantages of this simple
% method are 1) it's simple 2) hierarchical 3) the number of cluster can be
% determined exactly by the user.
%
% We show: 1) How to perform biclustering the data based on hierarchical
% clustering algorithm.
% 2) How to get the permutation vector, and display the end results.
%
% Last updated: Thu, Nov 22, 2012
% =======================================
% Kittipat "Bot" Kampa
% kittipat@gmail.com
% Integrated Brain Imaging Center (IBIC)
% University of Washington
% =======================================

clear; close all; clc;
%% Load the data


x = [0 0 1 0 0 1 0 1;
     0 0 0 0 0 0 0 0;
     0 1 0 1 0 0 1 0;
     0 0 0 0 0 0 0 0;
     0 0 1 0 0 1 0 1;
     0 1 0 1 0 0 1 0];

A = x+0.01*randn(size(x)); 

row_name = {'1','2','3','4','5','6'};
col_name = {'1','2','3','4','5','6','7','8'};


%% Hierarchical clustering along the column
method = 'average';
metric = 'euclidean';
% cluster along row
tree_row = linkage(A,method,metric);
figure; subplot(2,1,1); title('Clustered along only row');
[~,T_row,perm_row] = dendrogram(tree_row,0); % 0 indicating # of clusters = # of examples
A_row = A(perm_row,:);
% cluster along column
tree_col = linkage(A',method,metric);
subplot(2,1,2); title('Clustered along only column');
[~,T_col,perm_col] = dendrogram(tree_col,0);
A_col = A(:,perm_col);
% cluster along both row then column
A_row_col = A_row(:,perm_col);

figure; 
subplot(2,2,1); imagesc(A); title('The original matrix');
subplot(2,2,3); imagesc(A_row); title('Clustered along only row');
set(gca,'YTick',[1:size(A,1)]); set(gca,'YTickLabel',row_name(perm_row)); 
subplot(2,2,2); imagesc(A_col); title('Clustered along only column');
set(gca,'XTick',[1:size(A,2)]); set(gca,'XTickLabel',col_name(perm_col)); 
subplot(2,2,4); imagesc(A_row_col); title('Clustered along row then column');
set(gca,'YTick',[1:size(A,1)]); set(gca,'YTickLabel',row_name(perm_row)); 
set(gca,'XTick',[1:size(A,2)]); set(gca,'XTickLabel',col_name(perm_col)); 