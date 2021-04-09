/*
    /!\
    Req.
        - data classes , 
        - res folder (26*26 champions tiles) , 
        - Detection_Video_Results.csv from inference
*/
let greyRiftEquivalence = {
    0: 'bluebase',
    93: 'Red Jungle',
    130: 'Top Lane',
    145: 'Mid Lane',
    155: 'Bottom Lane',
    187: 'Blue Jungle',
    221: 'River',
    255: 'redbase',
};

let data = '';
let stats = {};
let RED_TEAM = [];
let BLUE_TEAM = [];
let mapStyle = 'default';

async function init() {
    try {
        data = await csvLoader(
            '/data/' + fileToLoadName + '-simple.csv' ||
                '/data/Detection_Video_Results_full.csv'
        );

        stats = await fetch('/data/' + fileToLoadName + '-simple-stats.json');
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
    const championsLineStatsCode = (name) => `<tr>
    <td width="10%"><img src="/data/tiles/${name}.png">${name}</td>
    <td>
        <button class="btn btn-outline-secondary btn-small" data-action="btnPath" data-name="${name}"><i class="bi bi-geo-alt-fill"></i></button>
        <button class="btn btn-outline-success btn-small" data-action="btnCompare" data-name="${name}"><i class="bi bi-plus"></i></button>
        <button class="btn btn-outline-warning btn-small" data-action="btnHeatMap" data-name="${name}"><i class="bi bi-thermometer-high"></i></button>
    </td>
  </tr>`;

    tbblue.innerHTML = '';
    tbred.innerHTML = '';

    for (const property in stats) {
        if (stats[property].team == 0) {
            tbblue.innerHTML += championsLineStatsCode(stats[property].name);
        } else {
            tbred.innerHTML += championsLineStatsCode(stats[property].name);
        }
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

async function renderNew() {
    const canvas = document.querySelector('#rift');
    const ctx = canvas.getContext('2d');

    var img = new Image();
    await new Promise(
        (r) => (img.onload = r),
        (img.src = '/data/minimap/' + mapStyleName[mapStyle] + '.png')
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

    for (let index = 0; index < data.length; index++) {
        const champions = data[index];

        if (champions.name == champ) {
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
    var img = new Image();
    await new Promise(
        (r) => (img.onload = r),
        (img.src = '/data/tiles/' + displayChampName + '.png')
    );
    ctx.drawImage(img, last.x, last.y);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#00ff00';
    ctx.stroke();
}

init();

var canvas = document.getElementById('gradient');
var context = canvas.getContext('2d');

var width = 256; //canvas.width;
var height = 256; //canvas.height;

var grid = [];
function init_grid() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    for (var i = 0; i < width; i++) {
        grid[i] = [];
        for (var j = 0; j < height; j++) {
            grid[i][j] = 0.0;
        }
    }
}

var radius = 5;

// from http://homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm
function _gaussian(x, y) {
    stdev = 1;
    return (
        (1.0 / Math.sqrt(2 * Math.PI * stdev)) *
        Math.exp(-(x * x + y * y) / (2 * stdev * stdev))
    );
}

// from http://homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm
function gaussian_grid(radius) {
    var _gaussian_grid = [];
    for (var x = -radius; x <= radius; x++) {
        _gaussian_grid[x + radius] = [];
        for (var y = -radius; y <= radius; y++) {
            _gaussian_grid[x + radius][y + radius] = Math.round(
                127 * _gaussian(x, y)
            );
        }
    }
    return _gaussian_grid;
}

var radius = 3;
var _gaussian_grid = gaussian_grid(radius);

function gaussian(xi, yi) {
    return _gaussian_grid[xi + radius][yi + radius];
}

var maximum = 0;
function apply_gaussian(x, y) {
    for (var xi = -radius; xi <= radius; xi++) {
        for (var yi = -radius; yi <= radius; yi++) {
            var cell_value = (grid[x + xi][y + yi] += gaussian(xi, yi));
            maximum = Math.max(cell_value, maximum);
        }
    }
}

function add_point(x, y) {
    apply_gaussian(x, y);
}

function each_row(action) {
    for (var y = 1; y <= height; y++) {
        action(y);
    }
}

function each_cell(action) {
    each_row(function (y) {
        for (var x = 1; x <= width; x++) {
            action(x, y);
        }
    });
}

function print_grid() {
    each_row(function (y) {
        console.log(grid[y].join('\t') + '\n');
    });
}
// Render grid translates our grid to the canvas. It ignores all points that have no value (=0)
// and gives a color to those who have, but this is depending on the maximum value
// TODO fix the color generation, it does not give a very smooth image
function render_grid() {
    each_cell(function (x, y) {
        var value = grid[x - 1][y - 1];
        // console.log(value);
        if (value > 0) {
            color = (value / maximum) * 255;
            context.fillStyle = 'rgba(200,' + color + ', 0, 0.5)';
            context.fillRect(x, y, 1, 1);
        }
    });
}

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
