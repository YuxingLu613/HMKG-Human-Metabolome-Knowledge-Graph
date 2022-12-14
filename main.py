from utils import read_json_file
from convert_xml import *
from build_graph import build_graph, count_nodes, count_relations, create_node, create_relations
# from transE import TransE,dataloader

if __name__=="__main__":
    from py2neo import Graph
    import argparse
    import pandas as pd
    import os
    import random
    
    parser = argparse.ArgumentParser(description='Needed args in building HMKG')
    parser.add_argument("-XML_DATA_PATH",type=str,default="",help="xml data from HMDB")
    parser.add_argument("-JSON_DATA_PATH",type=str,default="./data/part_of_hmdb.json",help="json data from HMDB")
    parser.add_argument("-SELECT_METABOLITIES",type=str,default="./data/selected_metabolities.csv",help="selected metabolities to create subgraph")
    parser.add_argument("-CREATE_GRAPH",type=bool,default=True,help="choose to create Neo4j KG")
    parser.add_argument("-CREATE_TRIPLE",type=bool,default=True,help="choose to create KG triples")
    parser.add_argument("-EMBED_KG",type=bool,default=True,help="conduct KG embedding")
    parser.add_argument("-DATA_DIR",type=str,default="./data",help="the output dirctory of KG data")
    
    args=parser.parse_args()
    
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    graph.delete_all()
    
    if args.XML_DATA_PATH:
        pass
    
    json_data=read_json_file(args.JSON_DATA_PATH)
    
    if args.SELECT_METABOLITIES:
        selected_metabolities=pd.read_csv(args.SELECT_METABOLITIES)["0"].tolist()[:]
        Nodes,Relations=build_graph(json_data,selected_metabolities)
    else:
        Nodes,Relations=build_graph(json_data)
    
    nodes_num=count_nodes(Nodes)
    relations_num=count_relations(Relations)
    
    if args.CREATE_GRAPH:
        graph=create_node(graph,Nodes)
        graph=create_relations(graph,Relations)
        
    if args.CREATE_TRIPLE:
        result = graph.run("MATCH (e1)-[r]->(e2) RETURN e1, type(r), e2")
        with open(os.path.join(args.DATA_DIR,"triples.txt"),"w+") as f:
            for record in result:
                f.write("\t".join([str(record["e1"]),str(record["type(r)"]),str(record["e2"])]))
                f.write("\n")
        
        nodes=graph.run("MATCH (e1) RETURN e1")
        nodes=nodes.to_data_frame().drop_duplicates().reset_index(drop=True)
        relations=graph.run("MATCH ()-[r]-() RETURN type(r)")
        relations=relations.to_data_frame().drop_duplicates().reset_index(drop=True)

        with open(os.path.join(args.DATA_DIR,"entities.dict"),"w+") as f:
            for index,record in nodes.iterrows():
                f.write(str(index)+'\t'+str(record["e1"]))
                f.write("\n")
        
        with open(os.path.join(args.DATA_DIR,"relations.dict"),"w+") as f:
            for index,record in relations.iterrows():
                f.write(str(index)+'\t'+str(record["type(r)"]))
                f.write("\n")
        
    if args.EMBED_KG:
        with open(os.path.join(args.DATA_DIR,"triples.txt"),"r") as f:
            triples=f.readlines()
        train_data=random.sample(triples,int(0.7*len(triples)))
        triples=[i for i in triples if i not in train_data]
        
        with open(os.path.join(args.DATA_DIR,"train.txt"),"w+") as f:
            for i in train_data:
                f.write(i)

        valid_data=random.sample(triples,int(0.67*len(triples)))
        triples=[i for i in triples if i not in valid_data]
        with open(os.path.join(args.DATA_DIR,"valid.txt"),"w+") as f:
            for i in valid_data:
                f.write(i)
        
        with open(os.path.join(args.DATA_DIR,"test.txt"),"w+") as f:
            for i in triples:
                f.write(i)
        
        # entity_set, relation_set, triple_list, valid_triple_list = dataloader("triples.txt")
        # transE = TransE(entity_set, relation_set, triple_list, embedding_dim=50, lr=0.0001, margin=4.0, norm=1, C = 0.25, valid_triple_list=valid_triple_list)
        # transE.data_initialise()
        # transE.training_run(epochs=500, batch_size=512, out_file_title="HMKG_torch_")
    
    