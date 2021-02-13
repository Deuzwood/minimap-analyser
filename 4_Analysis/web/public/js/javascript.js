import * as load from './csvLoader.js'

/*
    /!\
    Req.
        - data classes , 
        - res folder (26*26 champions tiles) , 
        - Detection_Video_Results.csv from inference
*/

let data = ''
let stats = {}
async function init(){
    try {
        data = await load.csvLoader('data/Detection_Video_Results.csv')

        const canvas = document.querySelector('#rift');
        const ctx = canvas.getContext('2d');
        let lastFrame = 0
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

init()

function displayStats(){
    const championsLineStatsCode = (name, data) => `<p>${name} , ${data.detected}</p>` 
    statsSection.innerHTML = ''
    for (const [key, value] of Object.entries(stats)) {
        if(value.detected > 20){
            statsSection.innerHTML += championsLineStatsCode(key,value);
        }

      }
      
}