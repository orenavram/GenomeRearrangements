import logging
import datetime
import sys


def get_numeric_gene(ORFs_dir_path, group_index, group_genes):
    raise TypeError #TODO


def get_genome_numeric_representation(orthologs_table_path, ORFs_dir_path, output_path):

    logger.info(f'{datetime.datetime.now()}: starting to run...')

    group_index = 0
    with open(orthologs_table_path) as f:
        genome_names = f.readline().rstrip().split(',')[1:]  # skip OG_name
        genome_name_to_numeric_genome = dict.fromkeys(genome_names, '')  # genome name -> numeric core genome
        for line in f:
            group_genes = line.rstrip().split(',')[1:]  # skip OG_name
            if not all(group_genes):
                # at least one group_genes is missing, i.e., not a core gene
                continue
            group_index += 1
            genome_name_to_numeric_gene = get_numeric_gene(ORFs_dir_path, group_index, group_genes)
            for genome_name in genome_name_to_numeric_genome:
                genome_name_to_numeric_genome[genome_name] += genome_name_to_numeric_gene[genome_name]

    with open(output_path, 'w') as f:
        for genome_name in genome_name_to_numeric_genome:
            f.write(f'>{genome_name}\n{genome_name_to_numeric_genome[genome_name]}\n')


if __name__ == '__main__':
    print(f'Starting {sys.argv[0]}. Executed command is:\n{" ".join(sys.argv)}')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('orthologs_table_path', help='A path to an ortholog table (step 11 of microbializer)')
    parser.add_argument('ORFs_dir_path', help='A path to a ORF directory (step 01 of microbializer)')
    parser.add_argument('output_path', help='A path to which the numeric core genomes will be written')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('main')

    get_genome_numeric_representation(args.orthologs_table_path, args.ORFs_dir_path.rstrip('/'), args.output_path)
