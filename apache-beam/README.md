# Test a pipeline with apache beam

Run the default pipeline

```bash
pip install -r requirements.txt
python -m apache_beam.examples.wordcount \
  --output outputs --input data/*txt
```


Run the modified pipeline

```bash
python wordcount.py --output outputs --input data/*txt
```
