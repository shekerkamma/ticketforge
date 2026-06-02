# AI Analyst Workspace Layout

Use this layout when bootstrapping or repairing an analytics workspace.

```text
<workspace>/
├── .knowledge/
│   ├── user/
│   ├── datasets/
│   ├── analyses/
│   ├── corrections/
│   ├── setup-state.yaml
│   └── active.yaml
├── data/
├── outputs/
└── working/
    └── runs/
```

Recommended durable artifacts:
- `.knowledge/user/profile.md`
- `.knowledge/user/business-context.md`
- `.knowledge/datasets/<dataset-id>/manifest.yaml`
- `.knowledge/datasets/<dataset-id>/schema.md`
- `.knowledge/datasets/<dataset-id>/metrics/index.yaml`
- `.knowledge/analyses/index.yaml`
- `.knowledge/corrections/index.yaml`
- `working/runs/<timestamp>_<slug>/`
