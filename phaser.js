const config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 300 },
      debug: false
    }
  },
  scene: {
    preload: preload,
    create: create,
    update: update
  }
};

const game = new Phaser.Game(config);

function preload() {
  this.load.image('flag', 'https://upload.wikimedia.org/wikipedia/commons/1/11/Flag_of_Lithuania.svg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original');
}

function create() {
  this.physics.add.image(400, 300, 'square');
}

function update() {
  // finish
}
