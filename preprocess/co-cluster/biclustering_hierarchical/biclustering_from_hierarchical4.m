%% Biclustering
% Using function Biclustering on  a bigger input matrix
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

% -- Data 1 -- 
x = zeros(150,10);
% x_row = 1:15,16-18,19-80,81-105,106-125,126-150
% x_col = 1:4,5-6,7-14,15-20
x(1:15,7:10) = 1;
x(1:15,11:14) = 0.6;
x(16:18,5:6) = 0.6;
x(19:80,1:4) = 0.4;
x(81:105,7:14) = 0.8;
x(106:125,15:20) = 1;
x(126:150,1:4) = 0.5;

% % -- data2 ---
% x = [0 0 1 0 0 1 0 1;
%      0 0 0 0 0 0 0 0;
%      0 1 0 1 0 0 1 0;
%      0 0 0 0 0 0 0 0;
%      0 0 1 0 0 1 0 1;
%      0 1 0 1 0 0 1 0];

A = x+0.01*randn(size(x)); 
[numRow,numCol] = size(A);
% row_name = {'A','B','C','D','E','F'};
row_name = num2cell(1:numRow);
col_name = num2cell(1:numCol);
%% hierarchical biclustering
k_row = 3; k_col = 3;
[row_clust_idx, col_clust_idx, y_index, x_index]=Biclustering(A, k_row, k_col);

%% Plot the result
A_x = A(:,x_index);
A_xy = A_x(y_index,:);
figure; 
% subplot(2,2,1); imagesc(A);
subplot(2,2,2); imagesc(col_clust_idx(x_index)'); title('column cluster');
set(gca,'XTick',1:numCol); set(gca,'XTickLabel',col_clust_idx(x_index));
daspect([1 0.5 1]);
subplot(2,2,3); imagesc(row_clust_idx(y_index(:))); title('row cluster');
set(gca,'YTick',1:numRow); set(gca,'YTickLabel',row_clust_idx(y_index));
daspect([0.1 1 1]);
subplot(2,2,4); imagesc(A_xy);
set(gca,'YTick',1:numRow); set(gca,'YTickLabel',row_name(y_index)); 
set(gca,'XTick',1:numCol); set(gca,'XTickLabel',col_name(x_index));