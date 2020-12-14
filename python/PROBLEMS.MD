
 ### Big sur 下pyenv 安装版本失败问题：
 1. reinstall zlib bzip2
```shell
brew reinstall zlib bzip2
```

2. update .zshrc or .bashrc dependent on your shell
```shell
export PATH="$HOME/.pyenv/bin:$PATH"
export PATH="/usr/local/bin:$PATH"

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export LDFLAGS="-L/usr/local/opt/zlib/lib -L/usr/local/opt/bzip2/lib"
export CPPFLAGS="-I/usr/local/opt/zlib/include -I/usr/local/opt/bzip2/include"
```

3. install python 3.6.0, you can change the version
```shell
export PATH="/usr/local/opt/tcl-tk/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
export PKG_CONFIG_PATH="/usr/local/opt/tcl-tk/lib/pkgconfig"
export PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I/usr/local/opt/tcl-tk/include' --with-tcltk-libs='-L/usr/local/opt/tcl-tk/lib -ltcl8.6 -ltk8.6'"

CFLAGS="-I$(brew --prefix tcl-tk)/include -I$(brew --prefix openssl)/include -I$(brew --prefix bzip2)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include" LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib" pyenv install --patch 3.9.0 < <(curl -sSL https://github.com/python/cpython/commit/8ea6353.patch\?full_index\=1)
```

https://www.jianshu.com/p/042bfd496f74
https://github.com/pyenv/pyenv/issues/1737

 ### pyenv 找不到tk问题

 > 3.9没问题，2.7没问题，其他版本需要处理

 1. Uninstall your python version. For example: pyenv uninstall 3.7.2
 2. Install TK: brew install tcl-tk
 3. Follow the post install steps and config tk:
```shell
export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
export PATH=$PATH:/usr/local/opt/tcl-tk/bin
```
 4. Reload your terminal session and make sure all settings above are correctly set
 5. Install python: pyenv install 3.7.2

 https://stackoverflow.com/questions/22550068/python-not-configured-for-tk/31299142


 ### tk版本问题
 RuntimeError: tk.h version (8.6) doesn't match libtk.a version (8.5)
 
3.8+ work；3.5、3.6、3.7 not work
```shell
py_version=3.8.0
yes|pyenv uninstall $py_version
env \
  PATH="$(brew --prefix tcl-tk)/bin:$PATH" \
  LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
  CPPFLAGS="-I$(brew --prefix tcl-tk)/include" \
  PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
  CFLAGS="-I$(brew --prefix tcl-tk)/include" \
  PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
  pyenv install $py_version
```