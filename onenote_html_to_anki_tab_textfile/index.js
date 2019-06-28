'use strict';

let fs = require('fs');
let path = require('path');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const text = fs.readFileSync(path.join(__dirname, 'Example Sentences.mht'), 'utf8');
const dom = new JSDOM(text);
const liNodes = dom.window.document.querySelectorAll("li");

function sanitize(content) {
    return content.replace(/=/g, '').replace(/\n/g, '').replace(/  /g, ' ').replace(/   /g, ' ').replace(/\<\/span\>/g,'');
}

const sentences = [];
liNodes.forEach((value) => {
    const sentence = [];
    value.childNodes.forEach((spanEle) => {
        if (!spanEle.outerHTML) { return; }

        const isBold = spanEle.outerHTML.includes('font-weight:bold');
        const segment = sanitize(spanEle.textContent);
        if (isBold) {
            sentence.push(`{{c1::${segment}}}`);
        } else {
            sentence.push(segment);
        }
        console.log(spanEle);
    });
    sentences.push(sentence.join(' ').replace(/  /g, ' '));
});

fs.writeFileSync('anki_import.txt', sentences.join('\n'));