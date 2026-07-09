const _require = eval("require");
// 本机无法进行js与flash交互有安全机制问题， 通过开端口形式进行flash页面引入
const createMain = (fn, post, ip, fileName, none) => {
  fn(post, ip, fileName);
};

let device = {};
//本机websocket
const openWS = () => {};

function getLocalIP(fn) {
  const os = _require("os");
  const osType = os.type(); //系统类型
  const netInfo = os.networkInterfaces(); //网络信息
  let ip = [];
  let str = `请选择启动ip`;
  if (osType === "Windows_NT") {
    let i = 0;
    for (let dev in netInfo) {
      //win7的网络信息中显示为本地连接，win10显示为以太网
      // if (dev === '本地连接' || dev === '以太网') {
      for (let j = 0; j < netInfo[dev].length; j++) {
        if (netInfo[dev][j].family === "IPv4") {
          // ip = netInfo[dev][j].address;
          ip.push(netInfo[dev][j].address);
          str += `
第${i++}个IP：${netInfo[dev][j].address}`;
        }
      }
      // }
    }
  } else if (osType === "Linux") {
    ip = netInfo.eth0[0].address;
  } else if (osType === "Darwin") {
    // macOS: 遍历所有网络接口获取 IPv4 地址
    for (let dev in netInfo) {
      for (let j = 0; j < netInfo[dev].length; j++) {
        if (netInfo[dev][j].family === "IPv4" && !netInfo[dev][j].internal) {
          ip.push(netInfo[dev][j].address);
        }
      }
    }
    if (ip.length === 0) {
      ip.push("127.0.0.1");
    }
  } else {
    // 其他操作系统
  }
  // let chouseIpFn = () => {
  // 	const readline = _require('readline').createInterface({
  // 		input: process.stdin,
  // 		output: process.stdout,
  // 	});
  // 	readline.question(`${str}
  // 	`, name => {
  // 		let chouseIp = ip[name]
  // 		if (chouseIp) {
  // 			console.log('已选择： ' + chouseIp)
  // 			fn && fn(chouseIp)
  // 			readline.close();
  // 		} else {
  // 			console.log('请选择正确选项')
  // 			readline.close();
  // 			chouseIpFn()
  // 		}
  // 	});
  // }
  // chouseIpFn()
  return ip;
}

try {
  if (module) module.exports = { openWS, createMain };
} catch (error) {}
/**
 * 
sad
var mx:int = this.mouseX;
         var my:int = this.mouseY;
         ExternalInterface.call("API.GetCursorPositionHtml",mx,my);
         if(mx < -30)
         {
            mx = 34;
         }
         if(my < -79)
         {
            my = 0;
         }
         return new Point(mx,my);
happy peaceful
var mx:int = this.mouseX;
         var my:int = this.mouseY;
         ExternalInterface.call("API.GetCursorPositionHtml",mx,my);
         if(mx < -70)
         {
            mx = 0;
         }
         if(my < -70)
         {
            my = 0;
         }
         return new Point(mx,my);

prostrate
var mx:int = this.mouseX;
         var my:int = this.mouseY;
         ExternalInterface.call("API.GetCursorPositionHtml",mx,my);
         if(mx < -33)
         {
            mx = 35;
         }
         if(my < -83)
         {
            my = 21;
         }
         return new Point(mx,my);
upset
var mx:int = this.mouseX;
         var my:int = this.mouseY;
         ExternalInterface.call("API.GetCursorPositionHtml",mx,my);
         if(mx < -38)
         {
            mx = 29;
         }
         if(my < -68)
         {
            my = 24;
         }
         return new Point(mx,my);

 */

let fileNames = [
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "I",
  "J",
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "I",
  "J",
  "K",
  "L",
  "M",
  "N",
  "O",
  "P",
  "Q",
  "R",
  "S",
  "T",
  "U",
  "V",
  "W",
  "X",
  "Y",
  "Z",
  "_",
];

let url = {
  host: "",
  port: "",
  fileName: "",
};
global.openLocalHost = (fn) => {
  if (fn) fn({ host: "", port: "", fileName: "" });
};
