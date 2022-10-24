
let vis_methods = []

let slices = document.getElementById("slices");
let slice = slices.getElementsByTagName("li");
cloneNode = slice[0].cloneNode(true)

let data_select = document.getElementById("data_select")

let dataset_item = [
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
    {
        "name": "newcomb",
        "path": "../data/dataset/truth/newcomb/",
    },
    {
        "name": "FR",
        "path": "../data/dataset/truth/vdBunt_data/",
    },
]

let result_item = [
    {
        "name": "node_add_Frishman",
        "path": "../data/result/synth/node_add/",
    },
    {
        "name": "test_Frishman",
        "path": "../data/result/synth/test/",
    },
    {
        "name": "newcomb_Frishman",
        "path": "../data/result/truth/newcomb/",
    },
    {
        "name": "FR_Frishman",
        "path": "../data/result/truth/vdBunt_data/",
    },
    {
        "name": "VRND32T_Frishman",
        "path": "../data/result/truth/vdBunt_data/",
    },
    {
        "name": "node_add_Aging",
        "path": "../data/result/synth/node_add/",
    },
    {
        "name": "test_Aging",
        "path": "../data/result/synth/test/",
    },
    {
        "name": "newcomb_Aging",
        "path": "../data/result/truth/newcomb/",
    },
    {
        "name": "FR_Aging",
        "path": "../data/result/truth/vdBunt_data/",
    },
    {
        "name": "VRND32T_Aging",
        "path": "../data/result/truth/vdBunt_data/",
    },
]

function fd_main(path, filename) {
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

function fix_main(path, filename) {
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
                vis_methods.push(new fix_layout("viser" + i, data_config.distance_scale))
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

let seleter_item
let func_main

function main() {
    // seleter_item = dataset_item
    seleter_item = result_item

    // func_main = fd_main
    func_main = fix_main
    
    for (let index = 0; index < seleter_item.length; index++) {
        newOpt = document.createElement("option")
        newOpt.text = seleter_item[index].name
        newOpt.value = index
        data_select.appendChild(newOpt)
    }

    func_main(seleter_item[0].path, seleter_item[0].name);
}

function OnSelecterChanged() {
    vis_clear()
    func_main(seleter_item[data_select.value].path, seleter_item[data_select.value].name);
}

main()
