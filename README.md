# CADFEM-Bench website

A plain-language guide to [CADFEM-Bench](https://huggingface.co/datasets/Conditiondark/cadfem-bench) v1.9: 217 CAD +
finite-element tasks for AI models, each phrased as a question, with renders of the real CAD parts, how scoring works and
GPT-6 Astra's first results. The site shows no reference answers.

Live site: https://ayushdebnath012.github.io/cadfem-bench/

- Benchmark data: https://huggingface.co/datasets/Conditiondark/cadfem-bench
- Two Astra failures explained step by step: [a wrong number](https://ayushdebnath012.github.io/cadfem-bench/case-study.html) and [no answer](https://ayushdebnath012.github.io/cadfem-bench/case-study-2.html)
- One spec page per task (overview, flow, input, output, evaluation): [specs/](specs/README.md)
- Per-task input / output / metric spec: [task-specs.csv](task-specs.csv), [task-specs.json](task-specs.json)
- Astra failure study: https://huggingface.co/datasets/Conditiondark/astra-cadfem-failures

Each task keeps its source's licence (listed per task in the benchmark). The site text, renders and page code are CC BY 4.0.
