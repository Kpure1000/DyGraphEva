
class force_directed {
    constructor(svg_id, distance_scale) {
        this.svg = d3.select('#' + svg_id)
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [-width / 2, -height / 2, width, height])
        this.distance_scale = distance_scale;
    }

    clear()
    {
        this.svg.selectAll("*").remove()
    }
    
    vis(data) {
        let nodes = data.nodes;
        let links = data.links;
        let maxweight = 0
        for (let index = 0; index < links.length; index++) {
            let w = links[index].weight
            if (w > maxweight) maxweight = w
        }

        let simulation = d3.forceSimulation()
            .force("link",
                d3.forceLink()
                    .id(d => d.id)
                    .distance(d => {
                        return d.weight == null ? 30 : // 30 is d3 default
                            (this.distance_scale ? this.distance_scale / (d.weight) : 1.0 / d.weight); 
                    })
                    // .strength(0.1)
                )
            .force("charge", 
                d3.forceManyBody()
                    .strength(-78)
                    .distanceMin(1)
                    .distanceMax(199))
            .force("x", d3.forceX())
            .force("y", d3.forceY())
    
        simulation.nodes(nodes)
            .on("tick", ticked)

        simulation.force("link").links(links)

        let get_group_color = d3.scaleOrdinal(d3.schemeCategory20)

        let link = this.svg.append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 1.9)
            .selectAll("line")

        let node = this.svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.8)
            .selectAll("circle")

        let title = this.svg.append("g")
            .attr("font-size","5pt")
            .attr("fill", "#fff")
            .attr("style", "user-select: none;")
            .style("font-weight", "bold")
            .style("text-anchor", "middle")
            .selectAll("text")
        
        title = title
            .data(nodes)
            .enter()
            .append("text")
            .attr("x",d=>d.x)
            .attr("y",d=>d.y)
            .attr("dy", 3)
            .text(d=>d.id)
            .on("click", function(d){
                selected_node_id = d.id;
            })
            // .call(drag(simulation))

        link = link
            .data(links)
            .enter()
            .append("line")
            .call(link => link.append("title").text(d => "(" + d.source.id + ", " + d.target.id + "), w: " + d.weight))

        node = node
            .data(nodes)
            .enter()
            .append("circle")
            .attr("fill", d => get_group_color(d.group))
            .on("click", function(d){
                selected_node_id = d.id;
            })
            // .call(drag(simulation))

        let scale = 1.0
        let translate = { 'x': 0.0, 'y': 0.0 }

        this.svg.call(d3.zoom()
            .extent([[0, 0], [width, height]])
            .scaleExtent([0.5, 6])
            .on('zoom', () => {
                if (is_rescale == true) {
                    scale = d3.event.transform.k
                    translate.x = d3.event.transform.x
                    translate.y = d3.event.transform.y
                }
            })
        )

        function ticked() {
            title.attr("x",d=>d.x * scale + translate.x)
                .attr("y",d=>d.y * scale + translate.y)
    
            link.attr("x1", d => d.source.x * scale + translate.x)
                .attr("y1", d => d.source.y * scale + translate.y)
                .attr("x2", d => d.target.x * scale + translate.x)
                .attr("y2", d => d.target.y * scale + translate.y);

            node.attr("cx", d => d.x * scale + translate.x)
                .attr("cy", d => d.y * scale + translate.y)
                .attr("fill", (d)=>{
                    if (d.id == selected_node_id) return "#f00";
                    return get_group_color(d.group);
                })
                .attr("r", (d)=>{
                    if (d.id == selected_node_id) return 7.7;
                    return 6.5;
                })

        }
        simulation.alphaTarget(0.001)
        function drag(simulation) {
            function dragstarted(event) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                event.fx = event.x;
                event.fy = event.y;
            }
            function dragged(event) {
                event.fx = d3.event.x;
                event.fy = d3.event.y;
            }
            function dragended(event) {
                if (!event.active) simulation.alphaTarget(0);
                event.fx = null;
                event.fy = null;
            }

            return d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
        }
    }

}
