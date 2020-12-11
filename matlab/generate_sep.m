src_dir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks_gauss';
dst_dir = 'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks_sep';
FileList = dir(fullfile(src_dir, '*.txt'));

for iFile = 1:numel(FileList)
    File = fullfile(FileList(iFile).folder, FileList(iFile).name);
    instance = FileList(iFile).name(1:end-4);
    mask = readMaskFile(File);
    bw = bwlabel(mask);
    max_idx = max(max(bw));
    for i = 1:max_idx
        current_mask = bw == i;
        dlmwrite(strcat(dst_dir, '\', instance, '_', sprintf('%03d', i), '.txt'), current_mask, 'delimiter', '');
    end
end