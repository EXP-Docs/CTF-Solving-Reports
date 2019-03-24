UNICODE_RANGE = 65000;
XSS_ASCII_RANGE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\"/?><';:.,|\\+=-_*&^%$#@!~`\r\n"
for (i = 0; i < UNICODE_RANGE; i++) {
    raw_ch = String.fromCharCode(i)
    low_ch = "";
    upp_ch = "";

    if (XSS_ASCII_RANGE.includes(raw_ch.toLowerCase())) {
        low_ch = raw_ch.toLowerCase();
    }

    if (XSS_ASCII_RANGE.includes(raw_ch.toUpperCase())) {
        upp_ch = raw_ch.toUpperCase();
    }

    if ((low_ch != "" || upp_ch != "") && !(XSS_ASCII_RANGE.includes(raw_ch))) {
        console.log(
            "Unicode-Idx: [" + i + "], " + 
            "Raw-Unicode: [" + raw_ch + "], " + 
            "Unicode-Hex: [\\u" + (i).toString(16) + "], " + 
            "To-LowerCase-ASCII: [" + low_ch + "], " + 
            "To-UpperCase-ASCII: [" + upp_ch + "]");
    }
}