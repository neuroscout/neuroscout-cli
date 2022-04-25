import json
from copy import deepcopy

def convert_to_v1(model):
    """ Convert a 0.x BIDS Stats Model to v1.
    Currently tailed to convert simple Neuroscout-style models """
    model = deepcopy(model)
    
    # Add version
    model["BIDSModelVersion"] = 1.0
    
    # Steps -> Nodes
    model["Nodes"] = model.pop("Steps")
    
    for node in model["Nodes"]:
        # Level == Name
        node["Level"] = node["Level"].lower()
        node["Name"] = node["Level"]
        
        # Set GroupBy for each group correctly
        if node["Level"] == "run":
            node["GroupBy"] = ["run", "subject"]
        elif node["Level"] == "subject":
            node["GroupBy"] = ["subject", "contrast"]
        elif node["Level"] == "dataset":
            node["GroupBy"] = ["contrast"]
        
        # Model is mandatory, add constant
        if "Model" not in node:
            node['Model'] = {}
            node['Model']['X'] = [1]
        else:
            node['Model']['X'].append(1)
             
        # Contrast "type" -> "Test". Add default. 
        if "Contrasts" in node:
            for con in node["Contrasts"]:
                if "type" in con:
                    con["Test"] = con.pop("type")
                else:
                    con["Test"] = "t"
                
        # DummyContrast "Type" -> "Test"
        # add "Type" = "Meta" to "X"
        if "DummyContrasts" in node:
            node['DummyContrasts']['Test'] = \
                node['DummyContrasts'].pop('Type')
            
            if node['DummyContrasts']['Test'] == 'FEMA':
                node['DummyContrasts']['Test'] = 't'
                node['Model']['Type'] = 'Meta'
                
        # Indirect Transformations call
        if "Transformations" in node:
            node["Transformations"] = {
                "Transformer": "pybids-transforms-v1",
                "Instructions": node.pop("Transformations")
            }
    
    return model


def check_convert_model(model_path):
    model = json.load(model_path.open())
    
    if "BIDSModelVersion" not in model or model["BIDSModelVersion"] < 1.0:
        new_model = convert_to_v1(model)
        model_path = model_path.parent / "model_v1.json"
        json.dump(new_model, model_path.open('w'))
    
    return model_path
