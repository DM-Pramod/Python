
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
<!-- node.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Node Details</title>
</head>
<body>
    <table>
        <tr>
            <th>Type</th>
            <th>Node ID</th>
            <th>From</th>
            <th>To</th>
        </tr>
        <tr>
            <td id="node-type"></td>
            <td id="node-id"></td>
            <td id="node-from"></td>
            <td id="node-to"></td>
        </tr>
    </table>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const nodeData = {{ node_data | safe }};
            document.getElementById('node-type').textContent = nodeData.type;
            document.getElementById('node-id').textContent = nodeData.node_id;
            document.getElementById('node-from').textContent = nodeData.window_start;
            document.getElementById('node-to').textContent = nodeData.window_end;
        });
    </script>
</body>
</html>

=============================================
<!-- edge.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edge Details</title>
</head>
<body>
    <table>
        <tr>
            <th>Vessel</th>
            <th>Next Node ID</th>
            <th>From Node ID</th>
            <th>Days</th>
        </tr>
        <tr>
            <td id="vessel"></td>
            <td id="next-node-id"></td>
            <td id="from-node-id"></td>
            <td id="days"></td>
        </tr>
    </table>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const edgeData = {
                vessel: "{{ vessel }}",
                arc: {{ arc_data | safe }}
            };
            document.getElementById('vessel').textContent = edgeData.vessel;
            document.getElementById('next-node-id').textContent = edgeData.arc.upstr.node_id;
            document.getElementById('from-node-id').textContent = edgeData.arc.dwnstr.node_id;
            document.getElementById('days').textContent = `${edgeData.arc.arc_upstr_window_start}, ${edgeData.arc.arc_upstr_window_end}, ${edgeData.arc.arc_dwnstr_window_start}, ${edgeData.arc.arc_dwnstr_window_end}`;
        });
    </script>
</body>
</html>

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
    node_data = json.dumps({
        "type": node.type,
        "node_id": node.node_id,
        "window_start": node.window_start,
        "window_end": node.window_end
    })
    return template.render(node_data=node_data)

def generate_edge_html(vn, arc):
    template = env.get_template('edge.html')
    arc_data = json.dumps({
        "upstr": {"node_id": arc.upstr.node_id},
        "dwnstr": {"node_id": arc.dwnstr.node_id},
        "arc_upstr_window_start": arc.arc_upstr_window_start,
        "arc_upstr_window_end": arc.arc_upstr_window_end,
        "arc_dwnstr_window_start": arc.arc_dwnstr_window_start,
        "arc_dwnstr_window_end": arc.arc_dwnstr_window_end
    })
    return template.render(vessel=vn, arc_data=arc_data)

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

=======================================================================================================================================================================





<style>
    #network {
      width: 100%;
      height: 800px;
      border: 1px solid lightgray;
    }
    .tooltip-table {
      border-collapse: collapse;
      width: 100%;
    }
    .tooltip-table th, .tooltip-table td {
      border: 1px solid black;
      padding: 5px;
      text-align: left;
    }
    .tooltip-table th {
      background-color: #f2f2f2;
    }
    .tooltip {
      position: absolute;
      background-color: white;
      border: 1px solid black;
      padding: 10px;
      z-index: 1000;
    }
  </style>
<script type="text/javascript">
    var nodes = {{ nodes | safe }};
    var edges = {{ edges | safe }};
  
    var container = document.getElementById('network');
    var data = {
      nodes: new vis.DataSet(nodes),
      edges: new vis.DataSet(edges)
    };
    var options = {
      nodes: {
        shape: 'dot',
        size: 16,
        font: {
          size: 32,
          color: '#ffffff'
        },
        borderWidth: 2
      },
      edges: {
        width: 2
      },
      interaction: {
        hover: true
      },
      physics: {
        stabilization: false
      }
    };
    var network = new vis.Network(container, data, options);
  
    network.on("hoverNode", function (params) {
      var node = nodes.find(n => n.id === params.node);
      var tooltipContent = `
        <table class="tooltip-table">
          <tr><th>ID</th><td>${node.id}</td></tr>
          <tr><th>Type</th><td>${node.type}</td></tr>
          <tr><th>From</th><td>${node.From}</td></tr>
          <tr><th>To</th><td>${node.To}</td></tr>
        </table>`;
      var tooltip = document.createElement('div');
      tooltip.innerHTML = tooltipContent;
      tooltip.className = 'tooltip';
      tooltip.id = 'tooltip';
      document.body.appendChild(tooltip);
  
      document.onmousemove = function (e) {
        var x = e.clientX, y = e.clientY;
        tooltip.style.top = (y + 20) + 'px';
        tooltip.style.left = (x + 20) + 'px';
      };
    });
  
    network.on("blurNode", function (params) {
      var tooltip = document.getElementById('tooltip');
      if (tooltip) {
        tooltip.remove();
      }
      document.onmousemove = null;
    });
  
    network.on("hoverEdge", function (params) {
      var edge = edges.find(e => e.id === params.edge);
      var tooltipContent = `
        <table class="tooltip-table">
          <tr><th>Vessel</th><td>${edge.Vessel}</td></tr>
          <tr><th>Next_NodeID</th><td>${edge.Next_NodeID}</td></tr>
          <tr><th>From_NodeID</th><td>${edge.From_NodeID}</td></tr>
          <tr><th>DAYS</th><td>${edge.DAYS}</td></tr>
        </table>`;
      var tooltip = document.createElement('div');
      tooltip.innerHTML = tooltipContent;
      tooltip.className = 'tooltip';
      tooltip.id = 'tooltip';
      document.body.appendChild(tooltip);
  
      document.onmousemove = function (e) {
        var x = e.clientX, y = e.clientY;
        tooltip.style.top = (y + 20) + 'px';
        tooltip.style.left = (x + 20) + 'px';
      };
    });
  
    network.on("blurEdge", function (params) {
      var tooltip = document.getElementById('tooltip');
      if (tooltip) {
        tooltip.remove();
      }
      document.onmousemove = null;
    });
  
    // Set node colors based on type
    nodes.forEach(node => {
      switch (node.type) {
        case 'Load':
          node.color = 'red';
          break;
        case 'Discharge':
          node.color = 'purple';
          break;
        case 'Source':
          node.color = 'green';
          break;
        case 'can_in':
        case 'can_out':
          node.color = 'blue';
          break;
        default:
          node.color = 'gray';
      }
    });
  
    // Set edge colors based on properties
    edges.forEach(edge => {
      switch (edge.type) {
        case 'Type1':
          edge.color = { color: 'red' };
          break;
        case 'Type2':
          edge.color = { color: 'blue' };
          break;
        case 'Type3':
          edge.color = { color: 'green' };
          break;
        default:
          edge.color = { color: 'gray' };
      }
    });
  
    // Update the dataset with the new colors
    data.nodes.update(nodes);
    data.edges.update(edges);
  </script>
    
