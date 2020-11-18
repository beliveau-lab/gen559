def get_ORFs(seq):
    '''Identifies ORFs in input DNA sequence and returns the positions and lengths of any found'''

    # Create a list to hold function return.
    output_list = []

    ## Iterate through input sequence, looking for valid ORFs.

    # Create variable to keep track of index in sequence.
    idx = 0

    # Loop through input DNA sequence in windows of 3 nt.
    for i in range(idx, len(seq)-2, 1):
        window = seq[i:i+3]

        # Check if current window is a start codon.
        if window == "ATG":

            ## If so, search for a stop codon.

            # Create and populate a list of in-frame codons.
            in_frame_codons = []
            for j in range(i, len(seq)-i, 3):
                in_frame_codons.append(seq[j:j+3])

            # Search for a stop codon in in_frame_codons.
            if "TGA" or "TAA" or "TAG" in in_frame_codons:
                for k in range(0, len(in_frame_codons), 1):
                    if in_frame_codons[k] in ["TGA", "TAA", "TAG"]:

                        # If found, add ORF info to output list.
                        ORF_seq = seq[i:k*3+3]
                        ORF_len = len(ORF_seq)/ 3 - 1
                        output_list.append('%s\t%s' % (ORF_seq, ORF_len))

                        # Update idx variable.
                        idx = i

    # Check if output list is empty:
    if len(output_list) == 0:
        return 'Warning, no valid ORFs found!'

    else:
        return output_list


def translate_ORF(seq, codon_table='codons.txt'):
    '''Translates an input DNA sequence using a provided codon table'''

    ## Check input sequence for a valid ORF.

    # Check that seq begins with a start codon, ends with a stop codon,
    # and that the length of the sequence is a clean multiple of 3 using modulo '%' division.
    if seq[0:3] == 'ATG' and seq[-3:] in ["TGA", "TAA", "TAG"] and len(seq) % 3 == 0:

        ## If true, build codon:amino acid dictionary and translate ORF.

        # Make list to hold output.
        protein = []

        # Open codon table, extract contents.
        with open(codon_table, 'r') as f:
            codon_info = [line.strip() for line in f]

        # Create empty dictionary to hold codon:amino acid information.
        codon_dict = {}

        # Populate dictionary from input codon table.
        for i in range(0, len(codon_info), 1):
            codon_dict[codon_info[i].split('\t')[0]] = codon_info[i].split('\t')[2]

        # Process input sequence and translate using codon_dict.
        for i in range(0, len(seq)-2, 3):
            codon_seq = seq[i:i+3]

            # Check if current codon is a stop codon, break loop if so.
            if codon_dict[codon_seq] == '0':
                break

            # Else, add the amino acid corresponding to the current codon to the protein list.
            else:
                protein.append(codon_dict[codon_seq])

        # Return the translated protein as a string.
        return ''.join(protein)


    # If not true, return warning message
    else:
        return('Warning, input sequence is not a valid ORF')
