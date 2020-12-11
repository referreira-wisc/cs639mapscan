%Convert png to jpg
inputFolder = 'train/mask'
outputFolder = 'train/segment'

pixelMappings = [ 200,0,0 ; 0,64,0; 200,200,0 ; 128,200,0 ; 0,200,0 ; 0,0,100 ; 0,0,200 ; 200,128,0 ]
%urban, forest, crop1, crop2, crop3, river, lake, grass

fileNames = dir(inputFolder);

for i = 1:length(fileNames)
    currFileName = fileNames(i).name;
    isFile = contains(currFileName, '.txt');
    if ~isFile
        continue
    end
    
    fullInputName = strcat(inputFolder, '/', currFileName);
    fullOutputName = strcat(outputFolder, '/', currFileName);
    fullOutputName = strrep(lower(fullOutputName), '.txt', '.png');
    
    fid = fopen(fullInputName,'rt');
    C = textscan(fid, '%s', 'Delimiter','');
    fclose(fid);
    %# extract digits
    matrix = cell2mat(cellfun(@(s)s-'0', C{1}, 'Uniform',false));
    matrix = matrix + 1;
    
    outputMatrix = zeros(size(matrix,1), size(matrix,2), 3);
    for r = 1:size(matrix,1)
        for c = 1:size(matrix,2)
            label = matrix(r,c);
            outputMatrix(r,c,1) = pixelMappings(label, 1);
            outputMatrix(r,c,2) = pixelMappings(label, 2);
            outputMatrix(r,c,3) = pixelMappings(label, 3);
        end
    end
    
    imwrite(outputMatrix, fullOutputName)
end