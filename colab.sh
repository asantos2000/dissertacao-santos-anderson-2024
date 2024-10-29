  rm -rf cfr2sbvr configuration checkpoint
  git clone https://github.com/asantos2000/master-degree-santos-anderson.git cfr2sbvr
  pip install -r cfr2sbvr/code/requirements.txt
  cp -r cfr2sbvr/code/src/configuration .
  cp -r cfr2sbvr/code/src/checkpoint .
  cp -r cfr2sbvr/code/config.colab.yaml config.yaml