# fa-deploy-ws Setup

Setup guide for the internal `fa-deploy-ws` workspace used for FiveAges robot deployment.

```{admonition} Access Required
:class: warning

This workspace requires access to private repositories. Contact your team lead for access if needed.
```

```{admonition} Source of truth
:class: important

The `fa-deploy-ws` README is **not public**. After you have access, follow **that repository’s README** and its init / quick-start scripts. Flags, robot IDs, and on-robot YAML are documented only there.
```

## Overview

`fa-deploy-ws` is the internal counterpart of [open-deploy-ws](3-open_deploy_ws.md). Public users stay on `open-deploy-ws`.

What is verified on the **public** side and still applies as the pattern:

- Clone the workspace, then run **`./init_repo.sh`** (same script name as [open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md)).
- Do **not** `git submodule update --init --recursive`.
- After init, `colcon build`, then `source install/setup.bash` in the launch terminal (standard ROS overlay).

Extra flags, robot IDs, and on-robot YAML live in the private README — copy them from there.

## Related public pages

- [Install Environment](2-install_environment.md)
- [open-deploy-ws Setup](3-open_deploy_ws.md)
- [Workspace Layout](../3-concepts/2-workspace_layout.md)
- [Go to real hardware](../2-how_to/6-deployment/9-go_real_hardware/0-index.md)
- [WBC controller reference](../4-reference/controllers/3-ocs2_wbc.md)
