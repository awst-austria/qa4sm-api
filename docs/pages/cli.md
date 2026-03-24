# Command Line Programs

This package includes a `qa4sm` command-line interface that provides convenient access to common QA4SM API operations.

## Quick Start

All CLI commands share the `--instance` option to specify the QA4SM instance:
```bash
qa4sm --instance qa4sm.eu <command>
```

The default instance is `qa4sm.eu`.

**Note:** Only `qa4sm.eu` is relevant for most users.

## Available Commands

### Authentication Commands

#### `qa4sm api setup`

Authenticate and store your API token for the QA4SM instance.

```bash
qa4sm api setup
```

This command will:
- Prompt you for your QA4SM username and password
- Retrieve your API token from the QA4SM service
- Store the token in `~/.qa4smapirc` for future use

**Options:**
- `-i, --instance TEXT`: QA4SM instance to authenticate with [default: qa4sm.eu]

#### `qa4sm api check`

Verify that your stored credentials allow access to a QA4SM instance.

```bash
qa4sm api check
```

**Options:**
- `-i, --instance TEXT`: QA4SM instance to check [default: qa4sm.eu]

### Validation Commands

#### `qa4sm validate`

Start a new validation run using a configuration file.

```bash
qa4sm validate CONFIG_FILE
```

This command submits a validation job to the QA4SM service for processing.

**Arguments:**
- `CONFIG_FILE`: Path to the validation configuration JSON file

**Options:**
- `-i, --instance TEXT`: QA4SM instance to submit validation to [default: qa4sm.eu]

**Example:**
```bash
qa4sm validate my_validation_config.json
```

### Download Commands

#### `qa4sm download config`

Download the configuration JSON file from an existing validation run.

```bash
qa4sm download config RUN_ID
```

**Arguments:**
- `RUN_ID`: Validation run ID (UUID) to download configuration for

**Options:**
- `-o, --out_path PATH`: Path where the config file is stored [default: current directory]
- `-i, --instance TEXT`: QA4SM instance [default: qa4sm.eu]

**Example:**
```bash
qa4sm download config 9aeb663b-e24e-4541-8331-6ec3e0318d1f -o configs/
```

#### `qa4sm download results`

Download all results (NetCDF, graphics, statistics) from a validation run.

```bash
qa4sm download results RUN_ID
```

This command downloads:
- NetCDF data file (`<run_id>.nc`)
- Graphics (extracted to `qa4sm_graphics/` directory)
- Summary statistics CSV (`summary_stats.csv`)

**Arguments:**
- `RUN_ID`: Validation run ID (UUID) to download results for

**Options:**
- `-o, --out_path PATH`: Path where results are stored [default: current directory]
- `-i, --instance TEXT`: QA4SM instance [default: qa4sm.eu]

**Example:**
```bash
qa4sm download results 9aeb663b-e24e-4541-8331-6ec3e0318d1f -o results/
```

## Common Workflow

A typical workflow using the CLI:

```bash
# 1. Set up authentication (first time only)
qa4sm api setup

# 2. Check that authentication works
qa4sm api check

# 3. Download a configuration template from an existing run
qa4sm download config 9aeb663b-e24e-4541-8331-6ec3e0318d1f -o templates/

# 4. Edit the configuration template
vim templates/9aeb663b-e24e-4541-8331-6ec3e0318d1f.json

# 5. Submit a new validation with your configuration
qa4sm validate my_config.json

# 6. Download the results when the validation is complete
qa4sm download results <new_run_id> -o results/
```

## Getting Help

Get help for any command:

```bash
# General help
qa4sm --help

# Help for a specific command
qa4sm validate --help
qa4sm download --help
qa4sm api --help
```

## Notes

- The CLI uses the same authentication mechanism (`~/.qa4smapirc`) as the Python API
- All commands output helpful messages about their progress
- The download commands will create directories if they don't exist
- Run IDs are UUIDs and can be found in validation URLs on the QA4SM web interface
- Only `qa4sm.eu` is relevant for most users; other instances (test.qa4sm.eu, etc.) are for development purposes only