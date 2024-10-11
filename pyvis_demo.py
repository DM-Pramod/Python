from pyvis.network import Network as GNetwork
import json
from jinja2 import Environment, FileSystemLoader
from config import Config 

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
                if node.type == 'term_source' :
                    type = 'source'
                elif node.type == 'term_sink':
                    type = 'sink'

                G.add_node(
                    node.node_id,
                    shape="dot",
                    label="{} Node ={}\n f_i={}\n t_i={}".format(node.type, node.node_id,node.window_start, node.window_end,),
                    color=(
                        self.config.COLOR[type]
                        if type != "out-charters"
                        else self.config.COLOR_OUT_CHARTERS[type]
                    ),
                    title=f"""
                        <table style="width:100%; border-collapse: collapse;">
                            <tr>
                                <th style="text-align: left; padding: 5px;">Type</th>
                                <th style="text-align: left; padding: 5px;">Node ID</th>
                                <th style="text-align: left; padding: 5px;">From</th>
                                <th style="text-align: left; padding: 5px;">To</th>
                            </tr>
                            <tr>
                                <td style="text-align: left; padding: 5px;">{node.type}</td>
                                <td style="text-align: left; padding: 5px;">{node.node_id}</td>
                                <td style="text-align: left; padding: 5px;">{node.window_start}</td>
                                <td style="text-align: left; padding: 5px;">{node.window_end}</td>
                            </tr>
                        </table>
                    """,
                )

                self.nds.append({"type":node.type, "id":node.node_id,"From":node.window_start, "To":node.window_end})

            for arc in self.arcs:
                G.add_edge(
                    arc.upstr.node_id,
                    arc.dwnstr.node_id,
                    label="Vessel={}\nFrom={}\nTo={}\nDays={}".format(
                        vn,
                        arc.upstr.node_id,
                        arc.dwnstr.node_id,
                        (arc.arc_upstr_window_start, arc.arc_upstr_window_end, arc.arc_dwnstr_window_start, arc.arc_dwnstr_window_end),
                        # (arc.laden_days,arc.ballast_days,arc.waiting_days,arc.port_days)
                    ),
                    title=f"""
                        <table style="width:100%; border-collapse: collapse;">
                            <tr>
                                <th style="text-align: left; padding: 5px;">Vessel</th>
                                <th style="text-align: left; padding: 5px;">Next Node ID</th>
                                <th style="text-align: left; padding: 5px;">From Node ID</th>
                                <th style="text-align: left; padding: 5px;">Days</th>
                            </tr>
                            <tr>
                                <td style="text-align: left; padding: 5px;">{vn}</td>
                                <td style="text-align: left; padding: 5px;">{arc.upstr.node_id}</td>
                                <td style="text-align: left; padding: 5px;">{arc.dwnstr.node_id}</td>
                                <td style="text-align: left; padding: 5px;">{arc.arc_upstr_window_start}, {arc.arc_upstr_window_end}, {arc.arc_dwnstr_window_start}, {arc.arc_dwnstr_window_end}</td>
                            </tr>
                        </table>
                    """,
                )
            #******************************
                self.eds.append({"Vessel":vn,
                        "Next_NodeID":arc.upstr.node_id,
                        "From_NodeID":arc.dwnstr.node_id,
                        "DAYS":(arc.arc_upstr_window_start, arc.arc_upstr_window_end, arc.arc_dwnstr_window_start, arc.arc_dwnstr_window_end)},)
            # print("**************")


            G.repulsion(node_distance=200, spring_length=200)
            if file_name:
                path = "{}/visual/" + file_name + ".html"
            else:
                path = "{}/visual/custom_poc_supernode_{}_{}.html"
            G.show(
                path.format(self.config.CASENAME, vn, v)
            )
