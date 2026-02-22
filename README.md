# Data Models

This repository contains 1 file and reusable github actions:

1. `example.model.csv`: The CSV representation of the example data model. This file is created by the collective effort of data curators and annotators from a *community* (e.g. *HTAN*), and will be used to create the jsonschemas used within Curator.

Data models can become really large and often times the "Valid Values" column can often contain many values without any descriptions. In this scenario, you can add descriptions to these valid values by adding extra rows in your data model csv under one condition.  The valid value CANNOT appear in any string value in the "DependsOn" column unless you wanted it to be a valid value of a column AND a column.

## How to use

This data model repository will allow you to maintain your data model in a way that is more intuitive than writing jsonschemas.  Each template will generate a specific jsonschema and these jsonschemas can be used in Curator on Synapse: https://docs.synapse.org/synapse-docs/managing-metadata-with-curator.

To generate jsonschemas, you will want to install the Synapse Python Client along with the curation extension.

```
pip install "synapseclient[curator]"
```

To generate jsonschemas

```
synapse generate-json-schema example.model.csv --data-model-labels display_label
```
