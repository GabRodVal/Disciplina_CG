
function setup() {
    createCanvas(600,600);
} 

function randColor(){
    stroke(255,
    255,
    abs(sin(frameCount*0.006)) * 150 +55);
}

function halo(length, max) {
    if(max == 0) {
        return;
    }

    randColor();
    strokeWeight(max); 
    noFill();
    circle(0,0,length);

    

    push();
    translate(length/2,0);
    //rotate(PI/3);
    halo(length*2/3, max-1);
    pop();

    push();
    translate(-length/2,0);
    halo(length*2/3, max-1);
    pop();

    push();
    translate(0,length/2);
    halo(length*2/3, max-1);
    pop();

    push();
    translate(0,-length/2);
    halo(length*2/3, max-1);
    pop();

    /*push();
    halo(length*2/3, max-1);
    pop();*/

    /*push();
    rotate(-PI/3);
    halo(length*2/3, max-1);
    pop();*/

}

function draw() {
    background(55);
    let limit = 6;

    translate(width/2, height/2);
    halo(300, limit);
    //fracTree(200,limit);
}
