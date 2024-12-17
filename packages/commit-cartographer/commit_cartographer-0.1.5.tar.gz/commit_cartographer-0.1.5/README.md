# Commit Cartographer

A Python tool that generates visual flowcharts of Git repository activity by analyzing commit patterns across directories.

## Features

- 🔍 **Intelligent Analysis**: Counts commits per directory while focusing only on currently existing structure
- 📊 **Visual Representation**: Generates Mermaid flowcharts with directory relationships
- 🎨 **Color Gradients**: Uses a 10-step color gradient to represent commit density
- 🌳 **Directory Depth**: Supports up to 4 levels of directory nesting
- 📁 **Repository Structure**: Shows parent-child relationships between directories


## Installation

To use this project, ensure you have [uv](https://github.com/astral-sh/uv) installed.

## Usage

To run the tool, execute the following command in your terminal:

```bash
uv run commit-cartographer/cli.py [path_to_your_repo]
```

If no path is provided, it defaults to the current directory.

## Output

The script generates a Markdown file named `git_activity.md`, which contains the Mermaid flowchart diagram representing the commit activity in the specified Git repository.

## Example

After running the script, you will find a `git_activity.md` file with content similar to the following:

```mermaid
flowchart LR
    root_node[/root\]
    style root_node fill:#ffffff,stroke:#333,stroke-width:2px
    root_node --> node_src[/src\]
    style node_src fill:#ff00ff,stroke:#333,stroke-width:2px
    root_node --> node_cla[/cla\]
    style node_cla fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_aws[/aws\]
    style node_src_aws fill:#55aaff,stroke:#333,stroke-width:2px
    root_node --> node_icons[/icons\]
    style node_icons fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_php[/php\]
    style node_src_php fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_az[/az\]
    style node_src_az fill:#00ffff,stroke:#333,stroke-width:2px
    node_src_az --> node_src_az_2.53.0[/2.53.0\]
    style node_src_az_2.53.0 fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_heroku[/heroku\]
    style node_src_heroku fill:#00ffff,stroke:#333,stroke-width:2px
    root_node --> node_.vscode[/.vscode\]
    style node_.vscode fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_infracost[/infracost\]
    style node_src_infracost fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_fig[/fig\]
    style node_src_fig fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_usermn[/usermn\]
    style node_src_usermn fill:#00ffff,stroke:#333,stroke-width:2px
    node_src_usermn --> node_src_usermn_sdc[/sdc\]
    style node_src_usermn_sdc fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_deno[/deno\]
    style node_src_deno fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_dotnet[/dotnet\]
    style node_src_dotnet fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_example[/example\]
    style node_src_example fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_shopify[/shopify\]
    style node_src_shopify fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_task[/task\]
    style node_src_task fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_capgo[/capgo\]
    style node_src_capgo fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_wordpress[/wordpress\]
    style node_src_wordpress fill:#00ffff,stroke:#333,stroke-width:2px
    root_node --> node_.devcontainer[/.devcontainer\]
    style node_.devcontainer fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_magnolia[/magnolia\]
    style node_src_magnolia fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_gcloud[/gcloud\]
    style node_src_gcloud fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_python[/python\]
    style node_src_python fill:#00ffff,stroke:#333,stroke-width:2px
    node_src --> node_src_preset[/preset\]
    style node_src_preset fill:#00ffff,stroke:#333,stroke-width:2px
    root_node --> node_.husky[/.husky\]
    style node_.husky fill:#00ffff,stroke:#333,stroke-width:2px
```
You can also add the `--style` option to generate a tree diagram:

```bash
uv run commit-cartographer/cli.py [path_to_your_repo] --style tree
```
```
root/
└── orchestration/ (26 commits)
    └── assets/ (20 commits)
        └── dbt/ (4 commits)
        └── ebirdapi/ (14 commits)
            └── .dlt/ (2 commits)
            └── schemas/ (4 commits)
                └── export/ (2 commits)
                └── import/ (2 commits)
    └── utils/ (2 commits)
└── orchestration_tests/ (4 commits)
└── schemas/ (10 commits)
    └── export/ (5 commits)
    └── import/ (5 commits)
└── scripts/ (3 commits)
└── transformation/ (57 commits)
    └── analyses/ (1 commits)
    └── macros/ (1 commits)
    └── models/ (43 commits)
        └── sources/ (6 commits)
            └── ebirdapi/ (6 commits)
        └── staging/ (37 commits)
            └── docs/ (21 commits)
    └── seeds/ (1 commits)
    └── snapshots/ (1 commits)
    └── tests/ (1 commits)
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.