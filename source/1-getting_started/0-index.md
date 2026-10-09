# Introduction

This section guides you through setting up your development environment and running your first robot demos.

**Read in this order** (same as the sidebar):

1. [Install Environment](2-install_environment.md)
2. [Quick Demo (Public)](1-quick_demo_public.md)
3. [open-deploy-ws Setup](3-open_deploy_ws.md) / [fa-deploy-ws Setup](4-fa_deploy_ws.md)
4. [FAQ](5-faq.md) if something fails

Do not start with the Quick Demo before ROS 2 Jazzy + rosdep are installed.

## Prerequisites

Before you begin, ensure you have:

- **Ubuntu 24.04** (Jazzy Jalisco target platform)
- **ROS 2 Jazzy** installed
- **Python 3.12** (Jazzy baseline; do not mix 3.10/3.11 venvs)
- **Git** with GitHub access (SSH key, or HTTPS / `gh` auth — `.gitmodules` remotes are SSH)
- **16GB+ RAM** recommended for builds with simulation
- **NVIDIA GPU** (optional, required for Isaac Sim)

## Choose Your Path

| If you are... | Start with... |
|---------------|---------------|
| Setting up from scratch | [Install Environment](2-install_environment.md) |
| Environment already installed | [Quick Demo (Public)](1-quick_demo_public.md) |
| Using public robots | [open-deploy-ws Setup](3-open_deploy_ws.md) |
| FiveAges team member | [fa-deploy-ws Setup](4-fa_deploy_ws.md) |
| Troubleshooting | [FAQ](5-faq.md) |

## Quick Path Summary

```{mermaid}
flowchart LR
    A[Install ROS 2 Jazzy] --> B{Which path?}
    B -->|Public| C[Clone open-deploy-ws]
    B -->|Internal| D[Clone fa-deploy-ws]
    C --> E[./init_repo.sh]
    D --> F[./init_repo.sh]
    E --> G[colcon build]
    F --> G
    G --> H[Run demo.launch.py]
```

## Time Estimates

| Task | Time |
|------|------|
| ROS 2 Jazzy installation | 15-30 minutes |
| Workspace clone + init | 5-10 minutes |
| Full workspace build | 10-30 minutes |
| First demo launch | 2-5 minutes |

## What's Next

After completing setup:
1. Follow the [Learning Path](../0-overview/2-learning_path.md) for structured learning
2. Continue by role in [More applications](../6-more_applications/0-index.md) (现场调试, 传统方案算法工程师, VLA 采训推, 仿真工程师)
3. Explore [How-To Guides](../2-how_to/0-index.md) for specific tasks
4. Reference the [Architecture](../0-overview/1-architecture.md) when you need context
