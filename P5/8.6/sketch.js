let count = 0;

function setup() {
    createCanvas(600,600);
}  
function fracTree(max) {
    if(max == 0){
        return
    }


    line(0, 0, 0, -100);
    count++;
    text(count,10,-50)
    translate(0, -100);

    push();
    rotate(PI/6);
    fracTree(max-1);
    pop();

    push();
    rotate(-PI/6);
    fracTree(max-1);
    pop();
}

function draw() {
    background(240);
    let limit = 4;

    translate(width/2, height-20);
    count = 0;
    fracTree(limit);
}
