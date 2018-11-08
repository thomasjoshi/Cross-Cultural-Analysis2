%% Biclustering
% We wrap all the hierarchical clustering algorithm into a function:
% [row_clust_idx, col_clust_idx, y_index, x_index]=Biclustering(A, k_row, k_col);
% We use the same example as shown in biclustering_from_hierarchical2.m
% except that we use the function to perform clustering instead.
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
k_row = 4; k_col = 3;
[row_clust_idx, col_clust_idx, y_index, x_index]=Biclustering(A, k_row, k_col);


%% Plot the result
figure(1);
% Plot the end-result cluster label for each row and column
subplot(2,2,2); imagesc(A);
set(gca,'YTick',1:numRow); set(gca,'YTickLabel',row_clust_idx); 
set(gca,'XTick',1:numCol); set(gca,'XTickLabel',col_clust_idx);
title('original input matrix');
xlabel('cluster index with original order');
ylabel('cluster index with original order');

% Rearrange the cluster according to the dendrogram
A_x = A(:,x_index);
A_xy = A_x(y_index,:);
subplot(2,2,3); imagesc(A_xy);
set(gca,'YTick',1:numRow); set(gca,'YTickLabel',row_name(y_index)); 
set(gca,'XTick',1:numCol); set(gca,'XTickLabel',col_name(x_index));
title('cluster rearranged by the denrogram');
xlabel('original index'); ylabel('original index');

subplot(2,2,4); imagesc(A_xy);
set(gca,'YTick',1:numRow); set(gca,'YTickLabel',row_clust_idx(y_index)); 
set(gca,'XTick',1:numCol); set(gca,'XTickLabel',col_clust_idx(x_index));
title('cluster rearranged by the denrogram');
xlabel('cluster index'); ylabel('cluster index');

% save the figure to jpg
f1 = figure(1);
print(f1,'-djpeg',['hier_bicluster_row',num2str(k_row),'_col',num2str(k_col),'.jpg']);

f2 = figure(2);
print(f2,'-djpeg',['dendrogram_hier_bicluster_row',num2str(k_row),'_col',num2str(k_col),'.jpg']);
