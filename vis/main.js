
let vis_methods = []

let slices = document.getElementById("slices");
let slice = slices.getElementsByTagName("li");
cloneNode = slice[0].cloneNode(true)

let data_select = document.getElementById("data_select")
let vis_select = document.getElementById("vis_select")
let rescale_check = document.getElementById("can_rescale")

let dataset_item = [
    {
        "name": "cluster",
        "path": "../data/dataset/synth/cluster/",
    },
    {
        "name": "newcomb",
        "path": "../data/dataset/truth/newcomb/",
    },
    {
        "name": "FR",
        "path": "../data/dataset/truth/vdBunt_data/",
    },
    {
        "name": "VRND32T",
        "path": "../data/dataset/truth/vdBunt_data/",
    },
    {
        "name": "mammalia-pa",
        "path": "../data/dataset/truth/mammalia-pa/",
    },
]

let result_item = [
    {
        "name": "cluster_Frishman",
        "path": "../data/result/synth/cluster/",
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
        "name": "mammalia-pa_Frishman",
        "path": "../data/result/truth/mammalia-pa/",
    },
    {
        "name": "cluster_Aging",
        "path": "../data/result/synth/cluster/",
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
    {
        "name": "mammalia-pa_Aging",
        "path": "../data/result/truth/mammalia-pa/",
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
                vis_methods.push(new fix_layout("viser" + i))
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

let vismethod_item = [
    {
        "name": "force_directed",
        "func": fd_main,
        "data": dataset_item,
    },
    {
        "name": "positioned",
        "func": fix_main,
        "data": result_item,
    },
]

let seleter_item
let func_main

function OnSelecterChanged() {
    vis_clear()
    func_main(seleter_item[data_select.value].path, seleter_item[data_select.value].name);
}

function OnVisMethodChanged() {
    vis_clear()

    func_main = vismethod_item[vis_select.value].func;
    seleter_item = vismethod_item[vis_select.value].data;

    data_select.innerHTML=''
    for (let index = 0; index < seleter_item.length; index++) {
        newOpt = document.createElement("option")
        newOpt.text = seleter_item[index].name
        newOpt.value = index
        data_select.appendChild(newOpt)
    }

    func_main(seleter_item[data_select.value].path, seleter_item[data_select.value].name);
}

function OnRecaleChanged() {
    is_rescale = rescale_check.checked
    console.log(is_rescale)
}

function main() {
    // seleter_item = dataset_item
    // // seleter_item = result_item

    // func_main = fd_main
    // // func_main = fix_main
    
    vis_select.innerHTML=''
    for (let index = 0; index < vismethod_item.length; index++) {
        newOpt = document.createElement("option")
        newOpt.text = vismethod_item[index].name
        newOpt.value = index
        vis_select.appendChild(newOpt)
    }
    
    // func_main(seleter_item[0].path, seleter_item[0].name);
    OnVisMethodChanged()
}

main()
