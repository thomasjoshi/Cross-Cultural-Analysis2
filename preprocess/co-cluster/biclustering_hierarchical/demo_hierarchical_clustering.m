% In this example, we will cluster the data using just hierarchical
% agglomerative clustering algorithm (i.e., linkage and dendrogram) in MATLAB.
% We show how to determine the number of output clusters from dendrogram.
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
figure; imagesc(A);

%% Hierarchical clustering along the column
method = 'average';
metric = 'euclidean';
tree = linkage(A,method,metric);
figure; dendrogram(tree);

% The first cluster starts with 7 because we have originally 6 samples
% (rows), each of which is assigned with a cluster value 1-6. Therefore,
% the new cluster is 6+i.
% tree =
% 
%     3.0000    6.0000    0.0394  % ---> cluster#7 (because we have 6 rows originally)
%     1.0000    5.0000    0.0404  % ---> cluster#8
%     2.0000    4.0000    0.0528  % ---> cluster#9
%     8.0000    9.0000    1.7423  % ---> cluster#10
%     7.0000   10.0000    2.0983  % ---> cluster#11 and final (root)

% You will notice in the plot that (3,6) comes first followed by (1,5) and
% (2,4). Such order agrees with that of the matrix "tree" given above.
%
% ......What if we want to reorder the node order?
%% Reordering the node
leafOrder = [1 2 3 4 5 6]; % The original order of A
figure; dendrogram(tree,'Reorder', leafOrder);
% This does not look good, well, but at least the (leaf) nodes are ordered
% according to what I like.

% Now, let's do some optimal order
D = pdist(A);
leafOrder = optimalleaforder(tree,D)
figure; dendrogram(tree,'Reorder', leafOrder);

%% Now, how can we control the number of the leaf nodes??
figure; dendrogram(tree,0); % Showing all the leaf nodes
figure; [~,T] = dendrogram(tree,2);
% T is the label of each original row of A after we reduce the number of
% leaf node. For example,
% T(j) is the label of the original row j of A after reducing/pruning the leaf node   
% find(T==1) is the indices of the original row falling in the leaf node 1 
%
% In fact, we can see T as the cluster number!

%% Permutation vector
[~,T,perm_vector_col] = dendrogram(tree)
[~,T,perm_vector_col] = dendrogram(tree,2)

