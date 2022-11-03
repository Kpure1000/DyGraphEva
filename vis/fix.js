
// let selected_node_id = -1

class fix_layout {
    constructor(svg_id) {
        this.svg = d3.select('#' + svg_id)
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [-width / 2, -height / 2, width, height])
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
            xmax = Number.NEGATIVE_INFINITY, ymax = Number.NEGATIVE_INFINITY
        for (let n in nodes) {
            let node = nodes[n]
            nodes_dict[nodes[n].id] = node
            xmin = Math.min(node.x, xmin)
            ymin = Math.min(node.y, ymin)
            xmax = Math.max(node.x, xmax)
            ymax = Math.max(node.y, ymax)
        }
        let date_center_x = (xmin + xmax) * 0.5
        let date_center_y = (ymin + ymax) * 0.5
        // let data_radius = Math.sqrt(Math.pow((xmax - xmin), 2) + Math.pow((ymax - ymin), 2)) * 0.6
        let data_radius = Math.max(xmax - xmin, ymax - ymin) * 0.6
        let svg_radius = Math.min(width, height) * 0.5

        for (let n in nodes) {
            let node = nodes[n]
            node.x -= date_center_x 
            node.x = node.x * svg_radius / data_radius
            node.y -= date_center_y
            node.y = node.y * svg_radius / data_radius
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

        let title = this.svg.append("g")
            .attr("font-size","3pt")
            .attr("fill", "#fff")
            .attr("style", "user-select: none;")
            .style("font-weight", "bold")
            .style("text-anchor", "middle")
            .selectAll("text")
        
        title = title
            .data(nodes)
            .enter()
            .append("text")
            .call(title => title.append("title").text(d => d.id))
            .text(d=>d.id)
            .on("click", function(d){
                selected_node_id = d.id;
            })
            .attr("x",d=>d.x)
            .attr("y",d=>d.y)
            .attr("dy", 2)
            .attr("x",d=>d.x)
            .attr("y",d=>d.y)

        link = link
            .data(links)
            .enter()
            .append("line")
            .call(link => link.append("title").text(d => "(" + d.source + ", " + d.target + "), w: " + d.weight))
            .attr("x1", d => nodes_dict[d.source].x)
            .attr("y1", d => nodes_dict[d.source].y)
            .attr("x2", d => nodes_dict[d.target].x)
            .attr("y2", d => nodes_dict[d.target].y)

        let selected_fill = d => {
            if (d.id == selected_node_id)
                return "#f00";
            return get_group_color(d.group);
        }
        let selected_size = d => {
            if (d.id == selected_node_id)
                return 5.64;
            return 4.75;
        }

        node = node
            .data(nodes)
            .enter()
            .append("circle")
            .attr("fill", d => get_group_color(d.group))
            .on("click", function(d){
                selected_node_id = d.id;
            })
            .call(node => node.append("title").text(d => d.id))
            .attr("cx", d => d.x)
            .attr("cy", d => d.y)
            .attr("fill", selected_fill)
            .attr("r", selected_size)

        let scale = 1.0
        let translate = { 'x': 0.0, 'y': 0.0 }

        this.svg.call(d3.zoom()
            .extent([[0, 0], [width, height]])
            .scaleExtent([0.5, 6])
            .on('zoom', () => {
                if (is_rescale) {
                    scale = d3.event.transform.k
                    translate.x = d3.event.transform.x
                    translate.y = d3.event.transform.y
                }
            })
        )

        setInterval(() => {
            this.svg
                .selectAll('circle')
                .attr("fill", selected_fill)
                .attr("r", selected_size)

            title
                .attr("x", d => d.x * scale + translate.x)
                .attr("y", d => d.y * scale + translate.y)

            link
                .attr("x1", d => nodes_dict[d.source].x * scale + translate.x)
                .attr("y1", d => nodes_dict[d.source].y * scale + translate.y)
                .attr("x2", d => nodes_dict[d.target].x * scale + translate.x)
                .attr("y2", d => nodes_dict[d.target].y * scale + translate.y)

            node
                .attr("cx", d => d.x * scale + translate.x)
                .attr("cy", d => d.y * scale + translate.y)


        }, 16)

    }

}
