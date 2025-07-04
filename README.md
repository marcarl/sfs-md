# Svensk författningssamling (SFS) som Markdown-filer

Detta repository innehåller Python-script för att ladda ner och konvertera SFS-författningar (Svensk författningssamling) från antingen Regeringskansliets publika söktjänst eller Riksdagens öppna API. Konvertering till Markdown sker med en uppsättning regler.

## Installation

1. Se till att du har Python 3.6+ installerat
2. Installera nödvändiga beroenden:

```bash
pip install -r requirements.txt
```

## Användning

### Välj källa för nedladdning

Scriptet stöder två olika källor:

- **rkrattsbaser** (standard): Hämtar strukturerad JSON-data från Regeringskansliets Elasticsearch API
- **riksdagen**: Hämtar HTML-filer från Riksdagens öppna data

### Ladda ner från Regeringskansliet (standard)

#### Ladda ner alla SFS-författningar

```bash
python download_sfs_documents.py
```

eller explicit:

```bash
python download_sfs_documents.py --source rkrattsbaser
```

**Observera:** För rkrattsbaser måste du ange specifika författnings-ID:n med `--ids` parametern.

#### Ladda ner specifika författningar från Regeringskansliet

```bash
python download_sfs_documents.py --ids "2025:764,2025:765"
```

### Ladda ner från Riksdagen

#### Ladda ner alla SFS-författningar från Riksdagen

```bash
python download_sfs_documents.py --ids all --source riksdagen
```

#### Ladda ner specifika författningar från Riksdagen

```bash
python download_sfs_documents.py --ids "sfs-2017-900,sfs-2009-400,sfs-2011-791" --source riksdagen
```

#### Med anpassad output-mapp

```bash
python download_sfs_documents.py --source rkrattsbaser --ids "2025:764" --out "sfs_json"
```

### Ange output-mapp

Du kan ange vilken mapp författningarna ska sparas i med `--out` parametern:

```bash
python download_sfs_documents.py --out "sfs_docs"
```

Eller kombinera med specifika författnings-ID:n:

```bash
python download_sfs_documents.py --ids "sfs-2017-900,sfs-2009-400" --out "mina_favorit_lagar"
```

### Exempel med Swedac-lagar

För att ladda ner alla lagar som styr Swedac till en specifik mapp:

```bash
python download_sfs_documents.py --ids "sfs-2017-900,sfs-2009-400,sfs-2009-641,sfs-2021-1252,sfs-2011-791,sfs-2011-811,sfs-2019-16,sfs-1991-93,sfs-1993-1634,sfs-2014-864,sfs-2002-574,sfs-2009-211,sfs-2006-985,sfs-2006-1592,sfs-2016-1128,sfs-2009-1079,sfs-2009-1078,sfs-2010-900,sfs-2011-338,sfs-2011-1244,sfs-2011-1261,sfs-1992-1514,sfs-1993-1066,sfs-1994-99,sfs-1997-857,sfs-1999-716,sfs-2005-403,sfs-2006-1043,sfs-2011-318,sfs-2011-345,sfs-2011-1200,sfs-2011-1480,sfs-2012-211,sfs-2012-238,sfs-1975-49,sfs-1999-779,sfs-1999-780" --out "swedac_lagar"
```

## Kommandoradsalternativ

```bash
python download_sfs_documents.py [--ids IDS] [--out MAPP] [--source KÄLLA]
```

### Parametrar

- `--ids`: Kommaseparerad lista med dokument-ID:n att ladda ner, eller "all" för att hämta alla från Riksdagen (default: "all")
- `--out`: Mapp att spara nedladdade dokument i (default: "sfs_docs")
- `--source`: Välj källa - "riksdagen" för HTML-format eller "rkrattsbaser" för JSON-format (default: "riksdagen")
