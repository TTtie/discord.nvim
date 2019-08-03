# Warning
This is a fork with Windows-specific changes. The Unix backport has not been tested properly, yet.

# Discord.NVIM
Discord Rich Presence for Neovim.

# Install
Install the plugin using your favorite plugin manager:

[Vundle](https://github.com/VundleVim/Vundle.vim):
```
Plugin 'TTtie/discord.nvim'
```
[Plug](https://github.com/junegunn/vim-plug):
```
Plug 'TTtie/discord.nvim', { 'do': ':UpdateRemotePlugins'}
```
> **Warning!**
> There is a bug with Git Credential Manager/Plug on Windows that breaks GitHub credentials due to how Plug does its URLs.
> To prevent that, add this before initializing Plug into your init.vim:
> ```vim
> let g:plug_url_format='https://github.com/%s.git' " The default value is https://git::@github.com/%s.git, which breaks GitHub credentials
> ```

[dein](https://github.com/Shougo/dein.vim):
```
call dein#add('TTtie/discord.nvim')
```
To finish things off, call `:UpdateRemotePlugins` and restart Neovim.

# TODO (original)
- [ ] Multiple clients: wait for lock
- [X] Rewrite the client in pure python, no cffi
- [X] Upload some language icons
- [X] Make the client ID configurable
- [X] Documentation
- [ ] Tests
- [ ] Pack ratelimit data in pidfiles
- [ ] Yarp
- [X] Activation on demand
