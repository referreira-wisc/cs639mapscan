function [overlay, L, C] = kmeansCluster(n_clusters, filename)

RGB = imread(filename);
RGB = RGB(1:224,:,:);

[L,C] = imsegkmeans(RGB,n_clusters);
%C = double(C) ./ 255;

C = jet(n_clusters);


H = reshape(C(L,:),[size(L) 3]);
K = im2double(RGB);
B = K .* 0.2 + H .* 0.8;
B = im2uint8(B);

overlay = reshape(permute(B,[3 2 1]),[],1);