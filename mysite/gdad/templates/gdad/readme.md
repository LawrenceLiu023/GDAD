# GDAD

G4-Disease Association Databse (GDAD) is a database disigned to store G4, gene and Gene-Disease Association (GDA) data, and to provide convenient search functions.

---

## Data tables

GDAD contains three data tables:

- G4
- GENE
- GDA

Details of each data table can be found on the corresponding page.

## Data sources

The G4 data are obtained different types of experiments.

The GENE data are obtained from [GENCODE](https://www.gencodegenes.org/human/release_19.html) human comprehensive gene annotation v19.

The GDA data are collected via [DisGeNET REST API](https://www.disgenet.org/api/). GDAD collects the expert-curated GDA data for all genes from [GENCODE](https://www.gencodegenes.org/human/release_19.html), which come from the following sources:

- UNIPROT: [UniProt/SwissProt](https://www.disgenet.org/www.uniprot.org/) is a database containing curated information about protein sequence, structure and function ( [The UniProt Consortium, 2018](https://www.ncbi.nlm.nih.gov/pubmed/29425356) ). GDAs were obtained from the [humsavar](https://www.uniprot.org/docs/humsavar) file. Only the associations marked as Disease are included.

- CTD: The [Comparative Toxicogenomics Database](http://ctdbase.org/) contains manually curated information about gene-disease relationships with focus on understanding the effects of environmental chemicals on human health ( [Davis et al., 2018](https://www.ncbi.nlm.nih.gov/pubmed/30247620) ). Only include associations marked as marker/mechanism or therapeutic are included.

- ORPHANET: [Orphanet](http://www.orpha.net/) is the reference portal for information on rare diseases and orphan drugs, for all audiences (© INSERM 1997). Its aim is to help improve the diagnosis, care and treatment of patients with rare diseases. All GDAs are kept.
- CLINGEN: [The Clinical Genome Resource](https://www.clinicalgenome.org/) is dedicated to building an authoritative central resource that defines the clinical relevance of genes and variants for use in precision medicine and research ( [Rehm et al., 2018](https://www.ncbi.nlm.nih.gov/pubmed/26014595) ). GDAs labeled as "refuted" are excluded.
- GENOMICS ENGLAND: [The Genomics England PanelApp](https://panelapp.genomicsengland.co.uk/) is a publically available knowledge base that allows virtual gene panels related to human disorders to be created, stored and queried. All GDAs are kept.
- CGI: [The Cancer Genome Interpreter](https://www.cancergenomeinterpreter.org/home) is a tool that (i) identifies known oncogenic alterations; (ii) predicts potential drivers among those of unknown significance and (iii) identify alterations in the tumor known to affect the response to anti-cancer drugs ( [Tamborero et al., 2018](https://www.ncbi.nlm.nih.gov/pubmed/29592813) ). It also distributes the catalog of Cancer Driver Genes, which is a selection of genes driving tumorigenesis in a certain tumor type(s) upon a certain alteration (mutation, copy number alteration and/or gene translocation). Only validated data are kept.
- PSYGENET: [PsyGeNET](http://psygenet.org/) (Psychiatric disorders Gene association NETwork) is a resource for the exploratory analysis of psychiatric diseases and their associated genes ( [Gutiérrez-Sacristán et al., 2009](https://www.ncbi.nlm.nih.gov/pubmed/25964630) ).

## Features

- Responsive layout, suitable for multiple devices
- Modern GUIs
- Search for associations between different data
- Designed for continuous operation
- Authoritative and reliable data
