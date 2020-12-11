clear all
images_dir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\satellite\greenbay\images'
results_dir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\satellite\greenbay\results'
stitch_dir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\satellite\greenbay'

files = dir(images_dir);
img_size = 256;
image = uint8(zeros(img_size*10, img_size*10, 3));
for f = 1:length(files)
    if files(f).name == "." || files(f).name == ".."
        continue;
    end
    
    img = imread(strcat(images_dir,'\',files(f).name));
    startx = 1 + floor((f-3)/10) * img_size;
    endx = startx + img_size - 1;
    starty = 1 + mod(f-3,10) * img_size;
    endy = starty + img_size - 1;
    image(starty:endy,startx:endx,:) = img;
end
imwrite(image,strcat(stitch_dir,'\satellite.png'));

files = dir(results_dir);
img_size = 224;
result = uint8(zeros(img_size*10, img_size*10, 3));
for f = 1:length(files)
    if files(f).name == "." || files(f).name == ".."
        continue;
    end
    
    img = imread(strcat(results_dir,'\',files(f).name));
    startx = 1 + floor((f-3)/10) * img_size;
    endx = startx + img_size - 1;
    starty = 1 + mod(f-3,10) * img_size;
    endy = starty + img_size - 1;
    result(starty:endy,startx:endx,:) = img;
end
imwrite(result,strcat(stitch_dir,'\result.png'));