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
