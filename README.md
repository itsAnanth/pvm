# PVM: Python Version Manager

A lightweight Python version manager for Windows. Install, manage, and switch between multiple Python versions with ease. Downloads official embeddable Python distributions, maintains isolated installations, and uses shims for seamless version switching without modifying system settings or registry.


# Installation

> [!IMPORTANT]
> If you already have a generic python installation, remove it from User path variables


```ps
powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/itsAnanth/pvm/refs/heads/main/powershell/install.ps1 | iex"
```

This command executes `powershell/install.ps1` script

It downloads pvm.exe at `%LOCALAPPDATA%/.pvm` and registers it in User Path environment variables

Restart all open terminal sessions and type `pvm` to get started


# Updation

```ps
powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/itsAnanth/pvm/refs/heads/main/powershell/update.ps1 | iex"
```