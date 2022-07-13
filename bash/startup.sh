#! /bin/bash
#! Remove broken symlinks, generate 

find $HOME/.oh-my-zsh/custom/ -xtype l -delete
