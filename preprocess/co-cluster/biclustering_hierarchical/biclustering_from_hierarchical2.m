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
% 2) How to determine the number of cluster in both row and column direction.
% 3) How to get the permutation vector, and display the end results.
%
% Last updated: Thu, Nov 23, 2012
% =======================================
% Kittipat "Bot" Kampa
% kittipat@gmail.com
% Integrated Brain Imaging Center (IBIC)
% University of Washington
% =======================================

clear; close all; clc;
%% Load the data

% % -- Data 1 -- 
% x = zeros(150,10);
% % x_row = 1:15,16-18,19-80,81-105,106-125,126-150
% % x_col = 1:4,5-6,7-14,15-20
% x(1:15,7:10) = 1;
% x(1:15,11:14) = 0.6;
% x(16:18,5:6) = 0.6;
% x(19:80,1:4) = 0.4;
% x(81:105,7:14) = 0.8;
% x(106:125,15:20) = 1;
% x(126:150,1:4) = 0.5;

% -- data2 ---
x = [0 0 1 0 0 1 0 1;
     0 0 0 0 0 0 0 0;
     0 1 0 1 0 0 1 0;
     0 0 0 0 0 0 0 0;
     0 0 1 0 0 0.5 0 0.6;
     0 1 0 1 0 0 1 0];

A = x+0.01*randn(size(x)); 

figure(1); 
set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
subplot(2,2,1); imagesc(A); title('original input matrix');
xlabel('original order index'); ylabel('original order index');

%%
[numRow,numCol] = size(A);
row_name = 1:numRow; row_name = num2cell(row_name);
col_name = 1:numCol; col_name = num2cell(col_name);

%% Hierarchical clustering along the column
method = 'average';
metric = 'euclidean';
% agglomerative clustering along row
tree_row = linkage(A,method,metric);
% agglomerative clustering along column
tree_col = linkage(A',method,metric);

%% Now, let's group the rows and columns
% clustering row
k_row = 3; % number of the clusters on row
figure(2); 
subplot(2,1,1);
[~,T_row,perm_row] = dendrogram(tree_row,k_row);
title('cluster along the rows');

% clustering column
k_col = 3; % number of the clusters along the column
subplot(2,1,2);
[~,T_col,perm_col] = dendrogram(tree_col,k_col);
title('cluster along the columns');


% Get the permutation vector
[y_idx, y_label] = findPermutationIndex(1:numRow, T_row, perm_row );
[x_idx, x_label] = findPermutationIndex(1:numCol, T_col, perm_col );

%% Plot the result
figure(1);
% Plot the end-result cluster label for each row and column
subplot(2,2,2); imagesc(A);
set(gca,'YTick',1:numRow); set(gca,'YTickLabel',T_row); 
set(gca,'XTick',1:numCol); set(gca,'XTickLabel',T_col);
title('original input matrix');
xlabel('cluster index with original order');
ylabel('cluster index with original order');

% Rearrange the cluster according to the dendrogram
A_x = A(:,x_idx);
A_xy = A_x(y_idx,:);
subplot(2,2,3); imagesc(A_xy);
set(gca,'YTick',1:numRow); set(gca,'YTickLabel',row_name(y_idx)); 
set(gca,'XTick',1:numCol); set(gca,'XTickLabel',col_name(x_idx));
title('cluster rearranged by the denrogram');
xlabel('original index'); ylabel('original index');

subplot(2,2,4); imagesc(A_xy);
set(gca,'YTick',1:numRow); set(gca,'YTickLabel',T_row(y_idx)); 
set(gca,'XTick',1:numCol); set(gca,'XTickLabel',T_col(x_idx));
title('cluster rearranged by the denrogram');
xlabel('cluster index'); ylabel('cluster index');

% save the figure to jpg
f1 = figure(1);
print(f1,'-djpeg',['hier_bicluster_row',num2str(k_row),'_col',num2str(k_col),'.jpg']);

f2 = figure(2);
print(f2,'-djpeg',['dendrogram_hier_bicluster_row',num2str(k_row),'_col',num2str(k_col),'.jpg']);
