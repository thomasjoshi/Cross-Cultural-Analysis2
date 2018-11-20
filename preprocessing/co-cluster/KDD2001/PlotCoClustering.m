function [row_clust_ids, col_clust_ids,y_index,x_index]=PlotCoClustering(A,clust_num)
% adds the cluster numbers on the plot, one per cluster
% Usage: [row_clust_idx, col_clust_idx,x_index,y_index]=PlotCoClustering(A,clust_num)
% Inputs: 
%       A: the [nxm] matrix to co-cluster, containing the co-occurrences of n instances
%           (rows) and m features (columns).
%       clust_num (default =2): The number of desired clusters.
% Outputs:
%       row_clust_ids: the cluster number for each instance  (rows)
%       col_clust_ids: the cluster number for each feature (columns)
%       y_index: The order of the y-axis (Instances)
%       x_index: The order of the x-axis (features)
%   Author: Assaf Gottlieb, 2008.
%
%   Contact: Assaf Gottlieb www.tau.ac.il/~assafgot
%            School of Physics and Astronomy, Tel Aviv University, Tel Aviv, Israel

[row_clust_ids, col_clust_ids,y_index,x_index]=SpectralCoClustering(A,clust_num,1);
figure(gcf);
real_clust_ids=unique(row_clust_ids);
real_clust_num=length(real_clust_ids);
clust_idx=zeros(real_clust_num,1);
for k=1:real_clust_num
    curr_clust_idx=find(row_clust_ids(y_index)==real_clust_ids(k));
    clust_idx(k)=int32(median(curr_clust_idx));
end;
clust_idx=int32(clust_idx);
%clust_ids=int32(clust_ids);
%y_index=int32(y_index);

set(gca,'YTick',clust_idx,'YTickLabel',1:real_clust_num,'FontSize',10);
