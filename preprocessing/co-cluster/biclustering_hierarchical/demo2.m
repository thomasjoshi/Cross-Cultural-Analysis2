% The program shows how to perform biclustering using "clustergram" command in matlab.
% 1) We made a simple toy data set for illustrative purpose.
% 2) We show a trick to obtain the permutation vectors from the CLUSTERGRAM object
%
% Last updated: Thu, Nov 22, 2012
% =======================================
% Kittipat "Bot" Kampa
% kittipat@gmail.com
% Integrated Brain Imaging Center (IBIC)
% University of Washington
% =======================================

clear; clc; close all

x = [0 0 1 0 0 1 0 1;
     0 0 0 0 0 0 0 0;
     0 1 0 1 0 0 1 0;
     0 0 0 0 0 0 0 0;
     0 0 1 0 0 1 0 1;
     0 1 0 1 0 0 1 0];
 


A = x+0.01*randn(size(x)); 
figure; imagesc(A);
gco = clustergram(A);

%% This is what we supposedly will get 
% x_index = [7 2 4 1 5 6 8 3]; % permutation vector in column 
% y_index = [6 3 2 4 5 1]; % permutation vector in row
% A_x = A(:,x_index);
% A_xy = A_x(y_index,:);
% figure; imagesc(A_xy);

%%
perm_col = str2num(char(get(gco,'ColumnLabels')));
perm_row = str2num(char(get(gco,'RowLabels')));
perm_row = flipud(perm_row);
B_x = A(:,perm_col);
B_xy = B_x(perm_row,:);
figure; imagesc(B_xy);
set(gco,'Dendrogram',3);