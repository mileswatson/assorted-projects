var canvas = document.querySelector("canvas");
canvas.width = window.innerWidth-25;
canvas.height = window.innerHeight-25;
var c = canvas.getContext("2d");

const size = 3;
const frameRate = 60;
const vel = 150;
const numParticles = 100;
const efficiency = 1;
const gravity = [-8, -8];


var w = canvas.width;
var h = canvas.height;
const twiceSizeSquared = 4*size*size;
const delay = 1/frameRate;

/*
class Node {
    constructor(past, value, next) {
        this.past = value;
        this.value = value;
        this.next = next;
    }
}*/

class Particle {

    constructor(position, velocity) {
        this.pos = position;
        this.vel = velocity
    }

    move(dt) {
        if (this.pos[0] < size) {
            this.pos[0] = size;
            this.vel[0] = -this.vel[0] * efficiency;
        } else if (this.pos[0] > w-size) {
            this.pos[0] = w-size;
            this.vel[0] = -this.vel[0] * efficiency;
        }
        if (this.pos[1] < size) {
            this.pos[1] = size;
            this.vel[1] = -this.vel[1] * efficiency;
        } else if (this.pos[1] > h-size) {
            this.pos[1] = h-size;
            this.vel[1] = -this.vel[1] * efficiency;
        }
        this.vel[0] += gravity[0] * dt
        this.vel[1] -= gravity[1] * dt
        this.pos[0] = this.pos[0] + this.vel[0] * dt;
        this.pos[1] = this.pos[1] + this.vel[1] * dt;
    }

    show() {
        c.beginPath();
        c.arc(this.pos[0], this.pos[1], size, 0, 2 * Math.PI);
        c.fill();
        c.stroke();
    }

    collide(other) {
        var dsp = [
            other.pos[0]-this.pos[0],
            other.pos[1]-this.pos[1]
        ]
        var distanceSquared = (dsp[0] * dsp[0]) + (dsp[1] * dsp[1]);
        if (distanceSquared <= twiceSizeSquared) {
            var distance = Math.sqrt(distanceSquared);
            var overlapSize = ((2 * size) - distance);
            dsp[0] = (dsp[0] / distance) * overlapSize;
            dsp[1] = (dsp[1] / distance) * overlapSize;
            this.pos[0] -= dsp[0];
            this.pos[1] -= dsp[1];
            other.pos[0] += dsp[0];
            other.pos[1] += dsp[1];
            var buffer = this.vel;
            this.vel = other.vel;
            other.vel = buffer;
        }
    }
}

function random(minimum, maximum) {
    return (Math.random()*(maximum-minimum))+minimum;
}

particles = []

for (var i = 0; i < numParticles; i++) {
    particles.push(new Particle(
        [random(0, 1), random(h, h-1)],
        [random(-vel, vel), random(-vel, vel)]
    ))
}

function addParticle(event) {
    if (mouseDown) {
        for (var i = 0; i < 10; i++) {
            particles.push(new Particle(
                [cursorX+random(-1,1), cursorY+random(-1, 1)],
                [random(-vel, vel), random(-vel, vel)]
            ));
        }
    }
}

/*
particles.push(new Particle(
    [100, 100],
    [10, 0]
));

particles.push(new Particle(
    [200, 100],
    [0, 0]
));
*/
function draw() {
    c.clearRect(0, 0, w, h);
    for (var i = 0; i < particles.length; i++) {
        for (var j = i+1; j < particles.length; j++) {
            particles[i].collide(particles[j]);
        }
        particles[i].move(delay);
        particles[i].show();
    }
    addParticle();
}

document.onmousemove = function(e){
    cursorX = e.pageX;
    cursorY = e.pageY;
}

document.onmousedown = function(e){
    mouseDown = true;
}

document.onmouseup = function(e){
    mouseDown = false;
}

mouseDown = false
document.addEventListener("mousedown", addParticle)
setInterval(draw, 1000*delay)