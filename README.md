This repository contains a Ctags-style tag builder for QML files.
To use in isolation, call the script as follows:

```
./qmltags.py /file/to/build/tags/for.qml
```

This will output the Ctags-style tags to stdout. 

For use with Vim's [Tagbar](http://majutsushi.github.io/tagbar/) 
plugin, add the following to your `.vimrc`:

```
let g:tagbar_type_qml = {
        \   'ctagstype':'qml'
        \ , 'kinds':['c:component', 'f:function', 'p:property', 's:signal']
        \ , 'ctagsbin':'/path/to/qmltags.py'
        \ , 'ctagsargs':''
        \ , 'sro':','
        \ , 'kind2scope':{'c':'component'}
        \ , 'scope2kind':{'component':'c'}
        \ }
```
