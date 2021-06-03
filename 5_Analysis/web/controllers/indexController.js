exports.index = function (req, res) {
    res.render('index');
};

exports.analyse = function (req, res) {
    const data = req.params.title;
    res.render('analyse', { data: data });
};
