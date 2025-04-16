## install 
```bash
virtualenv ./env
. ./env/bin/activate
pip install playwright mdutils
```
## run 
```bash
virtualenv ./env
. ./env/bin/activate
python process_parcours.py
# generate PDF with pandoc:
pandoc Parcours.md --variable colorlinks=true -o parcours.pdf
```
# edit
it is possible to edit every image after generation, existant image will never overwrite by script


   
