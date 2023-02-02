
let vis_methods = []

let slices = document.getElementById("slices");
let slice = slices.getElementsByTagName("li");
cloneNode = slice[0].cloneNode(true)

let data_select = document.getElementById("data_select")
let vis_select = document.getElementById("vis_select")
let rescale_check = document.getElementById("can_rescale")

nodes_out = document.getElementById('nodes_out')
nodes_out.disabled = true

function fd_main(path, filename) {
    nodes_out.style.display = 'block'
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


function sel_main(path, filename) {
    nodes_out.style.display = 'block'
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
                vis_methods.push(new select_vis("viser" + i, data_config.distance_scale))
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

        let load_count = 0
        let days_num = data_config.day_end - data_config.day_start + 1
        let cache_data = Array(days_num)

        let load_pros = []

        for (let i = 0, count = data_config.day_start; i < slice.length && count <= data_config.day_end; i++,count++) {
            let data_name = data_config.prefix + count
            const sl = slice[i];
            sl.getElementsByTagName("div")[1]
                .innerText = data_name;
            sl.getElementsByTagName("div")[0]
                .getElementsByTagName("svg")[0]
                .id = "viser" + i;
            load_pros.push(new Promise((resolve) => {
                vis_methods.push(new fix_layout("viser" + i))
                d3.json(path + data_name + ".json", d => {
                    resolve(d)
                })
            }).then(d => {
                cache_data[i] = d
            }))

        }
        Promise.all(load_pros).then(()=>{
            let nodess = []
            for (let i in cache_data) {
                nodess.push(cache_data[i].nodes)
            }
            let range = layout_normalize(nodess)
            for (let i = 0; i < days_num; i++) {
                vis_methods[i].vis(cache_data[i])
            }
        })
    })
}

function vis_clear() {
    for (let index = 0; index < vis_methods.length; index++) {
        const method = vis_methods[index];
        method.clear()
    }
    selected_nodes = []
    vis_methods = []
    slices.innerHTML = ""
    document.getElementById('txa_res').value = '[]'
}

function layout_normalize(nodess) {
    let xmin = Number.MAX_VALUE, ymin = Number.MAX_VALUE,
        xmax = Number.NEGATIVE_INFINITY, ymax = Number.NEGATIVE_INFINITY
    for (let nodes in nodess) {
        for (let n in nodess[nodes]) {
            let node = nodess[nodes][n]
            xmin = Math.min(node.x, xmin)
            ymin = Math.min(node.y, ymin)
            xmax = Math.max(node.x, xmax)
            ymax = Math.max(node.y, ymax)
        }
    }
    
    let date_center_x = (xmin + xmax) * 0.5
    let date_center_y = (ymin + ymax) * 0.5
    let data_radius = Math.max(xmax - xmin, ymax - ymin) * 0.6
    let svg_radius = Math.min(width, height) * 0.5
    
    for (let nodes in nodess) {
        for (let n in nodess[nodes]) {
            let node = nodess[nodes][n]
            node.x -= date_center_x
            node.x = node.x * svg_radius / data_radius
            node.y -= date_center_y
            node.y = node.y * svg_radius / data_radius
        }
    }
}

let vismethod_item = [
    {
        "name": "fixed_layout",
        "func": fix_main,
        "data": result_item,
    },
    {
        "name": "force_directed",
        "func": fd_main,
        "data": dataset_item,
    },
    {
        "name": "selection",
        "func": sel_main,
        "data": selected_item,
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

    nodes_out.style.display = 'none'

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

function OnSelectedNodesChange(id) {
    let index = selected_nodes.indexOf(id)
    if (index >= 0) {
        selected_nodes.splice(index, 1)
    } else {
        selected_nodes.push(id)
    }
    txa_res = document.getElementById('txa_res')
    txa_res.value = JSON.stringify(selected_nodes)
}

function OnApplyNodes() {
    txa_res = document.getElementById('txa_res')
    selected_nodes = JSON.parse(txa_res.value)
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
