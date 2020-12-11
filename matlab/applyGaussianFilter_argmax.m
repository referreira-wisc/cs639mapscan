clear all
maskDir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks\';
outputDir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks_gauss_argmax\';
FileList = dir(fullfile(maskDir, '*.txt'));

for iFile = 1:numel(FileList)
    maskFile = FileList(iFile).name;
    mask = readMaskFile(strcat(maskDir, maskFile));
    clear masks;
    n_classes = 8;
    for i = 0:n_classes-1
        img = im2uint8(mask == i);
        smooth = imgaussfilt(img,2);
        masks(:,:,i+1) = smooth;
    end
    [argvalue, argmax] = max(masks,[],3);
    outputFile = strcat(outputDir, maskFile);
    dlmwrite(outputFile, argmax-1, 'delimiter', '');
end
