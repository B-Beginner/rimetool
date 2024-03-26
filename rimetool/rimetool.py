import click
from .tools.vcf_to_dict import vcf_to_dict


@click.command()
@click.option('-vcf', type=str, help='.vcf的文件路径')


def main(vcf):
	vcf_to_dict(vcf)


if __name__ == '__main__':
	main()