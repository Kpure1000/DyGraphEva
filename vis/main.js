var loaded = {
}

let load_p = new Promise((resolve) => {
    d3.json("../data/dataset/synth/test.json", d => {
        resolve(d)
    })
}).then(d => {
    console.log("load success")
    loaded['data'] = d

    vis_method = new force_directed();
})
