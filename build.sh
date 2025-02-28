cp bases/grim/textualweb/app.py projects/grimweb/files/app/app.py
cp bases/grim/textualweb/app.tcss projects/grimweb/files/app/app.tcss
cd projects/grimweb
poetry build-project
cd ../..