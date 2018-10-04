## Quick experiments with :sparkles:Prodigy and [КРАМОЛА. Инакомыслие в СССР при Хрущеве и Брежневе.](http://www.e-reading.club/bookreader.php/1034359/KRAMOLA._Inakomyslie_v_SSSR_pri_Hruscheve_i_Brezhneve..html)(a text that I know well because I translated it).
## Experiment #1
* Steps to teach the model a new category -- Kramola.  Can the model learn to identify sedition text? 
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

Test the model: 
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

Outcome:
- High accuracy 96%.  Unable to identify "sedition speech", but extremely good at identifying manuscript format.  I can differentiate between the introductory sections and focuses only on the primary sources.  A very effective tool to separate the primary text from the book.

## Experiment #2
Train the model on new entities.  Can the model learn to identify имя, отчество, and/or фамилия?

1. Create a list of names to prime the model for pattern matching.  The model will recognize those patterns as name parts and use context to further learn the new entities.   

The names should be save in the following format:
```json
{"label": "имя", "pattern": "Иосиф"} 
{"label": "имя", "pattern": "Илья"} 
```

The file is available here [ru_memorial_PATTERNS.JSONL](https://github.com/apjanco/HSE-BOPOHOBO/blob/master/ru_memorial_PATTERNS.JSONL) and was created from records here [Memorial repo](https://github.com/MemorialInternational/nkvd).
1. Create a new dataset to store your annotations. 
`prodigy dataset memorial "Data for Memorial"`
1. It's often useful to further prime the model by manually annotating the correct answers.  This will give it a better idea of what you'd like it to learn. 
`prodigy ner.manual memorial xx_ent_wiki_sm КРАМОЛА.txt --label имя,отчество,фамилия`

1. Now you can start the annotation tool for active learning. 
`prodigy ner.teach gam xx_ent_wiki_sm КРАМОЛА.txt --patterns ru_memorial_PATTERNS.JSONL --label имя,отчество,фамилия`

![alt text](https://github.com/apjanco/HSE-BOPOHOBO/blob/master/kramola2.jpeg "A simple neural network")

1.  Train the model on your patterns and annotations. 
`prodigy ner.batch-train memorial xx_ent_wiki_sm -n 100 --output /Users/ajanco/projects/nkvd/model/ --label имя,отчество,фамилия`

1. Test the model on a text to assess the results. 


Outcome: 
