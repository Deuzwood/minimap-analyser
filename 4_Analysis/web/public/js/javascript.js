/*
    /!\
    Req.
        - data classes , 
        - res folder (26*26 champions tiles) , 
        - Detection_Video_Results.csv from inference
*/

let data = ''
let stats = {}
let mapStyle = "default"

let mapStyleName = {
    "default" : "rift",
    "replay" : "replayRift"
}

async function init(){
    try {
        data = await csvLoader('data/Detection_Video_Results.csv')
        stats = {}
        const canvas = document.querySelector('#rift');
        const ctx = canvas.getContext('2d');
        let lastFrame = 0

        var img = new Image();
        await new Promise(r => img.onload=r, img.src='/data/minimap/'+mapStyleName[mapStyle]+'.png');
        ctx.drawImage(img, 0,0, 256 ,256);

        for (let index = 0; index < data.length; index++) {

            const champions = data[index];

            if(stats[[champions.name]] === undefined){
                stats[[champions.name]] = { 'detected' : 0}
            }
            stats[[champions.name]].detected += 1

            if(champions.frame >= lastFrame){
                var img = new Image();
                await new Promise(r => img.onload=r, img.src='/data/res/'+champions.name+'.png');
                ctx.drawImage(img, champions.center.x, champions.center.y);
            }
            
            displayStats()
        }

    } catch (err) {
        console.log(err)
    }
}

async function displayStats(){
    const championsLineStatsCode = (name, data) => `<tr>
    <td>${name}</td>
    <td>${data.detected}</td>
    <td><button class="btn btn-secondary btn-small" data-action="btnPath" data-name="${name}">See path</button></td>
  </tr>` 
  statsTableBody.innerHTML = ''
    for (const [key, value] of Object.entries(stats)) {
        if(value.detected > 20){
            statsTableBody.innerHTML += championsLineStatsCode(key,value);
        }
    }

    document.querySelectorAll('button[data-action="btnPath"]').forEach( async element => {
        element.addEventListener('click', async event => {
            await renderNew()
            await renderPath(element.getAttribute('data-name'))
            
        })
    })
      
}

async function renderNew(){
    const canvas = document.querySelector('#rift');
    const ctx = canvas.getContext('2d');

    var img = new Image();
    await new Promise(r => img.onload=r, img.src='/data/minimap/'+mapStyleName[mapStyle]+'.png');
    ctx.drawImage(img, 0,0, 256 ,256);
}

async function renderPath(champ){

    const canvas = document.querySelector('#rift');
    const ctx = canvas.getContext('2d');

    ctx.beginPath();
    let firstTime = true

    for (let index = 0; index < data.length; index++) {

        const champions = data[index];

        if(champions.name == champ || parseInt(champions.label) == champ ){
            displayChampName = champions.name

            if(firstTime){
                ctx.moveTo( champions.center.x, champions.center.y)
                console.log("here");
                firstTime = false
            }else{
                console.log("then here");
                last = champions.center
                ctx.lineTo( champions.center.x, champions.center.y)
            }

        }


    }
    var img = new Image();
    await new Promise(r => img.onload=r, img.src='/data/res/'+displayChampName+'.png');
    ctx.drawImage(img, last.x, last.y);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#00ff00';
    ctx.stroke();
}

document.querySelector('#btnMap').addEventListener('click', event => {
    if(document.querySelector('#btnMap').getAttribute('data-style') == "default"){
        document.querySelector('#btnMap').setAttribute('data-style', 'replay')
        mapStyle = "replay"
    }else{
        document.querySelector('#btnMap').setAttribute('data-style', 'default')
        mapStyle = "default"
    }
    init()
})

init()