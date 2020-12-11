%Convert masks to png
%Convert png to jpg
inputFolder = 'stest/mask'
outputFolder = 'stest/segment'

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

    imwrite(matrix, fullOutputName)
end