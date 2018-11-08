% This program illustrate the example shown in matlab's clustergram
% webpage.
%
% Last updated: Thu, Nov 22, 2012
% =======================================
% Kittipat "Bot" Kampa
% kittipat@gmail.com
% Integrated Brain Imaging Center (IBIC)
% University of Washington
% =======================================

clear; clc; close all;

%% load the data
load filteredyeastdata
figure; imagesc(yeastvalues); colorbar;

%% Perform clustergram
% Create a clustergram object and display the dendrograms and heat map from
% the gene expression data in the first 30 rows of the yeastvalues matrix.
cgo = clustergram(yeastvalues(1:30,:));

% label the row and column
set(cgo,'RowLabels',genes(1:30),'ColumnLabels',times);

%% 
get(cgo);
set(cgo,'Linkage','complete','Dendrogram',3)