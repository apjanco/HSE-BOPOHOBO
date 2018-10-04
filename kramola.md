## Quick experiments with :sparkles:Prodigy and [КРАМОЛА. Инакомыслие в СССР при Хрущеве и Брежневе.](http://www.e-reading.club/bookreader.php/1034359/KRAMOLA._Inakomyslie_v_SSSR_pri_Hruscheve_i_Brezhneve..html)(a text that I know well because I translated it).
## Experiment #1
* example workflow for categorization task
1. Create a dataset to store your annotations. <br>
  `prodigy dataset kramola "Data for Kramola"`
1. Download the spaCy [multi-language model](https://spacy.io/models/xx) which includes Russian. <br>
  `python -m spacy download xx_ent_wiki_sm`
1. Start the annotation tool to teach the model a new category.<br>
  `prodigy textcat.teach kramola xx_ent_wiki_sm --label КРАМОЛА`
1. Train the model on the new category using the annotations you've created and saved in the dataset.<br>
  `prodigy textcat.batch-train kramola xx_ent_wiki_sm -n 200 --output /Users/ajanco/projects/kramola/model/train-curve`
1. It is often difficult to assess if a model would perform better if it was trained on more data or annotations.  Prodigy includes a task that will evaluate the relative improvement given set amounts of data.  If the change in accuracy drops, then this is a good sign that your problem isn't with insufficent data or annotations. <br>
  `prodigy textcat.train-curve kramola /Users/ajanco/projects/kramola/model/ --n-iter 10 --eval-split 0.2 --dropout 0.2  --n-samples 4`<br>
Output:<br>
```
Starting with model /Users/ajanco/projects/kramola/model/ 
Dropout: 0.2  Batch size: 10  Iterations: 10  Samples: 4 

%          ACCURACY 
25%        0.96       +0.96 
50%        0.98       +0.02 
75%        0.98       +0.01 
100%       0.98       -0.01 
```

Test the model 
```python
import spacy
from spacy import displacy
nlp = spacy.load('/Users/ajanco/projects/nkvd/model')
with open('/Users/ajanco/projects/kramola/КРАМОЛА.txt', 'r') as f:
    text = f.read()
doc = nlp(u'{}'.format(text))
print(doc.cats)
html = displacy.render(doc, style='dep', page=True)
```

Not useful for identifying complex "sedition speech", very good at identifying part of text
citation vs body of text 

![alt text](https://github.com/apjanco/HSE-BOPOHOBO/blob/master/kramola2.jpeg "A simple neural network")

## Experiment #2

Created ru_memorial_PATTERNS.JSONL from records in Memorial repo 
prodigy dataset memorial "Data for Memorial"

https://github.com/MemorialInternational/nkvd
prodigy ner.manual memorial xx_ent_wiki_sm КРАМОЛА.txt --label имя,отчество,фамилия

prodigy ner.teach gam xx_ent_wiki_sm КРАМОЛА.txt --patterns ru_memorial_PATTERNS.JSONL --label имя,отчество,фамилия
prodigy ner.batch-train memorial xx_ent_wiki_sm -n 100 --output /Users/ajanco/projects/nkvd/model/ --label имя,отчество,фамилия

https://prodi.gy/features/
file:///Users/ajanco/Downloads/displaCy_7_25.html


"You gave me a wonderful master who, made by me, teaches me, and teaching me, knows nothing himself." https://twitter.com/scott_bot/status/1046821426425159680

https://prodi.gy/demo?view_id=ner
