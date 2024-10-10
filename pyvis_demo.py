from pyvis.network import Network
from jinja2 import Environment, FileSystemLoader
import os
import json

class Visualization:
    def __init__(self):
        self.net = Network()
        self.template = None
        self.template_env = None
        self.nodes = []
        self.edges = []
        self.create_network()

    def load_data(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

    def create_network(self):
        data_file = "C:/Users/prdm/Desktop/PyPrac/network_data.json"
        data = self.load_data(data_file)

        for node in data['nodes']:
            self.net.add_node(node['id'], label=node['label'], title=node['title'])
            self.nodes.append(node)
        for edge in data['edges']:
            self.net.add_edge(edge['from'], edge['to'])
            self.edges.append(edge)

        self.setup_template_environment()
        self.render_and_save_html()

    def setup_template_environment(self):
        template_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Template Directory: {template_dir}")
        print(f"Template Directory Exists: {os.path.exists(template_dir)}")

        # Debug: Check if the template files are present
        template_files = os.listdir(template_dir) if os.path.exists(template_dir) else []
        print(f"Template Files: {template_files}")

        # Manually load the template
        try:
            self.template_env = Environment(loader=FileSystemLoader(template_dir))
            self.template = self.template_env.get_template('basic_network_template.html')
            print("Template loaded successfully")
        except Exception as e:
            print(f"An error occurred while loading the template: {e}")

    def render_and_save_html(self):
        nodes = json.dumps(self.net.nodes)
        edges = json.dumps(self.net.edges)
        oppath = "C:/Users/prdm/Desktop/PyPrac/networkx.html"

        # Render the template manually
        try:
            html = self.template.render(nodes=nodes, edges=edges)
            with open(oppath, "w+") as f:
                f.write(html)
            print(f"Network visualization saved to {oppath}")
        except Exception as e:
            print(f"An error occurred while saving the network visualization: {e}")

    def show_network(self):
        path = "C:/Users/prdm/Desktop/PyPrac/network.html"
        try:
            if self.net is not None:
                self.net.show(path, notebook=False)
        except Exception as e:
            print(e)

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

if __name__ == "__main__":
    v = Visualization()
    v.show_network()
