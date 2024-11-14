
import os
from pathlib import Path
import yaml

class RuleInformationProvider:
    """
    A class to provide information about rule classifications and templates based on YAML data.

    This class loads and processes rule classification data, template data, and example data from specified YAML files.
    It is used to generate markdown documentation for a given rule type, including details such as templates and examples.

    Attributes:
    -----------
    data_path : str
        Path to the directory containing the YAML files.
    template_dict : dict
        Dictionary containing template information loaded from the templates YAML file.
    examples_dict : dict
        Dictionary containing example information loaded from the examples YAML file.
    """
    
    def __init__(self, data_path):
        """
        Initializes the RuleInformationProvider with the specified data path.

        Parameters:
        -----------
        data_path : str
            Path to the directory containing the YAML files with rules, templates, and examples.
        """
        self.data_path = data_path
        self.template_dict = self._load_yaml(f'{data_path}/witt_templates.yaml', 'template_list')
        self.examples_dict = self._load_yaml(f'{data_path}/witt_examples.yaml', 'example_list')

    def _load_yaml(self, file_path, list_key=None):
        """
        Loads data from a YAML file.

        Parameters:
        -----------
        file_path : str
            Path to the YAML file to be loaded.
        list_key : str, optional
            Key used to extract a specific list from the YAML data. If provided, returns a dictionary indexed by 'id'.

        Returns:
        --------
        dict
            If list_key is provided, returns a dictionary with items indexed by 'id'.
        Any type
            If list_key is not provided, returns the entire data structure from the YAML file.
        """
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            if list_key:
                return {item['id']: item for item in data[list_key]}
            return data

    def get_classification_and_templates(self, section_title):
        """
        Retrieves classification information and templates for a specified rule section.

        Parameters:
        -----------
        section_title : str
            Title of the section for which to retrieve information.

        Returns:
        --------
        str
            A markdown formatted string containing the classification details, templates, and examples for the given section.
        """
        data = self._load_yaml(f'{self.data_path}/classify_subtypes.yaml')
        filtered_data = self._filter_sections_by_title(data, section_title)
        return self._convert_to_markdown(filtered_data)

    def _filter_sections_by_title(self, data, title):
        """
        Filters sections based on the given title.

        Parameters:
        -----------
        data : list
            List of sections to filter from.
        title : str
            Title to filter sections by.

        Returns:
        --------
        list
            A list of sections that match the given title.
        """
        return [section for section in data if section['section_title'] == title]

    def _convert_to_markdown(self, filtered_data):
        """
        Converts filtered rule classification data to markdown format.

        Parameters:
        -----------
        filtered_data : list
            List of filtered sections to convert into markdown.

        Returns:
        --------
        str
            A markdown formatted string representing the filtered sections.
        """
        def process_section(section, level=2):
            """
            Processes a section recursively and converts it to markdown format.

            Parameters:
            -----------
            section : dict
                The section to process.
            level : int, optional
                The heading level for the section title in markdown (default is 1).

            Returns:
            --------
            str
                A markdown formatted string for the section and its subsections.
            """
            markdown = f"{'#' * level} {section['section_title']}\n\n"
            markdown += f"**ID**: {section['section_id']}\n\n"
            markdown += f"**Definition**: {section['section_definition']}\n\n"

            if 'templates' in section and section['templates']:
                for template_id in section['templates']:
                    if template_id in self.template_dict:
                        template = self.template_dict[template_id]
                        markdown += f"**Template ID**: {template_id}\n\n"
                        markdown += f"**Template Explanation**: {template['explanation']}\n\n"
                        markdown += f"**Template Text**:\n\n```template\n{template['text']}```\n\n"
                    else:
                        markdown += f"**Template ID**: {template_id} - No details found.\n\n"
            else:
                markdown += "**Templates**: Look in the subsection(s).\n\n"

            if 'examples' in section and section['examples']:
                for example_id in section['examples']:
                    if example_id in self.examples_dict:
                        example = self.examples_dict[example_id]
                        markdown += f"**Example ID**: {example_id}\n\n"
                        markdown += f"**Example Text**:\n\n```example\n{example['text']}```\n\n"
                    else:
                        markdown += f"**Example ID**: {example_id} - No details found.\n\n"

            if 'subsections' in section:
                for subsection in section['subsections']:
                    markdown += process_section(subsection, level + 1)

            return markdown

        markdown = ""
        for section in filtered_data:
            markdown += process_section(section)
        return markdown

class RulesTemplateProvider:
    """
    A class to provide information about rules templates and their relationships from YAML data.

    This class loads and processes template data, subtemplate data, and their relationships from specified YAML files.
    It is used to extract information about templates and format them into readable output.

    Attributes:
    -----------
    data_directory : Path
        Path to the directory containing the YAML files.
    data_dicts : dict
        Dictionary containing data loaded from YAML files, including templates, subtemplates, and relationships.
    """
    
    def __init__(self, data_directory):
        """
        Initializes the RulesTemplateProvider with the specified data directory.

        Parameters:
        -----------
        data_directory : str or Path
            Path to the directory containing the YAML files with templates, subtemplates, and relationships.
        """
        self.data_directory = Path(data_directory)
        self.data_dicts = self._load_data()

    def _load_yaml(self, file_path):
        """
        Loads data from a YAML file.

        Parameters:
        -----------
        file_path : Path
            Path to the YAML file to be loaded.

        Returns:
        --------
        dict
            A dictionary containing the data from the YAML file.
        """
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}

    def _load_data(self):
        """
        Loads data from multiple YAML files required for template processing.

        Returns:
        --------
        dict
            A dictionary containing data from templates, subtemplates, and template relationships YAML files.
        """
        witt_template_relationship_file = self.data_directory / 'witt_template_subtemplate_relationship.yaml'
        witt_templates_file = self.data_directory / 'witt_templates.yaml'
        witt_subtemplates_file = self.data_directory / 'witt_subtemplates.yaml'

        witt_template_relationship_data = self._load_yaml(witt_template_relationship_file).get('template_subtemplate_relationship', {})
        witt_templates_data = self._load_yaml(witt_templates_file).get('template_list', [])
        witt_subtemplates_data = self._load_yaml(witt_subtemplates_file).get('subtemplate_list', [])

        return {
            'witt_template_relationship_data': witt_template_relationship_data,
            'witt_templates_data': witt_templates_data,
            'witt_subtemplates_data': witt_subtemplates_data
        }

    def _get_template_data(self, template_key, data):
        """
        Retrieves data for a specific template or subtemplate based on its key.

        Parameters:
        -----------
        template_key : str
            The key of the template or subtemplate to be retrieved.
        data : list or dict
            The data to search in, which can be a list of templates or a dictionary of relationships.

        Returns:
        --------
        dict or None
            The data corresponding to the specified template key, or None if not found.
        """
        if isinstance(data, dict):
            return data.get(template_key, None)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get('id', '') == template_key:
                    return item
        return None

    def _format_template_output(self, template_key, template_data):
        """
        Formats the output for a given template or subtemplate.

        Parameters:
        -----------
        template_key : str
            The key of the template or subtemplate.
        template_data : dict
            The data of the template or subtemplate to be formatted.

        Returns:
        --------
        str
            A formatted string representation of the template data.
        """
        title = template_data.get('title', '')
        output = f"## {template_key}: {title}\n\n" if title else f"## {template_key}\n\n"

        if not template_data:
            output += "Template data not found.\n\n"
            return output

        # Format subtemplates in use as a bullet list with titles if available
        if 'usesSubtemplate' in template_data:
            output += "### Subtemplate(s) in use\n"
            subtemplate_list = []
            for sub_key in template_data['usesSubtemplate']:
                sub_data = self._get_template_data(sub_key, self.data_dicts['witt_subtemplates_data'])
                sub_title = sub_data.get('title', '') if sub_data else "Unknown"
                subtemplate_list.append(f"- {sub_key}: {sub_title}")
            output += "\n".join(subtemplate_list) + "\n\n"
        
        if 'text' in template_data:
            output += f"### Text\n\n{template_data['text']}\n\n"
        if 'explanation' in template_data:
            output += f"### Explanation\n\n{template_data['explanation']}\n\n"
        return output

    def _process_template(self, template_key, processed_keys=None):
        """
        Processes a template or subtemplate recursively, including any subtemplates used,
        and avoids processing duplicates.

        Parameters:
        -----------
        template_key : str
            The key of the template or subtemplate to be processed.
        processed_keys : set, optional
            A set of keys that have already been processed to prevent duplicate entries.

        Returns:
        --------
        str
            A formatted string representation of the template and its subtemplates, without duplicates.
        """
        if processed_keys is None:
            processed_keys = set()

        # If this template or subtemplate has already been processed, skip it
        if template_key in processed_keys:
            return ''
        processed_keys.add(template_key)

        template_data = None

        # Determine whether it's a main template or subtemplate based on key prefix
        if template_key.startswith('T'):
            template_data = self._get_template_data(template_key, self.data_dicts['witt_templates_data']) or {}
            uses_subtemplate = self._get_template_data(template_key, self.data_dicts['witt_template_relationship_data'])
            if uses_subtemplate:
                template_data['usesSubtemplate'] = uses_subtemplate if isinstance(uses_subtemplate, list) else [uses_subtemplate]
        elif template_key.startswith('S'):
            template_data = self._get_template_data(template_key, self.data_dicts['witt_subtemplates_data']) or {}
            uses_subtemplate = self._get_template_data(template_key, self.data_dicts['witt_template_relationship_data'])
            if uses_subtemplate:
                template_data['usesSubtemplate'] = uses_subtemplate if isinstance(uses_subtemplate, list) else [uses_subtemplate]

        if not template_data:
            return f"# {template_key}\n\nTemplate data not found.\n\n"

        output = self._format_template_output(template_key, template_data)

        # Process each subtemplate recursively, avoiding duplicates
        if 'usesSubtemplate' in template_data:
            subtemplate_keys = template_data['usesSubtemplate']
            subtemplate_keys = [subtemplate_keys] if isinstance(subtemplate_keys, str) else subtemplate_keys
            for sub_key in subtemplate_keys:
                sub_key = sub_key.strip()
                output += self._process_template(sub_key, processed_keys)

        return output

    def get_rules_template(self, template_keys):
        """
        Retrieves the formatted rules templates for the specified list of template keys, avoiding duplicate subtemplates.

        Parameters:
        -----------
        template_keys : str or list of str
            The key(s) of the template(s) to be retrieved. Can be a single string key or a list of keys.

        Returns:
        --------
        str
            A formatted string representation of each template and its associated subtemplates, without duplicates.
        """
        # If a single template key is provided as a string, convert it to a list
        if isinstance(template_keys, str):
            template_keys = [template_keys]

        output = ""
        processed_subtemplates = set()  # Track processed templates and subtemplates to avoid duplicates

        for template_key in template_keys:
            output += self._process_template(template_key, processed_keys=processed_subtemplates)
            output += "\n\n"  # Separate each template with extra newlines for readability

        return output

# Example usage:
# rule_information_provider = RuleInformationProvider("../data")
# markdown_data = rule_provider.get_classification_and_templates("Data rules")
# print(markdown_data)

# rule_template_provider = RulesTemplateProvider("../data")
# markdown_data = processor.get_rules_template("T7")
# print(markdown_data)
