/*
    /!\
    Req.
        - data classes , 
        - res folder (26*26 champions tiles) , 
        - Detection_Video_Results.csv from inference
*/
let greyRiftEquivalence = {
    0: 'Red Base',
    93: 'Red Jungle',
    130: 'Top Lane',
    145: 'Mid Lane',
    155: 'Bottom Lane',
    187: 'Blue Jungle',
    221: 'River',
    255: 'Blue Base',
};

let data = '';
let stats = {};
let RED_TEAM = [];
let BLUE_TEAM = [];
let mapStyle = 'default';

async function init() {
    try {
        data = await csvLoader(
            '/data/' + fileToLoadName + '.csv' ||
                '/data/Detection_Video_Results_full.csv'
        );

        stats = await fetch('/data/' + fileToLoadName + '-stats.json');
        stats = await stats.json();

        const canvas = document.querySelector('#rift');
        const ctx = canvas.getContext('2d');

        //change max of FrameInptu
        frameInput.setAttribute('max', countFrame());

        for (const property in stats) {
            if (stats[property].team == 0) {
                BLUE_TEAM.push(stats[property]);
            } else {
                RED_TEAM.push(stats[property]);
            }
        }

        var img = new Image();
        await new Promise(
            (r) => (img.onload = r),
            (img.src = '/data/minimap/rift.png')
        );
        ctx.drawImage(img, 0, 0, 256, 256);

        await displayStats();
    } catch (err) {
        console.log(err);
    }
}

function buildCleanBoard() {
    const blueLine = (name, position) => `
    <td width="10%"><img src="/data/tiles/${name}.png"></td>
    <td>${position}</td>
    `;

    const redLine = (name, position) => `
    <td>${position}</td>
    <td width="10%"><img src="/data/tiles/${name}.png"></td>
    `;

    for (i = 0; i < 5; i++)
        for (let index = 0; index < 5; index++) {
            tb.innerHTML += line(blueLine(BLUE_TEAM[i]), redLine(RED_TEAM[i]));
        }
}

function countFrame() {
    return data[data.length - 1].frame;
}

function renderGradient(name) {
    init_grid();
    for (let i = 0; i < data.length - 1; i++) {
        if (data[i].name == name) {
            add_point(parseInt(data[i].center.x), parseInt(data[i].center.y));
        }
    }
    render_grid();
}

async function displayStats() {
    const championsLineStatsCode = (stats) => `<tr>
    <td width="10%"><img src="/data/tiles/${stats.name}.png"></td>
    <td width="10%">${stats.mainPosition}</td>
    <td>
        <button class="btn btn-outline-secondary btn-small" data-action="btnPath" data-name="${stats.name}"><i class="bi bi-geo-alt-fill"></i></button>
        <button class="btn btn-outline-success btn-small" data-action="btnCompare" data-name="${stats.name}"><i class="bi bi-plus"></i></button>
        <button class="btn btn-outline-warning btn-small" data-action="btnHeatMap" data-name="${stats.name}"><i class="bi bi-thermometer-high"></i></button>
    </td>
  </tr>`;

    tbblue.innerHTML = '';
    tbred.innerHTML = '';

    for (const property in stats) {
        console.log(stats[property]);
        if (stats[property].team == 0) {
            tbblue.innerHTML += championsLineStatsCode(stats[property]);
        } else {
            tbred.innerHTML += championsLineStatsCode(stats[property]);
        }
        addToChart(stats[property]);
    }

    document
        .querySelectorAll('button[data-action="btnPath"]')
        .forEach(async (element) => {
            element.addEventListener('click', async (event) => {
                await renderNew();
                await renderPath(element.getAttribute('data-name'));
            });
        });

    document
        .querySelectorAll('button[data-action="btnCompare"]')
        .forEach(async (element) => {
            element.addEventListener('click', async (event) => {
                await renderPath(element.getAttribute('data-name'));
            });
        });

    document
        .querySelectorAll('button[data-action="btnHeatMap"]')
        .forEach((element) => {
            element.addEventListener('click', async (event) => {
                renderGradient(element.getAttribute('data-name'));
            });
        });
}

async function getColor(name = 'Annie') {
    var img = new Image();

    await new Promise(
        (r) => (img.onload = r),
        (img.src = `/data/tiles/${name}.png`)
    );

    var colorThief = new ColorThief();
    var color = colorThief.getColor(img);
    return color;
}

async function renderNew() {
    const canvas = document.querySelector('#rift');
    const ctx = canvas.getContext('2d');

    var img = new Image();
    await new Promise(
        (r) => (img.onload = r),
        (img.src = '/data/minimap/rift.png')
    );
    ctx.drawImage(img, 0, 0, 256, 256);
}

async function renderPath(champ) {
    const canvas = document.querySelector('#rift');
    const ctx = canvas.getContext('2d');

    ctx.beginPath();
    let firstTime = true;
    let displayChampName = 'Annie';
    let last = {};

    let clr = await getColor(champ);
    let currentFrame = parseInt(frameInput.value);

    for (let index = 0; index < data.length; index++) {
        const champions = data[index];

        if (
            champions.name == champ &&
            champions.frame <= currentFrame &&
            champions.frame > currentFrame - 10 * 60
        ) {
            displayChampName = champions.name;

            if (firstTime) {
                ctx.moveTo(champions.center.x, champions.center.y);
                firstTime = false;
            } else {
                last = {
                    x: parseInt(champions.xmin),
                    y: parseInt(champions.ymin),
                };
                ctx.lineTo(
                    parseInt(champions.center.x),
                    parseInt(champions.center.y)
                );
            }
        }
    }
    ctx.lineWidth = 2;
    ctx.strokeStyle = `rgb(${clr})`;
    ctx.stroke();

    var img = new Image();
    await new Promise(
        (r) => (img.onload = r),
        (img.src = '/data/tiles/' + displayChampName + '.png')
    );
    ctx.drawImage(img, last.x, last.y);
}

function positionToRepartition(obj) {
    let sum = 0;
    for (const property in obj.position) {
        sum += obj.position[property];
    }

    obj.positionRepartition = {
        'Red Base': 0,
        'Red Jungle': 0,
        'Top Lane': 0,
        'Mid Lane': 0,
        'Bottom Lane': 0,
        'Blue Jungle': 0,
        River: 0,
        'Blue Base': 0,
    };
    percent = [];
    for (const property in obj.position) {
        percent.push(obj.position[property] / sum);
    }
    let index = 0;
    for (const property in obj.positionRepartition) {
        obj.positionRepartition[property] = percent[index];
        index++;
    }
}

init();

/* range */

frameInput.addEventListener('change', async (event) => {
    await renderNew();
    for (let index = 0; index < data.length; index++) {
        const champions = data[index];
        const canvas = document.querySelector('#rift');
        const ctx = canvas.getContext('2d');

        if (champions.frame == frameInput.value) {
            var img = new Image();
            await new Promise(
                (r) => (img.onload = r),
                (img.src = '/data/tiles/' + champions.name + '.png')
            );
            ctx.drawImage(
                img,
                parseInt(champions.xmin),
                parseInt(champions.ymin)
            );
        }
    }
});

var tooltip = new bootstrap.Tooltip(frameInput);

frameInput.addEventListener('input', (event) => {
    var title = fromFrameToTime(parseInt(frameInput.value));

    frameInput.setAttribute('title', title);
    tooltip._fixTitle();
    tooltip.show();
});

/* range utils */

function fromFrameToTime(frame) {
    const FPS = 10; // TODO
    return (frame / FPS).toString().toHHMMSS();
}

String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10);
    var hours = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - hours * 3600) / 60);
    var seconds = sec_num - hours * 3600 - minutes * 60;

    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }
    if (seconds < 10) {
        seconds = '0' + seconds;
    }
    return hours + ':' + minutes + ':' + seconds;
};

var chartData = {
    labels: [
        'Red Base',
        'Red Jungle',
        'Top Lane',
        'Mid Lane',
        'Bottom Lane',
        'Blue Jungle',
        'River',
        'Blue Base',
    ],
    datasets: [],
};

var ctx = document.getElementById('myChart');
var myChart = new Chart(ctx, {
    type: 'radar',
    data: chartData,
    options: {
        elements: {
            line: {
                borderWidth: 3,
            },
        },
    },
});

async function addToChart(champ) {
    positionToRepartition(champ);
    let arr = [];
    for (const property in champ.positionRepartition) {
        arr.push(champ.positionRepartition[property]);
    }
    console.log(arr);
    let clr = await getColor(champ.name);
    let strClr = `rgb(${clr})`;
    let strClra = `rgb(${clr},0.2)`;
    chartData.datasets.push({
        label: champ.name,
        data: arr,
        fill: true,
        backgroundColor: strClra,
        borderColor: strClr,
        pointBackgroundColor: strClr,
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: strClr,
        hidden: true,
    });
    myChart.update();
}
