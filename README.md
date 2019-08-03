# Warning
This is a fork with Windows-specific changes. The Unix backport has not been tested properly, yet.

# Discord.NVIM
Discord Rich Presence for Neovim.

# Install
Install the plugin using your favorite plugin manager:

[Vundle](https://github.com/VundleVim/Vundle.vim):
```vim
Plugin 'TTtie/discord.nvim'
```
[Plug](https://github.com/junegunn/vim-plug):
```vim
Plug 'TTtie/discord.nvim', { 'do': ':UpdateRemotePlugins'}
```
> **Warning!**  
> There is an issue with Git Credential Manager/Plug on Windows that breaks GitHub credentials due to Plug's default settings.  
> To prevent that, use the full repository URL instead:
> ```vim
> Plug 'https://github.com/TTtie/discord.nvim.git', { 'do': ':UpdateRemotePlugins'}
> ```

[dein](https://github.com/Shougo/dein.vim):
```vim
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
