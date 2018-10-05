## Quick experiments with :sparkles:Prodigy and [КРАМОЛА. Инакомыслие в СССР при Хрущеве и Брежневе](http://www.e-reading.club/bookreader.php/1034359/KRAMOLA._Inakomyslie_v_SSSR_pri_Hruscheve_i_Brezhneve..html)(a text that I know well because I translated it).
## Experiment #1
* Steps to teach the model a new category -- Kramola.  Can the model learn to identify sedition? 
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
- High accuracy 96%.  Unable to identify "sedition speech", but extremely good at identifying the manuscript format.  I can differentiate between the introductory sections and focuses only on the primary sources.  A very effective tool to separate the primary text from the book.

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

1. Establish if the model has sufficent data and starting patterns.<br>
`prodigy ner.train-curve memorial /Users/ajanco/projects/nkvd/model --n-iter 10 --eval-split 0.2 --dropout 0.2 --n-samples 4`

```
Starting with model /Users/ajanco/projects/nkvd/model
Dropout: 0.2  Batch size: 32  Iterations: 10  Samples: 4

%          RIGHT      WRONG      ACCURACY
25%        13         10         0.57       +0.57
50%        15         9          0.62       +0.06
75%        10         13         0.43       -0.19
100%       12         12         0.50       +0.07
```
VERY Poor results and not a data problem, but a learning problem. Names are very sparse data and difficult to identify from context.  The model knows Stalin (high frequency in the text) and names that begin at the beginning of paragraphs (Family, I.O.).  However, the tokenizer is combining I.O. as one imiia. 

1. View the results in context.
```python
import spacy
from spacy import displacy
nlp = spacy.load('/Users/ajanco/projects/nkvd/model')
with open('/Users/ajanco/projects/kramola/КРАМОЛА.txt', 'r') as f:
    text = f.read()
doc = nlp(u'{}'.format(text))
colors = {'ФАМИЛИЯ': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)', 'ИМЯ': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)', 'ОЧЕСТВО':'linear-gradient(90deg, #aa9cfc, #fc9ce7)' }
options = {'ents': ['ФАМИЛИЯ', 'ОЧЕСТВО', 'ИМЯ' ], 'colors': colors}
html = displacy.render(doc, style='ent', options=options, page=True)
with open('names.html', 'w') as f:
    f.write(html)
```
Outcome: 
![alt text](https://github.com/apjanco/HSE-BOPOHOBO/blob/master/names.jpeg "A simple neural network")

This one is an open question.  The model seems able to learn names that is has seen several times in the text, but not names that appear only once. Similarly, when names appear in a consistent place and format in the document (the sections Из хроники событий) several times, there are clear improvements.  I could try further annotations (I only made 300) or the spaCy's PhraseMatcher function, which would simply tag all the names in the patterns from Memorial.  

It's not ready for use, but it's not bad for the product of 3 hours on a plane from London.  
