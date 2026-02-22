# Data Models

> [!IMPORTANT]
> The default branch has been converted to `tyu-refresh`, but the content is still under review https://github.com/Sage-Bionetworks/data-models/pull/43.  Once this PR is merged, the default branch will be converted back to `main`.  Feedback would be greatly appreciated.

The Curator-Extension (formerly Schematic) data model is used to create JSON Schemas for [Curator to enable the contribution of valid metadata](https://docs.synapse.org/synapse-docs/managing-metadata-with-curator). See [JSON Schema documentation](https://json-schema.org/). This can be used by those that prefer working in a tabular format (CSV) over JSON or LinkML. A data model is created in the format specified [here](https://python-docs.synapse.org/en/latest/explanations/curator_data_model/).  The Curator-Extension in the Synapse Python Client can be used to convert to JSON Schema.

This repository will recommend three different ways to maintaining your data model when using the CSV format.

1. One CSV
1. Modular CSV
1. Contextualized CSV

## One CSV

[example.model.csv](./one_csv/example.model.csv) is a CSV representation of the example data model.

## Modular CSV

When data models get larger, it becomes overwhelming to maintain it all in one csv.  In this scenario, users can choose to break down the csv into smaller, more manageable chunks.  The [modules](./modules) folder contain an example of how the [example.model.csv](./example.model.csv) is broken down.

## Contextualized CSV

Motivated by the ARK portal https://github.com/ARK-Portal/data_model data model, the data model can be created to utilize "contexts" in order to have context-specific conditionally required attributes with the bonus of also being able to define context-specific valid value lists for model attributes and more. An small example of this can be found in the [contexts](./contexts/) folder. Each data model is within it's own csv, a user can modularize this as well in whatever way they choose.  In this scenario, each "template" would have it's own data model csv and the generate-json-schema command would be run for each template csv instead of concatenating all of the CSV together.

---

# Descriptions of valid values

The "Valid Values" column for attributes often contain many values without any descriptions. In this scenario, you can add descriptions to these valid values by adding extra rows and having these valid values appear as "Attributes".

> [!CAUTION]
> When adding valid value as an Attirbute to add a description of the valid value, it CANNOT appear in any string value in the "DependsOn" column unless you wanted it to be a data model attribute as well.

---

# Manually Generating JSON schemas

To manually generate jsonschemas, you are required to install the Synapse Python Client along with the curation extension. Each of the data model options above will have slightly different methods of generating JSON schemas.

> [!NOTE]
> This section assumes that you already have working proficiency with Python.

```
pip install "synapseclient[curator]"
```

## One CSV

Generate all data model jsonschemas from one CSV.

```
synapse generate-json-schema one_csv/example.model.csv --data-model-labels display_label
```

## Modular CSV

Concatenate all CSVs and generate all data model jsonschemas from the assembled CSV.

```
python scripts/assemble_csv_data_model.py modules assembled.csv
synapse generate-json-schema assembled.csv --data-model-labels display_label
```

## Contextualized CSV

Generate a jsonschema from each data model CSV.

```
synapse generate-json-schema contexts/clinical_model.csv --data-model-labels display_label
synapse generate-json-schema contexts/genomic_model.csv --data-model-labels display_label
```

---

# Best Practices: Operations for Data Models

## Purpose

This describes operational best practices for:

1. Ensuring day-to-day data model edits reliably produce JSON Schemas that work with Synapse Curator.
2. Creating official, versioned JSON Schema releases registered in Synapse.
3. Maintaining clear separation between **test (development)** and **production (released)** schema environments.

This guidance focuses on governance, change management, and release discipline.

---

## Guiding Principles

1. **The data model is a product.** It requires ownership, review, and lifecycle management.
2. **Schemas used in production must be immutable.**
3. **Development and production environments must be separated.**
4. **Validation must be reproducible and versioned.**
5. **Portals own their schemas.** Each portal is responsible for maintaining its own schema lifecycle.

---

## Environment Separation: Recommended Organizational Structure

Each portal is recommended to maintain **two separate Synapse schema organizations**.


### Test Schema Organization (Development)

**Purpose**

- Rapid iteration
- Curator compatibility testing
- Pre-release schema staging

**Characteristics**

- Schemas may change frequently.
- Versions may be overwritten.
- Clearly labeled as **non-production**.

**Recommended naming conventions**

- `test.sage.{portal_name}`

### Production Schema Organization (Released)

**Purpose**

- Official, versioned schema releases
- Stable references for Curator

**Characteristics**

- Schemas are immutable once released.
- Organized by version.
- Ideally never overwritten.

**Recommended naming conventions**

- `sage.schemas.{portal_name}`
- `org.synapse.{portal_name}`

---

## Daily Model Edits (Test Environment)

Ensure routine data model changes work with Synapse Curator and remain aligned with operational expectations.

### Every change should generate JSON Schemas

No model change is considered complete until JSON schemas are able to be generated and registered into the Test Schema Organization to ensure Synapse Curator compliance.

---

## Official Schema Releases (Production)

Create reproducible, traceable, immutable schema releases registered in Synapse.

### Schemas are versioned using explicit release numbers

Recommended: **Semantic Versioning**

- **MAJOR** – breaking changes
- **MINOR** – backward-compatible additions
- **PATCH** – non-breaking fixes

Versioning applies to the release set, not individual ad hoc files.

### Production releases must be immutable

Once a schema version is registered in the Production Schema Organization, it should never be modified. Corrections to the schema require a new version.

### Formal Release Process

Each portal should define a lightweight but explicit release process of their data model to

1. Confirm all changes can create Synapse compliant JSON schemas
1. Ability to create release artifacts within GitHub (e.g. use GitHub Release + tag feature)
1. Generate and register versioned JSONschemas to production JSONschema organization

---

# Using GitHub Actions

This repository also contains [template github actions](.github/workflows/ci.yml) that will generate jsonschemas from each of the recommended data model maintenance approaches.  These github action workflows lightly implement the what was described in the "Best Practices: Operations for Data Models" section above but Sage Portal Owners do NOT have to use these workflows to achieve the best practices.

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
