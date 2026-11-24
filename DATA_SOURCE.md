# Data source and reuse

- Dataset: Student Performance.
- Creator: Paulo Cortez.
- Citation: Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T.
- Dataset page: https://archive.ics.uci.edu/dataset/320/student+performance
- Download: https://archive.ics.uci.edu/static/public/320/student+performance.zip
- Accessed: 24 November 2026. No account was required.
- License shown by UCI: Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/. This permits redistribution and adaptation with attribution. No endorsement is implied.
- File included: `student-mat.csv`, extracted from the nested `student.zip`. Original CSV bytes are unchanged. Portuguese-language data is not used.
- SHA-256: `e47f9ee225e1ee6e69b7564e6dac7123e80b8486677fe111f351964cef5dec80`.
- Source data shape checked: 395 rows, 33 columns, no missing cells, no identical full rows.
- Changes: none to the source CSV. Grouped summaries and the chart are new derived outputs.

## Relevant fields

- `studytime`: reported weekly study hours, 1 = under 2, 2 = 2-5, 3 = 5-10, 4 = over 10. These are category labels, not exact hours.
- `G3`: final grade, 0 to 20. Zero grades are retained.
- `failures`: recorded past class failures. This analysis compares zero with any value above zero; it does not interpret the higher codes as exact counts.

See UCI for the full original field descriptions.
