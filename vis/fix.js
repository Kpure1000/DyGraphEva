
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
        
        for (let n in nodes) {
            let node = nodes[n]
            nodes_dict[nodes[n].id] = node
        }

        let maxweight = 0
        for (let index = 0; index < links.length; index++) {
            let w = links[index].weight
            if (w > maxweight) maxweight = w
        }

        // let get_group_color = d3.scaleOrdinal(d3.schemeCategory20)
        let get_group_color = ()=>{return "#E6E6E7"}

        let link = this.svg.append("g")
            .attr("stroke", "#E6E7E7")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 1.9)
            .selectAll("line")

        let node = this.svg.append("g")
            .attr("stroke", "#9FA0A0")
            .attr("stroke-width", 1.5)
            .selectAll("circle")

        let title = this.svg.append("g")
            .attr("font-size","3pt")
            .attr("fill", "#ccc")
            .attr("style", "user-select: none;")
            .style("font-weight", "bold")
            .style("text-anchor", "middle")
            .selectAll("text")
        
        title = title
            .data(nodes)
            .enter()
            .append("text")
            .text(d=>d.id)
            .call(title => title.append("title").text(d => d.id + ', group: ' + d.group))
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
                // return 5.64;
                return 4.2;
            // return 4.75;
            return 3.15;
        }

        node = node
            .data(nodes)
            .enter()
            .append("circle")
            .attr("fill", d => get_group_color(d.group))
            .on("click", function(d){
                selected_node_id = d.id;
            })
            .call(node => node.append("title").text(d => d.id + ', group: ' + d.group))
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
