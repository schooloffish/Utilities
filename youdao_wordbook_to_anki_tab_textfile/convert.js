'use strict';

let fs = require('fs');
let path = require('path');
let _ = require('lodash');
let parseString = require('xml2js').parseString;

let xmlString = fs.readFileSync(path.join(__dirname, 'youdao.xml'), 'utf8');
parseString(xmlString, { explicitArray: false }, (err, result) => {
    let promiseTasks = [];
    let tempArray = [];
    for (const phrase of result.wordbook.item) {
        _.isString(phrase.phonetic) || (phrase.phonetic = '');
        _.isString(phrase.trans) || (phrase.trans = '');
        let word = phrase.word.replace(/'/g, '`');
        let phonetic = phrase.phonetic.replace(/'/g, '`');
        let definition = phrase.trans.replace(/\r\n/g, '');
        let front = `${word} ${phonetic}`;
        let back = definition;
        tempArray.push(front + '\t' + back);
        if (tempArray.length === 300) {
            fs.appendFileSync('123.txt', '\n' + tempArray.join('\n'));
            tempArray.length = 0;
        }
    }
    fs.appendFileSync('123.txt', '\n' + tempArray.join('\n'));
});
