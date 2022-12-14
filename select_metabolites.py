import pandas as pd

def get_selected_metabolities(data_path):
    metabolities_data=pd.read_csv(data_path,low_memory=False)
    selected_list=metabolities_data["Library ID"].drop_duplicates().tolist()
    selected_list=list(set(selected_list))
    selected_list_new=[]
    for i in selected_list:
        if ";" not in i:
            selected_list_new.append(i)
        else:
            selected_list_new.extend(i.split(";"))
    selected_list=[i for i in selected_list_new if i[:4]=="HMDB" ]
    return selected_list
    
    
if __name__=="__main__":
    pos_ion_data=get_selected_metabolities("/Users/colton/Downloads/HMKG/RA代谢组学平台raw数据（含临床信息）/阳离子结果表.csv")
    neg_ion_data=get_selected_metabolities("/Users/colton/Downloads/HMKG/RA代谢组学平台raw数据（含临床信息）/阴离子结果表.csv")

    pd.DataFrame(list(set(pos_ion_data+neg_ion_data))).to_csv("./data/selected_metabolities.csv")