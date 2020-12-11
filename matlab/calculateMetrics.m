clear all
root_dir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\unet-master\results';
folders = dir(root_dir);
total_dice = [];
total_iou = [];
names = [];
for f = 1:length(folders)
    if folders(f).name == "." || folders(f).name == ".."
        continue;
    end
    
    folderName = strcat(root_dir,'\',folders(f).name,'\txt');

    %Get all file names
    truthNames = {};
    guessNames = {};

    fileNames = dir(folderName);
    for i = 1:length(fileNames)
        currFileName = fileNames(i).name;
        isTruth = contains(currFileName, 'gnd');
        isGuess = contains(currFileName, 'hat');
        if isTruth
            truthNames(length(truthNames) + 1) = {currFileName};  
        end
        if isGuess
            guessNames(length(guessNames) + 1) = {currFileName};  
        end
    end

    allTruth = [];
    allGuess = [];
    for i = 1:length(truthNames)
        %Get file names
        truthName1 = truthNames{i};
        guessName1 = guessNames{i};
        truthName1 = strcat(folderName, '/', truthName1);
        guessName1 = strcat(folderName, '/', guessName1);

        %Get truth matrix
        fid = fopen(truthName1,'rt');
        C = textscan(fid, '%s', 'Delimiter','');
        fclose(fid);
        %# extract digits
        truth1 = cell2mat(cellfun(@(s)s-'0', C{1}, 'Uniform',false));
        truth1 = truth1 + 1;

        %Get guess matrix
        fid = fopen(guessName1,'rt');
        C = textscan(fid, '%s', 'Delimiter','');
        fclose(fid);
        %# extract digits
        guess1 = cell2mat(cellfun(@(s)s-'0', C{1}, 'Uniform',false));
        guess1 = guess1 + 1;

        allTruth = [allTruth; reshape(truth1,[],1)];
        allGuess = [allGuess; reshape(guess1,[],1)];
    end

    % % THIS IS DICE CODE
    %     print accuracy and unique ints
    dice = [];
    for c = 1:8
        g = allGuess == c;
        t = allTruth == c;
        tp = sum(g & t, 'all');
        fp = sum(g & ~t, 'all');
        fn = sum(~g & t, 'all');
        d = 2*tp / (2*tp + fp + fn);
        dice = [dice; d];
    end
    dice = [dice; mean(allTruth==allGuess)];
    total_dice = [total_dice, dice];
    names = [names, string(folders(f).name)];
    
    % % IoU CODE
    iou = [];
    for c = 1:8
        g = allGuess == c;
        t = allTruth == c;
        intersection = sum(g .* t);
        union = sum(g) + sum(t) - intersection;
        iou = [iou; intersection/union];
    end
    iou = [iou; mean(iou)];
    total_iou = [total_iou, iou];

end