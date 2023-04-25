# Auto-GPT Allow Unzipped Plugins (Beta) - a dev plugin for Auto-GPT

## Overview

This tool enables faster, on-the-fly plugin testing by allowing unzipped plugins to work. 

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

Once installed, this plugin should allow Auto-GPT to call plugins in the ./plugin directory that are not zipped up.

Note: The plugins will not show up in Auto-GPT's plugin list, but plugin methods will be called.

## Limitations

Currently, the plugin does not support the following methods.
- chat_completion
- on_planning


## Feedback & Updates

Check back for updates often, and I look forward to your feedback!
