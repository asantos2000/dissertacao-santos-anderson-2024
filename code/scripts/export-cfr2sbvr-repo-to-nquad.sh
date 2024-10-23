# Assuming it will running from AllegroGraph home, and file does not exist.
#To overwrite existing file use --if-exists overwrite \
bin/agtool export \
    --output-format nquads \
    --compress \
    http://super:2002@localhost:10035/repositories/cfr2sbvr \
    cfr2sbvr.gzip