var md5 = require("md5");

function getGarbledString(originalString){
    function transformStringToUint8Array(str) {
      let pairs = [];
      for (let i = 0; i < str.length; i += 2) {
        pairs.push(str.slice(i, i + 2));
      }
      let values = pairs.map(pair => parseInt(pair, 16));
      let uint8Array = new Uint8Array(16);
      for (let i = 0; i < 16; i++) {
        uint8Array[i] = values[i];
      }
      return uint8Array;
    }
    let md5String = md5(originalString);
    let uint8Array = transformStringToUint8Array(md5String);
    md5_string = md5(uint8Array);
    uint8Array = transformStringToUint8Array(md5_string);
    let fixedString1 = "" + parseInt(new Date().getTime().toString()) / 1000;
    let fixedString2 = "536919696";
    array1 = [
        64,
        0.00390625,
        1,
        12,
        uint8Array[14],
        uint8Array[15],
        69,
        63,
        17,
        180,
        (fixedString1 >> 24) & 24,
        (fixedString1 >> 16) & 24,
        (fixedString1 >> 8) & 24,
        (fixedString1 >> 0) & 24,
        119,
        214,
        252,
        211,
    ]
    push_num = array1.reduce(function(a, b) { return a ^ b; });
    array1.push(push_num);
    array2 = [array1[0], array1[2], array1[4], array1[6], array1[8], array1[10], array1[12], array1[14], array1[16], array1[18], array1[1], array1[3], array1[5], array1[7], array1[9], array1[11], array1[13], array1[15], array1[17]]
    // array2 = [64,1,88,69,17,103,41,119,252,145,0.00390625,12,208,63,180,142,197,214,211]
    function _0x2f2740(a, c, e, b, d, f, t, n, o, i, r, _, x, u, s, l, v, h, g) {
        let w = new Uint8Array(19);
        return w[0] = a,
        w[1] = r,
        w[2] = c,
        w[3] = _,
        w[4] = e,
        w[5] = x,
        w[6] = b,
        w[7] = u,
        w[8] = d,
        w[9] = s,
        w[10] = f,
        w[11] = l,
        w[12] = t,
        w[13] = v,
        w[14] = n,
        w[15] = h,
        w[16] = o,
        w[17] = g,
        w[18] = i,
        String.fromCharCode.apply(null, w);
    }
    array2 = _0x2f2740.apply(null, array2)
    function _0x46fa4c(a, c) {
        let e, b = [], d = 0, f = "";
        for (let a = 0; a < 256; a++) {
            b[a] = a;
        }
        for (let c = 0; c < 256; c++) {
            d = (d + b[c] + a.charCodeAt(c % a.length)) % 256,
            e = b[c],
            b[c] = b[d],
            b[d] = e;
        }
        let t = 0;
        d = 0;
        for (let a = 0; a < c.length; a++) {
            t = (t + 1) % 256,
            d = (d + b[t]) % 256,
            e = b[t],
            b[t] = b[d],
            b[d] = e,
            f += String.fromCharCode(c.charCodeAt(a) ^ b[(b[t] + b[d]) % 256]);
        }
        return f;
    }
    ans = _0x46fa4c.apply(null, ['ÿ', array2])
    ans = '\u0002ÿ' + ans
    return ans;
}


function getXBogus(originalString){
    let short_str = 'Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe='
    var garbledString = getGarbledString(originalString);
    var XBogus = "";
    for (var i = 0; i <= 20; i += 3) {
        var charCodeAtNum0 = garbledString.charCodeAt(i);
        var charCodeAtNum1 = garbledString.charCodeAt(i + 1);
        var charCodeAtNum2 = garbledString.charCodeAt(i + 2);
        var baseNum = charCodeAtNum2 | charCodeAtNum1 << 8 | charCodeAtNum0 << 16;
        var str1 = short_str[(baseNum & 16515072) >> 18];
        var str2 = short_str[(baseNum & 258048) >> 12];
        var str3 = short_str[(baseNum & 4032) >> 6];
        var str4 = short_str[baseNum & 63];
        XBogus += str1 + str2 + str3 + str4;
    }
    return XBogus;
}

