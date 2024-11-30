# Assuming it will running from AllegroGraph home, and file does not exist.
# It will overwrite existing repo.

bin/agtool load \
    --supersede \
    --input nquads \
    http://super:2002@localhost:10035/repositories/cfr2sbvr \
    cfr2sbvr.gzip