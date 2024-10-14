from pyvis.network import Network as GNetwork
import json
from jinja2 import Environment, FileSystemLoader

class Visual():
    def create_visual(self, file_name=None):
        G = GNetwork(
            height="1200px",
            width="100%",
            notebook=True,
            cdn_resources="remote",
            directed=True,
            select_menu=True,
        )

        for node in self.nodes:
            type = node.type 
            if node.type == 'term_source':
                type = 'source'
            elif node.type == 'term_sink':
                type = 'sink'

            G.add_node(
                node.node_id,
                shape="dot",
                label="{} Node ={}\n f_i={}\n t_i={}".format(node.type, node.node_id, node.window_start, node.window_end),
                color=(
                    self.config.COLOR[type]
                    if type != "out-charters"
                    else self.config.COLOR_OUT_CHARTERS[type]
                ),
            )

        for arc in self.arcs:
            G.add_edge(
                arc.upstr.node_id,
                arc.dwnstr.node_id,
                label="Vessel={}\nFrom={}\nTo={}\nDays={}".format(
                    arc.vessel,
                    arc.upstr.node_id,
                    arc.dwnstr.node_id,
                    (arc.arc_upstr_window_start, arc.arc_upstr_window_end, arc.arc_dwnstr_window_start, arc.arc_dwnstr_window_end),
                ),
            )

        self.setup_template_environment()
        self.render_and_save_html(G)

        G.repulsion(node_distance=200, spring_length=200)
        if file_name:
            path = "{}/visual/" + file_name + ".html"
        else:
            path = "{}/visual/custom_poc_supernode_{}_{}.html"
        G.show(path.format(self.config.CASENAME, arc.vessel, arc))

    def setup_template_environment(self):
        template_dir = "outputs/Best_best_base_plan05Jul20245_test/input"
        try:
            self.template_env = Environment(loader=FileSystemLoader(template_dir))
            self.template = self.template_env.get_template('basic_network_template.html')
            print("Template loaded successfully")
        except Exception as e:
            print(f"An error occurred while loading the template: {e}")

    def render_and_save_html(self, G):
        oppath = "outputs/Best_best_base_plan05Jul20245_test//visual/new_nwk.html"
        try:
            html = self.template.render(network=G)
            with open(oppath, "w+") as f:
                f.write(html)
            print(f"Network visualization saved to {oppath}")
        except Exception as e:
            print(f"An error occurred while saving the network visualization: {e}")
