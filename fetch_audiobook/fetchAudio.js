const fs = require('fs');
const https = require('https');
const http = require('http');
const axios = require('axios');
const iconv = require("iconv-lite");
const listUrl = 'https://ting55.com/book/13698';
const baseUrl = 'https://ting55.com';

function getAudioSrc(source) {
    try {
        let src;
        const match = source.match(/mp3:"http.+?"/);
        if (match && match[0]) {
            src = match[0].match(/http.+?(?=")/)[0];
        } else {
            src = source.match(/m4a:"http.+?"/)[0].match(/http.+?(?=")/)[0];
        }
        return src;
    } catch (err) {
        console.log('cannot get src url of audio, error: ' + JSON.stringify(err));
        console.log(source);
    }
}

async function getHtml(url) {
    const res = await axios.get(url, { responseType: 'arraybuffer' });
    return iconv.decode(res.data, 'utf8');
}

function download(src, filename) {
    const httpEngine = src.startsWith('https') ? https : http;
    const file = fs.createWriteStream(filename);
    const request = httpEngine.get(src, function (response) {
        response.pipe(file);
    });
}

function wait(time) {
    return new Promise((resolve, reject) => {
        setTimeout(() => { resolve() }, time);
    });
}

(async () => {
    console.log(`analyzing...`);
    const mainHtml = await getHtml(listUrl);
    const playListString = mainHtml.match(/class="plist".+?div/)[0];

    const matches = playListString.match(/(?<=href=")\/book.+?(?=">)/g);
    console.log(`find ${matches} audios`);
    const urls = matches.map((i) => {
        let title = i.split('-').pop();
        while (title.length < 3) {
            title = '0' + title;
        }
        return { title: title + '.mp3', url: baseUrl + i };
    });
    for (let i = 0; i < urls.length; i++) {
        const urlItem = urls[i];
        try {
            const html = await getHtml(urlItem.url);
            urlItem.src = getAudioSrc(html);
            console.log(`title: ${urlItem.title}, src:${urlItem.src}`);
            if (urlItem.src) {
                download(urlItem.src, urlItem.title);
                await wait(4000);
            }
        }
        catch (err) {
            console.log('fetch failed, ' + urlItem.title);
            console.log(err);
        }
    }

    console.log(urls.map(i => i.src).join('\n'));
})();