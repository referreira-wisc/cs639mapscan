function removeWatermark(filename)
    img = imread(filename);
    img = img(1:224,:,:);
    imwrite(img, filename);
end