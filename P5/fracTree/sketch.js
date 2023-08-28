
function setup() {
    createCanvas(600,600);
} 

function randColor(){
    stroke(abs(sin(frameCount*0.01)) * 255,
    abs(sin(frameCount*0.008)) * 255,
    abs(sin(frameCount*0.006)) * 255);
}

function branch(max) {
    if(max == 0){
        return
    }
    line(0, 0, 0, -100);
    count++;
    text(count,10,-50)
    translate(0, -100);

    push();
    rotate(PI/6);
    branch(max-1);
    pop();

    push();
    rotate(-PI/6);
    branch(max-1);
    pop();
}

function fracTree(length, max) {
    if(max == 0) {
        return;
    }

    randColor();
    strokeWeight(max+2); 
    line(0,0,0,-length);

    translate(0,-length);

    push();
    rotate(PI/3);
    fracTree(length*2/3, max-1);
    pop();

    push();
    rotate(-PI/3);
    fracTree(length*2/3, max-1);
    pop();

}

function draw() {
    let V;
    background(240);
    V = createVector(width/2, height-20);
    let limit = 6;

    translate(V.x, V.y);
    fracTree(200,limit);
}
