let data_len = 15

let slices = document.getElementById("slices");

let slice = slices.getElementsByTagName("li");

for (let i = 0; i < data_len - 1; i++) {
    slices.appendChild(slice[0].cloneNode(true));
}

let vis_methods=[]

for (let i = 0; i < slice.length; i++) {
    let data_name = "newcomb_" + (i + 1)
    const sl = slice[i];
    sl.getElementsByTagName("div")[1]
        .innerText = data_name;
    sl.getElementsByTagName("div")[0]
        .getElementsByTagName("svg")[0]
        .id = "viser" + i;
            
    new Promise((resolve) => {
        vis_methods.push(new force_directed("viser" + i))
        d3.json("../data/dataset/truth/newcomb/" + data_name + ".json", d => {
            resolve(d)
        })
    }).then(d => {
        vis_methods[i].vis(d)
    })

}
