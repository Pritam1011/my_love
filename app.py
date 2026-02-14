from flask import Flask, render_template_string, send_file
import os

app = Flask(__name__)

# Read the HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Lavender Love 💜</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Quicksand:wght@600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
body{height:100vh;display:flex;justify-content:center;align-items:center;overflow:hidden;font-family:'Quicksand',sans-serif;background:linear-gradient(135deg,#d8b4fe,#a78bfa,#c084fc);background-size:300% 300%;animation:gradient 12s ease infinite;}
@keyframes gradient{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.floating-hearts{position:fixed;width:100%;height:100%;pointer-events:none;z-index:1;}
.floating-hearts span{position:absolute;width:15px;height:15px;background:rgba(255,255,255,0.7);transform:rotate(45deg);animation:floatUp linear infinite;}
.floating-hearts span::before,.floating-hearts span::after{content:"";position:absolute;width:15px;height:15px;background:inherit;border-radius:50%;}
.floating-hearts span::before{top:-7px;left:0;}
.floating-hearts span::after{left:-7px;top:0;}
@keyframes floatUp{0%{transform:translateY(100vh) rotate(45deg);opacity:0;}10%{opacity:1;}100%{transform:translateY(-10vh) rotate(45deg);opacity:0;}}
.card{background:rgba(255,255,255,0.25);backdrop-filter:blur(25px);padding:40px;border-radius:40px;box-shadow:0 25px 70px rgba(0,0,0,0.25);text-align:center;max-width:420px;width:90%;position:relative;z-index:10;}
.img-container img{width:220px;height:220px;border-radius:25px;object-fit:cover;border:6px solid rgba(255,255,255,0.6);}
h1{font-family:'Pacifico',cursive;font-size:2.2rem;color:white;margin-top:20px;text-shadow:0 5px 20px rgba(0,0,0,0.3);}
.button-area{position:relative;height:180px;margin-top:20px;}
#yesBtn{width:100px;height:100px;background:linear-gradient(145deg,#9333ea,#6b21a8);position:absolute;left:50%;top:20px;transform:translateX(-50%) rotate(-45deg);border:none;cursor:pointer;animation:pulse 2s infinite ease-in-out;pointer-events:auto;display:flex;justify-content:center;align-items:center;}
@keyframes pulse{0%{transform:translateX(-50%) rotate(-45deg) scale(1);}50%{transform:translateX(-50%) rotate(-45deg) scale(1.1);}100%{transform:translateX(-50%) rotate(-45deg) scale(1);}}
#yesBtn::before,#yesBtn::after{content:"";width:100px;height:100px;background:inherit;border-radius:50%;position:absolute;pointer-events:none;}
#yesBtn::before{top:-50px;left:0;}
#yesBtn::after{left:50px;top:0;}
.btn-text{transform:rotate(45deg);color:white;font-weight:bold;font-size:1.2rem;position:relative;z-index:10;cursor:pointer;user-select:none;}
#noBtn{position:absolute;left:50%;top:120px;transform:translateX(-50%);padding:12px 30px;border-radius:30px;border:none;background:white;color:#6b21a8;font-weight:bold;font-size:1.05rem;cursor:pointer;transition:all .3s cubic-bezier(.68,-.55,.27,1.55);box-shadow:0 4px 15px rgba(0,0,0,0.2);user-select:none;touch-action:manipulation;z-index:1000;}
#noBtn:active{transform:translateX(-50%) scale(0.95);}
#plea{position:absolute;width:100%;bottom:-10px;text-align:center;color:white;font-size:1.3rem;display:none;text-shadow:0 2px 10px rgba(0,0,0,0.3);white-space:nowrap;}
.credit{position:fixed;bottom:15px;width:100%;text-align:center;color:rgba(255,255,255,0.7);font-size:0.9rem;z-index:5;text-shadow:0 2px 5px rgba(0,0,0,0.3);}
@media (max-width:600px){.card{padding:30px;}h1{font-size:1.8rem;}.img-container img{width:180px;height:180px;}#plea{font-size:1.1rem;}}
</style>
</head>
<body>
<div class="floating-hearts">
<span style="left:0%;animation-duration:6s;"></span>
<span style="left:8%;animation-duration:7s;"></span>
<span style="left:16%;animation-duration:8s;"></span>
<span style="left:24%;animation-duration:9s;"></span>
<span style="left:32%;animation-duration:6s;"></span>
<span style="left:40%;animation-duration:7s;"></span>
<span style="left:48%;animation-duration:8s;"></span>
<span style="left:56%;animation-duration:9s;"></span>
<span style="left:64%;animation-duration:6s;"></span>
<span style="left:72%;animation-duration:7s;"></span>
<span style="left:80%;animation-duration:8s;"></span>
<span style="left:88%;animation-duration:9s;"></span>
</div>
<div class="card" id="card">
<div class="img-container"><img src="/image" alt="Our Photo"></div>
<h1>Will you be my Valentine? 💜</h1>
<div class="button-area" id="buttonArea">
<button id="yesBtn"><span class="btn-text" onclick="celebrate()">Yes!</span></button>
<button id="noBtn">No</button>
<div id="plea"></div>
</div>
</div>
<div class="credit">Created with 💜 by Pritam Dash</div>
<script>
const noBtn=document.getElementById("noBtn");const area=document.getElementById("buttonArea");const plea=document.getElementById("plea");
const messages=["Hari gali mu agyan? 🥺","gelu please 💜","oo ebe enti karia mo saha 😭","enti hebar nai 🌹","nai loo gelu 🥰"];
let index=0;let isMoving=false;
function dodgeButton(clientX,clientY){if(isMoving)return;const rect=noBtn.getBoundingClientRect();const dx=clientX-(rect.left+rect.width/2);const dy=clientY-(rect.top+rect.height/2);const distance=Math.sqrt(dx*dx+dy*dy);if(distance<100){isMoving=true;const maxX=area.clientWidth-noBtn.offsetWidth-10;const maxY=area.clientHeight-noBtn.offsetHeight-10;const newX=Math.max(10,Math.random()*maxX);const newY=Math.max(10,Math.random()*maxY);noBtn.style.left=newX+"px";noBtn.style.top=newY+"px";noBtn.style.transform="none";plea.style.display="block";plea.innerText=messages[index];index=(index+1)%messages.length;setTimeout(()=>{isMoving=false;},300);}}
area.addEventListener("mousemove",(e)=>{dodgeButton(e.clientX,e.clientY);});
area.addEventListener("touchmove",(e)=>{e.preventDefault();if(e.touches.length>0){dodgeButton(e.touches[0].clientX,e.touches[0].clientY);}},{passive:false});
noBtn.addEventListener("touchstart",(e)=>{e.preventDefault();dodgeButton(e.touches[0].clientX,e.touches[0].clientY);},{passive:false});
function celebrate(){const card=document.getElementById("card");card.innerHTML=`<div class="img-container"><img src="/image" alt="Our Photo" style="width:220px;height:220px;border-radius:25px;object-fit:cover;border:6px solid rgba(255,255,255,0.6);"></div><h1 style="font-size:2.5rem;margin-top:20px;">Yaaaay! 💜</h1><p style="color:white;font-size:1.8rem;margin-top:15px;text-shadow:0 2px 10px rgba(0,0,0,0.3);">mo gelu ta ummhaa😘 #Arprit</p>`;const duration=4000;const end=Date.now()+duration;(function frame(){confetti({particleCount:25,angle:60,spread:70,origin:{x:0},colors:['#9333ea','#ffffff','#c084fc']});confetti({particleCount:25,angle:120,spread:70,origin:{x:1},colors:['#9333ea','#ffffff','#c084fc']});if(Date.now()<end){requestAnimationFrame(frame);}})();}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/image')
def get_image():
    """Serve the couple photo"""
    # Check for different image formats
    if os.path.exists('us.png'):
        return send_file('us.png', mimetype='image/png')
    elif os.path.exists('us.jpg'):
        return send_file('us.jpg', mimetype='image/jpeg')
    elif os.path.exists('us.jpeg'):
        return send_file('us.jpeg', mimetype='image/jpeg')
    else:
        return "Image not found. Please add us.png or us.jpg to the root directory.", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
