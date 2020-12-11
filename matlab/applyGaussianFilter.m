maskDir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks\';
outputDir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks_gauss\';
FileList = dir(fullfile(maskDir, '*.txt'));

for iFile = 1:numel(FileList)
    maskFile = FileList(iFile).name;
    mask = readMaskFile(strcat(maskDir, maskFile));
    n_classes = 8;
    for i = 0:n_classes-1
        img = im2uint8(mask == i);
        smooth = imgaussfilt(img,2);
        regions = smooth > 80;
        if max(max(regions))
            outputFile = strcat(outputDir, maskFile(1:end-4), '_', string(i), '.txt');
            dlmwrite(outputFile, regions, 'delimiter', '');
        end
    end
end
