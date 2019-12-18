# prepare_espei_model_from_TDB
To extract model json file for ESPEI/pycalphad based on the existing TDB file


Input file: TDB file, this code will read the first TDB file in the current folder if there are more TDB files.

Output file 1: INPUT+MODEL.json, a model-json file for ESPEI/pycalphad.
Output file 2: phase_list_for_reference.txt, a list of all phases in yaml file format and the disorder-order phases listed at the end part within “[ ]”.
