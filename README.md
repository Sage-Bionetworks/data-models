# Data Models

The Curator-Extension (formerly Schematic) data model is used to create JSON Schemas for [Curator to enable the contribution of valid metadata](https://docs.synapse.org/synapse-docs/managing-metadata-with-curator). See [JSON Schema documentation](https://json-schema.org/). This can be used by those that prefer working in a tabular format (CSV) over JSON or LinkML. A data model is created in the format specified [here](https://python-docs.synapse.org/en/latest/explanations/curator_data_model/).  The Curator-Extension in the Synapse Python Client can be used to convert to JSON Schema.

This repository will recommend two different ways to maintaining your data model when using the CSV format.

1. One CSV
1. Modularize your CSV

## One CSV

`example.model.csv`: The CSV representation of the example data model. This file is created by the collective effort of data curators and annotators from a *community* (e.g. *HTAN*), and will be used to create the jsonschemas used within Curator.

## Modular CSV

The `modules` folder will contain the CSV but broken down into smaller CSVs and concatenated together at the end.

> NOTE: Data models can become really large and often times the "Valid Values" column can often contain many values without any descriptions. In this scenario, you can add descriptions to these valid values by adding extra rows in your data model csv under one condition.  The valid value CANNOT appear in any string value in the "DependsOn" column unless you wanted it to be a valid value of a column AND a column.

# Generating JSON schemas

To generate jsonschemas, you will want to install the Synapse Python Client along with the curation extension.

```
pip install "synapseclient[curator]"
```

To generate jsonschemas

```
synapse generate-json-schema example.model.csv --data-model-labels display_label
```

If you are using the modular CSV method, you will want to follow these instructions

```
python scripts/assemble_csv_data_model.py modules assembled.csv
synapse generate-json-schema assembled.csv --data-model-labels display_label
```

# GitHub Actions Best Practices

## Avoiding Merge Conflicts with Automated Commits

**Try to avoid** configuring GitHub Actions to commit generated files (like assembled CSVs or JSON schemas) back to the repository. This practice commonly leads to merge conflicts and complicates collaborative workflows.

### Problems with automated commits:
- Creates merge conflicts when multiple contributors work simultaneously
- Makes git history noisy with automated commits
- Complicates branch management and pull request reviews
- Can cause infinite loops if not properly configured

### Recommended alternative: Use GitHub Artifacts

Store generated files as build artifacts that can be downloaded

```yaml
- name: Upload assembled CSV
  uses: actions/upload-artifact@v6
  with:
    name: assembled-data-model
    path: assembled.csv
```

This approach keeps your repository clean while still providing access to generated files for downstream consumers and for github tagged releases, it will retain the artifact "forever"
