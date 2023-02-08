# HMKG: Human Metabolome Knowledge Graph
<p align="left"> <img src="https://komarev.com/ghpvc/?username=yuxinglu613&label=Profile%20views&color=0e75b6&style=flat" alt="yuxinglu613" /> </p>

## Introduction

The [Human Metabolome Database (HMDB)](https://hmdb.ca) is the largest metabolome database in the world. We provide a toolkit that can transform HMDB into a knowledge graph, named HMKG, which will help researchers get to know the relations among metabolities and provide a more intuitive and comprehensive understanding of metabolic processes. Additionally, we encourage researchers to apply deep learning and representation learning techniques on HMKG, which could help advance research in this field using AI.Also, we would like to use HMKG to introduce deep learning and representation learning techniques into metabolomics, thus boosting the AI development in metabolomics field.

## Goal and Philosophy

* Fill the blank of KG in Metabolomics.
* Explore the relationship between metabolites.
* Promote the development of metabolomics research.

## Content

```bash
.
├── README.md
├── build_graph.py
├── cal_simlarity.ipynb
├── convert_xml.py
├── data
│   ├── hmdb_metabolities.json (download by your own)
│   ├── hmdb_metabolities.json
│   └── selected_metabolities.csv
├── main.py
├── output
│   └── HMDB_embedding.json
├── requirements.txt
├── select_metabolites.py
└── utils.py
```

## Requirements

py2neo==4.3.0

pandas==1.4.4

xmltodict==0.12.0

## Usage

To generate HMKG, you need to first download the HMDB ***All Metabolitesdata*** file from [https://hmdb.ca/downloads](https://hmdb.ca/downloads) and store it into the ./data file.

Then you can run the code below.

```bash
python main.py -XML_DATA_PATH ./data/hmdb_metabolities.xml \ 
	       -JSON_DATA_PATH ./data/hmdb_metabolities.json \
	       -CREATE_GRAPH True
```

If you want to generate a subgraph using specific metebolities, you can add the required metabolities in the `./data/select_metabolities.csv` and add argument

```bash
python main.py -XML_DATA_PATH ./data/hmdb_metabolities.xml \ 
	       -JSON_DATA_PATH ./data/hmdb_metabolities.json \
	       -CREATE_GRAPH True \
	       -SELECT_METABOLITIES ./data/select_metabolities.csv
```

If you want generate triples for further researches or downstream tasks, you can add argument

```
python main.py -XML_DATA_PATH ./data/hmdb_metabolities.xml \ 
	       -JSON_DATA_PATH ./data/hmdb_metabolities.json \
	       -CREATE_GRAPH True \
	       -CREATE_TRIPLE True
```

---

More functions are being developed~

## KG Embedding

We recommend you to use the generated triples to conduct KG embedding and get the representation vector of the metabolities.

Some recommended repositories are listed below:

* GraphVite [https://github.com/DeepGraphLearning/graphvite](https://github.com/DeepGraphLearning/graphvite)
* RotateE [https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding]())
* KB2E [https://github.com/thunlp/KB2E](https://github.com/thunlp/KB2E)
* AnpliGraph [https://github.com/Accenture/AmpliGraph](https://github.com/Accenture/AmpliGraph)
* OpenKE [https://github.com/thunlp/OpenKE](https://github.com/thunlp/OpenKE)
* PyKEEN [https://github.com/SmartDataAnalytics/PyKEEN](https://github.com/SmartDataAnalytics/PyKEEN)
* Pykg2vec [https://github.com/Sujit-O/pykg2vec](https://github.com/Sujit-O/pykg2vec)
* Dist-KGE [https://github.com/uma-pi1/dist-kge](https://github.com/uma-pi1/dist-kge)
* ...

---

Here we apply the KG Embedding methods in [https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding]()) Repository, and get the TransE embedding of the sub knowledge graph containing 474 metabolities.

The Statistics of the subgraph are as follows:

| Metabolities | Nodes | Relations | Triples |
| ------------ | ----- | --------- | ------- |
| 474          | 93231 | 17        | 191,479 |

The TransE metrics are as follows:

| MRR    | MR     | HITS@1 | HITS@3 | HITS@10 |
| ------ | ------ | ------ | ------ | ------- |
| 0.2715 | 8598.2 | 0.1841 | 0.3104 | 0.4628  |

To calculate the similarity between metabolities' embeddings, you can use the ***cal_similarity.ipynb*** and enter two HMDB number to get the similarity.

## KG Embedding Results

TBA

## **Statistics**

TBA

## Citation

TBA
