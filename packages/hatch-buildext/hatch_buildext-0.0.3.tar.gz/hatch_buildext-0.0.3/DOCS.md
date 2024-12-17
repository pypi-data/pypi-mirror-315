# Config format

```toml
# pyproject.toml
[tool.hatch.build.targets.wheel.hooks.buildext]
dependencies = ["hatch-buildext"]

[tool.hatch.build.targets.wheel.hooks.buildext.options]
# TODO: ...

[tool.hatch.build.targets.wheel.hooks.buildext.extensions]
myapp = "path.to.resolver"
```
