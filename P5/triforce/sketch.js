let pontos = [];


function setup() {
    createCanvas(900,900);
}  

function medioP(p1, p2){
    let p3x = (p1.x+p2.x)/2;
    let p3y = (p1.y+p2.y)/2;
    let p3 = createVector(p3x,p3y);
    return p3;
}

function triangleArea(A,B,C){
    let areaT = (((B.x*C.y)+(C.x*A.y)+(A.x*B.y)) - ((C.x*B.y)+(A.x*C.y)+(B.x*A.y)))/2;
    return abs(areaT);
}

function triforce(A,B,C,n){
    if(n == 0||triangleArea(A,B,C)<=1500){
        console.log(triangleArea(A,B,C));
        fill(255,255,255);
        triangle(A.x,A.y,B.x,B.y,C.x,C.y)
        return;
    }
    let AB = medioP(A,B);
    let AC = medioP(A,C);
    let BC = medioP(B,C);

    //pop();
    triforce(A,AB,AC,n-1);
    triforce(AB,B,BC,n-1);
    triforce(AC,BC,C,n-1);
    //triforce(A,B,C,n-1);
    //push();
}

function draw() {

    pontos = [createVector(100,height-100), 
    createVector(width-100,height-100), 
    createVector(width/2,100)];

    background(abs(sin(frameCount*0.005)*50),25);
    //translate(width/2,height/2);
    //noStroke();
    //fill(abs(cos(frameCount*0.03))*255,abs(cos(frameCount*0.09))*255,abs(cos(frameCount*0.06))*255,)
    triforce(pontos[0],pontos[1],pontos[2],4);


}

