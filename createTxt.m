%Create the train.txt, val.txt, and trainval.txt files
trainFolder = 'strain/mask'
testFolder = 'stest/mask'
trainval = 'strainval.txt'
train = 'strain.txt'
val = 'sval.txt'

fileNames = dir(trainFolder);


%Go thru train frist
trainFID = fopen(train,'wt');
trainValFID = fopen(trainval, 'wt');
for i = 1:length(fileNames)
    currFileName = fileNames(i).name;
    isFile = contains(currFileName, '.txt');
    if ~isFile
        continue
    end
    
    outputName = strrep(lower(currFileName), '.txt', '')
    
    
    
    fprintf(trainFID, outputName);
    fprintf(trainFID, '\n');
    fprintf(trainValFID, outputName);
    fprintf(trainValFID, '\n');

end
fclose(trainFID);

fileNames = dir(testFolder);

valFID = fopen(val,'wt');
for i = 1:length(fileNames)
    currFileName = fileNames(i).name;
    isFile = contains(currFileName, '.txt');
    if ~isFile
        continue
    end
    
    outputName = strrep(lower(currFileName), '.txt', '')
    
    
    
    fprintf(valFID, outputName);
    fprintf(valFID, '\n');
    fprintf(trainValFID, outputName);
    fprintf(trainValFID, '\n');

end
fclose(valFID);
fclose(trainValFID);