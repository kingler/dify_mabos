class ProcessTemplate:
    def __init__(self):
        self.templates = {}

    def store_template(self, template_id, template_data):
        self.templates[template_id] = template_data

    def retrieve_template(self, template_id):
        return self.templates.get(template_id)

    def update_template(self, template_id, updated_data):
        if template_id in self.templates:
            self.templates[template_id].update(updated_data)

    def search_templates_by_type(self, process_type):
        return [template for template in self.templates.values() if template.get('type') == process_type]

    def search_templates_by_industry(self, industry):
        return [template for template in self.templates.values() if template.get('industry') == industry]

    def search_templates_by_keyword(self, keyword):
        return [template for template in self.templates.values() if keyword in template.get('description', '')]

    def retrieve_relevant_templates(self, criteria):
        relevant_templates = []
        if 'type' in criteria:
            relevant_templates.extend(self.search_templates_by_type(criteria['type']))
        if 'industry' in criteria:
            relevant_templates.extend(self.search_templates_by_industry(criteria['industry']))
        if 'keyword' in criteria:
            relevant_templates.extend(self.search_templates_by_keyword(criteria['keyword']))
        return list(set(relevant_templates))
