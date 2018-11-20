function [filtered_data,col_idx,row_idx]=FilterSparseData(data,min_occur)
% filter the data according to minimal occurences 
% Pay attention that only one iteration is done, so some rows or columns
% may have less than min_occur non-zero values
% usage [data,col_idx,row_idx]=FilterSparseData(data,min_occur);
% Inputs: 
%  data - the data matrix 
%   min_occur - minimal occurences on each row or column 
% Outputs:
%   filtered_data - the filtered data
%   col_idx - the mapping from the new filtered data columns to the original ones
%   row_idx - the mapping from the new filtered data rows to the original ones
%   Author: Assaf Gottlieb, 2008.
%
%   Contact: Assaf Gottlieb www.tau.ac.il/~assafgot
%            School of Physics and Astronomy, Tel Aviv University, Tel Aviv, Israel

data=full(real(data)); %in case its a logical or sparse matrix
row_idx=find(sum(data>0,2)>=min_occur);
col_idx=find(sum(data(row_idx,:)>0,1)>=min_occur);
row_idx=row_idx(find(sum(data(row_idx,col_idx)>0,2)));
col_idx=col_idx(find(sum(data(row_idx,col_idx)>0,1)));
filtered_data=data(row_idx,col_idx);
