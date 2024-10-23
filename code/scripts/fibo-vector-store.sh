le# Create vector store
# Run after ../src/create_kg.py
echo Connecting to http://$AG_USER:$AG_PASSWORD@$AG_HOST:$AG_PORT/repositories/$AG_REPOSITORY

echo running $ALLEGRO_HOME/bin/agtool llm index

# FIBO
if $ALLEGRO_HOME/bin/agtool llm index \
       http://$AG_USER:$AG_PASSWORD@$AG_HOST:$AG_PORT/repositories/$AG_REPOSITORY \
       $CFR2SBVR_HOME/scripts/fibo-vec.def ; then
    echo Finished successfully
else
    echo Failed to create vector store. Check logs above for errors. Exclude the vector store in the AllegroGraph UI before run again.
fi

# CFR
if $ALLEGRO_HOME/bin/agtool llm index \
       http://$AG_USER:$AG_PASSWORD@$AG_HOST:$AG_PORT/repositories/$AG_REPOSITORY \
       $CFR2SBVR_HOME/scripts/cfr-vec.def ; then
    echo Finished successfully
else
    echo Failed to create vector store. Check logs above for errors. Exclude the vector store in the AllegroGraph UI before run again.
fi