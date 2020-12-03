import argparse


def extract_variation(file, chrom):
    '''Takes in name of vcf file and returns a list of variants
    from a specified chromosome'''

    # Open specified file.
    with open(file, 'r') as f:

        # Extract SNVs if args.snv is True.
        if args.snv is True:
            # Create and populate of extracted variants. Skip header lines.
            # Only consider line if length of 'REF' and 'ALT' both = 1, i.e.
            # the line describes a SNV.
            variants = [line.strip() for line in f \
            if line.strip().split("\t")[0][0]!='#' \
            and line.strip().split("\t")[0] == chrom \
            and len(line.strip().split("\t")[3]) == 1 \
            and len(line.strip().split("\t")[4]) == 1]

        # Extract insertions if args.ins is True.
        elif args.insertion is True:

            # Create and populate of extracted variants. Skip header lines.
            # Only consider line if length of 'REF' = 1 and length of 'ALT'
            # > 1, i.e. the line describes an insertion.
            variants = [line.strip() for line in f \
            if line.strip().split("\t")[0][0]!='#' \
            and line.strip().split("\t")[0] == chrom \
            and len(line.strip().split("\t")[3]) == 1 \
            and len(line.strip().split("\t")[4]) > 1]

        # Extract deletions if args.del is True.
        if args.deletion is True:

            # Create and populate of extracted variants. Skip header lines.
            # Only consider line if length of 'REF' > 1 and length of 'ALT'
            # = 1, i.e. the line describes a deletion.
            variants = [line.strip() for line in f \
            if line.strip().split("\t")[0][0]!='#' \
            and line.strip().split("\t")[0] == chrom \
            and len(line.strip().split("\t")[3]) > 1 \
            and len(line.strip().split("\t")[4]) == 1]

    # Return list of extracted variants.
    return variants


# Create argument parser.
userInput = argparse.ArgumentParser(description= \
                                    'Takes an input vcf file and extracts ' \
                                    'extracts chromosome-specific variant ' \
                                    'information to return in a new .vcf file')

## Add arguments to parser.

# Add argument to import file.
userInput.add_argument('-f', '--file', action='store', required=True, \
                        help='The .vcf file to process (required)')

# Add argument to specify chromosome.
userInput.add_argument('-c', '--chrom', action='store', required=True, \
                        default='chr1', help='The chromosome from which ' \
                        'to extract variant information (required), ' \
                        'default="chr1"')

# Create mutually exclusive argument group.
mutEx = userInput.add_mutually_exclusive_group()

# Add SNV argument to mutEx group.
mutEx.add_argument('-s', '--snv', action='store_true', default=False,
                    help='Return SNV variants, default=False')

# Add insertion argument to mutEx group.
mutEx.add_argument('-i', '--insertion', action='store_true', default=False, \
                    help='Return insertion variants, default=False')

# Add deletion argument to mutEx group.
mutEx.add_argument('-d', '--deletion', action='store_true', default=False, \
                    help='Return deletion variants, default=False')

# Add argument to specify output filename stem.
userInput.add_argument('-o', '--output', action='store', required=True, \
                        default='my_variants', help='The stem of the ' \
                        'output file name (required), ' \
                        'default="my_variants"')

# Import user-specified command line values.
args = userInput.parse_args()

# Call extract_variation function with user input.
outputList = extract_variation(args.file, args.chrom)

# Create and write output file.
with open(args.output + '.vcf', 'w') as f:
    f.write('\n'.join(outputList))
