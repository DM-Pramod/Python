
//templates/node.html:
<table>
    <tr><th>Type</th><td>{{ node.type }}</td></tr>
    <tr><th>Node ID</th><td>{{ node.node_id }}</td></tr>
    <tr><th>From</th><td>{{ node.window_start }}</td></tr>
    <tr><th>To</th><td>{{ node.window_end }}</td></tr>
</table>


 //templates/edge.html
 <table>
    <tr><th>Vessel</th><td>{{ vessel }}</td></tr>
    <tr><th>Next Node ID</th><td>{{ arc.upstr.node_id }}</td></tr>
    <tr><th>From Node ID</th><td>{{ arc.dwnstr.node_id }}</td></tr>
    <tr><th>Days</th><td>{{ arc.arc_upstr_window_start }}, {{ arc.arc_upstr_window_end }}, {{ arc.arc_dwnstr_window_start }}, {{ arc.arc_dwnstr_window_end }}</td></tr>
</table>


from pyvis.network import Network as GNetwork
from jinja2 import Environment, FileSystemLoader
import json
from config import Config

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

def generate_node_html(node):
    template = env.get_template('node.html')
    return template.render(node=node)

def generate_edge_html(vn, arc):
    template = env.get_template('edge.html')
    return template.render(vessel=vn, arc=arc)

class Visual():

    def create_visual(self, file_name=None):
        self.nds = []
        self.eds = []

        for v in self.vessels:
            vn = v.node_id
            print(vn)

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
                    title=generate_node_html(node),
                )

                self.nds.append({"type": node.type, "id": node.node_id, "From": node.window_start, "To": node.window_end})

            for arc in self.arcs:
                G.add_edge(
                    arc.upstr.node_id,
                    arc.dwnstr.node_id,
                    label="Vessel={}\nFrom={}\nTo={}\nDays={}".format(
                        vn,
                        arc.upstr.node_id,
                        arc.dwnstr.node_id,
                        (arc.arc_upstr_window_start, arc.arc_upstr_window_end, arc.arc_dwnstr_window_start, arc.arc_dwnstr_window_end),
                    ),
                    title=generate_edge_html(vn, arc),
                )

                self.eds.append({
                    "Vessel": vn,
                    "Next_NodeID": arc.upstr.node_id,
                    "From_NodeID": arc.dwnstr.node_id,
                    "DAYS": (arc.arc_upstr_window_start, arc.arc_upstr_window_end, arc.arc_dwnstr_window_start, arc.arc_dwnstr_window_end),
                })

            G.repulsion(node_distance=200, spring_length=200)
            if file_name:
                path = "{}/visual/" + file_name + ".html"
            else:
                path = "{}/visual/custom_poc_supernode_{}_{}.html"
            G.show(
                path.format(self.config.CASENAME, vn, v)
            )


********************************************************************************************************************
<!-- node.html -->
<table>
    <tr>
        <th>Type</th>
        <th>Node ID</th>
        <th>From</th>
        <th>To</th>
    </tr>
    <tr>
        <td>{{ node.type }}</td>
        <td>{{ node.node_id }}</td>
        <td>{{ node.window_start }}</td>
        <td>{{ node.window_end }}</td>
    </tr>
</table>

=============================================
<!-- edge.html -->
<table>
    <tr>
        <th>Vessel</th>
        <th>Next Node ID</th>
        <th>From Node ID</th>
        <th>Days</th>
    </tr>
    <tr>
        <td>{{ vessel }}</td>
        <td>{{ arc.upstr.node_id }}</td>
        <td>{{ arc.dwnstr.node_id }}</td>
        <td>{{ arc.arc_upstr_window_start }}, {{ arc.arc_upstr_window_end }}, {{ arc.arc_dwnstr_window_start }}, {{ arc.arc_dwnstr_window_end }}</td>
    </tr>
</table>

===============================================
// Function to fetch HTML template
async function fetchTemplate(templatePath) {
    const response = await fetch(templatePath);
    return response.text();
}

// Function to render template with data
function renderTemplate(template, data) {
    return template.replace(/{{(\w+)}}/g, (match, key) => data[key] || '');
}

// Function to render Node Table
async function renderNodeTable(node) {
    const container = document.getElementById('node-table-container');
    const template = await fetchTemplate('node.html');
    const rendered = renderTemplate(template, node);
    container.innerHTML = rendered;
}

// Function to render Edge Table
async function renderEdgeTable(vn, arc) {
    const container = document.getElementById('edge-table-container');
    const template = await fetchTemplate('edge.html');
    const data = {
        vessel: vn,
        upstr_node_id: arc.upstr.node_id,
        dwnstr_node_id: arc.dwnstr.node_id,
        arc_upstr_window_start: arc.arc_upstr_window_start,
        arc_upstr_window_end: arc.arc_upstr_window_end,
        arc_dwnstr_window_start: arc.arc_dwnstr_window_start,
        arc_dwnstr_window_end: arc.arc_dwnstr_window_end
    };
    const rendered = renderTemplate(template, data);
    container.innerHTML = rendered;
}

=============================================================================================
from pyvis.network import Network as GNetwork
from jinja2 import Environment, FileSystemLoader
import json
from config import Config

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

def generate_node_html(node):
    template = env.get_template('node.html')
    return template.render(node=node)

def generate_edge_html(vn, arc):
    template = env.get_template('edge.html')
    return template.render(vessel=vn, arc=arc)

class Visual():

    def create_visual(self, file_name=None):
        self.nds = []
        self.eds = []

        for v in self.vessels:
            vn = v.node_id
            print(vn)

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
                    title=generate_node_html(node),
                )

                self.nds.append({"type": node.type, "id": node.node_id, "From": node.window_start, "To": node.window_end})

            for arc in self.arcs:
                G.add_edge(
                    arc.upstr.node_id,
                    arc.dwnstr.node_id,
                    label="Vessel={}\nFrom={}\nTo={}\nDays={}".format(
                        vn,
                        arc.upstr.node_id,
                        arc.dwnstr.node_id,
                        (arc.arc_upstr_window_start, arc.arc_upstr_window_end, arc.arc_dwnstr_window_start, arc.arc_dwnstr_window_end),
                    ),
                    title=generate_edge_html(vn, arc),
                )

                self.eds.append({
                    "Vessel": vn,
                    "Next_NodeID": arc.upstr.node_id,
                    "From_NodeID": arc.dwnstr.node_id,
                    "DAYS": (arc.arc_upstr_window_start, arc.arc_upstr_window_end, arc.arc_dwnstr_window_start, arc.arc_dwnstr_window_end),
                })

            G.repulsion(node_distance=200, spring_length=200)
            if file_name:
                path = "{}/visual/" + file_name + ".html"
            else:
                path = "{}/visual/custom_poc_supernode_{}_{}.html"
            G.show(
                path.format(self.config.CASENAME, vn, v)
            )

===============================================================
