
let vis_methods = []

let slices = document.getElementById("slices");
let slice = slices.getElementsByTagName("li");
cloneNode = slice[0].cloneNode(true)

let data_select = document.getElementById("data_select")

let dataset_item = [
    {
        "name": "newcomb",
        "path": "../data/dataset/truth/newcomb/",
    },
    {
        "name": "test",
        "path": "../data/dataset/synth/test0/",
    },
    {
        "name": "node_eva",
        "path": "../data/dataset/synth/node_eva/",
    },
    {
        "name": "node_add",
        "path": "../data/dataset/synth/node_add/",
    },
    {
        "name": "edge_eva",
        "path": "../data/dataset/synth/edge_eva/",
    },
    {
        "name": "cube",
        "path": "../data/dataset/synth/cube/",
    },
]

main(dataset_item[0].path, dataset_item[0].name);

function main(path, filename) {
    vis_clear()
    d3.json(path + filename + ".json", data_config => {
        for (let i = data_config.day_start; i < data_config.day_end + 1; i++) {
            slices.appendChild(cloneNode.cloneNode(true));
        }

        for (let i = 0, count = data_config.day_start; i < slice.length && count <= data_config.day_end; i++,count++) {
            let data_name = data_config.prefix + count
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

function vis_clear() {
    for (let index = 0; index < vis_methods.length; index++) {
        const method = vis_methods[index];
        method.clear()
    }
    vis_methods = []
    slices.innerHTML = ""
}


for (let index = 0; index < dataset_item.length; index++) {
    newOpt = document.createElement("option")
    newOpt.text = dataset_item[index].name
    newOpt.value = index
    data_select.appendChild(newOpt)
}

function OnDatasetChanged() {
    vis_clear()
    main(dataset_item[data_select.value].path, dataset_item[data_select.value].name);
}
