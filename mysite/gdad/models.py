from django.db import models

# Create your models here.


class G4(models.Model):
    # g4
    chr = models.CharField(max_length=31, default="")
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    strand = models.CharField(max_length=1, default="")
    cell_line = models.CharField(max_length=63, default="")
    technology = models.CharField(max_length=63, default="")
    doi = models.CharField(max_length=255, default="")

    def __str__(self):
        out_list = [
            self.chr,
            self.start,
            self.end,
            self.strand,
            self.cell_line,
            self.technology,
            self.doi,
        ]
        out_list = list(map(lambda x: str(x), out_list))
        out_str = "\t".join(out_list)
        return out_str

    def get_field_list(self) -> list[str]:
        """打印字段名列表。

        Returns:
            field_list (list[str]): 字段名列表。
        """
        field_list = [
            "chr",
            "start",
            "end",
            "strand",
            "cell_line",
            "technology",
            "doi",
        ]
        return field_list


class GeneSequence(models.Model):
    # gene_sequence
    chr = models.CharField(max_length=31, default="")
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    gene_symbol = models.CharField(max_length=31, default="")

    def __str__(self):
        out_list = [self.chr, self.start, self.end, self.gene_symbol]
        out_list = list(map(lambda x: str(x), out_list))
        out_str = "\t".join(out_list)
        return out_str

    def get_field_list(self) -> list[str]:
        """打印字段名列表。

        Returns:
            field_list (list[str]): 字段名列表。
        """
        field_list = [
            "chr",
            "start",
            "end",
            "gene_symbol",
        ]
        return field_list


class Gda(models.Model):
    # gda
    gene_id = models.CharField(max_length=31, default="")
    gene_symbol = models.CharField(max_length=31, default="")
    uniprot_id = models.CharField(max_length=63, default="")
    gene_dsi = models.FloatField()
    gene_dpi = models.FloatField()
    # gene_pli字段有很多科学计数法，差距过大，数值型字段无法支持
    gene_pli = models.CharField(max_length=15, default="")
    protein_class = models.CharField(max_length=31, default="")
    protein_class_name = models.CharField(max_length=63, default="")
    disease_id = models.CharField(max_length=15, default="")
    disease_name = models.CharField(max_length=255, default="")
    disease_class = models.CharField(max_length=255, default="")
    disease_class_name = models.CharField(max_length=1023, default="")
    disease_type = models.CharField(max_length=15, default="")
    disease_semantic_type = models.CharField(max_length=255, default="")
    gda_score = models.FloatField()
    ei = models.FloatField()
    el = models.CharField(max_length=31, default="")
    year_initial = models.PositiveIntegerField()
    year_final = models.PositiveIntegerField()

    def __str__(self):
        out_list = [
            self.gene_id,
            self.gene_symbol,
            self.disease_id,
            self.disease_name,
        ]
        out_list = list(map(lambda x: str(x), out_list))
        out_str = "\t".join(out_list)
        return out_str

    def get_field_list(self) -> list[str]:
        """打印字段名列表。

        Returns:
            field_list (list[str]): 字段名列表。
        """
        field_list = [
            "gene_id",
            "gene_symbol",
            "uniprot_id",
            "gene_dsi",
            "gene_dpi",
            "gene_pli",
            "protein_class",
            "protein_class_name",
            "disease_id",
            "disease_name",
            "disease_class",
            "disease_class_name",
            "disease_type",
            "disease_semantic_type",
            "gda_score",
            "ei",
            "el",
            "year_initial",
            "year_final",
        ]
        return field_list
