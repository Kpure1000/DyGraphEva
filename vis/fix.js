
// let selected_node_id = -1

class fix_layout {
    constructor(svg_id, distance_scale) {
        this.svg = d3.select('#' + svg_id)
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [-width / 2, -height / 2, width, height])
        this.distance_scale = 200//distance_scale * 1;
    }

    clear()
    {
        this.svg.selectAll("*").remove()
    }
    
    vis(data) {
        let nodes = data.nodes;
        let links = data.links;

        // ndoes list to dict and normalize nodes
        let nodes_dict = {}
        let xmin = Number.MAX_VALUE, ymin = Number.MAX_VALUE, 
            xmax = Number.MIN_VALUE, ymax = Number.MIN_VALUE
        for (let n in nodes) {
            nodes_dict[nodes[n].id] = nodes[n]
            xmin = Math.min(nodes[n].x, xmin)
            ymin = Math.min(nodes[n].y, ymin)
            xmax = Math.max(nodes[n].x, xmax)
            ymax = Math.max(nodes[n].y, ymax)
        }
        let date_center_x = (xmin + xmax) * 0.5
        let date_center_y = (ymin + ymax) * 0.5
        let data_radius = Math.sqrt(Math.pow((xmax - xmin), 2) +
            Math.pow((ymax - ymin), 2)) * 0.6
    
        for (let n in nodes) {
            nodes[n].x -= date_center_x 
            nodes[n].x /= data_radius
            nodes[n].y -= date_center_y
            nodes[n].y /= data_radius
        }

        let maxweight = 0
        for (let index = 0; index < links.length; index++) {
            let w = links[index].weight
            if (w > maxweight) maxweight = w
        }

        let get_group_color = d3.scaleOrdinal(d3.schemeCategory20)

        let link = this.svg.append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 1.9)
            .selectAll("line")

        let node = this.svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")

        // let title = this.svg.append("g")
        //     .attr("font-size","3pt")
        //     .attr("fill", "#fff")
        //     .attr("style", "user-select: none;")
        //     .style("font-weight", "bold")
        //     .style("text-anchor", "middle")
        //     .selectAll("text")
        
        // title = title
        //     .data(nodes)
        //     .enter()
        //     .append("text")
        //     .attr("x",d=>d.x * this.distance_scale)
        //     .attr("y",d=>d.y * this.distance_scale)
        //     .attr("dy", 2)
        //     .text(d=>d.id)
        //     .on("click", function(d){
        //         selected_node_id = d.id;
        //     })
        //     .attr("x",d=>d.x * this.distance_scale)
        //     .attr("y",d=>d.y * this.distance_scale)

        link = link
            .data(links)
            .enter()
            .append("line")
            .call(link => link.append("title").text(d => d.weight))
            .attr("x1", d => nodes_dict[d.source].x * this.distance_scale)
            .attr("y1", d => nodes_dict[d.source].y * this.distance_scale)
            .attr("x2", d => nodes_dict[d.target].x * this.distance_scale)
            .attr("y2", d => nodes_dict[d.target].y * this.distance_scale)

        node = node
            .data(nodes)
            .enter()
            .append("circle")
            .call(node => node.append("title").text(d => d.id))
            .attr("fill", d => get_group_color(d.group))
            .on("click", function(d){
                selected_node_id = d.id;
            })
            .attr("cx", d => d.x * this.distance_scale)
            .attr("cy", d => d.y * this.distance_scale)
            .attr("fill", (d)=>{
                if (d.id == selected_node_id) return "#f00";
                return get_group_color(d.group);
            })
            .attr("r", (d)=>{
                if (d.id == selected_node_id) return 4.75;
                return 4;
            })

            setInterval(()=>{
                this.svg.selectAll('circle').attr("fill", (d) => {
                    if (d.id == selected_node_id) return "#f00";
                    return get_group_color(d.group);
                }).attr("r", (d) => {
                    if (d.id == selected_node_id) return 4.75;
                    return 4;
                })
            }, 16)

    }

}
