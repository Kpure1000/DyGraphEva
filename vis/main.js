function main(path, filename) {
    d3.json(path + filename + ".json", data_config=>{
        let slices = document.getElementById("slices");

        let slice = slices.getElementsByTagName("li");

        for (let i = 0; i < data_config.days - 1; i++) {
            slices.appendChild(slice[0].cloneNode(true));
        }

        let vis_methods = []

        for (let i = 0; i < slice.length; i++) {
            let data_name = data_config.prefix + (i + 1)
            const sl = slice[i];
            sl.getElementsByTagName("div")[1]
                .innerText = data_name;
            sl.getElementsByTagName("div")[0]
                .getElementsByTagName("svg")[0]
                .id = "viser" + i;

            new Promise((resolve) => {
                vis_methods.push(new force_directed("viser" + i, data_config.distance_scale))
                d3.json(path + data_name + ".json", d => {
                    resolve(d)
                })
            }).then(d => {
                vis_methods[i].vis(d)
            })

        }
    })
    

}


// main("../data/dataset/truth/newcomb/", "newcomb");
// main("../data/dataset/synth/", "test");
main("../data/dataset/synth/node_eva/", "node_eva");