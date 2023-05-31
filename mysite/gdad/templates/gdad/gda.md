# GDA

- `gene_id`: The official gene symbol, from the NCBI.
- `gene_symbol`: The NCBI Official Full Name.
- `uniprot_id`: The Uniprot accession.
- `gene_dsi`: The Disease Specificity Index (DSI).
- `gene_dpi`: The Disease Pleiotropy Index (DPI).
- `gene_pli`: The pLI, defined as the probability of being loss-of-function intolerant, is a gene constraint metric provided by the GNOMAD consortium. A gene constraint metric aims at measuring how the naturally occurring LoF (loss of function) variation has been depleted from a gene by natural selection (in other words, how intolerant is a gene to LoF variation). LoF intolerant genes will have a high pLI value (>=0.9), while LoF tolerant genes will have low pLI values (<=0.1). The LoF variants considered are nonsense and essential splice site variants.
- `protein_class`: The class of protein.
- `protein_class_name`: The class name of protein.
- `disease_id`:  The disease ID.
- `disease_name`: The disease name, provided by the UMLS® Metathesaurus®.
- `disease_class`: The UMLS® semantic types.
- `disease_class_name`: The MeSH class: We classify the diseases according the MeSH hierarchy using the upper level concepts of the MeSH tree branch C (Diseases) plus three concepts of the F branch (Psychiatry and Psychology: "Behavior and Behavior Mechanisms", "Psychological Phenomena and Processes", and "Mental Disorders").
- `disease_type`: The top level concepts from the Human DiseaseOntology.
- `disease_semantic_type`: The DisGeNET disease type: disease, phenotype and group.
- `gda_score`: The DisGeNET score.
- `ei`: The Evidence Index.
- `el`: The Evidence Level.
- `year_initial`: First time that the association was reported.
- `year_final`: Last time that the association was reported.

See [DisGeNET](https://www.disgenet.org/dbinfo) for more details.

---

## Search GDA

- `ID`: The ID of GDA. Multiple entries should be separated by commas.
- `Disease name`: The disease name of GDA data. Multiple entries should be separated by spaces. GDA data which containing these keywords will be found regardless of the case of letters.
- `Gene symbol`: The gene symbol of GDA. Multiple entries should be separated by commas.

Search criteria that are not entered are considered to be unrestricted.

## Search GDA by G4 data

- `G4 ID`: The ID of G4. Multiple entries should be separated by commas. The relevant GDAs will be found.

Search criteria that are not entered are considered to be unrestricted.

## Search GDA by GENE data

- `Gene ID`: The ID of GENE. Multiple entries should be separated by commas. The relevant GDAs will be found.

Search criteria that are not entered are considered to be unrestricted.
