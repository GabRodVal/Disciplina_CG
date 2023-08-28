
let limit = 4;

function setup() {
    createCanvas(600,600);
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

    strokeWeight(max+2); 

    line(0,0,0,-length);
    translate(0,-length);

    let rand = Math.floor(Math.random() * 4) +1;

    for (let f = 0; f < rand; f++) {
        
        let theta = (Math.random()*PI -PI/2);
        push();
        rotate(theta);
        fracTree(length*2/3, max-1);
        pop();
    }

}

function draw() {

    translate(width/2, height-20);

    if(frameCount == 1){
        background(240);
        fracTree(200,limit);
    }
}

function mouseClicked(){
    background(240);
    fracTree(200,limit);
}
