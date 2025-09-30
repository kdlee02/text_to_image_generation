# Data Directory

This directory is used for storing optimization results, cached data, and other persistent files.

## Structure

- `results/` - Optimization results and logs
- `cache/` - Cached evaluation results to avoid re-computation
- `models/` - Downloaded or cached model files
- `exports/` - Exported data and reports

## File Naming Conventions

- Optimization results: `optimization_results_YYYYMMDD_HHMMSS.json`
- Cached evaluations: `eval_cache_[hash].json`
- Exported reports: `report_YYYYMMDD.html`

## Cleanup

To clean up old data files, you can safely delete files older than 30 days from the `cache/` directory.