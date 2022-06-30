class force_directed {
    constructor() {
        this.nodes = loaded.data.nodes;
        this.links = loaded.data.links;

        this.simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(d => d.id))
            .force("charge", d3.forceManyBody())
            .force("x", d3.forceX())
            .force("y", d3.forceY())

        this.simulation.nodes(this.nodes)
            .on("tick", ticked)

        this.simulation.force("link").links(this.links)

        let link = svg.append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .selectAll("line")

        let node = svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")

        let get_group_color = d3.scaleOrdinal(d3.schemeCategory20)

        link = link
            .data(this.links)
            .enter()
            .append("line")

        node = node
            .data(this.nodes)
            .enter()
            .append("circle")
            .attr("r", 5)
            .attr("fill", d => get_group_color(d.group))
            .call(drag(this.simulation))
            .call(node => node.append("title").text(d => d.id))

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
