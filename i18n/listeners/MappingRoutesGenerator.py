import json
import os

class MappingRoutesGenerator:

    def generate(self, language_file_path):
            language_files = os.scandir(os.path.join(language_file_path, 'languageFiles/en-US')) # 'en-US' is a standard language file for this generator 
            parse_route_record = []
            i18n_json_routes_map = {}

            def append_route_to_map(last_key_of_route, value):
                path = ''.join(parse_route_record) + "[\'%s\']" % last_key_of_route
                if value not in i18n_json_routes_map:
                    i18n_json_routes_map[value] = [] 
                i18n_json_routes_map[value].append(path)
                
            def parse_i18n_key_mapping(key_mappings):
                for key in key_mappings.keys():
                    if isinstance(key_mappings[key], dict):
                        parse_route_record.append("['%s']" % key)
                        parse_i18n_key_mapping(key_mappings[key])
                    else:
                        append_route_to_map(key, key_mappings[key])
                #pop out parent node when all children node had already been append to parse_route_record
                else:
                    if len(parse_route_record) > 0:
                        parse_route_record.pop()
            
            for language_file in language_files:
                with open(os.path.normpath(language_file.path), 'r', encoding='utf-8') as f:
                    language_key_text_mappings = json.load(f)
                    parse_i18n_key_mapping(language_key_text_mappings)
            json.dump(i18n_json_routes_map, open('./mappingRoutes.json', "w"),indent=4) 

if __name__=='__main__':
    MappingRoutesGenerator().generate()