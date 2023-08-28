
function setup() {
    createCanvas(400,400);
    rectMode(CENTER);
}  

function draw() {
    background(100);
    translate(width/2, 0);
    rotate(sin(0.05*frameCount)*PI/6);
    line(0,0,0,height-120);
    translate(0,height-120);
    circle(0,0,100);
}

