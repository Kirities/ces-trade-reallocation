# Reproduction, data dictionary, and figure guide

[中文版本](../zh-CN/reproducibility.md)

## Execution

Run commands from the repository root. Python 3.12 is the tested interpreter; the analytical scripts and tests use only the standard library. Figure rendering additionally needs the exact versions in `requirements.txt`.

```sh
python scripts/analyze.py
python scripts/figures.py
python scripts/validate.py
python -m unittest discover -s tests -v
```

`python scripts/reproduce.py` runs the same sequence. No API key, external account, source PDF, notebook service, or network call is needed after dependencies are installed. The raw-data manifest pins the archived extract by SHA-256. Live source pages can change; refreshing data requires an explicit new extract and documented vintage, rather than silently overwriting the original.

## Inputs and outputs

| File | Variables and interpretation |
|---|---|
| `data/raw/census_annual_extract.csv` | `partner`: Vietnam, China, or World; `year`: 2010-2024; `us_exports_musd`, `us_imports_musd`, `us_balance_musd`: U.S.-perspective goods values in nominal million USD |
| `data/raw/manifest.json` | Retrieval date, source URLs, units, extraction method, extract hash |
| `config/scenarios.json` | Scenario grid and benchmark; no parameter is presented as econometrically estimated |
| `results/annual_indicators.csv` | Import totals, residual rest of world, origin shares as fractions, 2017-based indices |
| `results/growth_decomposition.csv` | Endpoint years, change and both components in million USD; compound growth as a fraction; share change in percentage points |
| `results/scenario_grid.csv` | Calibration year, elasticity, tariff fractions, cost multiplier, assumed DVA fraction, resulting shares, price index, real-bundle percentage change, customs-receipt percentage change, revenue and compensation per USD 100, DVA proxy per USD 100 |
| `results/summary.json` | Principal empirical and model values used in the narrative |
| `results/validation.json` | Automated data, accounting, model-grid, link, and artifact checks with execution environment |

There are no missing observations within the selected 45-row extract. `World` is a total, so adding it to partner rows would double count. Neither imports from Vietnam nor the DVA proxy represent Vietnam's GDP. `dva_proxy_per_100` is a level, not a change, and records with different DVA assumptions reuse the same allocation.

## Figure guide

| Figure | Evidence type | Underlying data and interpretation |
|---|---|---|
| `trade_reallocation` | Observed and derived | Annual indicator table; an index panel and a common-scale import-share panel. Shading denotes the period from 2018, not a causal estimate. |
| `growth_decomposition` | Exact accounting | 2017-2024 row of the decomposition table; bars start at zero. |
| `scenario_sensitivity` | Illustrative model | Deterministic cost curves for four elasticities and retained-value curves for two Vietnam tariffs. No empirical uncertainty bands. |
| `cost_tariff_frontier` | Illustrative model | A fine grid at 2017 weights and elasticity 4; black line marks zero customs-receipt gain. The shared color scale is centered at zero. |

PNG files support ordinary repository viewing; SVG preserves editable vectors and text. English labels are shared between language versions. Captions and alt text distinguish observed values from assumptions. Alternative line styles and a directly labeled frontier supplement color; these choices are not a certification of universal accessibility.

## What validation establishes

The validator checks source-hash agreement, unique complete partner-year keys, finite values, balance arithmetic within rounding tolerance, positive residual imports, shares, decomposition identities, full-grid scenario reconstruction, the analytical cost threshold, bilingual document presence, relative Markdown links, and PNG/SVG existence. Unit tests cover baseline recovery, tariff/customs accounting, uniform price scaling, uniform tariffs, cost sensitivity, and invalid inputs. Figures were also inspected visually.

These checks establish internal consistency and actual local execution. They do not establish human review, causal identification, an independently audited source dataset, general-equilibrium validity, or acceptance by a journal. A clean-environment package installation on another machine is not inferred from the local run.
