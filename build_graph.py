from py2neo import Node, Relationship
from tqdm import tqdm
from utils import drop_duplicate, clean_quote


def build_graph(json_data, selected_metabolities=None):
    HMDB_list = []
    Name_Synonyms = []
    Taxonomy_list = []
    Alternative_parent = []
    Substituent_list = []
    External_descriptor = []
    Ontology_list = []
    External_property_list = []
    Predicted_property_list = []
    Spectrum_list = []
    Tissue_list = []
    Pathway_list = []
    Reference_list = []
    Disease_list = []
    Protein_list = []
    HMDB_dict_list = []
    Cellular_locations = []
    Biospecimen_locations = []
    Concentration = []
    Protein_list = []

    Rel_secondary_accession = []
    Rel_synonyms = []
    Rel_alternative_parent = []
    Rel_substituent = []
    Rel_external_descriptor = []
    Rel_taxonomy = []
    Rel_external_property = []
    Rel_predicted_property = []
    Rel_spectrum = []
    Rel_cellular_location = []
    Rel_biospecimen_location = []
    Rel_tissue = []
    Rel_pathway = []
    Rel_concentration = []
    Rel_reference_concentration = []
    Rel_reference_disease = []
    Rel_disease = []
    Rel_general_reference = []
    Rel_protein = []

    for h_key, h_value in tqdm(list(json_data.items())):

        if h_key not in selected_metabolities:
            continue
        id = 0
        HMDB_NO = h_key
        HMDB_dict = {}
        for key, value in h_value.items():

            if not value:
                continue

            if key == "secondary_accessions":

                if isinstance(value["accession"], str):
                    HMDB_list.append(clean_quote(value["accession"]))
                    Rel_secondary_accession.append(
                        [HMDB_NO, "secondary_accession", clean_quote(value["accession"])])
                else:
                    for v in value["accession"]:
                        HMDB_list.append(clean_quote(v))
                        Rel_secondary_accession.append(
                            [HMDB_NO, "secondary_accession", clean_quote(v)])

            elif key == 'synonyms':
                if isinstance(value["synonym"], str):
                    Name_Synonyms.append(clean_quote(value["synonym"]))
                    Rel_synonyms.append(
                        [HMDB_NO, "synonym", clean_quote(value["synonym"])])
                else:
                    for v in value["synonym"]:
                        Name_Synonyms.append(clean_quote(v))
                        Rel_synonyms.append(
                            [HMDB_NO, "synonym", clean_quote(v)])

            elif key == "taxonomy":
                if "alternative_parents" in value.keys():
                    alternative_parent = value.pop("alternative_parents")
                    if alternative_parent:
                        for v in list(alternative_parent.values())[0]:
                            Alternative_parent.append(clean_quote(v))
                            Rel_alternative_parent.append(
                                [HMDB_NO, "alternative_patient", clean_quote(v)])

                if "substituents" in value.keys():
                    substituent = value.pop("substituents")
                    if substituent:
                        for v in list(substituent.values())[0]:
                            Substituent_list.append(clean_quote(v))
                            Rel_substituent.append(
                                [HMDB_NO, "substituent", clean_quote(v)])
                if "external_descriptors" in value.keys():
                    external_descriptor = value.pop("external_descriptors")
                    if external_descriptor:
                        for v in list(external_descriptor.values())[0]:
                            External_descriptor.append(clean_quote(v))
                            Rel_external_descriptor.append(
                                [HMDB_NO, "external_descriptor", clean_quote(v)])
                value["HMDB_NO"] = HMDB_NO
                Taxonomy_list.append(value)
                Rel_taxonomy.append([HMDB_NO, "taxonomy", value])

            elif key == "experimental_properties":
                if isinstance(value["property"], dict):
                    External_property_list.append(value["property"])
                    Rel_external_property.append(
                        [HMDB_NO, "experimental_properties", value["property"]])
                else:
                    for v in value["property"]:
                        External_property_list.append(v)
                        Rel_external_property.append(
                            [HMDB_NO, "experimental_properties", v])

            elif key == "predicted_properties":
                if isinstance(value["property"], dict):
                    Predicted_property_list.append(value["property"])
                    Rel_predicted_property.append(
                        [HMDB_NO, "predicted_properties", value["property"]])
                else:
                    for v in value["property"]:
                        v["value"] = v["value"].replace("(", "")
                        v["value"] = v["value"].replace(")", "")
                        Predicted_property_list.append(v)
                        Rel_predicted_property.append(
                            [HMDB_NO, "predicted_properties", v])

            elif key == "spectra":
                if value:
                    if isinstance(value["spectrum"], dict):
                        Spectrum_list.append(value["spectrum"])
                        Rel_spectrum.append(
                            [HMDB_NO, "spectrum", value["spectrum"]])
                    else:
                        for v in value["spectrum"]:
                            Spectrum_list.append(v)
                            Rel_spectrum.append([HMDB_NO, "spectrum", v])

            elif key == "biological_properties":
                cellular_locations = value.pop("cellular_locations")
                if cellular_locations:
                    for v in list(cellular_locations.values()):
                        if isinstance(v, str):
                            Cellular_locations.append(clean_quote(v))
                            Rel_cellular_location.append(
                                [HMDB_NO, "cellular_locations", clean_quote(v)])
                        else:
                            for _ in v:
                                Cellular_locations.append(clean_quote(_))
                                Rel_cellular_location.append(
                                    [HMDB_NO, "cellular_locations", clean_quote(_)])
                biospecimen_locations = value.pop("biospecimen_locations")
                if biospecimen_locations:
                    for v in list(biospecimen_locations['biospecimen']):
                        Biospecimen_locations.append(clean_quote(v))
                        Rel_biospecimen_location.append(
                            [HMDB_NO, "biospecimen", clean_quote(v)])
                tissue_locations = value.pop("tissue_locations")
                if tissue_locations:
                    for v in list(tissue_locations):
                        Tissue_list.append(v)
                        Rel_tissue.append([HMDB_NO, "tissue", clean_quote(v)])
                pathways = value.pop("pathways")
                if pathways:
                    for v in list(pathways["pathway"]):
                        if not isinstance(v, dict):
                            continue
                        Pathway_list.append(v)
                        Rel_pathway.append([HMDB_NO, "pathway", v])

            elif key == "normal_concentrations":
                for v in value['concentration']:
                    if isinstance(v, str):
                        continue
                    else:
                        if "references" in v.keys():
                            reference = v.pop("references")
                            if reference and isinstance(reference["reference"], list):
                                for i in reference["reference"]:
                                    i["reference_text"] = clean_quote(
                                        i["reference_text"])
                                    Reference_list.append(i)
                                    Rel_reference_concentration.append(
                                        [v, "reference", i])
                            elif reference and isinstance(reference["reference"], dict):
                                reference["reference"]["reference_text"] = clean_quote(
                                    reference["reference"]["reference_text"])
                                Reference_list.append(reference["reference"])
                                Rel_reference_concentration.append(
                                    [v, "reference", reference["reference"]])
                    v["id"] = str(id)
                    v["status"] = "Normal"
                    id += 1
                    Concentration.append(v)
                    Rel_concentration.append([HMDB_NO, "Concentration", v])

            elif key == "abnormal_concentrations":
                for v in value['concentration']:
                    if isinstance(v, str):
                        continue
                    else:
                        if "references" in v.keys():
                            reference = v.pop("references")
                            if reference and isinstance(reference["reference"], list):
                                for i in reference["reference"]:
                                    i["reference_text"] = clean_quote(
                                        i["reference_text"])
                                    Reference_list.append(i)
                                    Rel_reference_concentration.append(
                                        [v, "reference", i])
                            elif reference and isinstance(reference["reference"], dict):
                                reference["reference"]["reference_text"] = clean_quote(
                                    reference["reference"]["reference_text"])
                                Reference_list.append(reference["reference"])
                                Rel_reference_concentration.append(
                                    [v, "reference", reference["reference"]])
                            v["id"] = str(id)
                            v["status"] = "Abnormal"
                            id += 1
                            Concentration.append(v)
                            Rel_concentration.append(
                                [HMDB_NO, "Concentration", v])

            elif key == "diseases":
                for v in value["disease"]:
                    if isinstance(v, str):
                        continue
                    else:
                        if "references" in v.keys():
                            reference = v.pop("references")
                            if isinstance(reference["reference"], list):
                                for i in reference["reference"]:
                                    i["reference_text"] = clean_quote(
                                        i["reference_text"])
                                    Reference_list.append(i)
                                    Rel_reference_disease.append(
                                        [v, "reference", i])
                            elif isinstance(reference["reference"], dict):
                                reference["reference"]["reference_text"] = clean_quote(
                                    reference["reference"]["reference_text"])
                                Reference_list.append(reference["reference"])
                                Rel_reference_disease.append(
                                    [v, "reference", reference["reference"]])
                            v["name"] = clean_quote(v["name"])
                            Disease_list.append(v)
                            Rel_disease.append([HMDB_NO, "Disease", v])

            elif key == "general_references":
                for v in value["reference"]:
                    if isinstance(v, str):
                        continue
                    else:
                        if "reference" in v.keys():
                            v["reference"]=clean_quote(v["reference"])
                            Reference_list.append(v)
                            Rel_general_reference.append([HMDB_NO, "reference", v])

            elif key == "protein_associations":
                for v in value["protein"]:
                    if isinstance(v, str):
                        continue
                    else:
                        Protein_list.append(v)
                        Rel_protein.append([HMDB_NO, "protein", v])

            elif key == "ontology":
                pass

            else:
                HMDB_dict[key] = value

        HMDB_dict_list.append(HMDB_dict)

    Nodes = {"HMDB": HMDB_list,
             "Synonyms": Name_Synonyms,
             "Taxonomy": Taxonomy_list,
             "Alternative_parent": Alternative_parent,
             "Substituent": Substituent_list,
             "External_descriptor": External_descriptor,
             "Ontology": Ontology_list,
             "External_property": External_property_list,
             "Predicted_property": Predicted_property_list,
             "Spectrum": Spectrum_list,
             "Tissue": Tissue_list,
             "Pathway": Pathway_list,
             "Reference": Reference_list,
             "Disease": Disease_list,
             "Protein": Protein_list,
             "HMDB_dict": HMDB_dict_list,
             "Cellular_locations": Cellular_locations,
             "Biospecimen_locations": Biospecimen_locations,
             "Concentration": Concentration
             }

    Relations = {
        "secondary_accession": Rel_secondary_accession,
        "synonyms": Rel_synonyms,
        "alternative_parent": Rel_alternative_parent,
        "substituent": Rel_substituent,
        "external_descriptor": Rel_external_descriptor,
        "taxonomy": Rel_taxonomy,
        "external_property": Rel_external_property,
        "predicted_property": Rel_predicted_property,
        "spectrum": Rel_spectrum,
        "cellular_location": Rel_cellular_location,
        "biospecimen_location": Rel_biospecimen_location,
        "tissue": Rel_tissue,
        "pathway": Rel_pathway,
        "concentration": Rel_concentration,
        "reference_concentration": Rel_reference_concentration,
        "reference_disease": Rel_reference_disease,
        "disease": Rel_disease,
        "general_reference": Rel_general_reference,
        "protein": Rel_protein,
    }
    return Nodes, Relations


def count_nodes(Nodes):
    nodes_num = 0
    for key, value in Nodes.items():
        if value:
            if isinstance(value[0], str):
                length = len(list(set(value)))
                nodes_num += length
            else:
                length = len(drop_duplicate(value))
                nodes_num += length
        print(f"{key} has {length} nodes")
    print(f"Total Node Num:{nodes_num}")
    return nodes_num


def count_relations(Relations):
    relation_num = 0
    for key, value in Relations.items():
        if value:
            if isinstance(value[0], str):
                length = len(list(set(value)))
                relation_num += length
            else:
                length = len(drop_duplicate(value))
                relation_num += length
        print(f"{key} has {length} relations")
    print(f"Total Relationship Num:{relation_num}")
    return relation_num


def create_node(graph, Nodes):
    HMDB_list,\
        Name_Synonyms,\
        Taxonomy_list,\
        Alternative_parent,\
        Substituent_list,\
        External_descriptor,\
        Ontology_list,\
        External_property_list,\
        Predicted_property_list,\
        Spectrum_list,\
        Tissue_list,\
        Pathway_list,\
        Reference_list,\
        Disease_list,\
        Protein_list,\
        HMDB_dict_list,\
        Cellular_locations,\
        Biospecimen_locations,\
        Concentration = Nodes.values()

    for i in tqdm(drop_duplicate(HMDB_dict_list), desc="Creating HMDB Nodes"):
        graph.create(Node("HMDB_NO", **i))

    for i in tqdm(drop_duplicate(HMDB_list), desc="Creating Secondary HMDB Nodes"):
        if graph.nodes.match("HMDB_NO").where(f"_.accession='{i}'").first():
            continue
        else:
            graph.create(Node("HMDB_Secondary", accession=i))

    for i in tqdm(drop_duplicate(Name_Synonyms), desc="Creating Synonym Nodes"):
        graph.create(Node("Synonyms", name=i))

    for i in tqdm(drop_duplicate(Taxonomy_list), desc="Creating Taxonomy Nodes"):
        graph.create(Node("Taxonomy", **i))

    for i in tqdm(drop_duplicate(Alternative_parent), desc="Creating AP Nodes"):
        graph.create(Node("Alternative_parent", name=i))

    for i in tqdm(drop_duplicate(Substituent_list), desc="Creating Substituent Nodes"):
        graph.create(Node("Substituent", name=i))

    for i in tqdm(drop_duplicate(External_descriptor), desc="Creating External Descriptor Nodes"):
        graph.create(Node("External_descriptor", name=i))

    for i in tqdm(drop_duplicate(External_property_list), desc="Creating External Property Nodes"):
        graph.create(Node("External_property", **i))

    for i in tqdm(drop_duplicate(Predicted_property_list), desc="Creating Predicted Property Nodes"):
        graph.create(Node("Predicted_property", **i))

    for i in tqdm(drop_duplicate(Spectrum_list), desc="Creating Spectrum Nodes"):
        graph.create(Node("Spectrum", **i))

    for i in tqdm(drop_duplicate(Cellular_locations), desc="Creating CL Nodes"):
        graph.create(Node("Cellular_location", name=i))

    for i in tqdm(drop_duplicate(Biospecimen_locations), desc="Creating BL Nodes"):
        graph.create(Node("Biospecimen_location", name=i))

    for i in tqdm(drop_duplicate(Tissue_list), desc="Creating Tissue Nodes"):
        graph.create(Node("Tissue", name=i))

    for i in tqdm(drop_duplicate(Pathway_list), desc="Creating Pathway Nodes"):
        graph.create(Node("Pathway", **i))

    for i in tqdm(drop_duplicate(Concentration), desc="Creating Concentration Nodes"):
        graph.create(Node("Concentration", **i))

    for i in tqdm(drop_duplicate(Reference_list), desc="Creating Reference Nodes"):
        graph.create(Node("Reference", **i))

    for i in tqdm(drop_duplicate(Disease_list), desc="Creating Disease Nodes"):
        graph.create(Node("Disease", **i))

    for i in tqdm(drop_duplicate(Protein_list), desc="Creating Protein Nodes"):
        graph.create(Node("Protein", **i))

    return graph


def create_relations(graph, Relations):
    Rel_secondary_accession,\
        Rel_synonyms,\
        Rel_alternative_parent,\
        Rel_substituent,\
        Rel_external_descriptor,\
        Rel_taxonomy,\
        Rel_external_property,\
        Rel_predicted_property,\
        Rel_spectrum,\
        Rel_cellular_location,\
        Rel_biospecimen_location,\
        Rel_tissue,\
        Rel_pathway,\
        Rel_concentration,\
        Rel_reference_concentration,\
        Rel_reference_disease,\
        Rel_disease,\
        Rel_general_reference,\
        Rel_protein = Relations.values()
    for sn, rel, en in tqdm(drop_duplicate(Rel_secondary_accession),desc="Creating Secondary HMDB Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            en = graph.nodes.match("HMDB_Secondary").where(
                f"_.accession='{en}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_synonyms),desc="Creating Synonym Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            en = graph.nodes.match("Synonyms").where(f"_.name='{en}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_taxonomy),desc="Creating Taxonomy Relations"):
        try:
            en = graph.nodes.match("Taxonomy").where(
                f"_.HMDB_NO='{sn}'").first()
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_alternative_parent),desc="Creating AP Relations"):
        try:
            sn = graph.nodes.match("Taxonomy").where(
                f"_.HMDB_NO='{sn}'").first()
            en = graph.nodes.match("Alternative_parent").where(
                f"_.name='{en}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_substituent),desc="Creating Substituent Relations"):
        try:
            sn = graph.nodes.match("Taxonomy").where(
                f"_.HMDB_NO='{sn}'").first()
            en = graph.nodes.match("Substituent").where(
                f"_.name='{en}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_external_descriptor),desc="Creating External Descriptor Relations"):
        try:
            sn = graph.nodes.match("Taxonomy").where(
                f"_.HMDB_NO='{sn}'").first()
            en = graph.nodes.match("External_descriptor").where(
                f"_.name='{en}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_external_property),desc="Creating External Property Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            kind, value = en["kind"], en["value"]
            en = graph.nodes.match("External_property").where(
                f"_.kind='{kind}' and _.value='{value}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_predicted_property),desc="Creating Predicted Property Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            kind, value = en["kind"], en["value"]
            en = graph.nodes.match("Predicted_property").where(
                f"_.kind='{kind}' and _.value='{value}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_spectrum),desc="Creating Spectrum Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            type, spectrum_id = en["type"], en["spectrum_id"]
            en = graph.nodes.match("Spectrum").where(
                f"_.type='{type}' and _.spectrum_id='{spectrum_id}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_concentration),desc="Creating Concentration Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            id = en["id"]
            en = graph.nodes.match("Concentration").where(
                f"_.id='{id}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_reference_concentration),desc="Creating Reference Concentration Relations"):
        try:
            id = sn["id"]
            sn = graph.nodes.match("Concentration").where(
                f"_.id='{id}'").first()
            if "pubmed_id" in en.keys():
                pubmed_id = en["pubmed_id"]
                if pubmed_id:
                    en = graph.nodes.match("Reference").where(
                        f"_.pubmed_id='{pubmed_id}'").first()
                else:
                    reference_text = en["reference_text"]
                    en = graph.nodes.match("Reference").where(
                        f"_.reference_text='{reference_text}'").first()
            else:
                reference_text = en["reference_text"]
                en = graph.nodes.match("Reference").where(
                    f"_.reference_text='{reference_text}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_cellular_location),desc="Creating Cellular Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            en = graph.nodes.match("Cellular_location").where(
                f"_.name='{en}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_biospecimen_location),desc="Creating Biospecimen Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            en = graph.nodes.match("Biospecimen_location").where(
                f"_.name='{en}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_tissue),desc="Creating Tissue Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            en = graph.nodes.match("Tissue").where(f"_.name='{en}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_pathway),desc="Creating Pathway Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            if not en:
                continue
            smpdb_id = en["smpdb_id"]
            en = graph.nodes.match("Pathway").where(
                f"_.smpdb_id='{smpdb_id}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_reference_disease),desc="Creating Reference Disease Relations"):
        try:
            name = sn["name"]
            sn = graph.nodes.match("Disease").where(f"_.name='{name}'").first()
            if "pubmed_id" in en.keys():
                pubmed_id = en["pubmed_id"]
                if pubmed_id:
                    en = graph.nodes.match("Reference").where(
                        f"_.pubmed_id='{pubmed_id}'").first()
                else:
                    reference_text = en["reference_text"]
                    en = graph.nodes.match("Reference").where(
                        f"_.reference_text='{reference_text}'").first()
            else:
                reference_text = en["reference_text"]
                en = graph.nodes.match("Reference").where(
                    f"_.reference_text='{reference_text}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_general_reference),desc="Creating General Reference Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            if "pubmed_id" in en.keys():
                pubmed_id = en["pubmed_id"]
                if pubmed_id:
                    en = graph.nodes.match("Reference").where(
                        f"_.pubmed_id='{pubmed_id}'").first()
                else:
                    reference_text = en["reference_text"]
                    en = graph.nodes.match("Reference").where(
                        f"_.reference_text='{reference_text}'").first()
            else:
                reference_text = en["reference_text"]
                en = graph.nodes.match("Reference").where(
                    f"_.reference_text='{reference_text}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_disease),desc="Creating Disease Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            name = en["name"]
            en = graph.nodes.match("Disease").where(f"_.name='{name}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)

    for sn, rel, en in tqdm(drop_duplicate(Rel_protein),desc="Creating Protein Relations"):
        try:
            sn = graph.nodes.match("HMDB_NO").where(
                f"_.accession='{sn}'").first()
            protein_accession = en["protein_accession"]
            en = graph.nodes.match("Protein").where(
                f"_.protein_accession='{protein_accession}'").first()
            graph.create(Relationship(sn, rel, en))
        except Exception as e:
            print(e)
    return graph
