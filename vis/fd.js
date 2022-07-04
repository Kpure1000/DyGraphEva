class force_directed {
    constructor(svg_id) {
        this.svg = d3.select('#' + svg_id)
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [-width / 2, -height / 2, width, height])

    }

    vis(data) {
        let nodes = data.nodes;
        let links = data.links;

        let simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(d => d.id).strength(0.1))
            .force("charge", d3.forceManyBody().strength(-18))
            .force("x", d3.forceX())
            .force("y", d3.forceY())

        let get_group_color = d3.scaleOrdinal(d3.schemeCategory20)

        let link = this.svg.append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.5)
            .attr("stroke-width", 0.7)
            .selectAll("line")

        let node = this.svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")

        link = link
            .data(links)
            .enter()
            .append("line")

        node = node
            .data(nodes)
            .enter()
            .append("circle")
            .attr("r", 4)
            .attr("fill", d => get_group_color(d.group))
            // .attr("fill", d => get_group_color(d.block))
            .call(drag(simulation))
            .call(node => node.append("title").text(d => d.id))

        simulation.nodes(nodes)
            .on("tick", ticked)

        simulation.force("link").links(links)

        function ticked() {
            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("cx", d => d.x)
                .attr("cy", d => d.y);

        }

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
