" Install Vundle:
" git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
"
" Install the plugins from this file:
" 1. Open Vim.
" 2. Run :PluginInstall
" 3. Restart Vim after installation completes

set nocompatible

if isdirectory(expand('~/.vim/bundle/Vundle.vim'))
  set rtp+=~/.vim/bundle/Vundle.vim
  call vundle#begin()
  Plugin 'VundleVim/Vundle.vim'
  Plugin 'scrooloose/nerdcommenter'
  Plugin 'vim-airline/vim-airline'
  Plugin 'MattesGroeger/vim-bookmarks'
  Plugin 'brookhong/ag.vim'
  Plugin 'octol/vim-cpp-enhanced-highlight'
  Plugin 'mattn/emmet-vim'
  Plugin 'pangloss/vim-javascript'
  Plugin 'derekwyatt/vim-fswitch'
  Plugin 'scrooloose/nerdtree'
  call vundle#end()
endif

filetype plugin indent on
syntax on

let mapleader = ","

set autoread
set hidden
set history=500
set number
set ruler
set wildmenu
set ignorecase
set smartcase
set hlsearch
set incsearch
set showmatch
set backspace=indent,eol,start
set whichwrap+=<,>,h,l
set expandtab
set smarttab
set shiftwidth=2
set tabstop=2
set autoindent
set smartindent
set wrap
set linebreak
set textwidth=500
set nobackup
set nowritebackup
set noswapfile
set encoding=utf8
set fileformats=unix,dos,mac
set clipboard=unnamedplus
set foldmethod=syntax
set nofoldenable
set wildignore=*.o,*~,*.pyc,.git\*,.hg\*,.svn\*

try
  colorscheme solarized
catch
endtry
set background=dark

command! W w !sudo tee % > /dev/null

nnoremap <leader><cr> :nohlsearch<cr>
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-h> <C-w>h
nnoremap <C-l> <C-w>l
nnoremap <M-j> :m .+1<cr>==
nnoremap <M-k> :m .-2<cr>==
vnoremap <M-j> :m '>+1<cr>gv=gv
vnoremap <M-k> :m '<-2<cr>gv=gv
inoremap jk <Esc>
nnoremap <F2> :tabnew<cr>
nnoremap <F3> :tabprevious<cr>
nnoremap <F4> :tabnext<cr>
nnoremap <leader>dp :tabedit %<cr>
nnoremap <leader>g viw"ay:Ag -rn <C-r>a .<cr>
vnoremap <leader>g "ay:Ag -rn "<C-r>a" .<cr>
nnoremap <leader>tr :NERDTreeToggle<cr>
nnoremap <leader>tf :NERDTreeFind<cr>
nnoremap <leader>sw :FSHere<cr>
nnoremap <leader>sb :BookmarkSave bookmarks<cr>
nnoremap <leader>lb :BookmarkLoad bookmarks<cr>

let NERDTreeWinSize=32
let NERDTreeWinPos="left"
let NERDTreeShowHidden=1
let NERDTreeMinimalUI=1
let NERDTreeAutoDeleteBuffer=1

autocmd BufWrite *.py,*.coffee %s/\s\+$//e
augroup remember_cursor_position
  autocmd!
  autocmd BufReadPost *
        \ if line("'\"") > 0 && line("'\"") <= line("$") |
        \   execute "normal! g`\"" |
        \ endif
augroup END
