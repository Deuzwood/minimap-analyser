async function load(file) {
    var xhr = new XMLHttpRequest();
    return new Promise(function (resolve, reject) {
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status >= 300) {
                    reject('Error ' + xhr.status);
                } else {
                    resolve(xhr.responseText);
                }
            }
        };
        xhr.open('get', file, true);
        xhr.send();
    });
}

async function csvLoader(file) {
    let csv = [];
    let data = await load(file);
    let classes = await load('/data/data_classes.txt');
    classes = classes.split('\r\n');
    data = data.split('\r\n');
    let header = data.shift();

    if (data[data.length - 1].length == 0) {
        data.pop();
    }

    header = header.split(',');
    let indexFrame = 0;
    for (let index = 0; index < data.length; index++) {
        const obj = {};
        const line = data[index].split(',');
        header.forEach((element, i) => {
            obj[[element]] = line[i];
        });
        obj.frame = indexFrame;
        obj.center = {
            x: (parseInt(obj.xmin) + parseInt(obj.xmax)) / 2,
            y: (parseInt(obj.ymin) + parseInt(obj.ymax)) / 2,
        };
        obj.name = classes[parseInt(obj.label)];

        if (parseInt(obj.confidence) != -1) {
            csv.push(obj);
        } else {
            indexFrame++;
        }
    }
    console.log(csv);
    return csv;
}
