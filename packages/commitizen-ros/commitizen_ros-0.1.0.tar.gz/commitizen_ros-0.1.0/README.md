# Commitizen ROS

A python package implementing a Commitizen Version Provider for ROS Package
Manifests

## Quick Start

Install with `pip`...

```bash
python3 -m pip install commitizen-ros
```

...and add the provider to your Commitizen configuration:
```toml
[tool.commitizen]
version_provider = [.., "commitizen_ros", ...]
```

## Description

The Commitizen ROS package adds ROS 1 and 2 `project.xml` package manifests
defined as per [REP127 (format 1)](https://ros.org/reps/rep-0127.html) and
[REP140 (format 2)](https://www.ros.org/reps/rep-0140.html) as sources and
targets for version data in
[Commitizen](https://commitizen-tools.github.io/commitizen/).


## Usage
No configuration is required (beyond adding the provider to your Commitizen
configuration) as the ROS `project.xml` name and location and contents are
specified by REPs 127 and 140.


## License
This package is licensed under the MIT License
