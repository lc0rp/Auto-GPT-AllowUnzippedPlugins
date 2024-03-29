# Auto-GPT Allow Unzipped Plugins (Beta) - a dev utility.

## Archived (Aug 31 2023)

Recent versions of Auto-GPT now support unzipped plugins, making this utility unnecessary.

## Overview

This utility enables faster, on-the-fly plugin testing by allowing unzipped plugins to work. 

Auto-GPT requires zipped plugins for great security reasons. For developers, zipping up plugins during the dev/test cycle slows things down. 

This tool acts as a proxy between Auto-GPT's plugin API and your unzipped plugins.

⚠️💀 **WARNING** 💀⚠️:
1. Do not use this tool with plugins you are not developing.
2. Only use this tool if your development workflow requires it.
3. Review the code of any plugin you use thoroughly, as plugins can execute any Python code, potentially leading to malicious activities, such as stealing your API keys.

## Installation

Download this repository as a .zip file, copy it to ./plugins/, and rename it to Auto-GPT-AllowUnzippedPlugins.zip.

To download it directly from your Auto-GPT directory, you can run this command on Linux or MacOS:

```
curl -o ./plugins/Auto-GPT-AllowUnzippedPlugins.zip https://github.com/KayLuke/Auto-GPT-AllowUnzippedPlugins/archive/refs/heads/master.zip
```

In PowerShell:

```
Invoke-WebRequest -Uri "https://github.com/KayLuke/Auto-GPT-AllowUnzippedPlugins/archive/refs/heads/master.zip" -OutFile "./plugins/Auto-GPT-AllowUnzippedPlugins.zip"
```

## Allowlist Plugin
For interactionless use, in your `.env` search for `ALLOWLISTED_PLUGINS` and add this Plugin:

```ini
################################################################################
### ALLOWLISTED PLUGINS
################################################################################

#ALLOWLISTED_PLUGINS - Sets the listed plugins that are allowed (Example: plugin1,plugin2,plugin3)
ALLOWLISTED_PLUGINS=AutoGPTAllowUnzippedPlugins
```

## Usage

1. Once installed, this plugin should allow Auto-GPT to call any plugin in the "Auto-GPT/plugins/" directory even if they're not zipped up.
2. Place your plugins in the "Auto-GPT/plugins/" folder, as you normally would, except that you do not have to zip them up.

## Limitations

1. The plugins will not show up in Auto-GPT's plugin list, but plugin methods will be called.
2. Currently, the plugin does not support the following methods.
- chat_completion
- on_planning


## Feedback & Updates

Check back for updates often, and I look forward to your feedback!
