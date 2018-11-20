function [result] = output_co_cluster(A,B,C,k)

result = 0;

[v_name v_index] = textread('video_index', '%s %d');
[m_name m_index] = textread('visual_meme_index', '%s %d');
[t_name t_index] = textread('tag_index', '%s %d');


video = cell(size(v_index));
for i = 1 : size(v_index)
    video(v_index(i)+1) = v_name(i);
end

visualmeme = cell(size(m_index));
for i = 1 : size(m_index)
    visualmeme(m_index(i)+1) = m_name(i);
end
visualmeme

tag = cell(size(t_index));
for i = 1 : size(t_index)
    tag(t_index(i)+1) = t_name(i);
end 
tag

for i = 1 : k
    groupA = A(:,i);
    groupB = B(:,i);
    A_list = find(groupA > 0);
    mlist = visualmeme(A_list)
    groupA(A_list)
    %groupB = groupB(1:123);
    B_list = find(groupB > 0);
    groupB(B_list)
    tlist = tag(B_list)
    pause
end  
