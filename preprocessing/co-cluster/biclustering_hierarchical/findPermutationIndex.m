function [perm_idx, label_idx] = findPermutationIndex(org_idx, label_of_org,label_order )
%Calculate the permutation vector to convert from the original index space
%into the new space

label_order = label_order(:)';
org_idx = org_idx(:)';
label_of_org = label_of_org(:)';
perm_idx = [];
label_idx = [];

for l = label_order
    members_in_label = org_idx(label_of_org==l);
    perm_idx = [perm_idx, members_in_label];
    label_idx = [label_idx, l+zeros(1,length(members_in_label))];
end

