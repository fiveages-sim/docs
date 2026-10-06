# Contributing

Guidelines for contributing to FiveAges Sim repositories.

## Code of Conduct

Be respectful and constructive in all interactions.

## Ways to Contribute

### Bug Reports

File issues with:
- Clear title describing the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Ubuntu version, ROS 2 distro)

### Feature Requests

Open an issue describing:
- Use case and motivation
- Proposed solution
- Alternatives considered

### Code Contributions

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit a pull request

### Documentation

- Fix typos or unclear explanations
- Add missing documentation
- Improve examples

## Development Setup

### Clone and Build

```bash
git clone https://github.com/fiveages-sim/<repo>.git
cd <repo>
# Follow repository-specific setup
colcon build
```

### Code Style

- Follow existing code style
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused

### Testing

- Test changes locally before submitting
- Add unit tests for new features
- Ensure existing tests pass

## Pull Request Process

### Before Submitting

- [ ] Code builds without errors
- [ ] Tests pass
- [ ] Documentation updated if needed
- [ ] Commit messages are clear

### PR Description

Include:
- Summary of changes
- Related issue (if any)
- Testing performed
- Breaking changes (if any)

### Review Process

1. Maintainer reviews code
2. Feedback addressed
3. Approval and merge

## Commit Messages

Use clear, descriptive commit messages:

```
Add support for new gripper model

- Add URDF for XYZ gripper
- Implement hardware interface
- Add launch file integration

Closes #123
```

## Licensing

Contributions are licensed under the repository's license. Ensure you have the right to contribute the code.

```{admonition} TODO
:class: warning

Organization-wide contribution guidelines and CLA process to be finalized.
```
