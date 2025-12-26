# PVM: Python Version Manager

A lightweight Python version manager for Windows. Install, manage, and switch between multiple Python versions with ease. Downloads official embeddable Python distributions, maintains isolated installations, and uses shims for seamless version switching without modifying system settings or registry.


# Installation

```ps
powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/itsAnanth/pvm/refs/heads/main/install.ps1 | iex"
```

This command executes the Install.ps1 script found at the root of the repository

It downloads pvm.exe at `%LOCALAPPDATA%/.pvm and registers it in User Path environment variables

Restart all open terminal sessions and type `pvm` to get started