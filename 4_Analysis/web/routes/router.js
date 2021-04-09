var express = require('express');
var router = express.Router();

const indexController = require('../controllers/indexController');

router.get('/', indexController.index);

router.get('/analyse/:title', indexController.analyse);

module.exports = router;
