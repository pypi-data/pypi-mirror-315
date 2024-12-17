import os

def output(path, iname, counts, qclist):
    imgtotal = sum(qclist)
    total = sum(counts)
    wbc = sum(counts) - counts[8] - counts[7]
    with open(os.path.join(path, iname+'_output.txt'), 'w') as f:
        f.write('Slie quality check\n')
        f.write(f'Total images: {imgtotal}\n')
        f.write(f'Blank: {qclist[0]}\n')
        f.write(f'Cluster: {qclist[1]}\n')
        f.write(f'Standard: {qclist[2]}\n')
        f.write('Cell counts on standard images\n')
        f.write(f'Total: {total} cells\n')
        f.write(f'RBC: {counts[8]} cells\n')
        f.write(f'WBC: {wbc} cells\n')
        f.write(f'Thrombocyte: {counts[7]} cells\n')
        f.write('---WBC count per cell type---\n')
        f.write(f'Neutrophil: {counts[0]} cells\n')
        f.write(f'Eosinphil: {counts[1]} cells\n')
        f.write(f'Blast: {counts[2]} cells\n')
        f.write(f'Erythroid precursor: {counts[3]} cells\n')
        f.write(f'Myeloid precursor: {counts[4]} cells\n')
        f.write(f'Lymphocyte: {counts[5]} cells\n')
        f.write(f'Monocyte+Macrophage: {counts[6]} cells\n')
        f.write(f'Immature monocyte: {counts[9]} cells\n')