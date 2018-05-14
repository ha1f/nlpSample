# Getting started

## Install command-line tools

### Install mecab

```sh
brew install mecab
brew install mecab-ipadic
```

### Install NEologd

https://github.com/neologd/mecab-ipadic-neologd

Make sure unxz installed.

```sh
brew install xz
```

```sh
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
./bin/install-mecab-ipadic-neologd -n
```

### Install CabocCha

Install CRF++ if needed

```sh
brew install crf++
```

```sh
brew install cabocha
```

### Install Juman, KNP

### Install Juman

http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN
からダウンロードして、解凍して、

```sh
cd ~/Downloads/juman-7.01
./configure
make
sudo make install
```

#### Install KNP

※結構時間かかるので注意

http://nlp.ist.i.kyoto-u.ac.jp/index.php?KNP
からダウンロードして、解凍して、

```sh
cd ~/Downloads/knp-4.19
./configure
make
sudo make install
```

## Setup python libraries

※Python3は最新バージョンにしておく

#### MeCab

```sh
pip install mecab-python3
```

#### word2vec

```sh
pip install gensim
```

#### juman, knp

```sh
pip install six
```

http://nlp.ist.i.kyoto-u.ac.jp/index.php?PyKNP
からダウンロードして、解凍して、

```sh
cd ~/Downloads/pyknp-0.3
python setup.py install
```

おまけで

```sh
pip install mojimoji
```

#### CaboCha

CaboChaラッパーは以下からダウンロードして
http://taku910.github.io/cabocha/

```sh
cd ~/Downloads/cabocha-0.69/python
python setup.py build && python setup.py install
```

