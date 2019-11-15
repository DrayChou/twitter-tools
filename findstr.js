var search_word = [
    "@"
];
var file_ls = [
    "./tweet.js",
    // "./tweet-part1.js",
    // "./tweet-part2.js",
];
var id_ls = [];

var csv_tweets = "tweets";
var csv_tweets_del = "tweets_del";
var csv_ids = "ids";
var csv_ids_del = "ids_del";
var fs = require("fs");
if (fs.existsSync(csv_tweets)) {
    fs.unlinkSync(csv_tweets);
}
if (fs.existsSync(csv_ids)) {
    fs.unlinkSync(csv_ids);
}

var log_into_csv = function(row) {
    if (!row || !row.hasOwnProperty("id_str")) {
        console.log('log_into_csv', "row", 'id_str', 'error');
        return false;
    }

    var id_str = row.id_str;
    // fs.appendFileSync(csv_ids + ".csv", "\"" + id_str + "\"," + "\n", function() {});

    var full_text = row.full_text.replace(/\n/g, '<br>');
    var date = new Date(row.created_at);
    var Y = date.getFullYear() + '-';
    var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
    var D = date.getDate() + ' ';
    var h = date.getHours() + ':';
    var m = date.getMinutes() + ':';
    var s = date.getSeconds();
    var create_str = Y + M + D + h + m + s;
    // fs.appendFileSync(csv_tweets + ".csv", id_str + "," + date.getTime() + "," + create_str + ",\"" + full_text + "\"" + "\n", function() {});

    for (var w in search_word) {
        if (!search_word.hasOwnProperty(w)) {
            break;
        }
        var word = search_word[w];
        if (row.full_text.search(word) >= 0) {
            id_ls.push(row.id_str);
            // console.log(row.id_str, ",", row.full_text);
            fs.appendFileSync(csv_tweets_del + "_" + word + ".csv", id_str + "," + date.getTime() + "," + create_str + ",\"" + full_text + "\"" + "\n", function() {});
            fs.appendFileSync(csv_ids_del + "_" + word + ".csv", "\"" + id_str + "\"," + "\n", function() {});
        }
    }
};

var tweets = {};
for (var fid in file_ls) {
    if (!file_ls.hasOwnProperty(fid)) {
        break;
    }

    var fname = file_ls[fid];
    tweets[fname] = require(fname);
    console.log(fname, tweets[fname].length);

    for (var i in tweets[fname]) {
        if (!tweets[fname].hasOwnProperty(i)) {
            console.log(fname, "tweets", i, 'error');
            break;
        }

        var row = tweets[fname][i];
        log_into_csv(row);
    }
}