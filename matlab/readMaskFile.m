function gt_m = readMaskFile(File)
    fid = fopen(File);
    gt = textscan(fid,'%s');
    fclose(fid);
    
    gt = string(gt{:});
    gt_m = zeros(numel(gt), strlength(gt(1)));
    for i = 1:numel(gt)
        chr = char(gt(i));
        gt_m(i,:) = chr(:)'-'0';
    end
end