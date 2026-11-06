# Methods and mathematical specification

[中文版本](../zh-CN/methods.md)

## 1. Measurement

Let $X_{Vy}$ denote U.S. nominal goods imports from Vietnam in year $y$, and $M_y$ total U.S. goods imports. Define $s_{Vy}=X_{Vy}/M_y$ and analogously $s_{Cy}$ for China. The rest-of-world amount is $M_y-X_{Vy}-X_{Cy}$. Units in CSV files are million USD; charts explicitly convert to billion USD or percentages. Census balances use the U.S. perspective: exports minus imports. Rounding discrepancies up to 0.11 million USD are allowed in the validation script.

Compound growth over $n$ annual intervals is $(X_1/X_0)^{1/n}-1$. Index charts use $100X_y/X_{2017}$. No seasonal adjustment, deflation, interpolation, imputation, or outlier removal is applied. Historical revisions are retained as retrieved, not reconstructed to an earlier vintage.

## 2. Symmetric growth decomposition

Since $X_V=s_VM$, the exact two-period identity is

$$\Delta X_V=\bar{s}_V\Delta M+\bar{M}\Delta s_V,$$

where bars denote arithmetic endpoint averages. Equivalently, the market term is $s_0\Delta M+\tfrac12\Delta s\Delta M$ and the share term is $M_0\Delta s+\tfrac12\Delta s\Delta M$. This is the average of the two possible sequential decompositions and assigns the interaction equally.

For 2017-2024, the components are USD 28,482.80 million and USD 61,357.40 million, summing to USD 89,840.20 million. The share component divided by the total is 68.30%. No term is identified as a causal effect.

## 3. Import-demand model

There are three differentiated origins $i\in\{V,C,R\}$. Baseline expenditure weights $w_i>0$ sum to one and are taken from one calibration year. Prices are normalized to one at that benchmark. A CES import aggregate is

$$Q=\left[\sum_i w_i^{1/\sigma}q_i^{(\sigma-1)/\sigma}\right]^{\sigma/(\sigma-1)},\qquad \sigma>1.$$

Producer-cost multipliers $c_i>0$ and hypothetical nonnegative ad valorem tariffs $t_i$ imply delivered prices $p_i=c_i(1+t_i)$. Cost minimization yields

$$D=\sum_iw_ip_i^{1-\sigma},\quad P=D^{1/(1-\sigma)},\quad s_i'=\frac{w_ip_i^{1-\sigma}}{D}.$$

For fixed tariff-inclusive expenditure $E=100$, tariff-exclusive customs value is $B_i=Es_i'/(1+t_i)$, quantity is $q_i=Es_i'/p_i$, and tariff revenue is $T=\sum_it_iB_i$. Thus $\sum_iB_i+T=E$. A cost multiplier is treated as a producer-price change with full transmission; no independent pass-through parameter or supply equilibrium is estimated.

The baseline uses $t_i=0$ and $c_i=1$, implying $P_0=1$, $s_i'=w_i$, and $Q_0=E$. Existing price and tariff differences are absorbed into benchmark weights. A hypothetical new tariff should therefore be understood as a wedge relative to this normalization. Applying it uniformly to all Chinese imports is deliberately stylized and does not reproduce actual product coverage.

## 4. Purchasing power and fiscal accounting

The model real bundle is $Q=E/P$, and its percentage change is $100(1/P-1)$. Compensation required at new prices to afford the baseline bundle is $CV=E(P-1)$ because $Q_0=E$. This is a conditional import-bundle compensating variation before tariff-revenue transfers, not an economy-wide welfare measure.

Revenue is not recycled into $E$. Adding revenue to expenditure after the fact would change demand and require a new budget closure. The repository therefore reports revenue and compensation separately and does not subtract them to claim a net welfare effect. Exporter customs receipts are also distinct from exporter profits or value added.

## 5. Cost threshold

Set Vietnam's tariff to zero, all other producer costs to one, and China's tariff to $\tau$. Vietnam's receipts equal baseline receipts when $s_V'=w_V$. Writing $r=1-w_V-w_C$ gives

$$c_V^*=\left[\frac{w_C(1+\tau)^{1-\sigma}+r}{1-w_V}\right]^{1/(1-\sigma)}.$$

With 2017 weights, $\sigma=4$, and $\tau=0.25$, $c_V^*=1.038639$, or a 3.86% cost increase. This is an algebraic boundary of the model, not an estimate of Vietnam's observed cost shock. It depends on the absence of a tariff on Vietnam; with a Vietnam tariff, customs receipts and expenditure shares no longer move proportionately.

## 6. Domestic-value proxy

For an assumed fraction $\lambda\in\{0.25,0.50,0.75\}$, define $A_V=\lambda B_V$. It is a retained-value accounting proxy at an assumed domestic-content fraction. No input-output coefficients, ownership adjustments, repatriated profits, or environmental externalities are measured. Increasing $\lambda$ is not a costless policy experiment: its costs are simply outside the model. It never changes demand shares in the implementation.

## 7. Parameter design and model boundaries

The Cartesian grid has 3 calibration years, 4 elasticities, 3 China tariffs, 2 Vietnam tariffs, and 4 Vietnam costs: 288 allocations. Adding 3 domestic-content fractions produces 864 rows. Plotting scripts also evaluate a deterministic fine grid for the displayed cost curves and frontier; these display calculations are not additional observations or estimated uncertainty.

The model assumes fixed nominal import expenditure, identical substitution elasticity across origins, unchanged origin preferences, perfectly elastic producer prices except for imposed cost shifts, full tariff transmission, and an aggregated rest of world. There is no domestic U.S. alternative, income feedback, retaliation, investment dynamics, endogenous capacity, input network, or bilateral exchange rate. Calibration matches benchmark shares by construction and does not validate the model's response parameters. Sensitivity ranges are neither estimated confidence intervals nor forecasts.
