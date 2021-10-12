import pandas as pd 
from snorkel.labeling import LabelingFunction

'''
    Useful Functions 
'''
def keyword_lookup(x,bio_functions:pd.DataFrame,bio_function_rules:pd.DataFrame):
    """Returns the id cooresponding to the label

    Args:
        x (str): some phrase

    Returns:
        int: the id
    """
    for i in range(len(bio_functions)):
        label_name = bio_functions.iloc[i]['function'] 
        label_id = bio_functions.iloc[i]['function_enumerated']        
        
        label_rule_name = label_name + "_rules"
        if label_rule_name in list(bio_function_rules.columns):
            phrases_to_look_for = bio_function_rules[label_rule_name].to_list()
            for phrase in phrases_to_look_for:
                # now you could make a counter and see the percentage match so if 10/20 phrases are in the text/abstract then you return the
                if phrase in x.text.lower():     
                    return label_id
        else:
            print(f"Label {label_name} does not have rules associated with it")

'''
    Main Code 
'''
phrases_to_look_for = []

def create_labeling_functions(bio_file:pd.DataFrame, bio_rules:pd.DataFrame):
    bio_file = pd.read_csv(bio_file)
    bio_rules = pd.read_csv(bio_rules)
    
    labeling_function_list = list()
    for i in range(len(bio_file)):
        label_name = bio_file.iloc[i]['function'] 
        label_rule_name = label_name + "_rules"
        if label_rule_name in list(bio_rules.columns):
            phrases_lst = bio_rules[label_rule_name].to_list()
            remove_na = [x for x in phrases_lst if pd.isnull(x) == False]
        for rule in remove_na:
            rule = rule.replace(" ", "_")
            phrases_to_look_for.append(rule)
        for phrase in phrases_to_look_for:
            labeling_function = LabelingFunction(name=f"keyword_{phrase}", f=keyword_lookup,
                            resources={"bio_functions":bio_file,"bio_function_rules":bio_rules})
            labeling_function_list.append(labeling_function)

    # Create a Labeling Function for each Label
    # for i in range(len(bio_functions)):
    #     label_name = bio_functions.iloc[i]['function']
    #     labeling_function = LabelingFunction(name=f"keyword_{label_name}", f=keyword_lookup,
    #             resources={"bio_functions":bio_functions,"bio_function_rules":function_rule_phrases})
    #     labeling_function_list.append(labeling_function)

    return labeling_function_list

create_labeling_functions('biomimicry_functions_enumerated.csv', 'biomimicry_function_rules.csv')

        