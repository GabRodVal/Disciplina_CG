
function setup() {
    createCanvas(400,400);
}  

function desenhaTerra() {
    push();
    rotate(0.01*frameCount);
    translate(width/4,0);
    fill("blue");
    noStroke();
    circle(0,0,30);
    rotate(0.05*frameCount);
    translate(40,0);
    desenhaLua();
    pop();
}

function desenhaMercurio() {
    push();
    rotate(0.02*frameCount);
    translate(width/4-20,0);
    fill("red");
    noStroke();
    circle(0,0,5);
    pop();
}


function desenhaLua() {
    fill(100);
    noStroke();
    circle(0,0,10);
}

function desenhaSol() 
{
    fill("yellow");
    noStroke();
    circle(0,0,100);

    desenhaTerra();

    desenhaMercurio();
}

function draw() {
    background(45, 3, 59, 25);
    translate(width/2, height/2);
    desenhaSol();
}

