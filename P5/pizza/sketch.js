
function setup() {
    createCanvas(900,900);
}  

function draw() {
    background(abs(sin(frameCount*0.005)*100),20);
    //translate(width/2,height/2);
    noStroke();
    fill(abs(cos(frameCount*0.03))*255,abs(cos(frameCount*0.09))*255,abs(cos(frameCount*0.06))*255,)
    //arc(mouseX,mouseY,180,180, -PI/2 ,abs(sin(frameCount*0.05)*2*PI)-PI/2,PIE);
    translate(mouseX,mouseY);
    rotate((frameCount*0.02)*PI);
    arc(0,0,180,180, -PI/2 ,abs(sin(frameCount*0.05)*2*PI)-PI/2,PIE);
}

