# GENE

- `ID`: The ID of GENE.
- `Chromsome`: The chromsome on which gene exists.
- `Start`: The 0-based start position of gene.
- `End`: The 0-based end position of gene.
- `Gene symbol`: The gene symbol of gene.

---

## Search GENE

- `ID`: The ID of GENE. Multiple entries should be separated by commas.
- `Chromsome`: The chromsome on which gene exists. Multiple entries should be separated by commas.
- `Start`: The 0-based start position of search. Genes between `Start` and `End` will be found.
- `End`: The 0-based end position of search. Genes between `Start` and `End` will be found.
- `Gene symbol`: The gene symbol of gene. Multiple entries should be separated by commas.

Search criteria that are not entered are considered to be unrestricted.

## Search GENE by G4 data

- `G4 ID`: The ID of G4. Multiple entries should be separated by commas. The relevant genes will be found.

Search criteria that are not entered are considered to be unrestricted.

## Search GENE by GDA data

- `GDA ID`: The ID of GDA. Multiple entries should be separated by commas. The relevant genes will be found.
- `Disease name`: The disease name of GDA data. Multiple entries should be separated by spaces. GDA data which containing these keywords will be found regardless of the case of letters. The relevant genes will be found.

Search criteria that are not entered are considered to be unrestricted.
